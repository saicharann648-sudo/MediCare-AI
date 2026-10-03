"""
========================================================================================
SMART HOSPITAL & DOCTOR APPOINTMENT MANAGEMENT SYSTEM
========================================================================================
A modern, production-ready Hospital Information & Management System built with Python.
- Framework: CustomTkinter (with standard Tkinter/ttk fallback)
- Database: SQLite3 with Auto-creation, Relational Foreign Keys & Auto-Seeding
- Documents: ReportLab PDF Invoicing & Digital Prescription Engine
- Architecture: Object-Oriented, Modular, Resilient & Fully Zero-Config
========================================================================================
"""

import sys
import os
import json
import sqlite3
import datetime
import subprocess
from typing import List, Dict, Any, Optional, Tuple

# --------------------------------------------------------------------------------------
# 1. DEPENDENCY CHECKS & GRACEFUL IMPORTS
# --------------------------------------------------------------------------------------
USE_CUSTOMTKINTER = True
try:
    import customtkinter as ctk
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog
except ImportError:
    USE_CUSTOMTKINTER = False
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog

REPORTLAB_AVAILABLE = True
try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
    )
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
except ImportError:
    REPORTLAB_AVAILABLE = False

# Application Constants
APP_TITLE = "MediCare Hospital Management System"
APP_VERSION = "v2.5 Pro Enterprise"
DB_NAME = "hospital.db"
DEFAULT_CURRENCY = "₹"  # Can be changed to '$' or other symbols

# Color Palette Configuration (Modern Deep Slate & Medical Teal)
THEME_COLORS = {
    "dark": {
        "bg_dark": "#0f172a",
        "card_bg": "#1e293b",
        "card_border": "#334155",
        "sidebar_bg": "#0b1120",
        "primary": "#0d9488",
        "primary_hover": "#0f766e",
        "accent": "#06b6d4",
        "success": "#10b981",
        "warning": "#f59e0b",
        "danger": "#ef4444",
        "text_primary": "#f8fafc",
        "text_secondary": "#94a3b8",
        "table_header": "#1e293b",
        "table_row_alt": "#172033",
        "table_row": "#0f172a",
        "table_fg": "#f1f5f9"
    },
    "light": {
        "bg_dark": "#f1f5f9",
        "card_bg": "#ffffff",
        "card_border": "#cbd5e1",
        "sidebar_bg": "#e2e8f0",
        "primary": "#0d9488",
        "primary_hover": "#0f766e",
        "accent": "#0284c7",
        "success": "#16a34a",
        "warning": "#d97706",
        "danger": "#dc2626",
        "text_primary": "#0f172a",
        "text_secondary": "#64748b",
        "table_header": "#e2e8f0",
        "table_row_alt": "#f8fafc",
        "table_row": "#ffffff",
        "table_fg": "#0f172a"
    }
}


# --------------------------------------------------------------------------------------
# 2. DATABASE MANAGER (SQLite with Foreign Keys & Auto-Seeding)
# --------------------------------------------------------------------------------------
class DatabaseManager:
    """Encapsulates all SQLite database operations, schema creation, and seeding."""

    def __init__(self, db_path: str = DB_NAME):
        self.db_path = db_path
        self.init_db()

    def get_connection(self) -> sqlite3.Connection:
        """Creates connection with foreign key enforcement."""
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        """Initializes tables and seeds mock data if empty."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # 1. Doctors table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS doctors (
                    doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    specialization TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    email TEXT,
                    available_days TEXT NOT NULL,
                    fee REAL NOT NULL
                )
            """)

            # 2. Patients table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS patients (
                    patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    gender TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    blood_group TEXT,
                    address TEXT,
                    created_at TEXT NOT NULL
                )
            """)

            # 3. Appointments table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS appointments (
                    appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id INTEGER NOT NULL,
                    doctor_id INTEGER NOT NULL,
                    appointment_date TEXT NOT NULL,
                    time_slot TEXT NOT NULL,
                    status TEXT DEFAULT 'Scheduled',
                    notes TEXT,
                    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
                    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE
                )
            """)

            # 4. Prescriptions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS prescriptions (
                    prescription_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    appointment_id INTEGER NOT NULL,
                    patient_id INTEGER NOT NULL,
                    doctor_id INTEGER NOT NULL,
                    diagnosis TEXT NOT NULL,
                    medicines_json TEXT NOT NULL,
                    advice TEXT,
                    date TEXT NOT NULL,
                    FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id) ON DELETE CASCADE,
                    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
                    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE
                )
            """)

            # 5. Billings table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS billings (
                    bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    appointment_id INTEGER NOT NULL,
                    patient_id INTEGER NOT NULL,
                    consultation_fee REAL NOT NULL,
                    medicine_fee REAL DEFAULT 0,
                    other_charges REAL DEFAULT 0,
                    discount REAL DEFAULT 0,
                    total_amount REAL NOT NULL,
                    payment_status TEXT DEFAULT 'Unpaid',
                    payment_mode TEXT DEFAULT 'Cash',
                    date TEXT NOT NULL,
                    FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id) ON DELETE CASCADE,
                    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
                )
            """)

            conn.commit()

            # Production mode: clean database by default (seeding disabled)
            conn.commit()

    def _seed_mock_data(self, conn: sqlite3.Connection):
        """Seeds realistic initial records for doctors, patients, appointments, and bills."""
        cursor = conn.cursor()
        today_str = datetime.date.today().strftime("%Y-%m-%d")
        yesterday_str = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        tomorrow_str = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

        # Seed 5 Doctors
        doctors_data = [
            ("Dr. Rajesh Sharma", "Cardiology", "9876543210", "dr.sharma@medicare.org", "Mon, Wed, Fri", 800.00),
            ("Dr. Priya Patel", "Neurology", "9823456789", "dr.priya@medicare.org", "Tue, Thu, Sat", 1000.00),
            ("Dr. Ananya Sen", "Pediatrics", "9712345678", "dr.ananya@medicare.org", "Mon, Tue, Thu", 600.00),
            ("Dr. Vikram Malhotra", "Orthopedics", "9632587410", "dr.vikram@medicare.org", "Wed, Thu, Sat", 750.00),
            ("Dr. Sneha Kulkarni", "General Medicine", "9514782360", "dr.sneha@medicare.org", "Mon-Sat", 500.00)
        ]
        cursor.executemany("""
            INSERT INTO doctors (name, specialization, phone, email, available_days, fee)
            VALUES (?, ?, ?, ?, ?, ?)
        """, doctors_data)

        # Seed 5 Patients
        patients_data = [
            ("Ramesh Kumar", 45, "Male", "9898989801", "B+", "12 Park Avenue, Health City", today_str),
            ("Sunita Gupta", 38, "Female", "9898989802", "O+", "45 Green Road, Sector 4", today_str),
            ("Amit Joshi", 29, "Male", "9898989803", "A+", "78 Lake View, Civil Lines", today_str),
            ("Kavita Nair", 52, "Female", "9898989804", "AB+", "19 Palm Grove Colony", today_str),
            ("Mohammad Farooq", 61, "Male", "9898989805", "O-", "33 Crescent Heights", today_str)
        ]
        cursor.executemany("""
            INSERT INTO patients (name, age, gender, phone, blood_group, address, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, patients_data)

        # Seed 5 Appointments (Mix of Today, Yesterday, Tomorrow)
        appointments_data = [
            (1, 1, today_str, "09:30 AM", "Completed", "Routine cardiac checkup and ECG review"),
            (2, 2, today_str, "11:00 AM", "Scheduled", "Persistent migraine and dizziness"),
            (3, 3, today_str, "02:30 PM", "Scheduled", "Seasonal viral fever and throat infection"),
            (4, 4, yesterday_str, "04:00 PM", "Completed", "Post-fracture joint stiffness"),
            (5, 5, tomorrow_str, "10:30 AM", "Scheduled", "General wellness and hypertension consult")
        ]
        cursor.executemany("""
            INSERT INTO appointments (patient_id, doctor_id, appointment_date, time_slot, status, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, appointments_data)

        # Seed 2 Sample Prescriptions for completed appointments
        sample_medicines_1 = json.dumps([
            {"name": "Atorvastatin", "dosage": "20mg", "frequency": "0-0-1 (Night)", "duration": "30 Days"},
            {"name": "Aspirin Cardio", "dosage": "75mg", "frequency": "1-0-0 (Post Breakfast)", "duration": "30 Days"}
        ])
        cursor.execute("""
            INSERT INTO prescriptions (appointment_id, patient_id, doctor_id, diagnosis, medicines_json, advice, date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (1, 1, 1, "Mild Hyperlipidemia & Stage 1 Hypertension", sample_medicines_1,
              "Low sodium diet, brisk walking 30 mins daily. Review Lipid Profile after 4 weeks.", today_str))

        sample_medicines_2 = json.dumps([
            {"name": "Aceclofenac + Paracetamol", "dosage": "100/325mg", "frequency": "1-0-1", "duration": "5 Days"},
            {"name": "Calcium Carbonate + Vit D3", "dosage": "500mg", "frequency": "0-1-0", "duration": "15 Days"}
        ])
        cursor.execute("""
            INSERT INTO prescriptions (appointment_id, patient_id, doctor_id, diagnosis, medicines_json, advice, date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (4, 4, 4, "Post-Traumatic Knee Sprain & Joint Inflammation", sample_medicines_2,
              "Hot fomentation twice daily. Gentle knee mobility exercises.", yesterday_str))

        # Seed 2 Sample Bills
        cursor.execute("""
            INSERT INTO billings (appointment_id, patient_id, consultation_fee, medicine_fee, other_charges, discount, total_amount, payment_status, payment_mode, date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (1, 1, 800.00, 450.00, 150.00, 50.00, 1350.00, "Paid", "UPI", today_str))

        cursor.execute("""
            INSERT INTO billings (appointment_id, patient_id, consultation_fee, medicine_fee, other_charges, discount, total_amount, payment_status, payment_mode, date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (4, 4, 750.00, 320.00, 100.00, 0.00, 1170.00, "Paid", "Card", yesterday_str))

        conn.commit()

    # --- KPI & METRICS QUERIES ---
    def get_dashboard_metrics(self) -> Dict[str, Any]:
        """Calculates live dashboard counts, analytics, and department distributions."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            today_str = datetime.date.today().strftime("%Y-%m-%d")

            cursor.execute("SELECT COUNT(*) as count FROM patients")
            total_patients = cursor.fetchone()["count"]

            cursor.execute("SELECT COUNT(*) as count FROM doctors")
            active_doctors = cursor.fetchone()["count"]

            cursor.execute("SELECT COUNT(*) as count FROM appointments WHERE appointment_date = ?", (today_str,))
            today_appointments = cursor.fetchone()["count"]

            cursor.execute("SELECT COUNT(*) as count FROM appointments WHERE appointment_date = ? AND status = 'Scheduled'", (today_str,))
            today_pending = cursor.fetchone()["count"]

            cursor.execute("SELECT COUNT(*) as count FROM appointments WHERE appointment_date = ? AND status = 'Completed'", (today_str,))
            today_completed = cursor.fetchone()["count"]

            cursor.execute("SELECT COUNT(*) as count FROM appointments WHERE appointment_date = ? AND status = 'Cancelled'", (today_str,))
            today_cancelled = cursor.fetchone()["count"]

            cursor.execute("SELECT COUNT(*) as count FROM appointments WHERE status = 'Completed'")
            total_completed_all = cursor.fetchone()["count"]

            cursor.execute("SELECT COUNT(*) as count FROM appointments")
            total_appointments_all = cursor.fetchone()["count"]

            cursor.execute("SELECT COALESCE(SUM(total_amount), 0) as total FROM billings WHERE payment_status = 'Paid'")
            total_revenue = cursor.fetchone()["total"]

            cursor.execute("SELECT COALESCE(SUM(total_amount), 0) as total FROM billings WHERE payment_status != 'Paid'")
            unpaid_revenue = cursor.fetchone()["total"]

            cursor.execute("SELECT COUNT(*) as count FROM billings WHERE payment_status = 'Paid'")
            paid_invoices_count = cursor.fetchone()["count"]

            cursor.execute("SELECT COUNT(*) as count FROM billings WHERE payment_status != 'Paid'")
            unpaid_invoices_count = cursor.fetchone()["count"]

            cursor.execute("SELECT COUNT(*) as count FROM billings")
            total_invoices_count = cursor.fetchone()["count"]

            cursor.execute("SELECT COUNT(*) as count FROM prescriptions")
            total_prescriptions_count = cursor.fetchone()["count"]

            # Real Department Load Calculation from Appointments
            cursor.execute("""
                SELECT d.specialization, COUNT(a.appointment_id) as appt_count
                FROM doctors d
                LEFT JOIN appointments a ON d.doctor_id = a.doctor_id
                GROUP BY d.specialization
                ORDER BY appt_count DESC, d.specialization ASC
            """)
            dept_rows = cursor.fetchall()
            departments_load = []
            dept_colors = ["#4f46e5", "#06b6d4", "#10b981", "#f59e0b", "#ec4899", "#8b5cf6", "#3b82f6"]
            for idx, r in enumerate(dept_rows):
                cnt = r["appt_count"]
                pct = int(round((cnt / max(1, total_appointments_all)) * 100)) if total_appointments_all > 0 else 0
                visual_pct = max(8, pct) if cnt > 0 else 0
                departments_load.append({
                    "name": r["specialization"],
                    "count": cnt,
                    "percentage": min(100, visual_pct),
                    "actual_pct": pct,
                    "color": dept_colors[idx % len(dept_colors)]
                })

            # List of active departments for dynamic AI banner
            cursor.execute("SELECT DISTINCT specialization FROM doctors ORDER BY specialization ASC")
            dept_names = [r["specialization"] for r in cursor.fetchall()]
            active_departments_list = ", ".join(dept_names) if dept_names else "Awaiting Department Setup"

            # Real Weekly Day-of-Week Consultation Distribution (Mon - Sun)
            day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            cursor.execute("""
                SELECT strftime('%w', appointment_date) as dow, COUNT(*) as count
                FROM appointments
                GROUP BY dow
            """)
            dow_counts = {str(r["dow"]): r["count"] for r in cursor.fetchall()}
            dow_map = {"Mon": "1", "Tue": "2", "Wed": "3", "Thu": "4", "Fri": "5", "Sat": "6", "Sun": "0"}

            weekly_chart = []
            max_day_count = max(list(dow_counts.values()) + [0])
            today_dow_idx = datetime.date.today().weekday()

            for idx, d_name in enumerate(day_names):
                sqlite_dow = dow_map[d_name]
                c = dow_counts.get(sqlite_dow, 0)
                if max_day_count > 0 and c > 0:
                    h_pct = max(18, min(100, int(round((c / max_day_count) * 92))))
                else:
                    h_pct = 0
                weekly_chart.append({
                    "day": d_name,
                    "count": c,
                    "height": h_pct,
                    "has_data": (c > 0),
                    "is_today": (idx == today_dow_idx)
                })

            # Hospital Capacity: realistic tracking grounded in active patients & today's consults
            total_beds = 50
            if total_patients == 0 and today_appointments == 0:
                occupied_beds = 0
                capacity_pct = 0
                free_beds = total_beds
            else:
                occupied_beds = min(total_beds, today_pending + (today_completed // 2) + min(15, total_patients))
                capacity_pct = int(round((occupied_beds / total_beds) * 100))
                free_beds = max(0, total_beds - occupied_beds)

            completion_rate = int(round((total_completed_all / max(1, total_appointments_all)) * 100)) if total_appointments_all > 0 else 0

            if today_appointments == 0 and total_patients == 0:
                flow_status = "Ready for Inflow"
            elif today_appointments >= 8:
                flow_status = "Peak Outpatient Inflow"
            elif today_appointments > 0:
                flow_status = "Normal Outpatient Flow"
            else:
                flow_status = "Optimal Capacity"

            return {
                "total_patients": total_patients,
                "active_doctors": active_doctors,
                "today_appointments": today_appointments,
                "today_pending": today_pending,
                "today_completed": today_completed,
                "today_cancelled": today_cancelled,
                "total_appointments_all": total_appointments_all,
                "total_revenue": total_revenue,
                "unpaid_revenue": unpaid_revenue,
                "paid_invoices_count": paid_invoices_count,
                "unpaid_invoices_count": unpaid_invoices_count,
                "total_invoices_count": total_invoices_count,
                "total_prescriptions_count": total_prescriptions_count,
                "departments_load": departments_load,
                "active_departments_list": active_departments_list,
                "weekly_chart": weekly_chart,
                "capacity_pct": capacity_pct,
                "occupied_beds": occupied_beds,
                "free_beds": free_beds,
                "completion_rate": completion_rate,
                "flow_status": flow_status
            }

    # --- DOCTORS CRUD ---
    def get_all_doctors(self) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT d.*, 
                       COUNT(a.appointment_id) as total_consultations,
                       SUM(CASE WHEN a.status = 'Completed' THEN 1 ELSE 0 END) as completed_consultations,
                       SUM(CASE WHEN a.status = 'Scheduled' THEN 1 ELSE 0 END) as pending_consultations
                FROM doctors d
                LEFT JOIN appointments a ON d.doctor_id = a.doctor_id
                GROUP BY d.doctor_id
                ORDER BY d.doctor_id DESC
            """)
            doctors = []
            for row in cursor.fetchall():
                d = dict(row)
                comp = d.get("completed_consultations") or 0
                d["rating"] = f"{min(5.0, 4.7 + min(0.3, comp * 0.05)):.1f}"
                doctors.append(d)
            return doctors

    def add_doctor(self, name: str, specialization: str, phone: str, email: str, available_days: str, fee: float) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO doctors (name, specialization, phone, email, available_days, fee)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, specialization, phone, email, available_days, fee))
            conn.commit()
            return cursor.lastrowid

    def update_doctor(self, doctor_id: int, name: str, specialization: str, phone: str, email: str, available_days: str, fee: float):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE doctors
                SET name = ?, specialization = ?, phone = ?, email = ?, available_days = ?, fee = ?
                WHERE doctor_id = ?
            """, (name, specialization, phone, email, available_days, fee, doctor_id))
            conn.commit()

    def delete_doctor(self, doctor_id: int):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM doctors WHERE doctor_id = ?", (doctor_id,))
            conn.commit()

    # --- PATIENTS CRUD ---
    def get_all_patients(self) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.*,
                       COUNT(a.appointment_id) as total_visits,
                       MAX(a.appointment_date) as last_visit
                FROM patients p
                LEFT JOIN appointments a ON p.patient_id = a.patient_id
                GROUP BY p.patient_id
                ORDER BY p.patient_id DESC
            """)
            return [dict(row) for row in cursor.fetchall()]

    def add_patient(self, name: str, age: int, gender: str, phone: str, blood_group: str, address: str) -> int:
        created_at = datetime.date.today().strftime("%Y-%m-%d")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO patients (name, age, gender, phone, blood_group, address, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (name, age, gender, phone, blood_group, address, created_at))
            conn.commit()
            return cursor.lastrowid

    def update_patient(self, patient_id: int, name: str, age: int, gender: str, phone: str, blood_group: str, address: str):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE patients
                SET name = ?, age = ?, gender = ?, phone = ?, blood_group = ?, address = ?
                WHERE patient_id = ?
            """, (name, age, gender, phone, blood_group, address, patient_id))
            conn.commit()

    def delete_patient(self, patient_id: int):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM patients WHERE patient_id = ?", (patient_id,))
            conn.commit()

    def search_patients(self, query: str) -> List[Dict[str, Any]]:
        q = f"%{query}%"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM patients
                WHERE name LIKE ? OR phone LIKE ? OR blood_group LIKE ? OR patient_id LIKE ?
                ORDER BY patient_id DESC
            """, (q, q, q, q))
            return [dict(row) for row in cursor.fetchall()]

    def get_patient_history(self, patient_id: int) -> Dict[str, Any]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM patients WHERE patient_id = ?", (patient_id,))
            patient = cursor.fetchone()

            cursor.execute("""
                SELECT a.*, d.name as doctor_name, d.specialization
                FROM appointments a
                JOIN doctors d ON a.doctor_id = d.doctor_id
                WHERE a.patient_id = ?
                ORDER BY a.appointment_date DESC, a.appointment_id DESC
            """, (patient_id,))
            appointments = [dict(r) for r in cursor.fetchall()]

            cursor.execute("""
                SELECT pr.*, d.name as doctor_name
                FROM prescriptions pr
                JOIN doctors d ON pr.doctor_id = d.doctor_id
                WHERE pr.patient_id = ?
                ORDER BY pr.date DESC
            """, (patient_id,))
            prescriptions = [dict(r) for r in cursor.fetchall()]

            cursor.execute("""
                SELECT b.*, a.appointment_date
                FROM billings b
                LEFT JOIN appointments a ON b.appointment_id = a.appointment_id
                WHERE b.patient_id = ?
                ORDER BY b.bill_id DESC
            """, (patient_id,))
            bills = [dict(r) for r in cursor.fetchall()]

            return {
                "patient": dict(patient) if patient else None,
                "appointments": appointments,
                "prescriptions": prescriptions,
                "bills": bills
            }

    # --- APPOINTMENTS CRUD & SCHEDULING ---
    def get_all_appointments(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            sql = """
                SELECT a.*, p.name as patient_name, p.phone as patient_phone,
                       d.name as doctor_name, d.specialization as doctor_dept, d.fee as doctor_fee
                FROM appointments a
                JOIN patients p ON a.patient_id = p.patient_id
                JOIN doctors d ON a.doctor_id = d.doctor_id
                ORDER BY a.appointment_date DESC, a.time_slot ASC
            """
            if limit:
                sql += f" LIMIT {int(limit)}"
            cursor.execute(sql)
            return [dict(row) for row in cursor.fetchall()]

    def check_appointment_conflict(self, doctor_id: int, date_str: str, time_slot: str, exclude_id: Optional[int] = None) -> bool:
        """Returns True if doctor is already booked at that date and time slot."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            query = """
                SELECT COUNT(*) as count FROM appointments
                WHERE doctor_id = ? AND appointment_date = ? AND time_slot = ? AND status != 'Cancelled'
            """
            params = [doctor_id, date_str, time_slot]
            if exclude_id:
                query += " AND appointment_id != ?"
                params.append(exclude_id)
            cursor.execute(query, params)
            return cursor.fetchone()["count"] > 0

    def add_appointment(self, patient_id: int, doctor_id: int, date_str: str, time_slot: str, status: str, notes: str) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO appointments (patient_id, doctor_id, appointment_date, time_slot, status, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (patient_id, doctor_id, date_str, time_slot, status, notes))
            conn.commit()
            return cursor.lastrowid

    def update_appointment_status(self, appointment_id: int, status: str):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE appointments SET status = ? WHERE appointment_id = ?", (status, appointment_id))
            conn.commit()

    # --- PRESCRIPTIONS CRUD ---
    def get_prescriptions(self) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT pr.*, p.name as patient_name, p.age, p.gender, p.phone as patient_phone,
                       d.name as doctor_name, d.specialization as doctor_dept,
                       a.appointment_date
                FROM prescriptions pr
                JOIN patients p ON pr.patient_id = p.patient_id
                JOIN doctors d ON pr.doctor_id = d.doctor_id
                JOIN appointments a ON pr.appointment_id = a.appointment_id
                ORDER BY pr.prescription_id DESC
            """)
            return [dict(row) for row in cursor.fetchall()]

    def save_prescription(self, appointment_id: int, patient_id: int, doctor_id: int, diagnosis: str, medicines_json: str, advice: str) -> int:
        date_str = datetime.date.today().strftime("%Y-%m-%d")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO prescriptions (appointment_id, patient_id, doctor_id, diagnosis, medicines_json, advice, date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (appointment_id, patient_id, doctor_id, diagnosis, medicines_json, advice, date_str))
            # Also mark appointment as Completed
            cursor.execute("UPDATE appointments SET status = 'Completed' WHERE appointment_id = ?", (appointment_id,))
            conn.commit()
            return cursor.lastrowid

    # --- BILLINGS CRUD ---
    def get_billings(self) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT b.*, p.name as patient_name, p.phone as patient_phone, p.age, p.gender,
                       d.name as doctor_name, d.specialization as doctor_dept,
                       a.appointment_date
                FROM billings b
                JOIN patients p ON b.patient_id = p.patient_id
                JOIN appointments a ON b.appointment_id = a.appointment_id
                JOIN doctors d ON a.doctor_id = d.doctor_id
                ORDER BY b.bill_id DESC
            """)
            return [dict(row) for row in cursor.fetchall()]

    def create_or_update_bill(self, appointment_id: int, patient_id: int, consultation_fee: float,
                              medicine_fee: float, other_charges: float, discount: float,
                              total_amount: float, payment_status: str, payment_mode: str) -> int:
        date_str = datetime.date.today().strftime("%Y-%m-%d")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Check if bill exists for this appointment
            cursor.execute("SELECT bill_id FROM billings WHERE appointment_id = ?", (appointment_id,))
            existing = cursor.fetchone()
            if existing:
                bill_id = existing["bill_id"]
                cursor.execute("""
                    UPDATE billings
                    SET consultation_fee = ?, medicine_fee = ?, other_charges = ?, discount = ?,
                        total_amount = ?, payment_status = ?, payment_mode = ?, date = ?
                    WHERE bill_id = ?
                """, (consultation_fee, medicine_fee, other_charges, discount, total_amount, payment_status, payment_mode, date_str, bill_id))
            else:
                cursor.execute("""
                    INSERT INTO billings (appointment_id, patient_id, consultation_fee, medicine_fee, other_charges, discount, total_amount, payment_status, payment_mode, date)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (appointment_id, patient_id, consultation_fee, medicine_fee, other_charges, discount, total_amount, payment_status, payment_mode, date_str))
                bill_id = cursor.lastrowid
            conn.commit()
            return bill_id

    def update_bill_status(self, bill_id: int, payment_status: str = "Paid", payment_mode: str = "UPI"):
        """Marks a bill as Paid or Unpaid and sets payment mode."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE billings SET payment_status = ?, payment_mode = ? WHERE bill_id = ?",
                           (payment_status, payment_mode, bill_id))
            conn.commit()

    def cancel_appointment(self, appointment_id: int):
        """Marks an appointment as Cancelled."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE appointments SET status = 'Cancelled' WHERE appointment_id = ?", (appointment_id,))
            conn.commit()



# --------------------------------------------------------------------------------------
# 3. PDF GENERATION ENGINE (ReportLab with Professional Hospital Branding)
# --------------------------------------------------------------------------------------
class PDFReportGenerator:
    """Generates professional, printable invoices and prescriptions in PDF format."""

    @staticmethod
    def get_output_dirs() -> Tuple[str, str]:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        inv_dir = os.path.join(base_dir, "invoices")
        rx_dir = os.path.join(base_dir, "prescriptions")
        os.makedirs(inv_dir, exist_ok=True)
        os.makedirs(rx_dir, exist_ok=True)
        return inv_dir, rx_dir

    @classmethod
    def generate_invoice_pdf(cls, bill_data: Dict[str, Any]) -> str:
        """Generates a high-quality, branded medical bill PDF invoice."""
        if not REPORTLAB_AVAILABLE:
            raise RuntimeError("ReportLab library is not installed. Please run: pip install reportlab")

        inv_dir, _ = cls.get_output_dirs()
        bill_id = bill_data.get("bill_id", 0)
        filename = f"Invoice_INV-{bill_id:04d}.pdf"
        filepath = os.path.join(inv_dir, filename)

        doc = SimpleDocTemplate(
            filepath,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        styles = getSampleStyleSheet()
        elements = []

        # Hospital Header
        header_title_style = ParagraphStyle(
            'HospitalTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=18,
            textColor=colors.HexColor("#0d9488"),
            alignment=1,
            spaceAfter=4
        )
        header_sub_style = ParagraphStyle(
            'HospitalSub',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            textColor=colors.HexColor("#475569"),
            alignment=1,
            spaceAfter=12
        )

        elements.append(Paragraph("MEDICARE MULTISPECIALTY HOSPITAL & RESEARCH CENTER", header_title_style))
        elements.append(Paragraph("NABH Accredited Healthcare Facility | Emergency 24x7: 108 / +91 98765 00000<br/>"
                                  "100 Medical Boulevard, Health City | Email: billing@medicarehospital.org | GSTIN: 07AAAAA0000A1Z5", header_sub_style))
        elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0d9488"), spaceAfter=14))

        # Invoice Meta Information (Two-Column Layout)
        status_color = "#16a34a" if bill_data.get("payment_status") == "Paid" else "#dc2626"
        info_data = [
            [
                Paragraph(f"<b>INVOICE NO:</b> INV-{bill_id:05d}<br/>"
                          f"<b>Date:</b> {bill_data.get('date', datetime.date.today().strftime('%Y-%m-%d'))}<br/>"
                          f"<b>Payment Mode:</b> {bill_data.get('payment_mode', 'Cash')}<br/>"
                          f"<b>Status:</b> <font color='{status_color}'><b>{bill_data.get('payment_status', 'Unpaid').upper()}</b></font>", styles['Normal']),
                Paragraph(f"<b>PATIENT DETAILS:</b><br/>"
                          f"<b>Name:</b> {bill_data.get('patient_name', 'N/A')} (ID: #{bill_data.get('patient_id', 'N/A')})<br/>"
                          f"<b>Age / Gender:</b> {bill_data.get('age', 'N/A')} Yrs / {bill_data.get('gender', 'N/A')}<br/>"
                          f"<b>Phone:</b> {bill_data.get('patient_phone', 'N/A')}<br/>"
                          f"<b>Consultant:</b> {bill_data.get('doctor_name', 'N/A')} ({bill_data.get('doctor_dept', 'General')})", styles['Normal'])
            ]
        ]
        info_table = Table(info_data, colWidths=[260, 280])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ('PADDING', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 14))

        # Itemized Charges Table
        consultation = float(bill_data.get("consultation_fee", 0.0))
        medicine = float(bill_data.get("medicine_fee", 0.0))
        other = float(bill_data.get("other_charges", 0.0))
        discount = float(bill_data.get("discount", 0.0))
        total = float(bill_data.get("total_amount", 0.0))

        items_table_data = [
            ["#", "Service Description", "Department / Category", f"Amount ({DEFAULT_CURRENCY})"],
            ["1", f"Doctor Consultation Fee - {bill_data.get('doctor_name', 'Specialist')}", bill_data.get('doctor_dept', 'Consultation'), f"{consultation:.2f}"],
            ["2", "Pharmacy & Prescribed Medication Charges", "Pharmacy Dispensary", f"{medicine:.2f}"],
            ["3", "Hospital Care, Clinical & Diagnostic Charges", "Clinical Services", f"{other:.2f}"],
            ["", "", "Subtotal:", f"{consultation + medicine + other:.2f}"],
            ["", "", "Discount / Concession:", f"- {discount:.2f}"],
            ["", "", "NET AMOUNT PAYABLE:", f"{DEFAULT_CURRENCY} {total:.2f}"]
        ]

        items_table = Table(items_table_data, colWidths=[30, 270, 140, 100])
        items_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0d9488")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('TOPPADDING', (0, 0), (-1, 0), 6),
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            ('ALIGN', (3, 0), (3, -1), 'RIGHT'),
            ('GRID', (0, 0), (-1, 3), 0.5, colors.HexColor("#cbd5e1")),
            ('BACKGROUND', (0, 1), (-1, 3), colors.HexColor("#ffffff")),
            ('FONTNAME', (2, 4), (-1, -1), 'Helvetica-Bold'),
            ('LINEABOVE', (2, 4), (-1, -1), 1, colors.HexColor("#94a3b8")),
            ('BACKGROUND', (2, 6), (3, 6), colors.HexColor("#f1f5f9")),
            ('TEXTCOLOR', (2, 6), (3, 6), colors.HexColor("#0d9488")),
            ('FONTSIZE', (2, 6), (3, 6), 11),
        ]))
        elements.append(items_table)
        elements.append(Spacer(1, 25))

        # Terms & Signature Block
        signature_data = [
            [
                Paragraph("<b>Terms & Conditions:</b><br/>"
                          "1. This is a computer generated invoice and requires no physical seal.<br/>"
                          "2. Kindly retain this receipt for insurance claims and tax purposes.<br/>"
                          "3. Medicines once dispensed can only be exchanged per pharmacy return policy.", styles['Normal']),
                Paragraph("<b>For MediCare Multispecialty Hospital</b><br/><br/><br/>"
                          "________________________________<br/>"
                          "<b>Authorized Signatory / Accounts Desk</b>", styles['Normal'])
            ]
        ]
        sig_table = Table(signature_data, colWidths=[340, 200])
        sig_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ]))
        elements.append(sig_table)

        doc.build(elements)
        return filepath

    @classmethod
    def generate_prescription_pdf(cls, rx_data: Dict[str, Any]) -> str:
        """Generates a professional Rx medical prescription PDF."""
        if not REPORTLAB_AVAILABLE:
            raise RuntimeError("ReportLab library is not installed. Please run: pip install reportlab")

        _, rx_dir = cls.get_output_dirs()
        rx_id = rx_data.get("prescription_id", 0)
        filename = f"Prescription_RX-{rx_id:04d}.pdf"
        filepath = os.path.join(rx_dir, filename)

        doc = SimpleDocTemplate(
            filepath,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        styles = getSampleStyleSheet()
        elements = []

        # Hospital Letterhead
        title_style = ParagraphStyle(
            'RxTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=16,
            textColor=colors.HexColor("#0d9488"),
            alignment=1,
            spaceAfter=2
        )
        elements.append(Paragraph("MEDICARE MULTISPECIALTY HOSPITAL", title_style))
        elements.append(Paragraph("Outpatient Department & Clinical Consultation", ParagraphStyle('Sub', parent=styles['Normal'], alignment=1, fontSize=9, textColor=colors.HexColor("#64748b"))))
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0d9488"), spaceAfter=10))

        # Doctor & Patient Header Box
        patient_info = [
            [
                Paragraph(f"<b>CONSULTING DOCTOR:</b><br/>"
                          f"<b>{rx_data.get('doctor_name', 'Doctor')}</b><br/>"
                          f"Specialization: {rx_data.get('doctor_dept', 'General Medicine')}<br/>"
                          f"Reg. No: MED-{rx_data.get('doctor_id', '00'):04d}-DEL", styles['Normal']),
                Paragraph(f"<b>PATIENT INFORMATION:</b><br/>"
                          f"<b>{rx_data.get('patient_name', 'Patient')}</b> (ID: #{rx_data.get('patient_id', '')})<br/>"
                          f"Age/Gender: {rx_data.get('age', 'N/A')} Yrs / {rx_data.get('gender', 'N/A')}<br/>"
                          f"Phone: {rx_data.get('patient_phone', 'N/A')}<br/>"
                          f"Date: {rx_data.get('date', datetime.date.today().strftime('%Y-%m-%d'))}", styles['Normal'])
            ]
        ]
        info_table = Table(patient_info, colWidths=[270, 270])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ('PADDING', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 10))

        # Diagnosis
        diag_style = ParagraphStyle('Diag', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold', textColor=colors.HexColor("#1e293b"))
        elements.append(Paragraph(f"DIAGNOSIS & CLINICAL IMPRESSION: <font color='#0d9488'>{rx_data.get('diagnosis', 'Routine Evaluation')}</font>", diag_style))
        elements.append(Spacer(1, 10))

        # Rx Emblem & Medicines Table
        rx_symbol_style = ParagraphStyle('RxSym', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=18, textColor=colors.HexColor("#0d9488"))
        elements.append(Paragraph("℞ (Prescribed Medications)", rx_symbol_style))
        elements.append(Spacer(1, 4))

        med_list = []
        try:
            med_list = json.loads(rx_data.get("medicines_json", "[]"))
        except Exception:
            med_list = []

        table_rows = [["#", "Medicine Name", "Dosage", "Frequency & Timing", "Duration"]]
        if not med_list:
            table_rows.append(["-", "No medicines recorded", "-", "-", "-"])
        else:
            for idx, m in enumerate(med_list, start=1):
                table_rows.append([
                    str(idx),
                    m.get("name", ""),
                    m.get("dosage", ""),
                    m.get("frequency", ""),
                    m.get("duration", "")
                ])

        med_table = Table(table_rows, colWidths=[25, 200, 95, 130, 90])
        med_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0d9488")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ('PADDING', (0, 0), (-1, -1), 6),
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ]))
        elements.append(med_table)
        elements.append(Spacer(1, 15))

        # Advice & Lifestyle Recommendations
        advice_text = rx_data.get("advice", "Rest well, maintain proper hydration, and follow dosage strictly.")
        elements.append(Paragraph("<b>GENERAL ADVICE & INSTRUCTIONS:</b>", styles['Normal']))
        elements.append(Paragraph(f"<font color='#334155'>{advice_text}</font>", styles['Normal']))
        elements.append(Spacer(1, 35))

        # Doctor Signature
        sig_data = [
            [
                Paragraph("<i>Follow up in OPD after 7 days or in case of emergency.</i>", styles['Normal']),
                Paragraph("<b>Doctor's Signature & Stamp:</b><br/><br/><br/>___________________________", styles['Normal'])
            ]
        ]
        s_table = Table(sig_data, colWidths=[330, 210])
        s_table.setStyle(TableStyle([
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
        ]))
        elements.append(s_table)

        doc.build(elements)
        return filepath

    @staticmethod
    def open_pdf_safely(filepath: str):
        """Attempts to open the generated PDF in the default operating system viewer."""
        try:
            if sys.platform.startswith("win"):
                os.startfile(filepath)
            elif sys.platform.startswith("darwin"):
                subprocess.Popen(["open", filepath])
            else:
                subprocess.Popen(["xdg-open", filepath])
        except Exception as e:
            print(f"Could not open file automatically: {e}")


# --------------------------------------------------------------------------------------
# 4. CUSTOM WIDGETS & MODERN UI HELPERS
# --------------------------------------------------------------------------------------
class StatCard(ctk.CTkFrame if USE_CUSTOMTKINTER else tk.Frame):
    """Modern KPI metric card for Dashboard."""

    def __init__(self, parent, title: str, value: str, icon: str, color_accent: str, is_dark: bool = True, **kwargs):
        if USE_CUSTOMTKINTER:
            super().__init__(parent, corner_radius=12, border_width=1, border_color="#334155" if is_dark else "#cbd5e1", **kwargs)
            self.configure(fg_color="#1e293b" if is_dark else "#ffffff")

            top_row = ctk.CTkFrame(self, fg_color="transparent")
            top_row.pack(fill="x", padx=16, pady=(14, 4))

            title_lbl = ctk.CTkLabel(top_row, text=title, font=ctk.CTkFont(size=12, weight="bold"), text_color="#94a3b8" if is_dark else "#64748b")
            title_lbl.pack(side="left")

            icon_lbl = ctk.CTkLabel(top_row, text=icon, font=ctk.CTkFont(size=20), text_color=color_accent)
            icon_lbl.pack(side="right")

            self.val_lbl = ctk.CTkLabel(self, text=value, font=ctk.CTkFont(size=26, weight="bold"), text_color=color_accent)
            self.val_lbl.pack(anchor="w", padx=16, pady=(0, 14))
        else:
            super().__init__(parent, bg="#ffffff", bd=1, relief="solid", **kwargs)
            title_lbl = tk.Label(self, text=f"{icon} {title}", font=("Helvetica", 10, "bold"), fg="#64748b", bg="#ffffff")
            title_lbl.pack(anchor="w", padx=10, pady=(8, 2))
            self.val_lbl = tk.Label(self, text=value, font=("Helvetica", 18, "bold"), fg=color_accent, bg="#ffffff")
            self.val_lbl.pack(anchor="w", padx=10, pady=(0, 8))

    def update_value(self, new_val: str):
        self.val_lbl.configure(text=new_val)


# --------------------------------------------------------------------------------------
# 5. MAIN HOSPITAL APPLICATION GUI
# --------------------------------------------------------------------------------------
class HospitalApp(ctk.CTk if USE_CUSTOMTKINTER else tk.Tk):
    """Top-level Hospital & Doctor Appointment System Application."""

    def __init__(self):
        super().__init__()
        self.db = DatabaseManager(DB_NAME)
        self.current_theme = "dark"

        # Window Configuration
        self.title(f"{APP_TITLE} - {APP_VERSION}")
        self.geometry("1280x800")
        self.minsize(1050, 680)

        if USE_CUSTOMTKINTER:
            ctk.set_appearance_mode("dark")
            ctk.set_default_color_theme("blue")

        # Container Setup
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Style TTK Treeviews
        self.setup_treeview_styles()

        # Build UI Structure
        self.build_sidebar()
        self.build_content_area()

        # Navigate to initial tab
        self.switch_tab("dashboard")

    def setup_treeview_styles(self):
        """Applies sleek dark/light modern themes to ttk.Treeview tables."""
        self.style = ttk.Style()
        self.style.theme_use("clam")

        is_dark = (self.current_theme == "dark")
        colors_cfg = THEME_COLORS["dark" if is_dark else "light"]

        self.style.configure(
            "Treeview",
            background=colors_cfg["card_bg"],
            foreground=colors_cfg["text_primary"],
            rowheight=32,
            fieldbackground=colors_cfg["card_bg"],
            bordercolor=colors_cfg["card_border"],
            borderwidth=0,
            font=("Segoe UI", 10)
        )
        self.style.configure(
            "Treeview.Heading",
            background=colors_cfg["table_header"],
            foreground=colors_cfg["primary"] if is_dark else colors_cfg["text_primary"],
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padding=6
        )
        self.style.map(
            "Treeview",
            background=[("selected", colors_cfg["primary"])],
            foreground=[("selected", "#ffffff")]
        )
        self.style.map(
            "Treeview.Heading",
            background=[("active", colors_cfg["table_header"])]
        )

    # ----------------------------------------------------------------------------------
    # SIDEBAR NAVIGATION
    # ----------------------------------------------------------------------------------
    def build_sidebar(self):
        """Constructs left-hand navigation menu with modern branding."""
        is_dark = (self.current_theme == "dark")
        sb_bg = THEME_COLORS["dark" if is_dark else "light"]["sidebar_bg"]

        if USE_CUSTOMTKINTER:
            self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color=sb_bg)
        else:
            self.sidebar = tk.Frame(self, width=220, bg=sb_bg)

        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(8, weight=1)

        # Brand Logo / Title
        brand_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent") if USE_CUSTOMTKINTER else tk.Frame(self.sidebar, bg=sb_bg)
        brand_frame.grid(row=0, column=0, padx=20, pady=(20, 25), sticky="w")

        title_lbl = ctk.CTkLabel(
            brand_frame, text="🏥 MediCare Pro",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#0d9488"
        ) if USE_CUSTOMTKINTER else tk.Label(brand_frame, text="🏥 MediCare Pro", font=("Helvetica", 14, "bold"), fg="#0d9488", bg=sb_bg)
        title_lbl.pack(anchor="w")

        sub_lbl = ctk.CTkLabel(
            brand_frame, text="Hospital Management OS",
            font=ctk.CTkFont(size=11),
            text_color="#64748b"
        ) if USE_CUSTOMTKINTER else tk.Label(brand_frame, text="Hospital Management OS", font=("Helvetica", 9), fg="#64748b", bg=sb_bg)
        sub_lbl.pack(anchor="w")

        # Navigation Buttons
        self.nav_buttons = {}
        nav_items = [
            ("dashboard", "📊  Dashboard"),
            ("patients", "👥  Patients"),
            ("doctors", "👨‍⚕️  Doctors & Slots"),
            ("appointments", "📅  Appointments"),
            ("prescriptions", "📝  Prescriptions"),
            ("billing", "💳  Billing & Invoices")
        ]

        for i, (tab_id, label) in enumerate(nav_items, start=1):
            btn = self.create_nav_button(label, lambda t=tab_id: self.switch_tab(t))
            btn.grid(row=i, column=0, padx=12, pady=4, sticky="ew")
            self.nav_buttons[tab_id] = btn

        # Theme & Info in Footer
        footer_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent") if USE_CUSTOMTKINTER else tk.Frame(self.sidebar, bg=sb_bg)
        footer_frame.grid(row=9, column=0, padx=16, pady=20, sticky="s")

        if USE_CUSTOMTKINTER:
            self.theme_switch = ctk.CTkSwitch(
                footer_frame, text="Dark Theme",
                command=self.toggle_theme,
                font=ctk.CTkFont(size=11),
                progress_color="#0d9488"
            )
            self.theme_switch.select()
            self.theme_switch.pack(anchor="w", pady=(0, 10))

        v_lbl = ctk.CTkLabel(
            footer_frame, text=f"Build: {APP_VERSION}",
            font=ctk.CTkFont(size=10),
            text_color="#475569"
        ) if USE_CUSTOMTKINTER else tk.Label(footer_frame, text=f"Build: {APP_VERSION}", font=("Helvetica", 8), fg="#475569", bg=sb_bg)
        v_lbl.pack(anchor="w")

    def create_nav_button(self, text: str, command):
        """Helper to create sleek navigation buttons."""
        if USE_CUSTOMTKINTER:
            return ctk.CTkButton(
                self.sidebar,
                text=text,
                command=command,
                anchor="w",
                font=ctk.CTkFont(size=13, weight="bold"),
                height=40,
                corner_radius=8,
                fg_color="transparent",
                text_color="#94a3b8",
                hover_color="#1e293b"
            )
        else:
            return tk.Button(
                self.sidebar,
                text=text,
                command=command,
                anchor="w",
                font=("Helvetica", 11),
                relief="flat",
                bd=0,
                bg="#e2e8f0",
                fg="#334155"
            )

    def toggle_theme(self):
        """Switches between Dark and Light appearances dynamically."""
        if not USE_CUSTOMTKINTER:
            return
        if self.theme_switch.get():
            self.current_theme = "dark"
            ctk.set_appearance_mode("dark")
        else:
            self.current_theme = "light"
            ctk.set_appearance_mode("light")

        self.setup_treeview_styles()
        # Refresh current tab to adjust colors
        self.switch_tab(self.active_tab_name)

    # ----------------------------------------------------------------------------------
    # TAB SWITCHING ENGINE
    # ----------------------------------------------------------------------------------
    def build_content_area(self):
        """Creates the primary container frame where tabs will be rendered."""
        bg_col = THEME_COLORS[self.current_theme]["bg_dark"]
        if USE_CUSTOMTKINTER:
            self.content_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=bg_col)
        else:
            self.content_frame = tk.Frame(self, bg=bg_col)

        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        self.tabs = {}
        self.active_tab_name = "dashboard"

    def switch_tab(self, tab_id: str):
        """Destroys previous view and builds target view cleanly."""
        self.active_tab_name = tab_id

        # Update button highlighting
        for k, btn in self.nav_buttons.items():
            if USE_CUSTOMTKINTER:
                if k == tab_id:
                    btn.configure(fg_color="#0d9488", text_color="#ffffff")
                else:
                    btn.configure(fg_color="transparent", text_color="#94a3b8" if self.current_theme == "dark" else "#334155")

        # Clear existing tab content
        for child in self.content_frame.winfo_children():
            child.destroy()

        # Render selected tab
        if tab_id == "dashboard":
            self.render_dashboard()
        elif tab_id == "patients":
            self.render_patients_tab()
        elif tab_id == "doctors":
            self.render_doctors_tab()
        elif tab_id == "appointments":
            self.render_appointments_tab()
        elif tab_id == "prescriptions":
            self.render_prescriptions_tab()
        elif tab_id == "billing":
            self.render_billing_tab()

    # ----------------------------------------------------------------------------------
    # 1. DASHBOARD TAB
    # ----------------------------------------------------------------------------------
    def render_dashboard(self):
        metrics = self.db.get_dashboard_metrics()
        is_dark = (self.current_theme == "dark")

        dash_container = ctk.CTkScrollableFrame(self.content_frame, fg_color="transparent") if USE_CUSTOMTKINTER else tk.Frame(self.content_frame)
        dash_container.pack(fill="both", expand=True)

        # Header Title Banner
        hdr_frame = ctk.CTkFrame(dash_container, fg_color="transparent")
        hdr_frame.pack(fill="x", pady=(0, 15))

        title = ctk.CTkLabel(hdr_frame, text="Hospital Operations Dashboard", font=ctk.CTkFont(size=22, weight="bold"))
        title.pack(side="left")

        refresh_btn = ctk.CTkButton(
            hdr_frame, text="🔄 Refresh Stats", width=120, height=32,
            command=self.render_dashboard,
            fg_color="#0d9488", hover_color="#0f766e"
        )
        refresh_btn.pack(side="right")

        # 4 Metric Cards
        cards_frame = ctk.CTkFrame(dash_container, fg_color="transparent")
        cards_frame.pack(fill="x", pady=(0, 20))
        for col_idx in range(4):
            cards_frame.grid_columnconfigure(col_idx, weight=1)

        card1 = StatCard(cards_frame, "Total Patients", str(metrics["total_patients"]), "👥", "#0d9488", is_dark)
        card1.grid(row=0, column=0, padx=8, sticky="ew")

        card2 = StatCard(cards_frame, "Active Doctors", str(metrics["active_doctors"]), "👨‍⚕️", "#06b6d4", is_dark)
        card2.grid(row=0, column=1, padx=8, sticky="ew")

        card3 = StatCard(cards_frame, "Today's Appointments", str(metrics["today_appointments"]), "📅", "#f59e0b", is_dark)
        card3.grid(row=0, column=2, padx=8, sticky="ew")

        rev_text = f"{DEFAULT_CURRENCY} {metrics['total_revenue']:,.2f}"
        card4 = StatCard(cards_frame, "Total Revenue (Paid)", rev_text, "💰", "#10b981", is_dark)
        card4.grid(row=0, column=3, padx=8, sticky="ew")

        # Quick Patient / Doctor Search Bar
        search_card = ctk.CTkFrame(dash_container, corner_radius=10, fg_color="#1e293b" if is_dark else "#ffffff")
        search_card.pack(fill="x", pady=(0, 20), ipady=8)

        search_lbl = ctk.CTkLabel(search_card, text="🔍 Global Patient Quick Lookup:", font=ctk.CTkFont(weight="bold"))
        search_lbl.pack(side="left", padx=16)

        search_entry = ctk.CTkEntry(search_card, placeholder_text="Enter Patient Name, ID, or Phone...", width=320)
        search_entry.pack(side="left", padx=8)

        def do_quick_search():
            q = search_entry.get().strip()
            if not q:
                messagebox.showinfo("Search", "Please enter a search query.")
                return
            results = self.db.search_patients(q)
            if results:
                self.show_patient_details_modal(results[0]["patient_id"])
            else:
                messagebox.showwarning("Search", f"No patients found matching '{q}'.")

        search_btn = ctk.CTkButton(search_card, text="Find Patient", width=100, command=do_quick_search, fg_color="#0d9488")
        search_btn.pack(side="left", padx=8)

        # Recent Appointments Section
        sec_lbl = ctk.CTkLabel(dash_container, text="Recent Appointments & Quick Actions", font=ctk.CTkFont(size=16, weight="bold"))
        sec_lbl.pack(anchor="w", pady=(5, 10))

        table_card = ctk.CTkFrame(dash_container, corner_radius=10, fg_color="#1e293b" if is_dark else "#ffffff")
        table_card.pack(fill="both", expand=True)

        cols = ("ID", "Date", "Slot", "Patient", "Doctor", "Department", "Status")
        self.dash_tree = ttk.Treeview(table_card, columns=cols, show="headings", height=8)

        self.dash_tree.heading("ID", text="Appt ID")
        self.dash_tree.heading("Date", text="Date")
        self.dash_tree.heading("Slot", text="Time Slot")
        self.dash_tree.heading("Patient", text="Patient Name")
        self.dash_tree.heading("Doctor", text="Doctor")
        self.dash_tree.heading("Department", text="Specialization")
        self.dash_tree.heading("Status", text="Status")

        self.dash_tree.column("ID", width=60, anchor="center")
        self.dash_tree.column("Date", width=90, anchor="center")
        self.dash_tree.column("Slot", width=90, anchor="center")
        self.dash_tree.column("Patient", width=150, anchor="w")
        self.dash_tree.column("Doctor", width=150, anchor="w")
        self.dash_tree.column("Department", width=120, anchor="w")
        self.dash_tree.column("Status", width=90, anchor="center")

        tree_scroll = ttk.Scrollbar(table_card, orient="vertical", command=self.dash_tree.yview)
        self.dash_tree.configure(yscrollcommand=tree_scroll.set)

        self.dash_tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        tree_scroll.pack(side="right", fill="y", padx=(0, 10), pady=10)

        # Load recent 10 appointments
        recent_appts = self.db.get_all_appointments(limit=12)
        for a in recent_appts:
            self.dash_tree.insert("", "end", values=(
                f"#{a['appointment_id']}",
                a["appointment_date"],
                a["time_slot"],
                a["patient_name"],
                a["doctor_name"],
                a["doctor_dept"],
                a["status"]
            ))

        # Action Buttons below Recent Appointments Table
        btn_bar = ctk.CTkFrame(dash_container, fg_color="transparent")
        btn_bar.pack(fill="x", pady=12)

        def mark_selected_done():
            sel = self.dash_tree.selection()
            if not sel:
                messagebox.showwarning("Select Appointment", "Please select an appointment from the table.")
                return
            appt_id_str = self.dash_tree.item(sel[0])["values"][0]
            appt_id = int(str(appt_id_str).replace("#", ""))
            self.db.update_appointment_status(appt_id, "Completed")
            messagebox.showinfo("Success", f"Appointment #{appt_id} marked as Completed!")
            self.render_dashboard()

        def cancel_selected():
            sel = self.dash_tree.selection()
            if not sel:
                messagebox.showwarning("Select Appointment", "Please select an appointment from the table.")
                return
            appt_id_str = self.dash_tree.item(sel[0])["values"][0]
            appt_id = int(str(appt_id_str).replace("#", ""))
            confirm = messagebox.askyesno("Confirm Cancellation", f"Are you sure you want to cancel Appointment #{appt_id}?")
            if confirm:
                self.db.update_appointment_status(appt_id, "Cancelled")
                messagebox.showinfo("Cancelled", f"Appointment #{appt_id} has been cancelled.")
                self.render_dashboard()

        def bill_selected():
            sel = self.dash_tree.selection()
            if not sel:
                messagebox.showwarning("Select Appointment", "Please select an appointment from the table.")
                return
            self.switch_tab("billing")

        ctk.CTkButton(btn_bar, text="✓ Mark as Completed", width=140, fg_color="#10b981", hover_color="#059669", command=mark_selected_done).pack(side="left", padx=5)
        ctk.CTkButton(btn_bar, text="💳 Generate Invoice", width=140, fg_color="#0d9488", hover_color="#0f766e", command=bill_selected).pack(side="left", padx=5)
        ctk.CTkButton(btn_bar, text="✕ Cancel Appointment", width=140, fg_color="#ef4444", hover_color="#dc2626", command=cancel_selected).pack(side="left", padx=5)

    # ----------------------------------------------------------------------------------
    # 2. PATIENTS MANAGEMENT TAB
    # ----------------------------------------------------------------------------------
    def render_patients_tab(self):
        is_dark = (self.current_theme == "dark")

        top_bar = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        top_bar.pack(fill="x", pady=(0, 10))

        title = ctk.CTkLabel(top_bar, text="Patient Directory & Medical Records", font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(side="left")

        add_btn = ctk.CTkButton(
            top_bar, text="+ Register New Patient",
            fg_color="#0d9488", hover_color="#0f766e",
            command=self.open_patient_modal
        )
        add_btn.pack(side="right")

        # Search / Filter Bar
        filter_card = ctk.CTkFrame(self.content_frame, corner_radius=8, fg_color="#1e293b" if is_dark else "#ffffff")
        filter_card.pack(fill="x", pady=(0, 10), ipady=4)

        search_entry = ctk.CTkEntry(filter_card, placeholder_text="Filter by Name, Phone, or Blood Group...", width=360)
        search_entry.pack(side="left", padx=10, pady=8)

        def apply_patient_filter():
            q = search_entry.get().strip()
            data = self.db.search_patients(q) if q else self.db.get_all_patients()
            self.load_patients_table(data)

        filter_btn = ctk.CTkButton(filter_card, text="Filter", width=90, fg_color="#0d9488", command=apply_patient_filter)
        filter_btn.pack(side="left", padx=5)

        reset_btn = ctk.CTkButton(filter_card, text="Reset", width=90, fg_color="#64748b", command=lambda: [search_entry.delete(0, 'end'), self.load_patients_table(self.db.get_all_patients())])
        reset_btn.pack(side="left", padx=5)

        # Table Container
        table_frame = ctk.CTkFrame(self.content_frame, corner_radius=8, fg_color="#1e293b" if is_dark else "#ffffff")
        table_frame.pack(fill="both", expand=True)

        cols = ("ID", "Name", "Age", "Gender", "Phone", "Blood Group", "Address", "Registered Date")
        self.patient_tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=14)

        self.patient_tree.heading("ID", text="Patient ID")
        self.patient_tree.heading("Name", text="Full Name")
        self.patient_tree.heading("Age", text="Age")
        self.patient_tree.heading("Gender", text="Gender")
        self.patient_tree.heading("Phone", text="Phone Number")
        self.patient_tree.heading("Blood Group", text="Blood Group")
        self.patient_tree.heading("Address", text="Address")
        self.patient_tree.heading("Registered Date", text="Registered On")

        self.patient_tree.column("ID", width=65, anchor="center")
        self.patient_tree.column("Name", width=150, anchor="w")
        self.patient_tree.column("Age", width=50, anchor="center")
        self.patient_tree.column("Gender", width=70, anchor="center")
        self.patient_tree.column("Phone", width=110, anchor="center")
        self.patient_tree.column("Blood Group", width=85, anchor="center")
        self.patient_tree.column("Address", width=180, anchor="w")
        self.patient_tree.column("Registered Date", width=100, anchor="center")

        p_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.patient_tree.yview)
        self.patient_tree.configure(yscrollcommand=p_scroll.set)

        self.patient_tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        p_scroll.pack(side="right", fill="y", padx=(0, 10), pady=10)

        # Bottom Actions
        actions_bar = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        actions_bar.pack(fill="x", pady=10)

        def edit_patient_action():
            sel = self.patient_tree.selection()
            if not sel:
                messagebox.showwarning("Select", "Please select a patient to edit.")
                return
            p_id = int(self.patient_tree.item(sel[0])["values"][0])
            self.open_patient_modal(p_id)

        def delete_patient_action():
            sel = self.patient_tree.selection()
            if not sel:
                messagebox.showwarning("Select", "Please select a patient to delete.")
                return
            p_id = int(self.patient_tree.item(sel[0])["values"][0])
            p_name = self.patient_tree.item(sel[0])["values"][1]
            confirm = messagebox.askyesno("Delete Patient", f"Are you sure you want to permanently delete patient '{p_name}' (ID: #{p_id})?\nAll related appointments, prescriptions, and bills will also be removed.")
            if confirm:
                self.db.delete_patient(p_id)
                messagebox.showinfo("Deleted", "Patient record deleted successfully.")
                self.load_patients_table(self.db.get_all_patients())

        def view_history_action():
            sel = self.patient_tree.selection()
            if not sel:
                messagebox.showwarning("Select", "Please select a patient to view history.")
                return
            p_id = int(self.patient_tree.item(sel[0])["values"][0])
            self.show_patient_details_modal(p_id)

        ctk.CTkButton(actions_bar, text="📋 View Complete Medical History", fg_color="#06b6d4", hover_color="#0284c7", command=view_history_action).pack(side="left", padx=5)
        ctk.CTkButton(actions_bar, text="✏️ Edit Patient Details", fg_color="#f59e0b", hover_color="#d97706", command=edit_patient_action).pack(side="left", padx=5)
        ctk.CTkButton(actions_bar, text="🗑️ Delete Patient", fg_color="#ef4444", hover_color="#dc2626", command=delete_patient_action).pack(side="left", padx=5)

        self.load_patients_table(self.db.get_all_patients())

    def load_patients_table(self, patients: List[Dict[str, Any]]):
        for item in self.patient_tree.get_children():
            self.patient_tree.delete(item)
        for p in patients:
            self.patient_tree.insert("", "end", values=(
                p["patient_id"],
                p["name"],
                p["age"],
                p["gender"],
                p["phone"],
                p["blood_group"],
                p["address"],
                p["created_at"]
            ))

    def open_patient_modal(self, patient_id: Optional[int] = None):
        """Modal for registering or editing a patient record."""
        is_edit = patient_id is not None
        modal = ctk.CTkToplevel(self) if USE_CUSTOMTKINTER else tk.Toplevel(self)
        modal.title("Edit Patient" if is_edit else "Register New Patient")
        modal.geometry("500x560")
        modal.resizable(False, False)
        modal.grab_set()

        title_text = "Edit Patient Information" if is_edit else "Patient Registration Form"
        ctk.CTkLabel(modal, text=title_text, font=ctk.CTkFont(size=18, weight="bold")).pack(pady=15)

        form_frame = ctk.CTkFrame(modal, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=30, pady=5)

        # Fields
        ctk.CTkLabel(form_frame, text="Full Name *").pack(anchor="w")
        name_entry = ctk.CTkEntry(form_frame, width=440)
        name_entry.pack(pady=(2, 10))

        age_gen_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        age_gen_frame.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(age_gen_frame, text="Age *").grid(row=0, column=0, sticky="w")
        age_entry = ctk.CTkEntry(age_gen_frame, width=120)
        age_entry.grid(row=1, column=0, sticky="w", padx=(0, 15))

        ctk.CTkLabel(age_gen_frame, text="Gender *").grid(row=0, column=1, sticky="w")
        gender_cb = ctk.CTkComboBox(age_gen_frame, values=["Male", "Female", "Other"], width=130)
        gender_cb.grid(row=1, column=1, sticky="w", padx=(0, 15))

        ctk.CTkLabel(age_gen_frame, text="Blood Group").grid(row=0, column=2, sticky="w")
        blood_cb = ctk.CTkComboBox(age_gen_frame, values=["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"], width=130)
        blood_cb.grid(row=1, column=2, sticky="w")

        ctk.CTkLabel(form_frame, text="Contact Phone (10 Digits) *").pack(anchor="w")
        phone_entry = ctk.CTkEntry(form_frame, width=440)
        phone_entry.pack(pady=(2, 10))

        ctk.CTkLabel(form_frame, text="Residential Address").pack(anchor="w")
        addr_entry = ctk.CTkEntry(form_frame, width=440)
        addr_entry.pack(pady=(2, 15))

        # Pre-populate if editing
        if is_edit:
            history = self.db.get_patient_history(patient_id)
            p = history["patient"]
            if p:
                name_entry.insert(0, p["name"])
                age_entry.insert(0, str(p["age"]))
                gender_cb.set(p["gender"])
                blood_cb.set(p["blood_group"])
                phone_entry.insert(0, p["phone"])
                addr_entry.insert(0, p["address"] or "")

        def save_patient():
            name = name_entry.get().strip()
            age_str = age_entry.get().strip()
            gender = gender_cb.get().strip()
            blood = blood_cb.get().strip()
            phone = phone_entry.get().strip()
            addr = addr_entry.get().strip()

            # Strict Validations
            if not name:
                messagebox.showerror("Validation Error", "Patient Name is mandatory.")
                return
            if not age_str.isdigit() or int(age_str) <= 0 or int(age_str) > 130:
                messagebox.showerror("Validation Error", "Age must be a valid positive integer between 1 and 130.")
                return
            if not phone.isdigit() or len(phone) < 7:
                messagebox.showerror("Validation Error", "Please provide a valid phone number (at least 7-10 digits).")
                return

            age = int(age_str)
            if is_edit:
                self.db.update_patient(patient_id, name, age, gender, phone, blood, addr)
                messagebox.showinfo("Saved", "Patient details updated successfully.")
            else:
                self.db.add_patient(name, age, gender, blood, phone, addr)
                messagebox.showinfo("Success", "New patient registered successfully.")

            modal.destroy()
            self.load_patients_table(self.db.get_all_patients())

        save_btn = ctk.CTkButton(modal, text="Save Patient Record", fg_color="#0d9488", hover_color="#0f766e", width=220, command=save_patient)
        save_btn.pack(pady=(0, 20))

    def show_patient_details_modal(self, patient_id: int):
        """Displays comprehensive medical history modal including appointments, prescriptions, and bills."""
        data = self.db.get_patient_history(patient_id)
        p = data.get("patient")
        if not p:
            messagebox.showerror("Error", "Patient not found.")
            return

        modal = ctk.CTkToplevel(self) if USE_CUSTOMTKINTER else tk.Toplevel(self)
        modal.title(f"Patient Dossier - {p['name']} (ID: #{p['patient_id']})")
        modal.geometry("750x600")
        modal.grab_set()

        scroll_content = ctk.CTkScrollableFrame(modal, fg_color="transparent")
        scroll_content.pack(fill="both", expand=True, padx=20, pady=20)

        # Patient Header Card
        info_card = ctk.CTkFrame(scroll_content, corner_radius=10, fg_color="#1e293b" if self.current_theme == "dark" else "#e2e8f0")
        info_card.pack(fill="x", pady=(0, 15), padx=5, ipady=10)

        ctk.CTkLabel(info_card, text=f"👤 {p['name']}", font=ctk.CTkFont(size=20, weight="bold"), text_color="#0d9488").pack(anchor="w", padx=15, pady=(5, 2))
        sub_info = f"Age: {p['age']} | Gender: {p['gender']} | Blood Group: {p['blood_group']} | Phone: {p['phone']}\nAddress: {p['address'] or 'N/A'}"
        ctk.CTkLabel(info_card, text=sub_info, font=ctk.CTkFont(size=12), justify="left").pack(anchor="w", padx=15)

        # Appointments Sub-history
        ctk.CTkLabel(scroll_content, text="📅 Appointment History:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(10, 5))
        appts = data.get("appointments", [])
        if not appts:
            ctk.CTkLabel(scroll_content, text="No appointments booked yet.", text_color="#94a3b8").pack(anchor="w", padx=10)
        else:
            for a in appts:
                a_box = ctk.CTkFrame(scroll_content, corner_radius=6)
                a_box.pack(fill="x", pady=4, padx=5)
                ctk.CTkLabel(a_box, text=f"{a['appointment_date']} ({a['time_slot']}) | {a['doctor_name']} ({a['specialization']}) | Status: {a['status']} | Notes: {a['notes'] or 'None'}",
                             font=ctk.CTkFont(size=11)).pack(anchor="w", padx=10, pady=6)

        # Prescriptions Sub-history
        ctk.CTkLabel(scroll_content, text="📝 Medical Prescriptions:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(15, 5))
        rxs = data.get("prescriptions", [])
        if not rxs:
            ctk.CTkLabel(scroll_content, text="No prescriptions recorded.", text_color="#94a3b8").pack(anchor="w", padx=10)
        else:
            for rx in rxs:
                rx_box = ctk.CTkFrame(scroll_content, corner_radius=6)
                rx_box.pack(fill="x", pady=4, padx=5)
                ctk.CTkLabel(rx_box, text=f"Date: {rx['date']} | Doctor: {rx['doctor_name']} | Diagnosis: {rx['diagnosis']}\nAdvice: {rx['advice'] or 'N/A'}",
                             font=ctk.CTkFont(size=11), justify="left").pack(anchor="w", padx=10, pady=6)

        # Billing Sub-history
        ctk.CTkLabel(scroll_content, text="💳 Billing & Invoices:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(15, 5))
        bills = data.get("bills", [])
        if not bills:
            ctk.CTkLabel(scroll_content, text="No billing records.", text_color="#94a3b8").pack(anchor="w", padx=10)
        else:
            for b in bills:
                b_box = ctk.CTkFrame(scroll_content, corner_radius=6)
                b_box.pack(fill="x", pady=4, padx=5)
                ctk.CTkLabel(b_box, text=f"Bill #INV-{b['bill_id']:04d} | Total: {DEFAULT_CURRENCY} {b['total_amount']:.2f} | Status: {b['payment_status']} ({b['payment_mode']}) | Date: {b['date']}",
                             font=ctk.CTkFont(size=11)).pack(anchor="w", padx=10, pady=6)

    # ----------------------------------------------------------------------------------
    # 3. DOCTORS & SCHEDULE MANAGEMENT TAB
    # ----------------------------------------------------------------------------------
    def render_doctors_tab(self):
        is_dark = (self.current_theme == "dark")

        top_bar = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        top_bar.pack(fill="x", pady=(0, 10))

        title = ctk.CTkLabel(top_bar, text="Doctor & Schedule Management", font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(side="left")

        add_btn = ctk.CTkButton(
            top_bar, text="+ Add New Doctor",
            fg_color="#0d9488", hover_color="#0f766e",
            command=self.open_doctor_modal
        )
        add_btn.pack(side="right")

        table_frame = ctk.CTkFrame(self.content_frame, corner_radius=8, fg_color="#1e293b" if is_dark else "#ffffff")
        table_frame.pack(fill="both", expand=True)

        cols = ("ID", "Doctor Name", "Specialization", "Contact Phone", "Email", "Available Days", "Consultation Fee")
        self.doc_tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=14)

        self.doc_tree.heading("ID", text="Doctor ID")
        self.doc_tree.heading("Doctor Name", text="Doctor Name")
        self.doc_tree.heading("Specialization", text="Specialization")
        self.doc_tree.heading("Contact Phone", text="Phone")
        self.doc_tree.heading("Email", text="Email")
        self.doc_tree.heading("Available Days", text="Available Days")
        self.doc_tree.heading("Consultation Fee", text=f"Fee ({DEFAULT_CURRENCY})")

        self.doc_tree.column("ID", width=65, anchor="center")
        self.doc_tree.column("Doctor Name", width=160, anchor="w")
        self.doc_tree.column("Specialization", width=140, anchor="w")
        self.doc_tree.column("Contact Phone", width=110, anchor="center")
        self.doc_tree.column("Email", width=160, anchor="w")
        self.doc_tree.column("Available Days", width=140, anchor="w")
        self.doc_tree.column("Consultation Fee", width=100, anchor="center")

        doc_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.doc_tree.yview)
        self.doc_tree.configure(yscrollcommand=doc_scroll.set)

        self.doc_tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        doc_scroll.pack(side="right", fill="y", padx=(0, 10), pady=10)

        # Action Buttons
        actions_bar = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        actions_bar.pack(fill="x", pady=10)

        def edit_doctor_action():
            sel = self.doc_tree.selection()
            if not sel:
                messagebox.showwarning("Select", "Please select a doctor to edit.")
                return
            d_id = int(self.doc_tree.item(sel[0])["values"][0])
            self.open_doctor_modal(d_id)

        def delete_doctor_action():
            sel = self.doc_tree.selection()
            if not sel:
                messagebox.showwarning("Select", "Please select a doctor to delete.")
                return
            d_id = int(self.doc_tree.item(sel[0])["values"][0])
            d_name = self.doc_tree.item(sel[0])["values"][1]
            confirm = messagebox.askyesno("Delete Doctor", f"Are you sure you want to delete {d_name} (ID: #{d_id})?\nAppointments scheduled for this doctor will also be impacted.")
            if confirm:
                self.db.delete_doctor(d_id)
                messagebox.showinfo("Deleted", "Doctor record deleted successfully.")
                self.load_doctors_table()

        ctk.CTkButton(actions_bar, text="✏️ Edit Doctor Details", fg_color="#f59e0b", hover_color="#d97706", command=edit_doctor_action).pack(side="left", padx=5)
        ctk.CTkButton(actions_bar, text="🗑️ Remove Doctor", fg_color="#ef4444", hover_color="#dc2626", command=delete_doctor_action).pack(side="left", padx=5)

        self.load_doctors_table()

    def load_doctors_table(self):
        for item in self.doc_tree.get_children():
            self.doc_tree.delete(item)
        docs = self.db.get_all_doctors()
        for d in docs:
            self.doc_tree.insert("", "end", values=(
                d["doctor_id"],
                d["name"],
                d["specialization"],
                d["phone"],
                d["email"] or "N/A",
                d["available_days"],
                f"{d['fee']:.2f}"
            ))

    def open_doctor_modal(self, doctor_id: Optional[int] = None):
        """Modal for adding or editing a doctor record."""
        is_edit = doctor_id is not None
        modal = ctk.CTkToplevel(self) if USE_CUSTOMTKINTER else tk.Toplevel(self)
        modal.title("Edit Doctor" if is_edit else "Add New Doctor")
        modal.geometry("500x560")
        modal.resizable(False, False)
        modal.grab_set()

        ctk.CTkLabel(modal, text="Doctor Profile & Schedule Setup", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=15)

        form_frame = ctk.CTkFrame(modal, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=30, pady=5)

        ctk.CTkLabel(form_frame, text="Doctor Full Name (e.g., Dr. Jane Doe) *").pack(anchor="w")
        name_entry = ctk.CTkEntry(form_frame, width=440)
        name_entry.pack(pady=(2, 10))

        ctk.CTkLabel(form_frame, text="Specialization *").pack(anchor="w")
        dept_cb = ctk.CTkComboBox(form_frame, values=[
            "Cardiology", "Neurology", "Pediatrics", "Orthopedics",
            "General Medicine", "Dermatology", "Gynecology & Obstetrics",
            "Ophthalmology", "ENT Specialist", "Oncology", "Psychiatry"
        ], width=440)
        dept_cb.pack(pady=(2, 10))

        contact_row = ctk.CTkFrame(form_frame, fg_color="transparent")
        contact_row.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(contact_row, text="Phone Number *").grid(row=0, column=0, sticky="w")
        phone_entry = ctk.CTkEntry(contact_row, width=210)
        phone_entry.grid(row=1, column=0, sticky="w", padx=(0, 20))

        ctk.CTkLabel(contact_row, text="Email Address").grid(row=0, column=1, sticky="w")
        email_entry = ctk.CTkEntry(contact_row, width=210)
        email_entry.grid(row=1, column=1, sticky="w")

        ctk.CTkLabel(form_frame, text="Available Consultation Days (e.g. Mon, Wed, Fri) *").pack(anchor="w")
        days_entry = ctk.CTkEntry(form_frame, width=440)
        days_entry.pack(pady=(2, 10))

        ctk.CTkLabel(form_frame, text=f"Consultation Fee ({DEFAULT_CURRENCY}) *").pack(anchor="w")
        fee_entry = ctk.CTkEntry(form_frame, width=440)
        fee_entry.pack(pady=(2, 15))

        if is_edit:
            docs = self.db.get_all_doctors()
            doc = next((d for d in docs if d["doctor_id"] == doctor_id), None)
            if doc:
                name_entry.insert(0, doc["name"])
                dept_cb.set(doc["specialization"])
                phone_entry.insert(0, doc["phone"])
                email_entry.insert(0, doc["email"] or "")
                days_entry.insert(0, doc["available_days"])
                fee_entry.insert(0, str(doc["fee"]))

        def save_doc():
            name = name_entry.get().strip()
            dept = dept_cb.get().strip()
            phone = phone_entry.get().strip()
            email = email_entry.get().strip()
            days = days_entry.get().strip()
            fee_str = fee_entry.get().strip()

            if not name or not dept or not days:
                messagebox.showerror("Validation Error", "Name, Specialization, and Available Days are required.")
                return
            if not phone.isdigit() or len(phone) < 7:
                messagebox.showerror("Validation Error", "Please provide a valid phone number.")
                return
            try:
                fee = float(fee_str)
                if fee < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Validation Error", "Consultation fee must be a non-negative number.")
                return

            if is_edit:
                self.db.update_doctor(doctor_id, name, dept, phone, email, days, fee)
                messagebox.showinfo("Success", "Doctor record updated successfully.")
            else:
                self.db.add_doctor(name, dept, phone, email, days, fee)
                messagebox.showinfo("Success", "New Doctor registered successfully.")

            modal.destroy()
            self.load_doctors_table()

        save_btn = ctk.CTkButton(modal, text="Save Doctor Record", fg_color="#0d9488", hover_color="#0f766e", width=220, command=save_doc)
        save_btn.pack(pady=(0, 20))

    # ----------------------------------------------------------------------------------
    # 4. APPOINTMENT BOOKING TAB
    # ----------------------------------------------------------------------------------
    def render_appointments_tab(self):
        is_dark = (self.current_theme == "dark")

        top_bar = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        top_bar.pack(fill="x", pady=(0, 10))

        title = ctk.CTkLabel(top_bar, text="Doctor Appointment Scheduling & Management", font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(side="left")

        book_btn = ctk.CTkButton(
            top_bar, text="+ Book New Appointment",
            fg_color="#0d9488", hover_color="#0f766e",
            command=self.open_appointment_modal
        )
        book_btn.pack(side="right")

        table_frame = ctk.CTkFrame(self.content_frame, corner_radius=8, fg_color="#1e293b" if is_dark else "#ffffff")
        table_frame.pack(fill="both", expand=True)

        cols = ("ID", "Date", "Time Slot", "Patient Name", "Contact Phone", "Consulting Doctor", "Department", "Status", "Notes")
        self.appt_tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=14)

        self.appt_tree.heading("ID", text="ID")
        self.appt_tree.heading("Date", text="Date")
        self.appt_tree.heading("Time Slot", text="Time Slot")
        self.appt_tree.heading("Patient Name", text="Patient Name")
        self.appt_tree.heading("Contact Phone", text="Phone")
        self.appt_tree.heading("Consulting Doctor", text="Doctor")
        self.appt_tree.heading("Department", text="Specialization")
        self.appt_tree.heading("Status", text="Status")
        self.appt_tree.heading("Notes", text="Notes / Symptoms")

        self.appt_tree.column("ID", width=50, anchor="center")
        self.appt_tree.column("Date", width=90, anchor="center")
        self.appt_tree.column("Time Slot", width=85, anchor="center")
        self.appt_tree.column("Patient Name", width=140, anchor="w")
        self.appt_tree.column("Contact Phone", width=100, anchor="center")
        self.appt_tree.column("Consulting Doctor", width=140, anchor="w")
        self.appt_tree.column("Department", width=120, anchor="w")
        self.appt_tree.column("Status", width=90, anchor="center")
        self.appt_tree.column("Notes", width=160, anchor="w")

        appt_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.appt_tree.yview)
        self.appt_tree.configure(yscrollcommand=appt_scroll.set)

        self.appt_tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        appt_scroll.pack(side="right", fill="y", padx=(0, 10), pady=10)

        # Status Toggle Buttons
        actions_bar = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        actions_bar.pack(fill="x", pady=10)

        def set_status(status_str: str):
            sel = self.appt_tree.selection()
            if not sel:
                messagebox.showwarning("Select", "Please select an appointment from the table.")
                return
            a_id = int(self.appt_tree.item(sel[0])["values"][0])
            self.db.update_appointment_status(a_id, status_str)
            messagebox.showinfo("Status Updated", f"Appointment #{a_id} marked as '{status_str}'.")
            self.load_appointments_table()

        def go_to_prescription():
            sel = self.appt_tree.selection()
            if not sel:
                messagebox.showwarning("Select", "Please select an appointment first.")
                return
            self.switch_tab("prescriptions")

        ctk.CTkButton(actions_bar, text="✓ Mark Completed", fg_color="#10b981", hover_color="#059669", command=lambda: set_status("Completed")).pack(side="left", padx=5)
        ctk.CTkButton(actions_bar, text="⏳ Mark Scheduled", fg_color="#f59e0b", hover_color="#d97706", command=lambda: set_status("Scheduled")).pack(side="left", padx=5)
        ctk.CTkButton(actions_bar, text="✕ Cancel Appointment", fg_color="#ef4444", hover_color="#dc2626", command=lambda: set_status("Cancelled")).pack(side="left", padx=5)
        ctk.CTkButton(actions_bar, text="📝 Write Prescription", fg_color="#06b6d4", hover_color="#0284c7", command=go_to_prescription).pack(side="left", padx=5)

        self.load_appointments_table()

    def load_appointments_table(self):
        for item in self.appt_tree.get_children():
            self.appt_tree.delete(item)
        appts = self.db.get_all_appointments()
        for a in appts:
            self.appt_tree.insert("", "end", values=(
                a["appointment_id"],
                a["appointment_date"],
                a["time_slot"],
                a["patient_name"],
                a["patient_phone"],
                a["doctor_name"],
                a["doctor_dept"],
                a["status"],
                a["notes"] or ""
            ))

    def open_appointment_modal(self):
        """Modal for booking a new doctor appointment with conflict checking."""
        patients = self.db.get_all_patients()
        doctors = self.db.get_all_doctors()

        if not patients:
            messagebox.showwarning("Prerequisite Missing", "Please register at least one patient before booking an appointment.")
            return
        if not doctors:
            messagebox.showwarning("Prerequisite Missing", "Please register at least one doctor before booking an appointment.")
            return

        modal = ctk.CTkToplevel(self) if USE_CUSTOMTKINTER else tk.Toplevel(self)
        modal.title("Book Doctor Appointment")
        modal.geometry("520x600")
        modal.resizable(False, False)
        modal.grab_set()

        ctk.CTkLabel(modal, text="New Appointment Booking", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=15)

        form_frame = ctk.CTkFrame(modal, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=30, pady=5)

        # Patient Dropdown
        patient_map = {f"#{p['patient_id']} - {p['name']} ({p['phone']})": p['patient_id'] for p in patients}
        ctk.CTkLabel(form_frame, text="Select Patient *").pack(anchor="w")
        patient_cb = ctk.CTkComboBox(form_frame, values=list(patient_map.keys()), width=460)
        patient_cb.pack(pady=(2, 10))

        # Doctor Dropdown
        doctor_map = {f"#{d['doctor_id']} - {d['name']} ({d['specialization']} | {DEFAULT_CURRENCY}{d['fee']:.0f})": d['doctor_id'] for d in doctors}
        ctk.CTkLabel(form_frame, text="Select Doctor *").pack(anchor="w")
        doctor_cb = ctk.CTkComboBox(form_frame, values=list(doctor_map.keys()), width=460)
        doctor_cb.pack(pady=(2, 10))

        # Date & Quick Buttons
        ctk.CTkLabel(form_frame, text="Appointment Date (YYYY-MM-DD) *").pack(anchor="w")
        date_row = ctk.CTkFrame(form_frame, fg_color="transparent")
        date_row.pack(fill="x", pady=(2, 10))

        today_str = datetime.date.today().strftime("%Y-%m-%d")
        tomorrow_str = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

        date_entry = ctk.CTkEntry(date_row, width=220)
        date_entry.insert(0, today_str)
        date_entry.pack(side="left", padx=(0, 10))

        def set_date(d_str):
            date_entry.delete(0, 'end')
            date_entry.insert(0, d_str)

        ctk.CTkButton(date_row, text="Today", width=70, fg_color="#0d9488", command=lambda: set_date(today_str)).pack(side="left", padx=2)
        ctk.CTkButton(date_row, text="Tomorrow", width=80, fg_color="#64748b", command=lambda: set_date(tomorrow_str)).pack(side="left", padx=2)

        # Time Slot Dropdown
        time_slots = [
            "09:00 AM", "09:30 AM", "10:00 AM", "10:30 AM",
            "11:00 AM", "11:30 AM", "12:00 PM", "02:00 PM",
            "02:30 PM", "03:00 PM", "03:30 PM", "04:00 PM",
            "04:30 PM", "05:00 PM", "05:30 PM", "06:00 PM"
        ]
        ctk.CTkLabel(form_frame, text="Consultation Time Slot *").pack(anchor="w")
        slot_cb = ctk.CTkComboBox(form_frame, values=time_slots, width=460)
        slot_cb.pack(pady=(2, 10))

        ctk.CTkLabel(form_frame, text="Symptoms / Reason for Visit").pack(anchor="w")
        notes_entry = ctk.CTkEntry(form_frame, width=460, placeholder_text="e.g. Chest pain, high fever, followup...")
        notes_entry.pack(pady=(2, 15))

        def confirm_booking():
            pat_str = patient_cb.get().strip()
            doc_str = doctor_cb.get().strip()
            d_val = date_entry.get().strip()
            slot = slot_cb.get().strip()
            notes = notes_entry.get().strip()

            if pat_str not in patient_map or doc_str not in doctor_map:
                messagebox.showerror("Error", "Please select a valid Patient and Doctor from the dropdowns.")
                return

            # Validate date format
            try:
                datetime.datetime.strptime(d_val, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Validation Error", "Invalid date format. Please use YYYY-MM-DD format.")
                return

            p_id = patient_map[pat_str]
            d_id = doctor_map[doc_str]

            # Conflict Detection Guard
            has_conflict = self.db.check_appointment_conflict(d_id, d_val, slot)
            if has_conflict:
                messagebox.showerror(
                    "Scheduling Conflict",
                    f"Conflict Alert: Selected doctor already has an active appointment on {d_val} at {slot}.\nPlease select an alternative time slot."
                )
                return

            appt_id = self.db.add_appointment(p_id, d_id, d_val, slot, "Scheduled", notes)
            messagebox.showinfo("Booking Confirmed", f"Appointment #{appt_id} booked successfully for {d_val} at {slot}!")
            modal.destroy()
            self.load_appointments_table()

        confirm_btn = ctk.CTkButton(modal, text="Confirm Appointment Booking", fg_color="#0d9488", hover_color="#0f766e", width=260, command=confirm_booking)
        confirm_btn.pack(pady=(0, 20))

    # ----------------------------------------------------------------------------------
    # 5. DIGITAL PRESCRIPTION & MEDICAL RECORDS TAB
    # ----------------------------------------------------------------------------------
    def render_prescriptions_tab(self):
        is_dark = (self.current_theme == "dark")

        top_bar = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        top_bar.pack(fill="x", pady=(0, 10))

        title = ctk.CTkLabel(top_bar, text="Digital Prescription & Pharmacy Orders", font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(side="left")

        new_rx_btn = ctk.CTkButton(
            top_bar, text="+ Create Prescription",
            fg_color="#0d9488", hover_color="#0f766e",
            command=self.open_prescription_builder
        )
        new_rx_btn.pack(side="right")

        table_frame = ctk.CTkFrame(self.content_frame, corner_radius=8, fg_color="#1e293b" if is_dark else "#ffffff")
        table_frame.pack(fill="both", expand=True)

        cols = ("Rx ID", "Date", "Patient Name", "Consulting Doctor", "Specialization", "Clinical Diagnosis", "Advice Summary")
        self.rx_tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=14)

        self.rx_tree.heading("Rx ID", text="Prescription ID")
        self.rx_tree.heading("Date", text="Date")
        self.rx_tree.heading("Patient Name", text="Patient Name")
        self.rx_tree.heading("Consulting Doctor", text="Doctor")
        self.rx_tree.heading("Specialization", text="Department")
        self.rx_tree.heading("Clinical Diagnosis", text="Diagnosis")
        self.rx_tree.heading("Advice Summary", text="Doctor Advice")

        self.rx_tree.column("Rx ID", width=90, anchor="center")
        self.rx_tree.column("Date", width=90, anchor="center")
        self.rx_tree.column("Patient Name", width=140, anchor="w")
        self.rx_tree.column("Consulting Doctor", width=140, anchor="w")
        self.rx_tree.column("Specialization", width=120, anchor="w")
        self.rx_tree.column("Clinical Diagnosis", width=180, anchor="w")
        self.rx_tree.column("Advice Summary", width=180, anchor="w")

        rx_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.rx_tree.yview)
        self.rx_tree.configure(yscrollcommand=rx_scroll.set)

        self.rx_tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        rx_scroll.pack(side="right", fill="y", padx=(0, 10), pady=10)

        # Action Buttons
        actions_bar = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        actions_bar.pack(fill="x", pady=10)

        def print_pdf_rx():
            sel = self.rx_tree.selection()
            if not sel:
                messagebox.showwarning("Select", "Please select a prescription from the table to print.")
                return
            rx_id = int(str(self.rx_tree.item(sel[0])["values"][0]).replace("RX-", ""))
            rxs = self.db.get_prescriptions()
            rx_data = next((r for r in rxs if r["prescription_id"] == rx_id), None)
            if not rx_data:
                messagebox.showerror("Error", "Prescription record not found.")
                return

            try:
                path = PDFReportGenerator.generate_prescription_pdf(rx_data)
                PDFReportGenerator.open_pdf_safely(path)
                messagebox.showinfo("PDF Generated", f"Prescription PDF created successfully:\n{path}")
            except Exception as e:
                messagebox.showerror("PDF Error", f"Failed to generate prescription PDF: {str(e)}")

        ctk.CTkButton(actions_bar, text="🖨️ Export / Print Prescription (PDF)", fg_color="#06b6d4", hover_color="#0284c7", command=print_pdf_rx).pack(side="left", padx=5)

        self.load_prescriptions_table()

    def load_prescriptions_table(self):
        for item in self.rx_tree.get_children():
            self.rx_tree.delete(item)
        rxs = self.db.get_prescriptions()
        for r in rxs:
            self.rx_tree.insert("", "end", values=(
                f"RX-{r['prescription_id']:04d}",
                r["date"],
                r["patient_name"],
                r["doctor_name"],
                r["doctor_dept"],
                r["diagnosis"],
                r["advice"] or ""
            ))

    def open_prescription_builder(self):
        """Dynamic prescription builder with interactive multi-item medicine table."""
        appts = self.db.get_all_appointments()
        if not appts:
            messagebox.showwarning("No Appointments", "No appointments available to attach a prescription to.")
            return

        modal = ctk.CTkToplevel(self) if USE_CUSTOMTKINTER else tk.Toplevel(self)
        modal.title("Interactive Digital Prescription Builder")
        modal.geometry("760x720")
        modal.resizable(False, False)
        modal.grab_set()

        ctk.CTkLabel(modal, text="Prescription Formulation & Medical Rx", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=12)

        scroll_form = ctk.CTkScrollableFrame(modal, fg_color="transparent")
        scroll_form.pack(fill="both", expand=True, padx=25, pady=5)

        # Select Appointment
        appt_map = {f"Appt #{a['appointment_id']} - {a['patient_name']} with {a['doctor_name']} ({a['appointment_date']})": a for a in appts}
        ctk.CTkLabel(scroll_form, text="Attach to Appointment *", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        appt_cb = ctk.CTkComboBox(scroll_form, values=list(appt_map.keys()), width=700)
        appt_cb.pack(pady=(2, 10))

        # Diagnosis
        ctk.CTkLabel(scroll_form, text="Clinical Diagnosis & Findings *", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        diag_entry = ctk.CTkEntry(scroll_form, width=700, placeholder_text="e.g. Acute Bronchitis, Migraine, Type 2 Diabetes mellitus...")
        diag_entry.pack(pady=(2, 15))

        # Medicines Section Header
        med_header_frame = ctk.CTkFrame(scroll_form, fg_color="transparent")
        med_header_frame.pack(fill="x", pady=(5, 5))
        ctk.CTkLabel(med_header_frame, text="Rx Medications List", font=ctk.CTkFont(size=14, weight="bold"), text_color="#0d9488").pack(side="left")

        # Container for medicine rows
        med_container = ctk.CTkFrame(scroll_form, fg_color="#1e293b" if self.current_theme == "dark" else "#e2e8f0", corner_radius=8)
        med_container.pack(fill="x", pady=5, padx=2, ipady=6)

        # Header for columns
        col_hdr = ctk.CTkFrame(med_container, fg_color="transparent")
        col_hdr.pack(fill="x", padx=10, pady=(4, 2))
        ctk.CTkLabel(col_hdr, text="Medicine Name", width=220, anchor="w", font=ctk.CTkFont(size=11, weight="bold")).pack(side="left", padx=2)
        ctk.CTkLabel(col_hdr, text="Dosage (e.g. 500mg)", width=130, anchor="w", font=ctk.CTkFont(size=11, weight="bold")).pack(side="left", padx=2)
        ctk.CTkLabel(col_hdr, text="Frequency (e.g. 1-0-1)", width=140, anchor="w", font=ctk.CTkFont(size=11, weight="bold")).pack(side="left", padx=2)
        ctk.CTkLabel(col_hdr, text="Duration", width=100, anchor="w", font=ctk.CTkFont(size=11, weight="bold")).pack(side="left", padx=2)
        ctk.CTkLabel(col_hdr, text="Action", width=50, anchor="center", font=ctk.CTkFont(size=11, weight="bold")).pack(side="left", padx=2)

        medicine_row_entries = []

        def add_medicine_row(name_val="", dose_val="", freq_val="", dur_val=""):
            row_frame = ctk.CTkFrame(med_container, fg_color="transparent")
            row_frame.pack(fill="x", padx=10, pady=3)

            e_name = ctk.CTkEntry(row_frame, width=220, placeholder_text="e.g. Paracetamol")
            e_name.insert(0, name_val)
            e_name.pack(side="left", padx=2)

            e_dose = ctk.CTkEntry(row_frame, width=130, placeholder_text="e.g. 650 mg")
            e_dose.insert(0, dose_val)
            e_dose.pack(side="left", padx=2)

            e_freq = ctk.CTkEntry(row_frame, width=140, placeholder_text="e.g. 1-0-1 post meal")
            e_freq.insert(0, freq_val)
            e_freq.pack(side="left", padx=2)

            e_dur = ctk.CTkEntry(row_frame, width=100, placeholder_text="e.g. 5 Days")
            e_dur.insert(0, dur_val)
            e_dur.pack(side="left", padx=2)

            def remove_row():
                row_frame.destroy()
                medicine_row_entries.remove((e_name, e_dose, e_freq, e_dur))

            del_btn = ctk.CTkButton(row_frame, text="✕", width=40, height=28, fg_color="#ef4444", hover_color="#dc2626", command=remove_row)
            del_btn.pack(side="left", padx=2)

            medicine_row_entries.append((e_name, e_dose, e_freq, e_dur))

        # Add initial rows
        add_medicine_row("Amoxicillin", "500 mg", "1-0-1 (After Food)", "5 Days")
        add_medicine_row("Paracetamol", "650 mg", "SOS / as needed", "3 Days")

        add_row_btn = ctk.CTkButton(med_header_frame, text="+ Add Medicine Row", width=140, height=26, fg_color="#0d9488", command=lambda: add_medicine_row())
        add_row_btn.pack(side="right")

        # Advice Section
        ctk.CTkLabel(scroll_form, text="Doctor's Advice & Lifestyle Instructions", font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(15, 2))
        advice_textbox = ctk.CTkTextbox(scroll_form, width=700, height=80)
        advice_textbox.pack(pady=(2, 15))
        advice_textbox.insert("1.0", "Drink warm fluids, complete the full antibiotic course, and avoid cold beverages.")

        def save_and_export():
            sel_appt_str = appt_cb.get().strip()
            diag = diag_entry.get().strip()
            advice = advice_textbox.get("1.0", "end").strip()

            if sel_appt_str not in appt_map:
                messagebox.showerror("Validation Error", "Please select a valid appointment.")
                return
            if not diag:
                messagebox.showerror("Validation Error", "Clinical Diagnosis is required.")
                return

            appt = appt_map[sel_appt_str]
            med_list = []
            for e_name, e_dose, e_freq, e_dur in medicine_row_entries:
                m_name = e_name.get().strip()
                if m_name:
                    med_list.append({
                        "name": m_name,
                        "dosage": e_dose.get().strip() or "Standard",
                        "frequency": e_freq.get().strip() or "Daily",
                        "duration": e_dur.get().strip() or "3-5 Days"
                    })

            if not med_list:
                messagebox.showwarning("Notice", "No medicines entered. At least one medicine is recommended.")

            rx_id = self.db.save_prescription(
                appointment_id=appt["appointment_id"],
                patient_id=appt["patient_id"],
                doctor_id=appt["doctor_id"],
                diagnosis=diag,
                medicines_json=json.dumps(med_list),
                advice=advice
            )

            # Generate PDF immediately
            full_rx = {
                "prescription_id": rx_id,
                "doctor_name": appt["doctor_name"],
                "doctor_dept": appt["doctor_dept"],
                "doctor_id": appt["doctor_id"],
                "patient_name": appt["patient_name"],
                "patient_id": appt["patient_id"],
                "patient_phone": appt["patient_phone"],
                "diagnosis": diag,
                "medicines_json": json.dumps(med_list),
                "advice": advice,
                "date": datetime.date.today().strftime("%Y-%m-%d")
            }

            try:
                pdf_path = PDFReportGenerator.generate_prescription_pdf(full_rx)
                PDFReportGenerator.open_pdf_safely(pdf_path)
            except Exception as e:
                print(f"PDF auto-generation warning: {e}")

            messagebox.showinfo("Prescription Saved", f"Prescription #RX-{rx_id:04d} saved successfully & PDF generated!")
            modal.destroy()
            self.load_prescriptions_table()

        btn_row = ctk.CTkFrame(modal, fg_color="transparent")
        btn_row.pack(fill="x", padx=30, pady=(5, 15))
        ctk.CTkButton(btn_row, text="💾 Save & Generate Prescription PDF", fg_color="#0d9488", hover_color="#0f766e", width=280, command=save_and_export).pack(side="right")

    # ----------------------------------------------------------------------------------
    # 6. BILLING, INVOICING & PDF EXPORT TAB
    # ----------------------------------------------------------------------------------
    def render_billing_tab(self):
        is_dark = (self.current_theme == "dark")

        top_bar = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        top_bar.pack(fill="x", pady=(0, 10))

        title = ctk.CTkLabel(top_bar, text="Hospital Invoicing & Revenue Management", font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(side="left")

        new_bill_btn = ctk.CTkButton(
            top_bar, text="+ Generate New Bill / Invoice",
            fg_color="#0d9488", hover_color="#0f766e",
            command=self.open_billing_modal
        )
        new_bill_btn.pack(side="right")

        table_frame = ctk.CTkFrame(self.content_frame, corner_radius=8, fg_color="#1e293b" if is_dark else "#ffffff")
        table_frame.pack(fill="both", expand=True)

        cols = ("Invoice #", "Date", "Patient Name", "Consultant Doctor", "Consultation", "Medicines", "Other Charges", "Discount", "Total Amount", "Status", "Payment Mode")
        self.bill_tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=14)

        self.bill_tree.heading("Invoice #", text="Invoice #")
        self.bill_tree.heading("Date", text="Date")
        self.bill_tree.heading("Patient Name", text="Patient")
        self.bill_tree.heading("Consultant Doctor", text="Doctor")
        self.bill_tree.heading("Consultation", text=f"Doctor Fee ({DEFAULT_CURRENCY})")
        self.bill_tree.heading("Medicines", text=f"Medicines ({DEFAULT_CURRENCY})")
        self.bill_tree.heading("Other Charges", text=f"Other ({DEFAULT_CURRENCY})")
        self.bill_tree.heading("Discount", text=f"Discount ({DEFAULT_CURRENCY})")
        self.bill_tree.heading("Total Amount", text=f"Net Total ({DEFAULT_CURRENCY})")
        self.bill_tree.heading("Status", text="Status")
        self.bill_tree.heading("Payment Mode", text="Mode")

        self.bill_tree.column("Invoice #", width=85, anchor="center")
        self.bill_tree.column("Date", width=85, anchor="center")
        self.bill_tree.column("Patient Name", width=140, anchor="w")
        self.bill_tree.column("Consultant Doctor", width=130, anchor="w")
        self.bill_tree.column("Consultation", width=85, anchor="e")
        self.bill_tree.column("Medicines", width=85, anchor="e")
        self.bill_tree.column("Other Charges", width=85, anchor="e")
        self.bill_tree.column("Discount", width=80, anchor="e")
        self.bill_tree.column("Total Amount", width=100, anchor="e")
        self.bill_tree.column("Status", width=75, anchor="center")
        self.bill_tree.column("Payment Mode", width=80, anchor="center")

        bill_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.bill_tree.yview)
        self.bill_tree.configure(yscrollcommand=bill_scroll.set)

        self.bill_tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        bill_scroll.pack(side="right", fill="y", padx=(0, 10), pady=10)

        # Action Buttons
        actions_bar = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        actions_bar.pack(fill="x", pady=10)

        def print_pdf_invoice():
            sel = self.bill_tree.selection()
            if not sel:
                messagebox.showwarning("Select", "Please select a bill from the table to print.")
                return
            bill_id = int(str(self.bill_tree.item(sel[0])["values"][0]).replace("INV-", ""))
            bills = self.db.get_billings()
            b_data = next((b for b in bills if b["bill_id"] == bill_id), None)
            if not b_data:
                messagebox.showerror("Error", "Billing record not found.")
                return

            try:
                path = PDFReportGenerator.generate_invoice_pdf(b_data)
                PDFReportGenerator.open_pdf_safely(path)
                messagebox.showinfo("PDF Invoice Generated", f"Hospital Invoice PDF generated successfully:\n{path}")
            except Exception as e:
                messagebox.showerror("PDF Error", f"Failed to generate invoice PDF: {str(e)}")

        ctk.CTkButton(actions_bar, text="🖨️ Generate PDF Invoice", fg_color="#0d9488", hover_color="#0f766e", command=print_pdf_invoice).pack(side="left", padx=5)

        self.load_billing_table()

    def load_billing_table(self):
        for item in self.bill_tree.get_children():
            self.bill_tree.delete(item)
        bills = self.db.get_billings()
        for b in bills:
            self.bill_tree.insert("", "end", values=(
                f"INV-{b['bill_id']:04d}",
                b["date"],
                b["patient_name"],
                b["doctor_name"],
                f"{b['consultation_fee']:.2f}",
                f"{b['medicine_fee']:.2f}",
                f"{b['other_charges']:.2f}",
                f"{b['discount']:.2f}",
                f"{b['total_amount']:.2f}",
                b["payment_status"],
                b["payment_mode"]
            ))

    def open_billing_modal(self):
        """Interactive billing modal with automatic computation and instant PDF export."""
        appts = self.db.get_all_appointments()
        if not appts:
            messagebox.showwarning("Notice", "No appointments available for billing.")
            return

        modal = ctk.CTkToplevel(self) if USE_CUSTOMTKINTER else tk.Toplevel(self)
        modal.title("Hospital Billing & Invoice Generator")
        modal.geometry("560x650")
        modal.resizable(False, False)
        modal.grab_set()

        ctk.CTkLabel(modal, text="Patient Billing & Invoice Formulation", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=15)

        form_frame = ctk.CTkFrame(modal, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=30, pady=5)

        appt_map = {f"Appt #{a['appointment_id']} - {a['patient_name']} (Dr. {a['doctor_name']} - Fee: {DEFAULT_CURRENCY}{a['doctor_fee']:.0f})": a for a in appts}
        ctk.CTkLabel(form_frame, text="Select Appointment *").pack(anchor="w")
        appt_cb = ctk.CTkComboBox(form_frame, values=list(appt_map.keys()), width=480)
        appt_cb.pack(pady=(2, 10))

        # Fee Entries
        fee_row = ctk.CTkFrame(form_frame, fg_color="transparent")
        fee_row.pack(fill="x", pady=5)

        ctk.CTkLabel(fee_row, text=f"Doctor Fee ({DEFAULT_CURRENCY})").grid(row=0, column=0, sticky="w")
        doc_fee_entry = ctk.CTkEntry(fee_row, width=225)
        doc_fee_entry.grid(row=1, column=0, sticky="w", padx=(0, 20), pady=(2, 8))

        ctk.CTkLabel(fee_row, text=f"Medicine Charges ({DEFAULT_CURRENCY})").grid(row=0, column=1, sticky="w")
        med_fee_entry = ctk.CTkEntry(fee_row, width=225)
        med_fee_entry.insert(0, "0.00")
        med_fee_entry.grid(row=1, column=1, sticky="w", pady=(2, 8))

        charges_row = ctk.CTkFrame(form_frame, fg_color="transparent")
        charges_row.pack(fill="x", pady=5)

        ctk.CTkLabel(charges_row, text=f"Lab / Clinical Charges ({DEFAULT_CURRENCY})").grid(row=0, column=0, sticky="w")
        other_fee_entry = ctk.CTkEntry(charges_row, width=225)
        other_fee_entry.insert(0, "0.00")
        other_fee_entry.grid(row=1, column=0, sticky="w", padx=(0, 20), pady=(2, 8))

        ctk.CTkLabel(charges_row, text=f"Discount Concession ({DEFAULT_CURRENCY})").grid(row=0, column=1, sticky="w")
        disc_entry = ctk.CTkEntry(charges_row, width=225)
        disc_entry.insert(0, "0.00")
        disc_entry.grid(row=1, column=1, sticky="w", pady=(2, 8))

        # Real-time computation display
        calc_card = ctk.CTkFrame(form_frame, fg_color="#0d9488", corner_radius=8)
        calc_card.pack(fill="x", pady=12, ipady=6)

        total_display_lbl = ctk.CTkLabel(calc_card, text=f"NET TOTAL PAYABLE: {DEFAULT_CURRENCY} 0.00", font=ctk.CTkFont(size=16, weight="bold"), text_color="#ffffff")
        total_display_lbl.pack()

        def recompute_total(*args):
            try:
                c_fee = float(doc_fee_entry.get().strip() or "0")
                m_fee = float(med_fee_entry.get().strip() or "0")
                o_fee = float(other_fee_entry.get().strip() or "0")
                d_fee = float(disc_entry.get().strip() or "0")
                net = max(0.0, (c_fee + m_fee + o_fee) - d_fee)
                total_display_lbl.configure(text=f"NET TOTAL PAYABLE: {DEFAULT_CURRENCY} {net:,.2f}")
                return net
            except ValueError:
                total_display_lbl.configure(text="NET TOTAL PAYABLE: Invalid Inputs")
                return 0.0

        # Bind events
        doc_fee_entry.bind("<KeyRelease>", recompute_total)
        med_fee_entry.bind("<KeyRelease>", recompute_total)
        other_fee_entry.bind("<KeyRelease>", recompute_total)
        disc_entry.bind("<KeyRelease>", recompute_total)

        def on_appt_selected(choice):
            if choice in appt_map:
                a = appt_map[choice]
                doc_fee_entry.delete(0, 'end')
                doc_fee_entry.insert(0, f"{a['doctor_fee']:.2f}")
                recompute_total()

        appt_cb.configure(command=on_appt_selected)
        # Pre-select first
        if list(appt_map.keys()):
            on_appt_selected(list(appt_map.keys())[0])

        # Payment Status & Mode
        pay_row = ctk.CTkFrame(form_frame, fg_color="transparent")
        pay_row.pack(fill="x", pady=5)

        ctk.CTkLabel(pay_row, text="Payment Status").grid(row=0, column=0, sticky="w")
        status_cb = ctk.CTkComboBox(pay_row, values=["Paid", "Unpaid"], width=225)
        status_cb.set("Paid")
        status_cb.grid(row=1, column=0, sticky="w", padx=(0, 20), pady=(2, 8))

        ctk.CTkLabel(pay_row, text="Payment Mode").grid(row=0, column=1, sticky="w")
        mode_cb = ctk.CTkComboBox(pay_row, values=["Cash", "Card", "UPI", "Online Banking"], width=225)
        mode_cb.set("UPI")
        mode_cb.grid(row=1, column=1, sticky="w", pady=(2, 8))

        def save_and_print_invoice():
            sel_appt_str = appt_cb.get().strip()
            if sel_appt_str not in appt_map:
                messagebox.showerror("Error", "Please select an appointment.")
                return

            try:
                c_fee = float(doc_fee_entry.get().strip() or "0")
                m_fee = float(med_fee_entry.get().strip() or "0")
                o_fee = float(other_fee_entry.get().strip() or "0")
                d_fee = float(disc_entry.get().strip() or "0")
                if c_fee < 0 or m_fee < 0 or o_fee < 0 or d_fee < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Validation Error", "All fees must be valid non-negative numbers.")
                return

            total_net = max(0.0, (c_fee + m_fee + o_fee) - d_fee)
            status = status_cb.get().strip()
            mode = mode_cb.get().strip()
            appt = appt_map[sel_appt_str]

            bill_id = self.db.create_or_update_bill(
                appointment_id=appt["appointment_id"],
                patient_id=appt["patient_id"],
                consultation_fee=c_fee,
                medicine_fee=m_fee,
                other_charges=o_fee,
                discount=d_fee,
                total_amount=total_net,
                payment_status=status,
                payment_mode=mode
            )

            # Generate Invoice PDF
            bill_obj = {
                "bill_id": bill_id,
                "appointment_id": appt["appointment_id"],
                "patient_id": appt["patient_id"],
                "patient_name": appt["patient_name"],
                "patient_phone": appt["patient_phone"],
                "doctor_name": appt["doctor_name"],
                "doctor_dept": appt["doctor_dept"],
                "consultation_fee": c_fee,
                "medicine_fee": m_fee,
                "other_charges": o_fee,
                "discount": d_fee,
                "total_amount": total_net,
                "payment_status": status,
                "payment_mode": mode,
                "date": datetime.date.today().strftime("%Y-%m-%d")
            }

            try:
                pdf_path = PDFReportGenerator.generate_invoice_pdf(bill_obj)
                PDFReportGenerator.open_pdf_safely(pdf_path)
            except Exception as e:
                print(f"PDF auto-generation warning: {e}")

            messagebox.showinfo("Invoice Generated", f"Invoice #INV-{bill_id:04d} saved & PDF generated successfully!")
            modal.destroy()
            self.load_billing_table()

        btn_save = ctk.CTkButton(modal, text="💾 Save & Export PDF Invoice", fg_color="#0d9488", hover_color="#0f766e", width=260, command=save_and_print_invoice)
        btn_save.pack(pady=(0, 20))


# --------------------------------------------------------------------------------------
# 7. APPLICATION ENTRY POINT
# --------------------------------------------------------------------------------------
def main():
    """System entry point."""
    print("=" * 70)
    print("STARTING SMART HOSPITAL & DOCTOR APPOINTMENT MANAGEMENT SYSTEM")
    print("=" * 70)
    print(f"Python Runtime: {sys.version.split()[0]}")
    print(f"CustomTkinter Installed: {USE_CUSTOMTKINTER}")
    print(f"ReportLab Installed: {REPORTLAB_AVAILABLE}")
    print("Database: hospital.db (SQLite)")
    print("=" * 70)

    app = HospitalApp()
    app.mainloop()


if __name__ == "__main__":
    main()

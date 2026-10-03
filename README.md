# 🏥 MediCare AI — Smart Hospital Management & Clinical OS

A production-grade AI Healthcare & Hospital Management Operating System designed with award-winning Behance aesthetics and clinical-grade reliability. Built using **Python, Flask, SQLite3, and ReportLab**.

---

### 🌟 Key Modules & Capabilities

- **Clinical Operations Command Center**: Real-time KPI analytics tracking total patient admissions, on-duty specialists, outpatient queue flow, and reconciled revenue.
- **Visual Healthcare Analytics**: Responsive weekly patient inflow charts with daily distribution and real-time department utilization tracking.
- **Live Bed Capacity & Census Tracker**: Instant monitoring of hospital bed occupancy, active clinical admissions, and free bed availability.
- **Master Patient Registry (EHR)**: Centralized Electronic Health Records management with comprehensive medical visit histories, emergency contacts, and blood group categorization.
- **Specialist Faculty Directory & Rosters**: Physician profiling, departmental categorization, consultation fee schedules, and weekly OPD availability.
- **Smart Outpatient Scheduling**: Conflict-free appointment booking engine with real-time doctor availability checks and token generation.
- **Digital E-Prescriptions**: Structured prescription writer featuring drug dosage, timing, duration, and instant one-click **ReportLab PDF exports**.
- **Hospital Invoicing & Cashier Ledger**: Itemized medical billing, pharmacy dispensary fee calculation, discount concessions, payment reconciliations (UPI, Cash, Card, Insurance), and official GST tax invoice generation.
- **Secure Clinical Authentication**: Protected staff login portal with SHA-256 password hashing, 30-day persistent sessions, and role-based access for Chief Physicians, Attending Specialists, and Receptionists.
- **Clinical Zero-Error Architecture**: Built for real-world medical deployment with sanitized inputs, error-proof database queries, and clean zero-record initialization.

---

### 🚀 Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Launch the System**:
   ```bash
   python server.py
   ```
   Open **http://127.0.0.1:5000** in your browser.

3. **Default Staff Credentials**:
   - **Administrator**: `admin` / `admin123`
   - **Specialist**: `doctor` / `doctor123`
   - **Receptionist**: `staff` / `staff123`

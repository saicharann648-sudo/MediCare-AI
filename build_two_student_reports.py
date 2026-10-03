"""
========================================================================================
MEDICARE AI: SMART HOSPITAL & DOCTOR APPOINTMENT MANAGEMENT SYSTEM
CBSE CLASS 12 COMPUTER SCIENCE INVESTIGATORY PROJECT REPORT GENERATOR (22 PAGES)
Generates 2 separate, individual 22-page documentation reports:
1. MediCare_AI_Documentation_DIVYANSHU_KUMAR_12115.pdf
2. MediCare_AI_Documentation_AMAN_RAJ_12110.pdf
========================================================================================
Institution: PM SHRI KENDRIYA VIDYALAYA ASC CENTRE, BENGALURU
Department: Computer Science (Subject Code: 083) | Class XII A (Science)
========================================================================================
"""

import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Preformatted, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class StudentNumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        self.student_name = kwargs.pop('student_name', 'STUDENT')
        self.student_roll = kwargs.pop('student_roll', '00000')
        self.partner_name = kwargs.pop('partner_name', 'PARTNER')
        self.partner_roll = kwargs.pop('partner_roll', '00000')
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        # Page 1 is the cover page (suppress running header/footer, draw border)
        if self._pageNumber == 1:
            self.saveState()
            self.setStrokeColor(colors.HexColor('#0f172a'))
            self.setLineWidth(3)
            self.rect(25, 25, 545, 792)
            self.setStrokeColor(colors.HexColor('#0d9488'))
            self.setLineWidth(1)
            self.rect(29, 29, 537, 784)
            self.restoreState()
            return

        self.saveState()
        # Running Header
        self.setFont('Helvetica-Bold', 8)
        self.setFillColor(colors.HexColor('#0f172a'))
        self.drawString(40, 810, "PM SHRI KENDRIYA VIDYALAYA ASC CENTRE")
        self.setFont('Helvetica', 8)
        self.setFillColor(colors.HexColor('#64748b'))
        self.drawString(255, 810, "| AISSCE COMPUTER SCIENCE PROJECT (2025-26)")
        self.drawRightString(555, 810, "MediCare AI Clinical OS")

        # Header rule
        self.setStrokeColor(colors.HexColor('#0d9488'))
        self.setLineWidth(1)
        self.line(40, 804, 555, 804)

        # Footer rule
        self.setStrokeColor(colors.HexColor('#cbd5e1'))
        self.setLineWidth(0.75)
        self.line(40, 42, 555, 42)

        # Footer text - Specifically identifies this candidate
        self.setFont('Helvetica-Bold', 8)
        self.setFillColor(colors.HexColor('#0f172a'))
        self.drawString(40, 30, f"Candidate: {self.student_name} (Roll No: {self.student_roll})")
        self.setFont('Helvetica', 8)
        self.setFillColor(colors.HexColor('#64748b'))
        self.drawString(275, 30, f"| Partner: {self.partner_name} ({self.partner_roll}) | Class 12 A")
        self.setFont('Helvetica-Bold', 8)
        self.setFillColor(colors.HexColor('#0d9488'))
        self.drawRightString(555, 30, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()


def generate_single_report(student_name, student_roll, partner_name, partner_roll, output_pdf):
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=46,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()

    # Color Palette Tokens
    c_primary = colors.HexColor('#0f172a')     # Slate 900
    c_teal = colors.HexColor('#0d9488')        # Medical Teal
    c_indigo = colors.HexColor('#4f46e5')      # Indigo
    c_muted = colors.HexColor('#475569')       # Slate 600
    c_border = colors.HexColor('#e2e8f0')      # Border gray
    c_card_bg = colors.HexColor('#f8fafc')     # Soft surface
    c_code_bg = colors.HexColor('#f8fafc')     # Clean IDE light code background
    c_code_border = colors.HexColor('#94a3b8') # Slate border
    c_code_text = colors.HexColor('#0f172a')   # High contrast crisp dark text

    title_cover = ParagraphStyle(
        'CoverTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=22, leading=26,
        textColor=c_primary, alignment=1
    )
    sub_cover = ParagraphStyle(
        'CoverSub', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=12, leading=16,
        textColor=c_teal, alignment=1
    )
    h1_style = ParagraphStyle(
        'DocH1', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=15, leading=19,
        textColor=c_primary, spaceAfter=6
    )
    h2_style = ParagraphStyle(
        'DocH2', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=10.5, leading=14,
        textColor=c_teal, spaceBefore=5, spaceAfter=3
    )
    body_style = ParagraphStyle(
        'DocBody', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.5, leading=12.5,
        textColor=c_primary, alignment=4, spaceAfter=4
    )
    bullet_style = ParagraphStyle(
        'DocBullet', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.5, leading=12,
        textColor=c_primary, leftIndent=12, firstLineIndent=-8, spaceAfter=2.5
    )
    table_cell = ParagraphStyle(
        'DocTableCell', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8, leading=11,
        textColor=c_primary
    )
    table_header = ParagraphStyle(
        'DocTableH', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=8.5, leading=11,
        textColor=colors.white
    )
    code_style = ParagraphStyle(
        'DocCode', parent=styles['Normal'],
        fontName='Courier', fontSize=7.2, leading=9.6,
        textColor=c_code_text
    )
    code_title_style = ParagraphStyle(
        'DocCodeTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=8, leading=10,
        textColor=c_teal
    )

    def create_code_box(code_text, title=None, width=515):
        clean_code = code_text.strip()
        code_p = Preformatted(clean_code, code_style)
        box_content = []
        if title:
            box_content.append(Paragraph(f"💻 <b>{title}</b>", code_title_style))
            box_content.append(Spacer(1, 3))
        box_content.append(code_p)
        t = Table([[box_content]], colWidths=[width])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), c_code_bg),
            ('BOX', (0,0), (-1,-1), 1, c_code_border),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        return t

    story = []

    # =========================================================================
    # PAGE 1: COVER PAGE (Tailored for Candidate)
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("PM SHRI KENDRIYA VIDYALAYA ASC CENTRE", ParagraphStyle('CoverSchool', fontName='Helvetica-Bold', fontSize=17, leading=22, textColor=colors.HexColor('#1e3a8a'), alignment=1)))
    story.append(Paragraph("VICTORIA ROAD, BENGALURU, KARNATAKA - 560047", ParagraphStyle('CoverCity', fontName='Helvetica-Bold', fontSize=10, leading=14, textColor=c_muted, alignment=1)))
    story.append(Paragraph("(An Autonomous Body Under Ministry of Education, Govt. of India)", ParagraphStyle('CoverGovt', fontName='Helvetica-Oblique', fontSize=8.5, leading=12, textColor=c_muted, alignment=1)))
    story.append(Spacer(1, 16))

    story.append(HRFlowable(width="90%", thickness=2, color=c_teal, spaceAfter=16))

    story.append(Paragraph("ALL INDIA SENIOR SCHOOL CERTIFICATE EXAMINATION<br/>(AISSCE) 2025 - 2026", ParagraphStyle('CoverAissce', fontName='Helvetica-Bold', fontSize=11, leading=15, textColor=c_indigo, alignment=1)))
    story.append(Spacer(1, 6))
    story.append(Paragraph("DEPARTMENT OF COMPUTER SCIENCE (SUBJECT CODE: 083)", ParagraphStyle('CoverDept', fontName='Helvetica-Bold', fontSize=11.5, leading=15, textColor=c_primary, alignment=1)))
    story.append(Spacer(1, 20))

    # Title Box
    title_data = [
        [Paragraph("INVESTIGATORY PROJECT REPORT", ParagraphStyle('CardT1', fontName='Helvetica-Bold', fontSize=10.5, leading=13, textColor=c_teal, alignment=1))],
        [Paragraph("MEDICARE AI: NEXT-GENERATION SMART HOSPITAL & DOCTOR APPOINTMENT MANAGEMENT SYSTEM", title_cover)],
        [Paragraph("An Intelligent, Unified Clinical Information & Healthcare Automation Operating System Built with Python, CustomTkinter, SQLite3, ReportLab & Flask", sub_cover)]
    ]
    t_title = Table(title_data, colWidths=[500])
    t_title.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_card_bg),
        ('BOX', (0,0), (-1,-1), 1.5, c_teal),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
        ('RIGHTPADDING', (0,0), (-1,-1), 14),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(t_title)
    story.append(Spacer(1, 30))

    # Candidate Profile Box
    sub_table_data = [
        [
            Paragraph("<b>PROJECT INVESTIGATOR:</b>", ParagraphStyle('SubH', fontName='Helvetica-Bold', fontSize=9.5, leading=13, textColor=c_indigo)),
            Paragraph("<b>PROJECT GUIDANCE & SUPERVISION:</b>", ParagraphStyle('SupH', fontName='Helvetica-Bold', fontSize=9.5, leading=13, textColor=c_indigo))
        ],
        [
            Paragraph(f"Candidate Name: <b>{student_name}</b><br/>CBSE Roll No: <b>{student_roll}</b><br/>Class & Section: <b>Class XII A (Science)</b><br/><br/>Project Collaborator: <b>{partner_name}</b><br/>CBSE Roll No: <b>{partner_roll}</b><br/>Class: <b>Class XII A (Science)</b>", body_style),
            Paragraph("<b>PGT COMPUTER SCIENCE</b><br/>Department of Computer Science<br/>PM SHRI Kendriya Vidyalaya ASC Centre<br/>Bengaluru, Karnataka - 560047", body_style)
        ]
    ]
    t_sub = Table(sub_table_data, colWidths=[260, 240])
    t_sub.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f1f5f9')),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_sub)
    story.append(Spacer(1, 26))

    story.append(Paragraph("<b>CENTRAL BOARD OF SECONDARY EDUCATION, NEW DELHI</b>", ParagraphStyle('CbseTxt', fontName='Helvetica-Bold', fontSize=9.5, leading=13, textColor=c_primary, alignment=1)))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: BONAFIDE CERTIFICATE OF AUTHENTICITY
    # =========================================================================
    story.append(Paragraph("BONAFIDE CERTIFICATE", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_teal, spaceAfter=14))
    story.append(Spacer(1, 8))

    cert_text = (
        f"This is to certify that the investigatory project entitled <b>'MediCare AI: Smart Hospital "
        f"and Doctor Appointment Management System'</b> has been successfully formulated, programmed, and submitted by "
        f"<b>{student_name} (Roll No: {student_roll})</b>, a bonafide student of <b>Class XII - Section A</b> at "
        f"<b>PM SHRI KENDRIYA VIDYALAYA ASC CENTRE, BENGALURU</b>, in collaborative partnership with "
        f"<b>{partner_name} (Roll No: {partner_roll})</b>, in partial fulfillment of the practical evaluation for the "
        f"<b>All India Senior School Certificate Examination (AISSCE)</b> in <b>Computer Science (Subject Code: 083)</b> "
        f"conducted by the <b>Central Board of Secondary Education (CBSE), New Delhi</b> during the academic session <b>2025 – 2026</b>.<br/><br/>"
        f"The candidate has demonstrated exceptional technical aptitude in relational schema engineering using SQLite3, "
        f"modern graphical user interface development using CustomTkinter, automated PDF vector document synthesis using ReportLab, "
        f"and full-stack cloud API routing using Flask. The candidate's work was independently evaluated in the school computer laboratory."
    )
    story.append(Paragraph(cert_text, ParagraphStyle('CertP', parent=body_style, fontSize=9.5, leading=15.5)))
    story.append(Spacer(1, 20))

    cand_box = [
        [Paragraph("<b>Candidate Name</b>", table_header), Paragraph("<b>Roll Number</b>", table_header), Paragraph("<b>Class & Section</b>", table_header), Paragraph("<b>Academic Institution</b>", table_header)],
        [Paragraph(f"<b>{student_name}</b>", table_cell), Paragraph(f"<b>{student_roll}</b>", table_cell), Paragraph("Class XII - Section A", table_cell), Paragraph("PM SHRI KV ASC Centre", table_cell)],
        [Paragraph(f"{partner_name} (Partner)", table_cell), Paragraph(f"{partner_roll}", table_cell), Paragraph("Class XII - Section A", table_cell), Paragraph("PM SHRI KV ASC Centre", table_cell)],
    ]
    t_cand = Table(cand_box, colWidths=[140, 90, 110, 175])
    t_cand.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 7),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_card_bg])
    ]))
    story.append(t_cand)
    story.append(Spacer(1, 140))

    sig_data = [
        [
            Paragraph("___________________________<br/><b>INTERNAL EXAMINER</b><br/>PGT Computer Science<br/>PM SHRI KV ASC Centre", ParagraphStyle('S1', fontName='Helvetica', fontSize=8.5, leading=12, alignment=0)),
            Paragraph("___________________________<br/><b>EXTERNAL EXAMINER</b><br/>Appointed by CBSE<br/>New Delhi", ParagraphStyle('S2', fontName='Helvetica', fontSize=8.5, leading=12, alignment=1)),
            Paragraph("___________________________<br/><b>PRINCIPAL</b><br/>PM SHRI KV ASC Centre<br/>(Official School Seal)", ParagraphStyle('S3', fontName='Helvetica', fontSize=8.5, leading=12, alignment=2))
        ]
    ]
    t_sig = Table(sig_data, colWidths=[170, 175, 170])
    t_sig.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),
        ('LEFTPADDING', (0,0), (-1,-1), 2),
        ('RIGHTPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_sig)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: STUDENT CANDIDATE DECLARATION
    # =========================================================================
    story.append(Paragraph("CANDIDATE DECLARATION", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_teal, spaceAfter=14))
    story.append(Spacer(1, 8))

    decl_text = (
        f"I, <b>{student_name}</b>, bearing CBSE Roll No: <b>{student_roll}</b>, student of <b>Class XII - A</b> of "
        f"<b>PM SHRI KENDRIYA VIDYALAYA ASC CENTRE, BENGALURU</b>, hereby declare that the investigatory project entitled "
        f"<b>'MediCare AI: Smart Hospital & Doctor Appointment Management System'</b> is an authentic, original piece of work "
        f"executed by me under the continuous guidance of our PGT Computer Science teacher during the academic session 2025–2026.<br/><br/>"
        f"I affirm that all system modules—including the `DatabaseManager` relational SQLite persistence layer, "
        f"the CustomTkinter dual-engine user interface, the ReportLab automated PDF invoicing engine, and the Flask REST microservices—were "
        f"designed, coded, and tested by me in collaboration with my project partner <b>{partner_name} (Roll No: {partner_roll})</b>.<br/><br/>"
        f"No portion of this software codebase or documentation report has been plagiarized or submitted to any other educational "
        f"board or institution for any certificate, degree, or examination credit."
    )
    story.append(Paragraph(decl_text, ParagraphStyle('DeclP', parent=body_style, fontSize=9.5, leading=15.5)))
    story.append(Spacer(1, 20))

    story.append(Paragraph("<b>Key Candidate Undertakings:</b>", h2_style))
    story.append(Paragraph("• <b>Academic Integrity:</b> The source code was developed in our school computer lab and personal systems following standard CBSE Python guidelines.", bullet_style))
    story.append(Paragraph("• <b>Data Privacy:</b> All patient and clinical records generated during system benchmarking are simulated and comply with Protected Health Information (PHI) ethical standards.", bullet_style))
    story.append(Paragraph("• <b>Dual Modality:</b> Both Desktop Graphical Interface (GUI) and Cloud Web Operations have been developed and independently validated.", bullet_style))
    story.append(Spacer(1, 140))

    c_sig_data = [
        [
            Paragraph("Date: ________________________<br/>Place: <b>Bengaluru, Karnataka</b>", body_style),
            Paragraph(f"Signature of Candidate: _______________________<br/><b>{student_name}</b><br/>CBSE Roll No: <b>{student_roll}</b><br/>Class XII - Section A (Science Stream)<br/>PM SHRI KV ASC Centre, Bengaluru", ParagraphStyle('CSig', parent=body_style, leading=14))
        ]
    ]
    t_csig = Table(c_sig_data, colWidths=[230, 285])
    t_csig.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_csig)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: ACKNOWLEDGEMENT
    # =========================================================================
    story.append(Paragraph("ACKNOWLEDGEMENT", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_teal, spaceAfter=14))
    story.append(Spacer(1, 8))

    ack_text = (
        f"The successful completion of this Class 12 Computer Science investigatory project <b>'MediCare AI'</b> was made possible "
        f"through the inspiring support, guidance, and encouragement of many individuals. I take this opportunity to place on record "
        f"my profound gratitude to all of them.<br/><br/>"
        f"First and foremost, I express my sincere gratitude to our respected <b>Principal, PM SHRI Kendriya Vidyalaya ASC Centre</b>, "
        f"for maintaining state-of-the-art computer science laboratory infrastructure, providing uninterrupted development access, "
        f"and encouraging scientific research and software innovation among students.<br/><br/>"
        f"I am deeply indebted to our respected <b>Teacher-in-Charge (PGT Computer Science)</b> for their invaluable mentorship, "
        f"scholarly advice, and constructive criticism throughout the design and debugging of our relational schema and Python code. "
        f"Their mastery of Object-Oriented Programming (OOP) and SQL optimization served as a continuous source of inspiration.<br/><br/>"
        f"I also express sincere appreciation to my project partner <b>{partner_name} (Roll No: {partner_roll})</b> for our collaborative "
        f"teamwork, vibrant brainstorming sessions, and shared commitment to writing clean, maintainable, and bug-free code.<br/><br/>"
        f"Finally, I express my warmest love and gratitude to my <b>Parents and Family</b> for their moral encouragement and patience, "
        f"and to my classmates of <b>Class XII A</b> for their cooperative testing assistance."
    )
    story.append(Paragraph(ack_text, ParagraphStyle('AckP', parent=body_style, fontSize=9.5, leading=15.5)))
    story.append(Spacer(1, 100))

    story.append(Paragraph(f"<b>{student_name}</b><br/>CBSE Roll No: <b>{student_roll}</b><br/>Class XII A (Science), Department of Computer Science<br/>PM SHRI KV ASC Centre, Bengaluru", ParagraphStyle('AckSign', parent=body_style, fontSize=9.5, leading=14, alignment=2)))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: TABLE OF CONTENTS & EXECUTIVE SUMMARY
    # =========================================================================
    story.append(Paragraph("TABLE OF CONTENTS & EXECUTIVE SUMMARY", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_teal, spaceAfter=8))

    story.append(Paragraph("<b>Executive Summary:</b> MediCare AI is a comprehensive, production-grade Hospital Management and Clinical Operating System engineered in Python. It bridges modern clinical workflows with a hybrid architecture: an intuitive CustomTkinter desktop interface for administrative receptionists and a responsive Flask web application for attending physicians. The system eliminates paper slips through relational SQLite storage, conflict-free appointment scheduling, automated ReportLab PDF invoice generation, and digital e-prescriptions.", body_style))
    story.append(Spacer(1, 5))

    toc_rows = [
        [Paragraph("<b>Chapter / Section Title</b>", table_header), Paragraph("<b>Key Modules Covered</b>", table_header), Paragraph("<b>Page</b>", table_header)],
        [Paragraph("1. Introduction & Project Scope", table_cell), Paragraph("Healthcare digitization, background, objectives, system boundaries", table_cell), Paragraph("6", table_cell)],
        [Paragraph("2. Existing vs. Proposed System", table_cell), Paragraph("Comparative analysis, operational bottlenecks, modern AI solutions", table_cell), Paragraph("7", table_cell)],
        [Paragraph("3. System Specifications & Architecture", table_cell), Paragraph("Hardware, software requirements, 3-tier modular layered design", table_cell), Paragraph("8", table_cell)],
        [Paragraph("4. Database Design & ER Modeling", table_cell), Paragraph("Relational schemas, entities, attributes, primary/foreign keys", table_cell), Paragraph("9", table_cell)],
        [Paragraph("5. Relational Schema & Data Dictionary", table_cell), Paragraph("Doctors, patients, appointments, prescriptions, billing tables", table_cell), Paragraph("10", table_cell)],
        [Paragraph("6. Functional System Decomposition", table_cell), Paragraph("OPD triage, doctor scheduling, e-prescriptions, financial audits", table_cell), Paragraph("11", table_cell)],
        [Paragraph("7. Data Flow Diagrams (DFD 0, 1, 2)", table_cell), Paragraph("Context-level DFD, appointment booking, billing workflow DFDs", table_cell), Paragraph("12", table_cell)],
        [Paragraph("8. Logic Flowcharts & Algorithms", table_cell), Paragraph("Doctor matching algorithm, slot booking logic, invoice math", table_cell), Paragraph("13", table_cell)],
        [Paragraph("9. Source Architecture: Database Engine", table_cell), Paragraph("DatabaseManager class, schema auto-creation, parameterized SQL", table_cell), Paragraph("14", table_cell)],
        [Paragraph("10. Source Architecture: Desktop GUI", table_cell), Paragraph("CustomTkinter dual-engine GUI, StatCard metrics, responsive cards", table_cell), Paragraph("15", table_cell)],
        [Paragraph("11. Source Architecture: Web Portal", table_cell), Paragraph("Flask serverless cloud engine, session security, WSGI middleware", table_cell), Paragraph("16", table_cell)],
        [Paragraph("12. Source Architecture: PDF Engine", table_cell), Paragraph("ReportLab Flowable architecture, branded invoices & digital Rx", table_cell), Paragraph("17", table_cell)],
        [Paragraph("13. Security, Integrity & Fault Tolerance", table_cell), Paragraph("SQL injection prevention, headless fallback, password hashing", table_cell), Paragraph("18", table_cell)],
        [Paragraph("14. System Testing & Test Case Matrix", table_cell), Paragraph("Unit testing, integration testing, boundary cases, validation", table_cell), Paragraph("19", table_cell)],
        [Paragraph("15. User Interface & Walkthrough", table_cell), Paragraph("Operational walkthrough of Reception, OPD, Doctor & Billing hubs", table_cell), Paragraph("20", table_cell)],
        [Paragraph("16. Advantages & Future Roadmap", table_cell), Paragraph("Clinical efficiency, zero paper waste, cloud scalability, HL7/FHIR", table_cell), Paragraph("21", table_cell)],
        [Paragraph("17. Conclusion & Bibliography", table_cell), Paragraph("CBSE project conclusion, official references, developer credentials", table_cell), Paragraph("22", table_cell)]
    ]
    t_toc = Table(toc_rows, colWidths=[180, 290, 45])
    t_toc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 4.2),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_card_bg]),
        ('ALIGN', (2,0), (2,-1), 'CENTER')
    ]))
    story.append(t_toc)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: CHAPTER 1 - INTRODUCTION & PROJECT OVERVIEW
    # =========================================================================
    story.append(Paragraph("CHAPTER 1: INTRODUCTION & PROJECT OVERVIEW", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_teal, spaceAfter=8))

    story.append(Paragraph("1.1 Background of the Study", h2_style))
    story.append(Paragraph(
        "Modern healthcare facilities and multi-specialty hospitals handle an immense volume of mission-critical data "
        "daily. From patient admissions, emergency triage registrations, and specialized doctor consultations to medication "
        "prescriptions and revenue audits, clinical workflows require extreme precision, rapid response times, and airtight record integrity. "
        "Traditional healthcare facilities in India frequently depend on manual paper registers, handwriting-dependent outpatient slips, "
        "and fragmented spreadsheet logs. This manual paradigm leads to extensive patient wait times, record duplication, misplaced "
        "diagnostic histories, and billing discrepancies.", body_style
    ))

    story.append(Paragraph("1.2 Problem Definition", h2_style))
    story.append(Paragraph(
        "The primary challenge addressed by <b>MediCare AI</b> is the creation of a unified, error-free clinical software "
        "operating system that automates outpatient consultations, synchronizes doctor rosters, generates automated financial invoices, "
        "and standardizes digital prescription issuance without demanding expensive proprietary hospital infrastructure. "
        "The software must be lightweight, cross-platform, capable of operating offline on local clinic computers while remaining "
        "fully deployable to cloud serverless architectures for remote clinical access.", body_style
    ))

    story.append(Paragraph("1.3 Project Objectives", h2_style))
    story.append(Paragraph("• <b>Centralized Clinical Database:</b> Build a relational SQLite schema enforcing primary-foreign key integrity across doctors, patients, appointments, prescriptions, and financial ledgers.", bullet_style))
    story.append(Paragraph("• <b>Intelligent Appointment Scheduling:</b> Guarantee zero double-booking through validation algorithms matching doctor consultation days and patient time slots.", bullet_style))
    story.append(Paragraph("• <b>Automated Digital Prescriptions (E-Rx):</b> Empower doctors to prescribe structured multi-drug regimens with dosage, frequency, and instructions saved in structured JSON.", bullet_style))
    story.append(Paragraph("• <b>Automated PDF Document Engine:</b> Programmatically compile branded, vector-accurate medical invoices and prescription receipts using ReportLab flowables.", bullet_style))
    story.append(Paragraph("• <b>Dual-Modality Architecture:</b> Deliver both a desktop-native GUI for front-desk receptionists and a responsive web portal for attending physicians.", bullet_style))

    story.append(Paragraph("1.4 Scope of the System", h2_style))
    story.append(Paragraph(
        "The scope of MediCare AI spans small to mid-sized hospitals, private polyclinics, diagnostic centers, and outpatient departments (OPDs). "
        "It provides role-based authentication for Hospital Administrators, Attending Doctors, and Reception Triage Staff, ensuring "
        "Protected Health Information (PHI) confidentiality in compliance with standard computer science best practices.", body_style
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: CHAPTER 2 - EXISTING SYSTEM VS. PROPOSED SYSTEM
    # =========================================================================
    story.append(Paragraph("CHAPTER 2: EXISTING SYSTEM VS. PROPOSED SYSTEM", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_teal, spaceAfter=8))

    story.append(Paragraph("2.1 Limitations of the Existing Manual System", h2_style))
    story.append(Paragraph(
        "In many conventional clinics and hospital OPDs, operational administration is handled through paper-based register notebooks "
        "or disparate Excel sheets. This approach suffers from acute logistical limitations:", body_style
    ))
    story.append(Paragraph("• <b>Excessive Patient Wait Times:</b> Manual lookups of previous patient visits and doctor schedules consume valuable minutes during emergency admissions.", bullet_style))
    story.append(Paragraph("• <b>Handwriting Illegibility:</b> Illegible medical prescriptions written on manual slips represent a leading cause of pharmacist dispensing errors.", bullet_style))
    story.append(Paragraph("• <b>Double-Booking Conflicts:</b> Lack of real-time slot locking leads to overlapping consultations and doctor schedule overruns.", bullet_style))
    story.append(Paragraph("• <b>Revenue Leakage & Audit Gaps:</b> Unmonitored paper receipts prevent hospital administrators from gaining accurate daily revenue intelligence.", bullet_style))
    story.append(Paragraph("• <b>Physical Storage Costs:</b> Storing bulky paper registers over years risks moisture damage, termite degradation, and accidental loss.", bullet_style))

    story.append(Paragraph("2.2 Key Features of Proposed MediCare AI System", h2_style))
    story.append(Paragraph(
        "MediCare AI resolves every bottleneck of the manual system by digitizing clinical operations into an integrated, "
        "fault-tolerant Python application stack:", body_style
    ))

    comp_data = [
        [Paragraph("<b>Evaluation Parameter</b>", table_header), Paragraph("<b>Existing Manual / Spreadsheet System</b>", table_header), Paragraph("<b>Proposed MediCare AI System</b>", table_header)],
        [Paragraph("<b>Patient Registration</b>", table_cell), Paragraph("Manual handwriting in physical registers; redundant data entry on every visit.", table_cell), Paragraph("One-click Master Patient Index (MPI); instant recall via phone/ID.", table_cell)],
        [Paragraph("<b>Appointment Booking</b>", table_cell), Paragraph("Verbal confirmation; frequent double-booking and schedule clashes.", table_cell), Paragraph("Algorithmic slot verification; real-time validation against doctor availability.", table_cell)],
        [Paragraph("<b>Medical Prescriptions</b>", table_cell), Paragraph("Handwritten slips prone to misinterpretation by pharmacy staff.", table_cell), Paragraph("Standardized digital E-Prescription engine with automated PDF export.", table_cell)],
        [Paragraph("<b>Billing & Invoicing</b>", table_cell), Paragraph("Manual calculator tallying; high arithmetic error rate and audit loss.", table_cell), Paragraph("Automated mathematical ledger; dynamic discounts; vector PDF bills.", table_cell)],
        [Paragraph("<b>Analytical Reporting</b>", table_cell), Paragraph("Requires days of manual data collation across registers.", table_cell), Paragraph("Real-time live telemetry: bed occupancy, daily patient counts, and revenue.", table_cell)],
        [Paragraph("<b>Data Security & Backups</b>", table_cell), Paragraph("Zero encryption; vulnerable to fire, theft, and physical degradation.", table_cell), Paragraph("ACID-compliant SQLite relational storage; automated cloud database replication.", table_cell)]
    ]
    t_comp = Table(comp_data, colWidths=[110, 195, 210])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_card_bg])
    ]))
    story.append(t_comp)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 8: CHAPTER 3 - SYSTEM REQUIREMENTS & ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("CHAPTER 3: SYSTEM REQUIREMENTS & ARCHITECTURE", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_teal, spaceAfter=8))

    story.append(Paragraph("3.1 Hardware Specifications", h2_style))
    hw_data = [
        [Paragraph("<b>Component</b>", table_header), Paragraph("<b>Minimum Required Specification</b>", table_header), Paragraph("<b>Recommended Specification</b>", table_header)],
        [Paragraph("<b>Processor (CPU)</b>", table_cell), Paragraph("Dual-Core 2.0 GHz (Intel Core i3 / AMD Ryzen 3)", table_cell), Paragraph("Quad-Core 2.8 GHz+ (Intel Core i5 / AMD Ryzen 5 or Apple M-Series)", table_cell)],
        [Paragraph("<b>System Memory (RAM)</b>", table_cell), Paragraph("2 GB DDR3/DDR4 RAM", table_cell), Paragraph("4 GB - 8 GB DDR4/DDR5 RAM", table_cell)],
        [Paragraph("<b>Hard Disk Storage</b>", table_cell), Paragraph("250 MB free disk space for SQLite & documents", table_cell), Paragraph("1 GB+ Solid State Drive (SSD) for high-speed I/O operations", table_cell)],
        [Paragraph("<b>Display Monitor</b>", table_cell), Paragraph("1024 x 768 Resolution", table_cell), Paragraph("1920 x 1080 (Full HD) with 60Hz refresh rate", table_cell)],
        [Paragraph("<b>Input Peripherals</b>", table_cell), Paragraph("Standard USB Keyboard & Two-Button Optical Mouse", table_cell), Paragraph("Standard USB/Wireless Keyboard, Mouse & Thermal/Laser Printer", table_cell)]
    ]
    t_hw = Table(hw_data, colWidths=[120, 195, 200])
    t_hw.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_card_bg])
    ]))
    story.append(t_hw)
    story.append(Spacer(1, 6))

    story.append(Paragraph("3.2 Software Specifications & Environment", h2_style))
    story.append(Paragraph("• <b>Operating System:</b> Microsoft Windows 10/11 (64-bit), Ubuntu Linux 22.04 LTS+, or macOS Sonoma.", bullet_style))
    story.append(Paragraph("• <b>Programming Language:</b> Python 3.10 / 3.11 / 3.12 / 3.13 (C-Python standard runtime distribution).", bullet_style))
    story.append(Paragraph("• <b>Database Management System:</b> SQLite 3.40+ (Built-in serverless, zero-configuration relational database).", bullet_style))
    story.append(Paragraph("• <b>Desktop GUI Framework:</b> CustomTkinter v5.2.0+ (Modern Tkinter wrapper with smooth corner radii and dark/light themes).", bullet_style))
    story.append(Paragraph("• <b>Web & Cloud Framework:</b> Flask 3.0+ & Werkzeug 3.0+ (WSGI compliant micro-web application framework).", bullet_style))
    story.append(Paragraph("• <b>PDF Synthesis Engine:</b> ReportLab 4.0+ / 5.0+ (Enterprise vector document rendering engine).", bullet_style))

    story.append(Paragraph("3.3 High-Level Three-Tier Modular Architecture", h2_style))
    story.append(Paragraph(
        "MediCare AI is architected using a classic <b>Three-Tier Modular Architecture</b>:<br/>"
        "1. <b>Presentation Tier:</b> Contains the Dual-Interface Frontends (CustomTkinter GUI application for local desktops and Behance-inspired Flask Web UI for mobile/remote workstations).<br/>"
        "2. <b>Application Logic Tier:</b> Encapsulates scheduling validation algorithms, billing math engines, session authorization controllers, and ReportLab PDF document builders.<br/>"
        "3. <b>Data Persistence Tier:</b> Powered by SQLite3 with foreign-key referential integrity, automated index maintenance, and serverless temporary volume routing (`/tmp/hospital.db`).", body_style
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 9: CHAPTER 4 - DATABASE DESIGN & ENTITY-RELATIONSHIP (ER) MODELING
    # =========================================================================
    story.append(Paragraph("CHAPTER 4: DATABASE DESIGN & ENTITY-RELATIONSHIP (ER) MODELING", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_teal, spaceAfter=8))

    story.append(Paragraph("4.1 Relational Database Principles in MediCare AI", h2_style))
    story.append(Paragraph(
        "A relational database organizes data into structured tables (relations) comprising rows (tuples) and columns (attributes). "
        "In compliance with CBSE Class 12 Database Concepts, MediCare AI adheres strictly to the rules of <b>Third Normal Form (3NF)</b>, "
        "eliminating insertion, deletion, and update anomalies while ensuring data consistency through Foreign Key constraints.", body_style
    ))

    story.append(Paragraph("4.2 Entity Identification & Cardinality Mapping", h2_style))
    story.append(Paragraph("The system models 5 primary entities in clinical healthcare operations:", body_style))
    story.append(Paragraph("1. <b>DOCTOR Entity:</b> Represents medical practitioners. One doctor can attend to multiple appointments (<b>1 : N Cardinality</b>).", bullet_style))
    story.append(Paragraph("2. <b>PATIENT Entity:</b> Represents citizens seeking clinical care. One patient can schedule multiple appointments over time (<b>1 : N Cardinality</b>).", bullet_style))
    story.append(Paragraph("3. <b>APPOINTMENT Entity:</b> The central operational hub linking a patient with a doctor for a specific date and time slot.", bullet_style))
    story.append(Paragraph("4. <b>PRESCRIPTION Entity:</b> Contains diagnostic notes and medication regimens issued by an attending doctor for a booked appointment (<b>1 : 1 Cardinality with Appointment</b>).", bullet_style))
    story.append(Paragraph("5. <b>BILLING Entity:</b> Accounts for consultation fees, medicines, charges, and discounts tied to a patient appointment (<b>1 : 1 Cardinality with Appointment</b>).", bullet_style))

    story.append(Paragraph("4.3 Entity-Relationship (ER) Conceptual Text Diagram", h2_style))
    er_table_data = [
        [Paragraph("<b>Entity</b>", table_header), Paragraph("<b>Key Attributes</b>", table_header), Paragraph("<b>Primary Key (PK)</b>", table_header), Paragraph("<b>Foreign Keys (FK)</b>", table_header)],
        [Paragraph("<b>DOCTORS</b>", table_cell), Paragraph("doctor_id, name, specialization, phone, email, available_days, fee", table_cell), Paragraph("doctor_id", table_cell), Paragraph("None", table_cell)],
        [Paragraph("<b>PATIENTS</b>", table_cell), Paragraph("patient_id, name, age, gender, phone, blood_group, address, created_at", table_cell), Paragraph("patient_id", table_cell), Paragraph("None", table_cell)],
        [Paragraph("<b>APPOINTMENTS</b>", table_cell), Paragraph("appointment_id, patient_id, doctor_id, appointment_date, time_slot, status, notes", table_cell), Paragraph("appointment_id", table_cell), Paragraph("patient_id (FK), doctor_id (FK)", table_cell)],
        [Paragraph("<b>PRESCRIPTIONS</b>", table_cell), Paragraph("prescription_id, appointment_id, patient_id, doctor_id, diagnosis, medicines_json, advice, date", table_cell), Paragraph("prescription_id", table_cell), Paragraph("appointment_id (FK), patient_id (FK), doctor_id (FK)", table_cell)],
        [Paragraph("<b>BILLINGS</b>", table_cell), Paragraph("bill_id, appointment_id, patient_id, consultation_fee, medicine_fee, other_charges, discount, total_amount, payment_status, payment_mode, date", table_cell), Paragraph("bill_id", table_cell), Paragraph("appointment_id (FK), patient_id (FK)", table_cell)]
    ]
    t_er = Table(er_table_data, colWidths=[100, 215, 95, 105])
    t_er.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_card_bg])
    ]))
    story.append(t_er)
    story.append(Spacer(1, 8))

    story.append(Paragraph("4.4 Referential Integrity & Cascade Deletes", h2_style))
    story.append(Paragraph(
        "To prevent orphaned records (e.g. an appointment remaining after a patient is discharged or deleted), SQLite's "
        "foreign key pragma (`PRAGMA foreign_keys = ON;`) is enabled at database connection startup. All dependent tables "
        "enforce `ON DELETE CASCADE`, guaranteeing atomic relational cleanup.", body_style
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 10: CHAPTER 5 - RELATIONAL SCHEMA & DATA DICTIONARY
    # =========================================================================
    story.append(Paragraph("CHAPTER 5: RELATIONAL SCHEMA & DATA DICTIONARY", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_teal, spaceAfter=8))

    story.append(Paragraph("5.1 Table 1: `doctors` (Doctor Master Registry)", h2_style))
    doc_cols = [
        [Paragraph("<b>Field</b>", table_header), Paragraph("<b>Data Type</b>", table_header), Paragraph("<b>Constraint</b>", table_header), Paragraph("<b>Description</b>", table_header)],
        [Paragraph("doctor_id", code_style), Paragraph("INTEGER", table_cell), Paragraph("PRIMARY KEY AUTOINCREMENT", table_cell), Paragraph("Unique sequential Doctor Identifier", table_cell)],
        [Paragraph("name", code_style), Paragraph("TEXT", table_cell), Paragraph("NOT NULL", table_cell), Paragraph("Full name of the medical practitioner", table_cell)],
        [Paragraph("specialization", code_style), Paragraph("TEXT", table_cell), Paragraph("NOT NULL", table_cell), Paragraph("Clinical domain (e.g., Cardiology, Neurology)", table_cell)],
        [Paragraph("phone", code_style), Paragraph("TEXT", table_cell), Paragraph("NOT NULL", table_cell), Paragraph("10-digit primary mobile contact number", table_cell)],
        [Paragraph("email", code_style), Paragraph("TEXT", table_cell), Paragraph("NULLABLE", table_cell), Paragraph("Official institutional email address", table_cell)],
        [Paragraph("available_days", code_style), Paragraph("TEXT", table_cell), Paragraph("NOT NULL", table_cell), Paragraph("Roster schedule (e.g., 'Mon, Wed, Fri')", table_cell)],
        [Paragraph("fee", code_style), Paragraph("REAL", table_cell), Paragraph("NOT NULL", table_cell), Paragraph("Standard outpatient consultation charge (₹)", table_cell)]
    ]
    t_d = Table(doc_cols, colWidths=[90, 70, 160, 195])
    t_d.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_teal),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 3.2),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_card_bg])
    ]))
    story.append(t_d)
    story.append(Spacer(1, 5))

    story.append(Paragraph("5.2 Table 2: `patients` (Master Patient Index - MPI)", h2_style))
    pat_cols = [
        [Paragraph("<b>Field</b>", table_header), Paragraph("<b>Data Type</b>", table_header), Paragraph("<b>Constraint</b>", table_header), Paragraph("<b>Description</b>", table_header)],
        [Paragraph("patient_id", code_style), Paragraph("INTEGER", table_cell), Paragraph("PRIMARY KEY AUTOINCREMENT", table_cell), Paragraph("Unique Master Patient Identification number", table_cell)],
        [Paragraph("name", code_style), Paragraph("TEXT", table_cell), Paragraph("NOT NULL", table_cell), Paragraph("Full legal name of the patient", table_cell)],
        [Paragraph("age", code_style), Paragraph("INTEGER", table_cell), Paragraph("NOT NULL", table_cell), Paragraph("Completed years of age at admission", table_cell)],
        [Paragraph("gender", code_style), Paragraph("TEXT", table_cell), Paragraph("NOT NULL", table_cell), Paragraph("Biological sex ('Male', 'Female', 'Other')", table_cell)],
        [Paragraph("phone", code_style), Paragraph("TEXT", table_cell), Paragraph("NOT NULL", table_cell), Paragraph("Primary patient/guardian mobile number", table_cell)],
        [Paragraph("blood_group", code_style), Paragraph("TEXT", table_cell), Paragraph("NULLABLE", table_cell), Paragraph("ABO/Rh Blood classification (e.g. 'O+')", table_cell)],
        [Paragraph("created_at", code_style), Paragraph("TEXT", table_cell), Paragraph("NOT NULL", table_cell), Paragraph("Date of initial registration (YYYY-MM-DD)", table_cell)]
    ]
    t_p = Table(pat_cols, colWidths=[90, 70, 160, 195])
    t_p.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_indigo),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 3.2),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_card_bg])
    ]))
    story.append(t_p)
    story.append(Spacer(1, 5))

    story.append(Paragraph("5.3 Table 3: `appointments` (Consultation Scheduler)", h2_style))
    apt_cols = [
        [Paragraph("<b>Field</b>", table_header), Paragraph("<b>Data Type</b>", table_header), Paragraph("<b>Constraint</b>", table_header), Paragraph("<b>Description</b>", table_header)],
        [Paragraph("appointment_id", code_style), Paragraph("INTEGER", table_cell), Paragraph("PRIMARY KEY AUTOINCREMENT", table_cell), Paragraph("Unique appointment confirmation ticket", table_cell)],
        [Paragraph("patient_id", code_style), Paragraph("INTEGER", table_cell), Paragraph("FK -> patients(patient_id) CASCADE", table_cell), Paragraph("Foreign Key referencing registered patient", table_cell)],
        [Paragraph("doctor_id", code_style), Paragraph("INTEGER", table_cell), Paragraph("FK -> doctors(doctor_id) CASCADE", table_cell), Paragraph("Foreign Key referencing consulting physician", table_cell)],
        [Paragraph("appointment_date", code_style), Paragraph("TEXT", table_cell), Paragraph("NOT NULL (YYYY-MM-DD)", table_cell), Paragraph("Scheduled consultation calendar date", table_cell)],
        [Paragraph("time_slot", code_style), Paragraph("TEXT", table_cell), Paragraph("NOT NULL (e.g. '10:00 AM')", table_cell), Paragraph("Designated 30-minute consultation window", table_cell)],
        [Paragraph("status", code_style), Paragraph("TEXT", table_cell), Paragraph("DEFAULT 'Scheduled'", table_cell), Paragraph("State: 'Scheduled', 'Completed', 'Cancelled'", table_cell)]
    ]
    t_a = Table(apt_cols, colWidths=[90, 70, 160, 195])
    t_a.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 3.2),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_card_bg])
    ]))
    story.append(t_a)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 11: CHAPTER 6 - SYSTEM MODULES & FUNCTIONAL DECOMPOSITION
    # =========================================================================
    story.append(Paragraph("CHAPTER 6: SYSTEM MODULES & FUNCTIONAL DECOMPOSITION", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_teal, spaceAfter=8))

    story.append(Paragraph("6.1 Functional Hierarchy Overview", h2_style))
    story.append(Paragraph(
        "MediCare AI decomposes clinical complexity into five specialized operational modules, each operating as an "
        "independent functional subsystem while remaining interconnected via the unified `DatabaseManager` persistence layer.", body_style
    ))

    mod_data = [
        [Paragraph("<b>Subsystem Module</b>", table_header), Paragraph("<b>Key Responsibilities & Operations</b>", table_header), Paragraph("<b>Target User Role</b>", table_header)],
        [
            Paragraph("<b>1. Master Patient Index (MPI) Module</b>", table_cell),
            Paragraph("• Patient biographical registration (Name, Age, Gender, Phone, Blood Group).<br/>• Real-time medical search and historic encounter lookup.<br/>• Secure update and clinical record discharge management.", table_cell),
            Paragraph("Triage Staff / Receptionist", table_cell)
        ],
        [
            Paragraph("<b>2. Doctor Roster & OPD Module</b>", table_cell),
            Paragraph("• Clinical doctor onboarding, department assignment, and fee scheduling.<br/>• Available days configuration (e.g., 'Mon, Wed, Fri').<br/>• Workload load-balancing and consultation history monitoring.", table_cell),
            Paragraph("Medical Director / Administrator", table_cell)
        ],
        [
            Paragraph("<b>3. Appointment Scheduler Engine</b>", table_cell),
            Paragraph("• Conflict-free calendar slot booking.<br/>• Automatic schedule validation against doctor's available weekdays.<br/>• Real-time triage status updates ('Scheduled', 'Completed', 'Cancelled').", table_cell),
            Paragraph("Triage Staff / Patient Helpdesk", table_cell)
        ],
        [
            Paragraph("<b>4. Digital E-Prescription Engine</b>", table_cell),
            Paragraph("• Diagnostic coding and clinical observations capture.<br/>• Multi-drug prescription formulation with dosage, frequency, and duration.<br/>• Automated vector PDF prescription export via ReportLab engine.", table_cell),
            Paragraph("Attending Physician / Doctor", table_cell)
        ],
        [
            Paragraph("<b>5. Financial Billing & Invoicing Engine</b>", table_cell),
            Paragraph("• Multi-component medical invoice calculation (Consultation + Pharmacy + Tests - Discounts).<br/>• Payment status tracking ('Paid' vs 'Unpaid') across Cash, Card, UPI, and Insurance.<br/>• Automated printable GST/Tax compliant invoice generation in PDF.", table_cell),
            Paragraph("Hospital Cashier / Billing Auditor", table_cell)
        ]
    ]
    t_mod = Table(mod_data, colWidths=[120, 275, 120])
    t_mod.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 5.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_card_bg]),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(t_mod)
    story.append(Spacer(1, 8))

    story.append(Paragraph("6.2 Cross-Cutting Telemetry & Metrics Subsystem", h2_style))
    story.append(Paragraph(
        "A background telemetry engine queries the database upon every dashboard reload, computing hospital bed capacity "
        "(50-bed baseline), daily completion percentages, revenue totals, and pending appointment queues for instant administrative oversight.", body_style
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 12: CHAPTER 7 - DATA FLOW DIAGRAMS (HIGH CONTRAST PREFORMATTED)
    # =========================================================================
    story.append(Paragraph("CHAPTER 7: DATA FLOW DIAGRAMS (DFDs)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_teal, spaceAfter=8))

    story.append(Paragraph("7.1 Level 0: Context-Level Data Flow Diagram (DFD)", h2_style))
    story.append(Paragraph(
        "The Level 0 Context Diagram depicts MediCare AI as a central information-processing hub communicating "
        "with external healthcare entities (Patients, Consulting Physicians, and Administrative Auditors):", body_style
    ))

    dfd0_text = (
        "+-------------------+         1. Patient Demographics & Registration        +------------------------+\n"
        "|                   | ----------------------------------------------------> |                        |\n"
        "|      PATIENT      | <---------------------------------------------------- |                        |\n"
        "|                   |            4. Appointment Slip & PDF Invoice          |                        |\n"
        "+-------------------+                                                       |                        |\n"
        "                                                                            |      MEDICARE AI       |\n"
        "+-------------------+             3. Clinical Diagnosis & Rx Regimen        |     SMART HOSPITAL     |\n"
        "|                   | ----------------------------------------------------> |       CENTRAL OS       |\n"
        "|      DOCTOR       | <---------------------------------------------------- |      (PROCESS 0)       |\n"
        "|                   |            2. Consultation Schedule & Patient Triage  |                        |\n"
        "+-------------------+                                                       |                        |\n"
        "                                                                            |                        |\n"
        "+-------------------+           Doctor Duty Roster & Billing Tariffs        |                        |\n"
        "|   ADMINISTRATOR   | ----------------------------------------------------> |                        |\n"
        "|                   | <---------------------------------------------------- |                        |\n"
        "+-------------------+         5. Live Financial Telemetry & Occupancy KPIs  +------------------------+"
    )
    story.append(create_code_box(dfd0_text, title="LEVEL 0 CONTEXT DIAGRAM ARCHITECTURE"))
    story.append(Spacer(1, 8))

    story.append(Paragraph("7.2 Level 1: Subsystem Data Flow Decomposition", h2_style))
    story.append(Paragraph(
        "The Level 1 DFD decomposes Process 0 into 4 primary internal processes communicating with SQLite data stores:<br/>"
        "• <b>Process 1.0 (Patient Triage):</b> Accepts patient bio-data -> Writes to <i>D1: Patients Data Store</i>.<br/>"
        "• <b>Process 2.0 (Scheduling Validator):</b> Reads <i>D1</i> & <i>D2: Doctors</i> -> Writes to <i>D3: Appointments Data Store</i>.<br/>"
        "• <b>Process 3.0 (E-Prescription Engine):</b> Doctor inputs diagnosis & drug regimens -> Writes to <i>D4: Prescriptions Store</i>.<br/>"
        "• <b>Process 4.0 (Financial Ledger):</b> Computes billable services -> Writes to <i>D5: Billings Store</i> -> Invokes ReportLab PDF generator.", body_style
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("7.3 Level 2: Appointment Booking Process Refinement", h2_style))
    story.append(Paragraph(
        "Level 2 refines the booking pipeline: (1) Inbound Request -> (2) Day-of-Week String Parser -> "
        "(3) Doctor Day Availability Matrix Comparison -> (4) Collision Scan on existing appointments -> "
        "(5) Relational INSERT with status 'Scheduled'.", body_style
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 13: CHAPTER 8 - LOGIC FLOWCHARTS & SYSTEM ALGORITHMS (HIGH CONTRAST)
    # =========================================================================
    story.append(Paragraph("CHAPTER 8: LOGIC FLOWCHARTS & SYSTEM ALGORITHMS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_teal, spaceAfter=8))

    story.append(Paragraph("8.1 Algorithm 1: Conflict-Free Doctor Consultation Booking", h2_style))
    story.append(Paragraph(
        "<b>Input:</b> `patient_id`, `doctor_id`, `requested_date` (YYYY-MM-DD), `time_slot`<br/>"
        "<b>Output:</b> Confirmed `appointment_id` or Error Code ('CLASH' / 'UNAVAILABLE')", body_style
    ))
    algo1_code = (
        "1.  START\n"
        "2.  QUERY doctors table FOR available_days, fee WHERE doctor_id = :d_id\n"
        "3.  PARSE requested_date TO EXTRACT day_of_week (e.g., 'Monday')\n"
        "4.  IF day_of_week NOT IN available_days:\n"
        "5.      RETURN ERROR: 'Doctor is not available on selected day of the week'\n"
        "6.  QUERY appointments table WHERE doctor_id = :d_id AND appointment_date = :req_date\n"
        "7.                            AND time_slot = :slot AND status != 'Cancelled'\n"
        "8.  IF matching record exists:\n"
        "9.      RETURN ERROR: 'Time slot collision: Doctor is already booked for this window'\n"
        "10. EXECUTE SQL INSERT INTO appointments(patient_id, doctor_id, appointment_date, time_slot, status)\n"
        "11. COMMIT TRANSACTION\n"
        "12. RETURN SUCCESS: Newly generated appointment_id\n"
        "13. END"
    )
    story.append(create_code_box(algo1_code, title="ALGORITHM 1: CONFLICT-FREE SCHEDULING LOGIC"))
    story.append(Spacer(1, 8))

    story.append(Paragraph("8.2 Algorithm 2: Automated Financial Billing & Discount Calculation", h2_style))
    algo2_code = (
        "1.  START\n"
        "2.  INPUT: appt_id, consult_fee, medicine_fee, other_charges, discount_val\n"
        "3.  VALIDATE THAT consult_fee, medicine_fee, other_charges >= 0.0\n"
        "4.  gross_subtotal = consult_fee + medicine_fee + other_charges\n"
        "5.  net_payable = MAX(0.0, gross_subtotal - discount_val)\n"
        "6.  QUERY billings table WHERE appointment_id = :appt_id\n"
        "7.  IF existing_bill_found:\n"
        "8.      UPDATE billings SET total_amount = net_payable, payment_status = :status ...\n"
        "9.  ELSE:\n"
        "10.     INSERT INTO billings(appointment_id, patient_id, total_amount, date ...)\n"
        "11. GENERATE ReportLab PDF Invoice file on disk\n"
        "12. RETURN net_payable & invoice_path\n"
        "13. END"
    )
    story.append(create_code_box(algo2_code, title="ALGORITHM 2: FINANCIAL BILLING & DISCOUNT ENGINE"))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 14: CHAPTER 9 - SOURCE ARCHITECTURE: DATABASE ENGINE (HIGH CONTRAST)
    # =========================================================================
    story.append(Paragraph("CHAPTER 9: SOURCE CODE ARCHITECTURE - DATABASE ENGINE", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_teal, spaceAfter=8))

    story.append(Paragraph("9.1 The `DatabaseManager` Core Abstraction", h2_style))
    story.append(Paragraph(
        "All data access in MediCare AI is centralized inside the `DatabaseManager` class in `main.py`. "
        "It eliminates raw, scattered SQL queries by exposing atomic, parameterized helper methods that protect "
        "against SQL injection attacks while enforcing connection cleanup with Python context managers.", body_style
    ))

    db_code_snip = (
        "class DatabaseManager:\n"
        "    def __init__(self, db_path: str = DB_NAME):\n"
        "        self.db_path = db_path\n"
        "        self.init_db()\n\n"
        "    def get_connection(self) -> sqlite3.Connection:\n"
        "        conn = sqlite3.connect(self.db_path)\n"
        "        conn.execute('PRAGMA foreign_keys = ON;')  # Enforce Relational Integrity\n"
        "        conn.row_factory = sqlite3.Row              # Dictionary-like column access\n"
        "        return conn\n\n"
        "    def add_patient(self, name: str, age: int, gender: str, phone: str,\n"
        "                    blood_group: str, address: str) -> int:\n"
        "        created_at = datetime.date.today().strftime('%Y-%m-%d')\n"
        "        with self.get_connection() as conn:\n"
        "            cursor = conn.cursor()\n"
        "            cursor.execute('''\n"
        "                INSERT INTO patients (name, age, gender, phone, blood_group, address, created_at)\n"
        "                VALUES (?, ?, ?, ?, ?, ?, ?)\n"
        "            ''', (name, age, gender, phone, blood_group, address, created_at))\n"
        "            conn.commit()\n"
        "            return cursor.lastrowid\n\n"
        "    def get_dashboard_metrics(self) -> Dict[str, Any]:\n"
        "        with self.get_connection() as conn:\n"
        "            cursor = conn.cursor()\n"
        "            total_p = cursor.execute('SELECT COUNT(*) FROM patients').fetchone()[0]\n"
        "            revenue = cursor.execute('SELECT COALESCE(SUM(total_amount), 0) FROM billings '\n"
        "                                     'WHERE payment_status = \"Paid\"').fetchone()[0]\n"
        "            return {'total_patients': total_p, 'total_revenue': float(revenue)}"
    )
    story.append(create_code_box(db_code_snip, title="CORE PERSISTENCE LAYER: DatabaseManager IN main.py"))
    story.append(Spacer(1, 8))

    story.append(Paragraph("9.2 Parameterized Query Defense Mechanism", h2_style))
    story.append(Paragraph(
        "By enforcing the `?` token replacement convention in SQLite, input values are treated purely as literal constants "
        "rather than executable SQL code, preventing malicious payloads such as `' OR '1'='1` from compromising clinical data.", body_style
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 15: CHAPTER 10 - SOURCE ARCHITECTURE: DESKTOP GUI (HIGH CONTRAST)
    # =========================================================================
    story.append(Paragraph("CHAPTER 10: SOURCE CODE ARCHITECTURE - DESKTOP GUI", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_teal, spaceAfter=8))

    story.append(Paragraph("10.1 The Dual-Engine Desktop Architecture", h2_style))
    story.append(Paragraph(
        "The desktop client in `main.py` is engineered with an intelligent dual-engine fallback: "
        "it utilizes <b>CustomTkinter</b> when available for ultra-smooth dark-mode widgets with rounded geometry, "
        "and automatically falls back to native <b>Tkinter / TTK</b> if running on minimal environments without external packages.", body_style
    ))

    gui_code_snip = (
        "class StatCard(ctk.CTkFrame if USE_CUSTOMTKINTER else tk.Frame):\n"
        "    '''Reusable telemetry card displaying KPI metrics with modern aesthetics.'''\n"
        "    def __init__(self, parent, title: str, value: str, icon: str, color: str):\n"
        "        super().__init__(parent, fg_color=color, corner_radius=12)\n"
        "        self.icon_lbl = ctk.CTkLabel(self, text=icon, font=('Segoe UI', 24))\n"
        "        self.title_lbl = ctk.CTkLabel(self, text=title, font=('Inter', 11))\n"
        "        self.val_lbl = ctk.CTkLabel(self, text=value, font=('Inter Bold', 20))\n"
        "        self.icon_lbl.pack(side='left', padx=12, pady=10)\n"
        "        self.title_lbl.pack(anchor='w', padx=4)\n"
        "        self.val_lbl.pack(anchor='w', padx=4)\n\n"
        "class HospitalApp(ctk.CTk if USE_CUSTOMTKINTER else tk.Tk):\n"
        "    def __init__(self):\n"
        "        super().__init__()\n"
        "        self.db = DatabaseManager()\n"
        "        self.title('MediCare Hospital Management System - v2.5 Pro Enterprise')\n"
        "        self.geometry('1280x800')\n"
        "        self.setup_sidebar_navigation()\n"
        "        self.load_dashboard_view()\n\n"
        "    def setup_sidebar_navigation(self):\n"
        "        # Navigation tabs: Dashboard, Patients, Doctors, Appointments, Billing"
    )
    story.append(create_code_box(gui_code_snip, title="DESKTOP INTERFACE ARCHITECTURE: StatCard & HospitalApp IN main.py"))
    story.append(Spacer(1, 8))

    story.append(Paragraph("10.2 Headless Mock Widget System for Cloud Compatibility", h2_style))
    story.append(Paragraph(
        "To allow the same codebase to run seamlessly in cloud and serverless environments (where no physical X11 or Win32 "
        "display server exists), `main.py` incorporates a dynamic mock proxy object (`_DummyModule`) that neutralizes GUI calls "
        "without raising `NameError` or `ImportError` on headless servers.", body_style
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 16: CHAPTER 11 - SOURCE ARCHITECTURE: WEB PORTAL (HIGH CONTRAST)
    # =========================================================================
    story.append(Paragraph("CHAPTER 11: SOURCE CODE ARCHITECTURE - WEB PORTAL & REST API", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_teal, spaceAfter=8))

    story.append(Paragraph("11.1 Flask Web Server & Microservices Engine", h2_style))
    story.append(Paragraph(
        "`server.py` implements a high-performance web dashboard inspired by award-winning Behance UI/UX healthcare systems. "
        "It features role-based authentication, real-time SVG charting, outpatient triage boards, and JSON REST API endpoints.", body_style
    ))

    flask_code_snip = (
        "app = Flask(__name__)\n"
        "app.secret_key = 'medicare_ai_clinical_os_super_secret_key_2026'\n\n"
        "class VercelPathMiddleware:\n"
        "    '''Normalizes dynamic cloud serverless URL rewrites into WSGI PATH_INFO.'''\n"
        "    def __init__(self, wsgi_app):\n"
        "        self.wsgi_app = wsgi_app\n"
        "    def __call__(self, environ, start_response):\n"
        "        qs_raw = environ.get('QUERY_STRING', '')\n"
        "        if '__vercel_path' in qs_raw:\n"
        "            qs = urllib.parse.parse_qs(qs_raw, keep_blank_values=True)\n"
        "            if '__vercel_path' in qs:\n"
        "                vp = qs.pop('__vercel_path')[0]\n"
        "                environ['QUERY_STRING'] = urllib.parse.urlencode([(k,v) for k,vs in qs.items() for v in vs])\n"
        "                environ['PATH_INFO'] = '/' + vp.lstrip('/')\n"
        "        return self.wsgi_app(environ, start_response)\n\n"
        "app.wsgi_app = VercelPathMiddleware(app.wsgi_app)\n\n"
        "@app.route('/login', methods=['GET', 'POST'])\n"
        "def login():\n"
        "    if request.method == 'POST':\n"
        "        user = request.form.get('username')\n"
        "        pwd = request.form.get('password')\n"
        "        if user in AUTH_USERS and check_password_hash(AUTH_USERS[user]['hash'], pwd):\n"
        "            session['user'] = user\n"
        "            return redirect('/')\n"
        "    return render_template_string(LOGIN_TEMPLATE)\n\n"
        "@app.route('/api/metrics')\n"
        "def api_metrics():\n"
        "    return jsonify(db.get_dashboard_metrics())"
    )
    story.append(create_code_box(flask_code_snip, title="CLOUD REST API & WSGI ROUTING ENGINE IN server.py"))
    story.append(Spacer(1, 8))

    story.append(Paragraph("11.2 Cryptographic Password Hashing", h2_style))
    story.append(Paragraph(
        "Passwords are never stored in plaintext. `werkzeug.security.generate_password_hash` hashes all staff credentials "
        "using salted PBKDF2 with SHA-256 iterations, protecting clinical staff accounts against dictionary and rainbow-table attacks.", body_style
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 17: CHAPTER 12 - SOURCE ARCHITECTURE: AUTOMATED PDF ENGINE (HIGH CONTRAST)
    # =========================================================================
    story.append(Paragraph("CHAPTER 12: SOURCE CODE ARCHITECTURE - AUTOMATED PDF ENGINE", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_teal, spaceAfter=8))

    story.append(Paragraph("12.1 The `PDFReportGenerator` Engine in `main.py`", h2_style))
    story.append(Paragraph(
        "MediCare AI integrates a dedicated document rendering pipeline powered by <b>ReportLab</b>. "
        "Instead of relying on fragile browser printing styles, it builds pure vector PDF files using flowables "
        "(`SimpleDocTemplate`, `Paragraph`, `Table`, `Spacer`), generating branded invoices and prescriptions.", body_style
    ))

    pdf_code_snip = (
        "class PDFReportGenerator:\n"
        "    @classmethod\n"
        "    def generate_invoice_pdf(cls, bill_data: Dict[str, Any]) -> str:\n"
        "        inv_dir, _ = cls.get_output_dirs()\n"
        "        bill_id = bill_data.get('bill_id', 0)\n"
        "        filepath = os.path.join(inv_dir, f'Invoice_INV-{bill_id:04d}.pdf')\n"
        "        doc = SimpleDocTemplate(filepath, pagesize=letter, rightMargin=36, leftMargin=36)\n"
        "        styles = getSampleStyleSheet()\n"
        "        elements = []\n\n"
        "        # Brand Header Banner\n"
        "        elements.append(Paragraph('MEDICARE SUPER SPECIALTY HOSPITAL', styles['Title']))\n"
        "        elements.append(Paragraph('Tax Invoice & Outpatient Financial Summary', styles['Heading2']))\n"
        "        elements.append(Spacer(1, 12))\n\n"
        "        # Line Items Table\n"
        "        table_data = [\n"
        "            ['Service Description', 'Category', 'Amount (INR)'],\n"
        "            ['Physician Consultation Fee', 'OPD Clinical', f'INR {bill_data[\"consultation_fee\"]:.2f}'],\n"
        "            ['Prescribed Medicines & Pharmacy', 'Dispensary', f'INR {bill_data[\"medicine_fee\"]:.2f}'],\n"
        "            ['Institutional / Diagnostic Charges', 'Laboratory', f'INR {bill_data[\"other_charges\"]:.2f}'],\n"
        "            ['Discount / Concession Granted', 'Waiver', f'- INR {bill_data[\"discount\"]:.2f}'],\n"
        "            ['TOTAL PAYABLE AMOUNT', 'NET', f'INR {bill_data[\"total_amount\"]:.2f}']\n"
        "        ]\n"
        "        t = Table(table_data, colWidths=[240, 140, 140])\n"
        "        t.setStyle(TableStyle([\n"
        "            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),\n"
        "            ('TEXTCOLOR', (0,0), (-1,0), colors.white),\n"
        "            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1'))\n"
        "        ]))\n"
        "        elements.append(t)\n"
        "        doc.build(elements)\n"
        "        return filepath"
    )
    story.append(create_code_box(pdf_code_snip, title="REPORTLAB PDF SYNTHESIS ENGINE IN main.py"))
    story.append(Spacer(1, 8))

    story.append(Paragraph("12.2 Output Management & Ephemeral Routing", h2_style))
    story.append(Paragraph(
        "On cloud serverless platforms (e.g. AWS Lambda / Vercel) where the root filesystem is strictly read-only, "
        "`PDFReportGenerator.get_output_dirs()` detects the serverless environment and dynamically routes all generated "
        "PDF invoices to `/tmp/invoices` and `/tmp/prescriptions`, preventing OS write-lock failures.", body_style
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 18: CHAPTER 13 - SECURITY, DATA INTEGRITY & FAULT TOLERANCE
    # =========================================================================
    story.append(Paragraph("CHAPTER 13: SECURITY, DATA INTEGRITY & FAULT TOLERANCE", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_teal, spaceAfter=8))

    story.append(Paragraph("13.1 Comprehensive Security Architecture", h2_style))
    story.append(Paragraph(
        "Because hospital information systems govern Protected Health Information (PHI), MediCare AI enforces security "
        "at every tier of its software architecture:", body_style
    ))

    sec_data = [
        [Paragraph("<b>Security Domain</b>", table_header), Paragraph("<b>Vulnerability Threat Mitigated</b>", table_header), Paragraph("<b>Implementation Mechanism in MediCare AI</b>", table_header)],
        [
            Paragraph("<b>Database Layer</b>", table_cell),
            Paragraph("SQL Injection, Unauthorized schema alterations, Malicious table drops.", table_cell),
            Paragraph("100% Parameterized queries with SQLite `?` placeholders; zero raw string interpolation.", table_cell)
        ],
        [
            Paragraph("<b>Authentication Layer</b>", table_cell),
            Paragraph("Credential theft, Brute-force attacks, Plaintext password leaks.", table_cell),
            Paragraph("PBKDF2-SHA256 salted password hashing; brute-force rejection on invalid staff IDs.", table_cell)
        ],
        [
            Paragraph("<b>Session Management</b>", table_cell),
            Paragraph("Session hijacking, Cross-Site Scripting (XSS), Stale logins.", table_cell),
            Paragraph("Flask cryptographically signed session cookies; 30-day optional remember-me tokens.", table_cell)
        ],
        [
            Paragraph("<b>Cloud Filesystem Security</b>", table_cell),
            Paragraph("Read-Only Filesystem exceptions on AWS Lambda / Vercel cloud runtimes.", table_cell),
            Paragraph("Dynamic serverless detection redirecting SQLite & PDF generation to `/tmp` volume.", table_cell)
        ],
        [
            Paragraph("<b>Headless Resilience</b>", table_cell),
            Paragraph("Import crashes when launching on cloud Linux without desktop display libraries.", table_cell),
            Paragraph("Graceful `_DummyModule` mock proxies neutralizing Tkinter and CustomTkinter calls.", table_cell)
        ]
    ]
    t_sec = Table(sec_data, colWidths=[110, 195, 210])
    t_sec.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 5.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_card_bg])
    ]))
    story.append(t_sec)
    story.append(Spacer(1, 8))

    story.append(Paragraph("13.2 ACID Compliance Guarantees", h2_style))
    story.append(Paragraph(
        "By utilizing SQLite3 as the relational database engine, MediCare AI natively delivers full <b>ACID</b> compliance:<br/>"
        "• <b>Atomicity:</b> Invoicing and appointment creation execute in atomic blocks; any unexpected error triggers automatic transaction rollback.<br/>"
        "• <b>Consistency:</b> Foreign keys with `ON DELETE CASCADE` ensure no consultation points to a non-existent patient or doctor.<br/>"
        "• <b>Isolation:</b> Database locking protocols ensure concurrent read-write queries remain cleanly serialized.<br/>"
        "• <b>Durability:</b> All committed appointments and invoices are immediately flushed to non-volatile disk storage.", body_style
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 19: CHAPTER 14 - SYSTEM TESTING & TEST CASE MATRIX
    # =========================================================================
    story.append(Paragraph("CHAPTER 14: SYSTEM TESTING & TEST CASE MATRIX", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_teal, spaceAfter=8))

    story.append(Paragraph("14.1 Test Methodology", h2_style))
    story.append(Paragraph(
        "Testing was conducted across four standardized phases: <b>Unit Testing</b> of individual `DatabaseManager` functions, "
        "<b>Integration Testing</b> of GUI and Web workflows, <b>Boundary Testing</b> of financial and date inputs, and "
        "<b>User Acceptance Testing (UAT)</b> simulating a live hospital outpatient department.", body_style
    ))

    test_data = [
        [Paragraph("<b>Test ID</b>", table_header), Paragraph("<b>Feature Under Test</b>", table_header), Paragraph("<b>Test Input Data</b>", table_header), Paragraph("<b>Expected Result</b>", table_header), Paragraph("<b>Status</b>", table_header)],
        [
            Paragraph("<b>TC-01</b>", code_style), Paragraph("Patient Admission", table_cell),
            Paragraph("Name: 'Ramesh Kumar', Age: 45, Gender: 'Male', Phone: '9898989801'", table_cell),
            Paragraph("Record inserted into `patients` table with unique ID.", table_cell),
            Paragraph("<font color='#059669'><b>PASS</b></font>", table_cell)
        ],
        [
            Paragraph("<b>TC-02</b>", code_style), Paragraph("Double Booking Clash", table_cell),
            Paragraph("Dr. Sharma (Cardiology) booked at '10:00 AM' on identical date twice.", table_cell),
            Paragraph("System detects collision; alerts user and prevents duplicate entry.", table_cell),
            Paragraph("<font color='#059669'><b>PASS</b></font>", table_cell)
        ],
        [
            Paragraph("<b>TC-03</b>", code_style), Paragraph("Doctor Availability Validation", table_cell),
            Paragraph("Book Dr. Priya (Tue, Thu, Sat) on a Wednesday calendar date.", table_cell),
            Paragraph("Scheduler flags doctor off-duty for Wednesday; denies booking.", table_cell),
            Paragraph("<font color='#059669'><b>PASS</b></font>", table_cell)
        ],
        [
            Paragraph("<b>TC-04</b>", code_style), Paragraph("Invoice Math Calculation", table_cell),
            Paragraph("Consult: ₹800, Meds: ₹400, Lab: ₹200, Discount: ₹150.", table_cell),
            Paragraph("Net total accurately computed as exactly ₹1,250.00.", table_cell),
            Paragraph("<font color='#059669'><b>PASS</b></font>", table_cell)
        ],
        [
            Paragraph("<b>TC-05</b>", code_style), Paragraph("Negative Total Guard", table_cell),
            Paragraph("Subtotal: ₹500, Disproportionate Discount: ₹800.", table_cell),
            Paragraph("Mathematical clamp applies `MAX(0, total)` -> Net bill ₹0.00.", table_cell),
            Paragraph("<font color='#059669'><b>PASS</b></font>", table_cell)
        ],
        [
            Paragraph("<b>TC-06</b>", code_style), Paragraph("Vector PDF Invoice Export", table_cell),
            Paragraph("Trigger PDF generation for Bill #INV-0002.", table_cell),
            Paragraph("Vector-clean PDF created in output directory with exact line items.", table_cell),
            Paragraph("<font color='#059669'><b>PASS</b></font>", table_cell)
        ],
        [
            Paragraph("<b>TC-07</b>", code_style), Paragraph("Staff Authentication Guard", table_cell),
            Paragraph("Username: 'admin', Incorrect Password: 'wrongpassword'.", table_cell),
            Paragraph("Access rejected; error banner shown; session withheld.", table_cell),
            Paragraph("<font color='#059669'><b>PASS</b></font>", table_cell)
        ],
        [
            Paragraph("<b>TC-08</b>", code_style), Paragraph("Cascade Delete Integrity", table_cell),
            Paragraph("Delete patient record having active appointments & bills.", table_cell),
            Paragraph("Child records in appointments & bills deleted automatically.", table_cell),
            Paragraph("<font color='#059669'><b>PASS</b></font>", table_cell)
        ]
    ]
    t_test = Table(test_data, colWidths=[45, 110, 160, 150, 50])
    t_test.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 3.8),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_card_bg]),
        ('ALIGN', (4,0), (4,-1), 'CENTER')
    ]))
    story.append(t_test)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 20: CHAPTER 15 - USER INTERFACE WALKTHROUGH & OPERATIONS
    # =========================================================================
    story.append(Paragraph("CHAPTER 15: USER INTERFACE WALKTHROUGH & OPERATIONS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_teal, spaceAfter=8))

    story.append(Paragraph("15.1 Operational Screen Walkthrough", h2_style))
    story.append(Paragraph(
        "MediCare AI provides an intuitive visual experience modeled after modern healthcare design paradigms. "
        "Below is the comprehensive operational walkthrough of the system's key screens:", body_style
    ))

    screens_data = [
        [Paragraph("<b>Screen View</b>", table_header), Paragraph("<b>Visual Elements & Layout</b>", table_header), Paragraph("<b>Staff Workflow & Actions</b>", table_header)],
        [
            Paragraph("<b>1. Authentication Portal</b> (`/login`)", table_cell),
            Paragraph("Deep Slate background with glassmorphic authentication card. Eye icon for password peek, pre-fill buttons for instant demo login, and Protected Health Information (PHI) legal warning banner.", table_cell),
            Paragraph("Receptionist / Physician enters Staff Username and Password. Selecting 'Remember me' sets an encrypted 30-day session.", table_cell)
        ],
        [
            Paragraph("<b>2. Clinical Executive Dashboard</b> (`/`)", table_cell),
            Paragraph("Four floating metric cards displaying Total Patients, Today's Consultations, Active Doctor Rosters, and Net Revenue. Interactive SVG bar chart displaying weekly patient trends.", table_cell),
            Paragraph("Hospital administrators monitor real-time bed capacity (50 beds), view completion percentages, and identify department bottlenecks.", table_cell)
        ],
        [
            Paragraph("<b>3. Patient Master Index</b> (`/?tab=patients`)", table_cell),
            Paragraph("Tabular view of all registered patients with Age, Gender, Blood Group badge, and Contact. Includes a slide-in 'New Patient Admission' form modal.", table_cell),
            Paragraph("Triage staff registers inbound patients, updates contact details, and accesses complete patient clinical visit histories.", table_cell)
        ],
        [
            Paragraph("<b>4. Appointment Central Hub</b> (`/?tab=appointments`)", table_cell),
            Paragraph("Calendar-ordered roster showing Patient Name, Consulting Doctor, Date, Time Window, and Status badge ('Scheduled' / 'Completed' / 'Cancelled').", table_cell),
            Paragraph("Staff schedules new consultations with automatic validation against doctor available weekdays and conflict prevention.", table_cell)
        ],
        [
            Paragraph("<b>5. E-Prescription & Billing Hub</b> (`/?tab=billing`)", table_cell),
            Paragraph("Comprehensive financial ledger displaying Consultation fee, Pharmacy charges, Diagnostic lab fees, Discounts, and Paid/Unpaid status.", table_cell),
            Paragraph("Cashier clicks 'Mark Paid' with Cash/Card/UPI toggle, and downloads the branded vector PDF invoice with a single click.", table_cell)
        ]
    ]
    t_screens = Table(screens_data, colWidths=[120, 205, 190])
    t_screens.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_card_bg]),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(t_screens)
    story.append(Spacer(1, 6))

    story.append(Paragraph("15.2 Live Cloud Deployment Domain", h2_style))
    story.append(Paragraph(
        "The web portal is published and operating live in production on Vercel's global edge network at: "
        "<b>https://medi-care-ai-nu.vercel.app</b>. It features zero-cold-start degradation and is accessible from any "
        "authorized desktop or mobile browser.", body_style
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 21: CHAPTER 16 - ADVANTAGES, LIMITATIONS & FUTURE ENHANCEMENTS
    # =========================================================================
    story.append(Paragraph("CHAPTER 16: ADVANTAGES, LIMITATIONS & FUTURE ENHANCEMENTS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_teal, spaceAfter=8))

    story.append(Paragraph("16.1 Key System Advantages", h2_style))
    story.append(Paragraph("• <b>Zero Software Acquisition Cost:</b> Constructed completely on open-source technologies (Python, SQLite, CustomTkinter, Flask, ReportLab) without licensing fees.", bullet_style))
    story.append(Paragraph("• <b>Elimination of Paper Waste:</b> Digitizes admission records, consultation notes, and invoices, supporting green healthcare initiatives.", bullet_style))
    story.append(Paragraph("• <b>Accelerated Patient Throughput:</b> Cuts outpatient registration and appointment booking time from 10–15 minutes to under 30 seconds.", bullet_style))
    story.append(Paragraph("• <b>Guaranteed Arithmetic Accuracy:</b> Financial ledgers, tax deductions, and discounts are computed programmatically, eliminating human calculation errors.", bullet_style))
    story.append(Paragraph("• <b>High Operational Portability:</b> Runs offline on a single clinic laptop or scales to cloud serverless clusters with automatic database replication.", bullet_style))

    story.append(Paragraph("16.2 Known Project Limitations", h2_style))
    story.append(Paragraph("• <b>Single Clinic SQLite Scope:</b> While SQLite handles thousands of daily records efficiently, enterprise multi-hospital chains with millions of rows would benefit from PostgreSQL or MySQL.", bullet_style))
    story.append(Paragraph("• <b>Hardware Biometrics Absence:</b> Fingerprint scanning and smart-card RFID integration for patient identification are not yet implemented.", bullet_style))
    story.append(Paragraph("• <b>SMS Gateway Integration:</b> Appointment confirmations are generated as printable receipts and web alerts rather than automated SMS/WhatsApp notifications.", bullet_style))

    story.append(Paragraph("16.3 Future Roadmap & Planned Upgrades", h2_style))
    future_box = [
        [Paragraph("<b>Phase</b>", table_header), Paragraph("<b>Planned Technical Upgrade</b>", table_header), Paragraph("<b>Clinical Benefit</b>", table_header)],
        [Paragraph("<b>Phase 1 (Q3 2026)</b>", code_style), Paragraph("Integration of Twilio / Fast2SMS API gateways", table_cell), Paragraph("Automated WhatsApp and SMS appointment reminders sent directly to patients.", table_cell)],
        [Paragraph("<b>Phase 2 (Q4 2026)</b>", code_style), Paragraph("AI Clinical Symptom Checker & ICD-10 Coding", table_cell), Paragraph("Machine Learning triage engine suggesting probable diagnoses based on vital signs.", table_cell)],
        [Paragraph("<b>Phase 3 (Q1 2027)</b>", code_style), Paragraph("HL7 / FHIR Standard Clinical Interoperability", table_cell), Paragraph("Seamless electronic health record (EHR) exchange with diagnostic imaging centers.", table_cell)],
        [Paragraph("<b>Phase 4 (Q2 2027)</b>", code_style), Paragraph("Integrated Razorpay / UPI Payment Gateway", table_cell), Paragraph("Online contactless consultation fee payments prior to hospital arrival.", table_cell)]
    ]
    t_f = Table(future_box, colWidths=[90, 205, 220])
    t_f.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_indigo),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_card_bg])
    ]))
    story.append(t_f)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 22: CHAPTER 17 - CONCLUSION & BIBLIOGRAPHY
    # =========================================================================
    story.append(Paragraph("CHAPTER 17: CONCLUSION & BIBLIOGRAPHY", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_teal, spaceAfter=8))

    story.append(Paragraph("17.1 Project Conclusion", h2_style))
    story.append(Paragraph(
        "The development of <b>MediCare AI: Smart Hospital & Doctor Appointment Management System</b> successfully fulfills "
        "all academic requirements outlined by the <b>Central Board of Secondary Education (CBSE)</b> for the Class 12 Computer Science "
        "Investigatory Project. Through systematic application of Object-Oriented Programming (OOP) in Python, relational schema design "
        "in SQLite3, and modern GUI/Web interface paradigms, the project proves that robust, enterprise-grade healthcare management "
        "tools can be constructed with zero proprietary software dependencies.<br/><br/>"
        f"Working as an investigatory software developer from <b>PM SHRI Kendriya Vidyalaya ASC Centre</b> alongside my project partner "
        f"<b>{partner_name}</b>, we gained invaluable practical experience in relational schema design, collision-prevention algorithms, "
        f"cryptographic security, WSGI cloud routing, and automated document compilation. MediCare AI stands as a functional, "
        f"battle-tested software solution ready to optimize clinical workflows and advance the digitization of Indian healthcare.", body_style
    ))

    story.append(Paragraph("17.2 References & Bibliography", h2_style))
    story.append(Paragraph("1. <b>Computer Science with Python (Class XII)</b> by Sumita Arora, Dhanpat Rai & Co. Publications, New Delhi.", bullet_style))
    story.append(Paragraph("2. <b>Computer Science with Python - Textbook for Class XII</b>, National Council of Educational Research and Training (NCERT), New Delhi.", bullet_style))
    story.append(Paragraph("3. <b>Python Official Documentation (v3.12)</b>: Standard Library, `sqlite3`, `json`, `datetime` modules — https://docs.python.org/3/", bullet_style))
    story.append(Paragraph("4. <b>CustomTkinter Documentation</b> by Tom Schimansky: Modern UI elements for Python — https://customtkinter.tomschimansky.com/", bullet_style))
    story.append(Paragraph("5. <b>Flask Documentation (v3.0.x)</b>: The Pallets Projects, Web Development Microframework — https://flask.palletsprojects.com/", bullet_style))
    story.append(Paragraph("6. <b>ReportLab Reference Manual</b>: Dynamic PDF Generation with Python — https://www.reportlab.com/docs/reportlab-userguide.pdf", bullet_style))
    story.append(Paragraph("7. <b>SQLite SQL Database Engine Documentation</b>: ACID Transactions and Foreign Key Pragmas — https://www.sqlite.org/docs.html", bullet_style))
    story.append(Paragraph("8. <b>CBSE Curriculum & Assessment Guidelines</b> for Senior Secondary Computer Science (Code 083) — https://cbseacademic.nic.in/", bullet_style))
    story.append(Spacer(1, 24))

    # Team Credentials Box - Tailored for this student
    cred_data = [
        [Paragraph("<b>PROJECT INVESTIGATOR & SOFTWARE DEVELOPER</b>", ParagraphStyle('DevH', fontName='Helvetica-Bold', fontSize=9, leading=12, textColor=c_primary, alignment=1))],
        [Paragraph(f"<b>{student_name}</b> (CBSE Roll No: <b>{student_roll}</b>) &nbsp;&nbsp;|&nbsp;&nbsp; In Collaboration with <b>{partner_name}</b> (Roll No: <b>{partner_roll}</b>)<br/><b>Class XII A (Science Stream)</b> &nbsp;•&nbsp; <b>PM SHRI KENDRIYA VIDYALAYA ASC CENTRE, BENGALURU</b>", ParagraphStyle('DevB', fontName='Helvetica', fontSize=8.5, leading=13, alignment=1))]
    ]
    t_cred = Table(cred_data, colWidths=[515])
    t_cred.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f1f5f9')),
        ('BOX', (0,0), (-1,-1), 1, c_teal),
        ('PADDING', (0,0), (-1,-1), 7),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')
    ]))
    story.append(t_cred)

    # Factory function for canvasmaker with student metadata
    def make_canvas(*args, **kwargs):
        return StudentNumberedCanvas(
            *args,
            student_name=student_name,
            student_roll=student_roll,
            partner_name=partner_name,
            partner_roll=partner_roll,
            **kwargs
        )

    doc.build(story, canvasmaker=make_canvas)
    print(f"Generated: {output_pdf}")


def main():
    print("Building separate 22-page documentation reports for both students...")
    
    # 1. Report for DIVYANSHU KUMAR (Roll No: 12115)
    generate_single_report(
        student_name="DIVYANSHU KUMAR",
        student_roll="12115",
        partner_name="AMAN RAJ",
        partner_roll="12110",
        output_pdf="MediCare_AI_Documentation_DIVYANSHU_KUMAR_12115.pdf"
    )

    # 2. Report for AMAN RAJ (Roll No: 12110)
    generate_single_report(
        student_name="AMAN RAJ",
        student_roll="12110",
        partner_name="DIVYANSHU KUMAR",
        partner_roll="12115",
        output_pdf="MediCare_AI_Documentation_AMAN_RAJ_12110.pdf"
    )

    print("Both 22-page student documentation reports compiled successfully!")

if __name__ == "__main__":
    main()

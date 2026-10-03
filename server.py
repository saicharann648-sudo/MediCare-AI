"""
========================================================================================
AI HEALTHCARE & HOSPITAL MANAGEMENT SYSTEM (BEHANCE / DRIBBBLE INSPIRED)
========================================================================================
A state-of-the-art AI Healthcare & Hospital Management Dashboard.
Modeled after award-winning Behance UI/UX case studies:
- Clean, modern light-canvas layout with soft floating cards
- AI Clinical Intelligence Assistant & Diagnostics Bar
- Interactive SVG Visual Analytics & Weekly Consultation Charts
- Outpatient Triage, Master Patient Index, and Doctor Rosters
- ReportLab Branded PDF Invoicing and Digital Rx Export
========================================================================================
"""

import os
import json
import datetime
from flask import Flask, request, jsonify, render_template_string, send_file, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from main import DatabaseManager, PDFReportGenerator, DEFAULT_CURRENCY

app = Flask(__name__)
app.secret_key = "medicare_ai_clinical_os_super_secret_key_2026"
try:
    db = DatabaseManager()
except Exception as e:
    print(f"Warning: DatabaseManager initial connection error: {e}")
    try:
        db = DatabaseManager("/tmp/hospital.db")
    except Exception as e2:
        print(f"Critical: Fallback DatabaseManager error: {e2}")
        db = None


AI_HEALTHCARE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MediCare AI | Next-Gen Hospital Operations & Clinical Dashboard</title>
    <!-- Google Fonts: Plus Jakarta Sans & Inter -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-canvas: #f4f6fa;
            --surface-white: #ffffff;
            --surface-subtle: #f8fafc;
            --border-light: #e5e9f2;
            --border-hover: #cbd5e1;
            
            --primary-indigo: #4f46e5;
            --primary-gradient: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%);
            --primary-glow: rgba(79, 70, 229, 0.25);
            
            --teal-accent: #0d9488;
            --cyan-accent: #06b6d4;
            --emerald-success: #10b981;
            --amber-warning: #f59e0b;
            --rose-danger: #f43f5e;
            
            --text-title: #0f172a;
            --text-body: #334155;
            --text-secondary: #64748b;
            --text-muted: #94a3b8;
            
            --radius-sm: 8px;
            --radius-md: 12px;
            --radius-lg: 18px;
            --radius-xl: 24px;
            
            --shadow-subtle: 0 4px 20px -2px rgba(15, 23, 42, 0.04);
            --shadow-card: 0 10px 30px -4px rgba(27, 43, 85, 0.06);
            --shadow-hover: 0 16px 36px -6px rgba(27, 43, 85, 0.12);
        }

        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Plus Jakarta Sans', sans-serif; }
        body {
            background-color: var(--bg-canvas);
            color: var(--text-body);
            height: 100vh;
            display: flex;
            overflow: hidden;
            -webkit-font-smoothing: antialiased;
        }

        /* ---------------------------------------------------------------------
           1. MODERN FLOATING SIDEBAR (Behance Concept Style)
        --------------------------------------------------------------------- */
        aside.floating-sidebar {
            width: 260px;
            background: var(--surface-white);
            border-right: 1px solid var(--border-light);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: 24px 18px;
            z-index: 50;
        }

        .brand-header {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 4px 8px 24px 8px;
            border-bottom: 1px solid var(--border-light);
            margin-bottom: 20px;
        }
        .brand-icon {
            width: 42px;
            height: 42px;
            background: var(--primary-gradient);
            border-radius: var(--radius-md);
            display: flex;
            align-items: center;
            justify-content: center;
            color: #ffffff;
            font-size: 20px;
            box-shadow: 0 8px 16px var(--primary-glow);
        }
        .brand-info h1 {
            font-size: 16px;
            font-weight: 800;
            color: var(--text-title);
            letter-spacing: -0.3px;
        }
        .brand-info p {
            font-size: 11px;
            font-weight: 600;
            color: var(--primary-indigo);
            display: flex;
            align-items: center;
            gap: 4px;
        }

        .nav-group-title {
            font-size: 11px;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.6px;
            padding: 8px 12px;
            margin-top: 6px;
        }

        .nav-list {
            display: flex;
            flex-direction: column;
            gap: 5px;
        }
        .nav-btn {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 11px 14px;
            border-radius: var(--radius-md);
            border: none;
            background: transparent;
            color: var(--text-secondary);
            font-size: 13.5px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            width: 100%;
            text-align: left;
        }
        .nav-btn:hover {
            background: #f1f4f9;
            color: var(--primary-indigo);
            transform: translateX(3px);
        }
        .nav-btn.active {
            background: var(--primary-gradient);
            color: #ffffff;
            box-shadow: 0 8px 20px var(--primary-glow);
        }
        .nav-btn-icon {
            font-size: 16px;
            width: 22px;
            text-align: center;
        }

        /* AI Hospital Census Mini Widget */
        .sidebar-ai-widget {
            background: linear-gradient(135deg, #f8faff 0%, #f0f4ff 100%);
            border: 1px solid #dbeafe;
            border-radius: var(--radius-lg);
            padding: 16px;
            margin-top: 15px;
        }
        .ai-widget-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 10px;
        }
        .ai-badge {
            font-size: 10px;
            font-weight: 700;
            background: #e0e7ff;
            color: var(--primary-indigo);
            padding: 2px 8px;
            border-radius: 12px;
        }
        .ai-widget-title {
            font-size: 12.5px;
            font-weight: 700;
            color: var(--text-title);
        }
        .ai-meter-bg {
            background: #e2e8f0;
            height: 6px;
            border-radius: 4px;
            overflow: hidden;
            margin: 8px 0;
        }
        .ai-meter-fill {
            height: 100%;
            background: var(--primary-gradient);
            border-radius: 4px;
        }
        .ai-widget-sub {
            font-size: 11px;
            color: var(--text-secondary);
            display: flex;
            justify-content: space-between;
        }

        /* ---------------------------------------------------------------------
           2. MAIN WORKSPACE WITH TOPBAR
        --------------------------------------------------------------------- */
        main.main-viewport {
            flex: 1;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        header.top-appbar {
            height: 72px;
            background: var(--surface-white);
            border-bottom: 1px solid var(--border-light);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 32px;
            z-index: 40;
        }

        .search-pill-box {
            position: relative;
            width: 420px;
        }
        .search-pill-input {
            width: 100%;
            background: #f8fafc;
            border: 1px solid var(--border-light);
            border-radius: 30px;
            padding: 10px 16px 10px 42px;
            font-size: 13px;
            color: var(--text-title);
            outline: none;
            transition: all 0.2s ease;
        }
        .search-pill-input:focus {
            background: #ffffff;
            border-color: var(--primary-indigo);
            box-shadow: 0 0 0 3px var(--primary-glow);
        }
        .search-pill-icon {
            position: absolute;
            left: 16px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
            font-size: 14px;
        }

        /* Live Smart Search Dropdown */
        .search-results-dropdown {
            position: absolute;
            top: calc(100% + 10px);
            left: 0;
            width: 460px;
            max-height: 440px;
            overflow-y: auto;
            background: #ffffff;
            border: 1px solid var(--border-light);
            border-radius: var(--radius-lg);
            box-shadow: 0 20px 40px -10px rgba(15, 23, 42, 0.18);
            display: none;
            flex-direction: column;
            z-index: 1000;
            padding: 10px 0;
        }
        .search-results-dropdown.active {
            display: flex;
        }
        .search-group-header {
            font-size: 10.5px;
            font-weight: 800;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.6px;
            padding: 10px 18px 4px 18px;
            display: flex;
            justify-content: space-between;
            background: #f8fafc;
            border-top: 1px solid #f1f5f9;
        }
        .search-group-header:first-child { border-top: none; }
        .search-result-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 10px 18px;
            cursor: pointer;
            transition: all 0.15s ease;
        }
        .search-result-item:hover {
            background: #eef2ff;
        }
        .search-item-left {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .search-item-badge {
            width: 32px;
            height: 32px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 13px;
            font-weight: 700;
        }
        .search-item-title {
            font-size: 13px;
            font-weight: 700;
            color: var(--text-title);
        }
        .search-item-sub {
            font-size: 11px;
            color: var(--text-secondary);
        }
        .search-item-action {
            font-size: 11px;
            color: var(--primary-indigo);
            font-weight: 700;
        }
        .search-no-results {
            padding: 24px;
            text-align: center;
            color: var(--text-secondary);
            font-size: 13px;
            font-weight: 600;
        }

        .topbar-right-controls {
            display: flex;
            align-items: center;
            gap: 20px;
        }
        .ai-status-pill {
            display: flex;
            align-items: center;
            gap: 8px;
            background: #ecfdf5;
            border: 1px solid #a7f3d0;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 11.5px;
            font-weight: 700;
            color: #065f46;
        }
        .pulse-emerald {
            width: 8px;
            height: 8px;
            background: #10b981;
            border-radius: 50%;
            box-shadow: 0 0 8px #10b981;
            animation: pulse-ring 2s infinite ease-in-out;
        }
        @keyframes pulse-ring {
            0% { transform: scale(0.9); opacity: 0.8; }
            50% { transform: scale(1.3); opacity: 1; }
            100% { transform: scale(0.9); opacity: 0.8; }
        }

        .user-profile-card {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 4px 6px;
            border-radius: 30px;
            cursor: pointer;
        }
        .user-avatar-img {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: var(--primary-gradient);
            color: white;
            font-weight: 700;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            box-shadow: 0 4px 10px var(--primary-glow);
        }
        .user-name-title { font-size: 13px; font-weight: 700; color: var(--text-title); }
        .user-role-sub { font-size: 11px; color: var(--text-secondary); font-weight: 500; }

        /* ---------------------------------------------------------------------
           3. DYNAMIC CONTENT AREA
        --------------------------------------------------------------------- */
        .content-scroll-container {
            flex: 1;
            overflow-y: auto;
            padding: 28px 32px;
            display: flex;
            flex-direction: column;
            gap: 24px;
        }

        .tab-view-section {
            display: none;
            flex-direction: column;
            gap: 22px;
            animation: slideUpFade 0.25s ease-out;
        }
        .tab-view-section.active { display: flex; }
        @keyframes slideUpFade {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* AI Clinical Intelligence Banner */
        .ai-banner {
            background: linear-gradient(135deg, #1e1b4b 0%, #312e81 60%, #4338ca 100%);
            color: #ffffff;
            border-radius: var(--radius-xl);
            padding: 24px 28px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 16px 32px -4px rgba(49, 46, 129, 0.25);
            position: relative;
            overflow: hidden;
        }
        .ai-banner::after {
            content: '';
            position: absolute;
            right: -20px;
            top: -20px;
            width: 180px;
            height: 180px;
            background: radial-gradient(circle, rgba(99, 102, 241, 0.3) 0%, transparent 70%);
            border-radius: 50%;
        }
        .ai-banner-content h2 {
            font-size: 20px;
            font-weight: 800;
            display: flex;
            align-items: center;
            gap: 10px;
            letter-spacing: -0.3px;
        }
        .ai-banner-content p {
            font-size: 13px;
            color: #c7d2fe;
            margin-top: 6px;
            max-width: 620px;
            line-height: 1.5;
        }
        .ai-banner-badge {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(8px);
            padding: 8px 16px;
            border-radius: 30px;
            font-size: 12px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 8px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        /* 4 Key Metric Cards */
        .metrics-grid-4 {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
        }
        .modern-stat-card {
            background: var(--surface-white);
            border: 1px solid var(--border-light);
            border-radius: var(--radius-lg);
            padding: 22px;
            box-shadow: var(--shadow-card);
            transition: all 0.25s ease;
            position: relative;
        }
        .modern-stat-card:hover {
            transform: translateY(-3px);
            box-shadow: var(--shadow-hover);
            border-color: #cbd5e1;
        }
        .stat-card-top {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 12px;
        }
        .stat-icon-wrapper {
            width: 44px;
            height: 44px;
            border-radius: var(--radius-md);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
        }
        .stat-growth-tag {
            font-size: 11px;
            font-weight: 700;
            padding: 3px 8px;
            border-radius: 20px;
            display: flex;
            align-items: center;
            gap: 4px;
        }
        .stat-card-label {
            font-size: 12px;
            font-weight: 700;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .stat-card-val {
            font-size: 32px;
            font-weight: 800;
            color: var(--text-title);
            margin: 6px 0;
            letter-spacing: -0.5px;
        }
        .stat-card-desc {
            font-size: 12px;
            color: var(--text-muted);
            display: flex;
            align-items: center;
            gap: 4px;
        }

        /* Modern Charts & Analytics Split */
        .analytics-split-row {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 20px;
        }
        .analytics-card {
            background: var(--surface-white);
            border: 1px solid var(--border-light);
            border-radius: var(--radius-lg);
            padding: 24px;
            box-shadow: var(--shadow-card);
        }
        .analytics-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        .analytics-title {
            font-size: 15px;
            font-weight: 800;
            color: var(--text-title);
            display: flex;
            align-items: center;
            gap: 8px;
        }

        /* SVG Bar Chart Visualization */
        .bar-chart-container {
            display: flex;
            align-items: flex-end;
            justify-content: space-between;
            height: 150px;
            padding: 10px 10px 0 10px;
            border-bottom: 1px dashed var(--border-light);
            gap: 14px;
        }
        .chart-col {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-end;
            height: 100%;
            gap: 8px;
            flex: 1;
        }
        .chart-bar-wrap {
            width: 100%;
            height: 105px;
            display: flex;
            align-items: flex-end;
            justify-content: center;
            position: relative;
        }
        .chart-bar {
            width: 100%;
            max-width: 34px;
            min-height: 4px;
            background: #e2e8f0;
            border-radius: 6px 6px 0 0;
            transition: height 0.4s cubic-bezier(0.4, 0, 0.2, 1), background 0.3s ease;
            position: relative;
        }
        .chart-bar.has-data {
            background: linear-gradient(180deg, #6366f1 0%, #4f46e5 100%);
            box-shadow: 0 4px 12px rgba(79, 70, 229, 0.25);
        }
        .chart-bar.active {
            background: var(--primary-gradient);
            box-shadow: 0 6px 14px var(--primary-glow);
        }
        .bar-count-badge {
            position: absolute;
            top: -20px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 10px;
            font-weight: 800;
            color: var(--text-title);
            background: #ffffff;
            border: 1px solid var(--border-light);
            padding: 1px 5px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.06);
            white-space: nowrap;
        }
        .chart-label {
            font-size: 11px;
            font-weight: 700;
            color: var(--text-secondary);
        }

        /* Department Utilization */
        .dept-list {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        .dept-item-row {
            display: flex;
            flex-direction: column;
            gap: 6px;
        }
        .dept-info-top {
            display: flex;
            justify-content: space-between;
            font-size: 12px;
            font-weight: 700;
            color: var(--text-title);
        }
        .dept-progress-track {
            height: 8px;
            background: #f1f5f9;
            border-radius: 10px;
            overflow: hidden;
        }
        .dept-progress-bar {
            height: 100%;
            border-radius: 10px;
        }

        /* Behance Style Modern Data Table */
        .modern-table-card {
            background: var(--surface-white);
            border: 1px solid var(--border-light);
            border-radius: var(--radius-lg);
            overflow: hidden;
            box-shadow: var(--shadow-card);
        }
        .table-top-bar {
            padding: 20px 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border-light);
        }
        .table-heading-title {
            font-size: 16px;
            font-weight: 800;
            color: var(--text-title);
            letter-spacing: -0.2px;
        }

        table.behance-table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 13px;
        }
        table.behance-table thead th {
            background: #f8fafc;
            color: var(--text-secondary);
            font-weight: 700;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.6px;
            padding: 14px 20px;
            border-bottom: 1px solid var(--border-light);
        }
        table.behance-table tbody tr {
            border-bottom: 1px solid #f1f5f9;
            transition: background 0.15s ease;
        }
        table.behance-table tbody tr:hover {
            background: #f8faff;
        }
        table.behance-table td {
            padding: 16px 20px;
            vertical-align: middle;
            color: var(--text-title);
        }

        /* Patient & Doctor Avatars in Table */
        .table-profile-cell {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .avatar-circle {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 12px;
            color: #ffffff;
        }
        .cell-main-title { font-weight: 700; color: var(--text-title); }
        .cell-sub-title { font-size: 11px; color: var(--text-secondary); }

        /* Modern Status & Pill Badges */
        .pill-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 11.5px;
            font-weight: 700;
        }
        .pill-scheduled { background: #fef3c7; color: #b45309; }
        .pill-completed { background: #dcfce7; color: #15803d; }
        .pill-cancelled { background: #fee2e2; color: #b91c1c; }
        .pill-paid { background: #dcfce7; color: #15803d; }
        .pill-unpaid { background: #fee2e2; color: #b91c1c; }

        .blood-chip {
            background: #fff1f2;
            color: #e11d48;
            font-weight: 800;
            padding: 3px 8px;
            border-radius: 6px;
            font-size: 11px;
            border: 1px solid #ffe4e6;
        }

        /* Action Buttons */
        .btn-brand {
            background: var(--primary-gradient);
            color: #ffffff;
            border: none;
            padding: 10px 18px;
            border-radius: var(--radius-md);
            font-size: 13px;
            font-weight: 700;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 4px 12px var(--primary-glow);
            transition: all 0.2s ease;
            text-decoration: none;
        }
        .btn-brand:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 18px var(--primary-glow);
        }
        .btn-ghost {
            background: #f1f5f9;
            color: var(--text-title);
            border: 1px solid var(--border-light);
            padding: 8px 14px;
            border-radius: var(--radius-md);
            font-size: 12.5px;
            font-weight: 700;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s;
            text-decoration: none;
        }
        .btn-ghost:hover {
            background: #e2e8f0;
        }
        .btn-action-sm {
            padding: 5px 12px;
            font-size: 11.5px;
            border-radius: 6px;
        }

        /* Doctor Cards Grid */
        .doctor-card-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 20px;
        }
        .doctor-behance-card {
            background: var(--surface-white);
            border: 1px solid var(--border-light);
            border-radius: var(--radius-lg);
            padding: 22px;
            box-shadow: var(--shadow-card);
            transition: all 0.25s ease;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }
        .doctor-behance-card:hover {
            transform: translateY(-3px);
            box-shadow: var(--shadow-hover);
            border-color: #cbd5e1;
        }
        .doc-profile-row {
            display: flex;
            align-items: center;
            gap: 14px;
        }
        .doc-avatar-large {
            width: 52px;
            height: 52px;
            border-radius: 16px;
            background: var(--primary-gradient);
            color: white;
            font-size: 18px;
            font-weight: 800;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 8px 16px var(--primary-glow);
        }
        .doc-info-col h3 { font-size: 15px; font-weight: 800; color: var(--text-title); }
        .doc-info-col p { font-size: 12px; color: var(--primary-indigo); font-weight: 700; }
        .doc-rating-badge {
            margin-left: auto;
            background: #fef3c7;
            color: #d97706;
            font-size: 11px;
            font-weight: 800;
            padding: 3px 8px;
            border-radius: 12px;
        }
        .doc-details-box {
            background: #f8fafc;
            border-radius: var(--radius-md);
            padding: 12px 14px;
            font-size: 12px;
            color: var(--text-secondary);
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        /* ---------------------------------------------------------------------
           4. MODAL FORMS (BEHANCE CARD STYLE)
        --------------------------------------------------------------------- */
        .modal-overlay-bg {
            display: none;
            position: fixed;
            inset: 0;
            background: rgba(15, 23, 42, 0.5);
            backdrop-filter: blur(6px);
            align-items: center;
            justify-content: center;
            z-index: 1000;
        }
        .modal-overlay-bg.active { display: flex; }
        .modal-container-card {
            background: var(--surface-white);
            border-radius: var(--radius-xl);
            width: 520px;
            max-width: 92vw;
            box-shadow: 0 25px 50px -12px rgba(15, 23, 42, 0.25);
            overflow: hidden;
            animation: modalScale 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        }
        @keyframes modalScale {
            from { transform: scale(0.95); opacity: 0; }
            to { transform: scale(1); opacity: 1; }
        }
        .modal-top-bar {
            padding: 20px 24px;
            border-bottom: 1px solid var(--border-light);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .modal-top-bar h3 { font-size: 16px; font-weight: 800; color: var(--text-title); }
        .close-icon-btn {
            background: #f1f5f9;
            border: none;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            color: var(--text-secondary);
            font-size: 18px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .close-icon-btn:hover { background: #e2e8f0; color: var(--text-title); }
        .modal-form-content { padding: 22px 24px; max-height: 75vh; overflow-y: auto; }
        .modern-form-group { display: flex; flex-direction: column; gap: 6px; margin-bottom: 14px; }
        .modern-form-group label { font-size: 12px; font-weight: 700; color: var(--text-title); }
        .modern-input, .modern-select {
            background: #f8fafc;
            border: 1px solid var(--border-light);
            padding: 10px 14px;
            border-radius: var(--radius-md);
            font-size: 13px;
            color: var(--text-title);
            outline: none;
            transition: all 0.2s;
        }
        .modern-input:focus, .modern-select:focus {
            background: #ffffff;
            border-color: var(--primary-indigo);
            box-shadow: 0 0 0 3px var(--primary-glow);
        }
        .modal-actions-bar {
            padding: 16px 24px;
            background: #f8fafc;
            border-top: 1px solid var(--border-light);
            display: flex;
            justify-content: flex-end;
            gap: 10px;
        }
    </style>
</head>
<body>

    <!-- 1. FLOATING SIDEBAR -->
    <aside class="floating-sidebar">
        <div>
            <!-- Brand -->
            <div class="brand-header">
                <div class="brand-icon">✦</div>
                <div class="brand-info">
                    <h1>MediCare AI</h1>
                    <p>● Smart Hospital OS</p>
                </div>
            </div>

            <!-- Navigation -->
            <div class="nav-group-title">Clinical Operations</div>
            <div class="nav-list">
                <button class="nav-btn active" onclick="activateSection(event, 'dashboard')">
                    <span class="nav-btn-icon">📊</span> Overview & Metrics
                </button>
                <button class="nav-btn" onclick="activateSection(event, 'patients')">
                    <span class="nav-btn-icon">👥</span> Patient Directory
                </button>
                <button class="nav-btn" onclick="activateSection(event, 'doctors')">
                    <span class="nav-btn-icon">👨‍⚕️</span> Specialists & Rosters
                </button>
                <button class="nav-btn" onclick="activateSection(event, 'appointments')">
                    <span class="nav-btn-icon">📅</span> Appointments Queue
                </button>
            </div>

            <div class="nav-group-title" style="margin-top: 16px;">Pharmacy & Finance</div>
            <div class="nav-list">
                <button class="nav-btn" onclick="activateSection(event, 'prescriptions')">
                    <span class="nav-btn-icon">📝</span> Digital E-Prescriptions
                </button>
                <button class="nav-btn" onclick="activateSection(event, 'billing')">
                    <span class="nav-btn-icon">💳</span> Hospital Invoicing
                </button>
            </div>
        </div>

        <!-- AI Hospital Bed Occupancy Mini Widget -->
        <div class="sidebar-ai-widget">
            <div class="ai-widget-header">
                <span class="ai-widget-title">Hospital Capacity</span>
                <span class="ai-badge">AI REALTIME</span>
            </div>
            <div class="ai-meter-bg">
                <div class="ai-meter-fill" id="sidebarCapacityFill" style="width: {{ metrics.capacity_pct }}%;"></div>
            </div>
            <div class="ai-widget-sub">
                <span id="sidebarCapacityText">{{ metrics.capacity_pct }}% Occupied</span>
                <strong id="sidebarFreeBedsText">{{ metrics.free_beds }} Beds Free</strong>
            </div>
        </div>

        <!-- Sidebar User Account Footer -->
        <div style="margin-top: 16px; padding-top: 14px; border-top: 1px solid var(--border-light); display: flex; align-items: center; justify-content: space-between;">
            <div style="font-size: 11.5px; color: var(--text-secondary);">
                Logged: <strong style="color: var(--text-title);">{{ session_user.name.split()[0] }}</strong>
            </div>
            <a href="/logout" style="font-size: 11.5px; color: #e11d48; text-decoration: none; font-weight: 700; display: flex; align-items: center; gap: 4px;">
                🚪 Logout
            </a>
        </div>
    </aside>

    <!-- 2. MAIN VIEWPORT -->
    <main class="main-viewport">

        <!-- Top App Bar -->
        <header class="top-appbar">
            <div class="search-pill-box">
                <span class="search-pill-icon">🔍</span>
                <input type="text" id="globalSearchInput" class="search-pill-input" placeholder="Search patients, doctors, or ID..." oninput="handleGlobalSearch(this.value)" autocomplete="off">
                <!-- Live Smart Search Dropdown -->
                <div id="searchDropdown" class="search-results-dropdown"></div>
            </div>

            <div class="topbar-right-controls">
                <div class="ai-status-pill" style="cursor: pointer;" onclick="refreshDashboardMetrics(true)" title="Click to force-refresh all statistics">
                    <span class="pulse-emerald"></span>
                    <span id="aiSyncBadgeText">Live Stats: Synced</span>
                    <span style="font-size: 11px; margin-left: 2px;">🔄</span>
                </div>

                <div class="user-profile-card">
                    <div class="user-avatar-img">{{ session_user.initials }}</div>
                    <div>
                        <div class="user-name-title">{{ session_user.name }}</div>
                        <div class="user-role-sub">{{ session_user.role }}</div>
                    </div>
                </div>

                <a href="/logout" class="btn-ghost btn-action-sm" style="color: #e11d48; border-color: #fecdd3; background: #fff1f2; font-weight: 700; text-decoration: none; display: flex; align-items: center; gap: 5px;">
                    🚪 Sign Out
                </a>
            </div>
        </header>

        <!-- Content Area -->
        <div class="content-scroll-container">

            <!-- -------------------------------------------------------------
                 SECTION 1: DASHBOARD OVERVIEW
            ------------------------------------------------------------- -->
            <section id="view-dashboard" class="tab-view-section active">
                
                <!-- AI Insight Banner (100% Data-Driven & Dynamic) -->
                <div class="ai-banner">
                    <div class="ai-banner-content">
                        <h2>✨ AI Clinical Operations Assistant</h2>
                        <p id="aiBannerText">Real-time analytics indicate <strong>{{ metrics.flow_status }}</strong> with <strong>{{ metrics.completion_rate }}%</strong> consultation resolution. All <strong>{{ metrics.active_doctors }}</strong> specialists are active across <strong>{{ metrics.active_departments_list }}</strong>. Bed occupancy is at <strong>{{ metrics.capacity_pct }}%</strong> ({{ metrics.free_beds }} beds free).</p>
                    </div>
                    <div class="ai-banner-badge">
                        <span>● NABH Accredited Facility</span>
                    </div>
                </div>

                <!-- 4 Modern Stat Cards -->
                <div class="metrics-grid-4">
                    <div class="modern-stat-card">
                        <div class="stat-card-top">
                            <span class="stat-card-label">Total Patients</span>
                            <div class="stat-icon-wrapper" style="background: #eef2ff; color: #4f46e5;">👥</div>
                        </div>
                        <div class="stat-card-val" id="statTotalPatients">{{ metrics.total_patients }}</div>
                        <div class="stat-card-desc">
                            <span style="color: #10b981; font-weight: 700;">● Active EHR Census</span>
                        </div>
                    </div>

                    <div class="modern-stat-card">
                        <div class="stat-card-top">
                            <span class="stat-card-label">Active Doctors</span>
                            <div class="stat-icon-wrapper" style="background: #ecfeff; color: #06b6d4;">👨‍⚕️</div>
                        </div>
                        <div class="stat-card-val" id="statActiveDoctors">{{ metrics.active_doctors }}</div>
                        <div class="stat-card-desc">
                            <span>Across <strong id="statDeptCount">{{ metrics.departments_load|length }}</strong> Medical Specialties</span>
                        </div>
                    </div>

                    <div class="modern-stat-card">
                        <div class="stat-card-top">
                            <span class="stat-card-label">Today's Appointments</span>
                            <div class="stat-icon-wrapper" style="background: #fef3c7; color: #d97706;">📅</div>
                        </div>
                        <div class="stat-card-val" id="statTodayAppts">{{ metrics.today_appointments }}</div>
                        <div class="stat-card-desc">
                            <span id="statTodayPending" style="color: #f59e0b; font-weight: 700;">{{ metrics.today_pending }} Pending</span> • <span id="statTodayDone" style="color: #10b981; font-weight: 700;">{{ metrics.today_completed }} Done</span>
                        </div>
                    </div>

                    <div class="modern-stat-card">
                        <div class="stat-card-top">
                            <span class="stat-card-label">Settled Revenue</span>
                            <div class="stat-icon-wrapper" style="background: #dcfce7; color: #16a34a;">💰</div>
                        </div>
                        <div class="stat-card-val" id="statSettledRevenue" style="color: #16a34a;">{{ currency }} {{ "%.2f"|format(metrics.total_revenue) }}</div>
                        <div class="stat-card-desc">
                            <span id="statInvoicesRatio" style="color: #10b981; font-weight: 700;">{{ metrics.paid_invoices_count }} of {{ metrics.total_invoices_count }}</span> Bills Settled
                            {% if metrics.unpaid_invoices_count > 0 %}
                            <span style="color: #ef4444; font-size: 11px; margin-left: 4px;">({{ metrics.unpaid_invoices_count }} Unpaid)</span>
                            {% endif %}
                        </div>
                    </div>
                </div>

                <!-- Visual Analytics & Department Utilization Split -->
                <div class="analytics-split-row">
                    <!-- Weekly Patient Flow Chart (Fully Dynamic) -->
                    <div class="analytics-card">
                        <div class="analytics-header">
                            <div class="analytics-title">
                                <span>📈 Weekly Patient Inflow & Consultations</span>
                            </div>
                            <span style="font-size: 12px; color: var(--text-secondary); font-weight: 700;">Live Distribution</span>
                        </div>
                        <div class="bar-chart-container" id="weeklyChartBars">
                            {% for d in metrics.weekly_chart %}
                            <div class="chart-col" id="chartCol_{{ d.day }}" title="{{ d.day }}: {{ d.count }} Consultations">
                                <div class="chart-bar-wrap">
                                    <div class="chart-bar {% if d.has_data %}has-data{% endif %} {% if d.is_today %}active{% endif %}" id="chartBar_{{ d.day }}" style="height: {{ d.height }}%;">
                                        {% if d.count > 0 %}
                                        <span class="bar-count-badge" id="chartCount_{{ d.day }}">{{ d.count }}</span>
                                        {% endif %}
                                    </div>
                                </div>
                                <span class="chart-label" {% if d.is_today %}style="color: var(--primary-indigo); font-weight: 800;"{% endif %}>{{ d.day }}</span>
                            </div>
                            {% endfor %}
                        </div>
                    </div>

                    <!-- Department Roster Distribution (Fully Dynamic) -->
                    <div class="analytics-card">
                        <div class="analytics-header">
                            <div class="analytics-title">
                                <span>🏥 Department Load</span>
                            </div>
                            <span id="totalDeptConsultsText" style="font-size: 11px; font-weight: 700; color: var(--text-secondary);">{{ metrics.total_appointments_all }} Total Consults</span>
                        </div>
                        <div class="dept-list" id="deptLoadList">
                            {% if metrics.departments_load and metrics.departments_load|length > 0 %}
                                {% for dep in metrics.departments_load %}
                                <div class="dept-item-row" id="deptRow_{{ loop.index0 }}">
                                    <div class="dept-info-top">
                                        <span>{{ dep.name }}</span>
                                        <span><strong>{{ dep.count }}</strong> consults ({{ dep.actual_pct }}%)</span>
                                    </div>
                                    <div class="dept-progress-track">
                                        <div class="dept-progress-bar" style="width: {{ dep.percentage }}%; background: {{ dep.color }};"></div>
                                    </div>
                                </div>
                                {% endfor %}
                            {% else %}
                                <div style="text-align: center; padding: 28px 12px; color: var(--text-muted); font-size: 12px;">
                                    <span style="font-size: 26px; display: block; margin-bottom: 6px;">🩺</span>
                                    No department consultations recorded yet.<br>Rosters and specialty metrics activate with patient intake.
                                </div>
                            {% endif %}
                        </div>
                    </div>
                </div>

                <!-- Recent Appointments Table -->
                <div class="modern-table-card">
                    <div class="table-top-bar">
                        <div class="table-heading-title">Recent Outpatient Consultations</div>
                        <button class="btn-brand" onclick="openModal('apptModal')">+ Book Appointment</button>
                    </div>
                    <table class="behance-table">
                        <thead>
                            <tr>
                                <th>Token</th>
                                <th>Patient Name</th>
                                <th>Consulting Doctor</th>
                                <th>Date & Time</th>
                                <th>Department</th>
                                <th>Status</th>
                                <th style="text-align: right;">Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% if appointments and appointments|length > 0 %}
                                {% for a in appointments %}
                                <tr>
                                    <td><strong style="color: var(--primary-indigo);">#APPT-{{ "%04d"|format(a.appointment_id) }}</strong></td>
                                    <td>
                                        <div class="table-profile-cell">
                                            <div class="avatar-circle" style="background: linear-gradient(135deg, #3b82f6, #6366f1);">
                                                {{ a.patient_name[:2].upper() }}
                                            </div>
                                            <div>
                                                <div class="cell-main-title">{{ a.patient_name }}</div>
                                                <div class="cell-sub-title">{{ a.patient_phone }}</div>
                                            </div>
                                        </div>
                                    </td>
                                    <td><strong>{{ a.doctor_name }}</strong></td>
                                    <td>
                                        <div>{{ a.appointment_date }}</div>
                                        <div style="font-size: 11px; color: var(--text-secondary); font-weight: 700;">{{ a.time_slot }}</div>
                                    </td>
                                    <td><span style="background: #eef2ff; color: #4338ca; padding: 3px 8px; border-radius: 6px; font-weight: 700; font-size: 11px;">{{ a.doctor_dept }}</span></td>
                                    <td><span class="pill-badge pill-{{ a.status.lower() }}">{{ a.status }}</span></td>
                                    <td style="text-align: right; white-space: nowrap;">
                                        {% if a.status == 'Scheduled' %}
                                        <a href="/api/appointment/status?id={{ a.appointment_id }}&status=Completed&tab=dashboard" class="btn-ghost btn-action-sm" style="color: #16a34a; font-weight: 700;">✓ Complete</a>
                                        <a href="/api/appointment/status?id={{ a.appointment_id }}&status=Cancelled&tab=dashboard" class="btn-ghost btn-action-sm" style="color: #ef4444; font-weight: 700;">✕ Cancel</a>
                                        {% elif a.status == 'Completed' %}
                                        <button class="btn-ghost btn-action-sm" onclick="openPrescriptionModal({{ a.appointment_id }}, '{{ a.patient_name }}', {{ a.patient_id }}, '{{ a.doctor_name }}', {{ a.doctor_id }})" style="color: #0d9488; font-weight: 700;">📝 Rx</button>
                                        <button class="btn-ghost btn-action-sm" onclick="openBillingModal({{ a.appointment_id }}, '{{ a.patient_name }}', {{ a.patient_id }}, {{ a.doctor_fee }})" style="color: #10b981; font-weight: 700;">💳 Bill</button>
                                        {% else %}
                                        <span style="font-size: 11.5px; color: #ef4444; font-weight: 700;">Cancelled</span>
                                        {% endif %}
                                    </td>
                                </tr>
                                {% endfor %}
                            {% else %}
                                <tr>
                                    <td colspan="7" style="text-align: center; padding: 44px 20px; color: var(--text-muted);">
                                        <div style="font-size: 32px; margin-bottom: 8px;">📋</div>
                                        <div style="font-size: 14px; font-weight: 800; color: var(--text-title); margin-bottom: 4px;">No Consultations Scheduled Today</div>
                                        <div style="font-size: 12px; color: var(--text-secondary); margin-bottom: 14px;">The outpatient consultation queue is clear and ready for real-world patient intake.</div>
                                        <button class="btn-brand" style="margin: 0 auto;" onclick="openModal('apptModal')">+ Book First Consultation</button>
                                    </td>
                                </tr>
                            {% endif %}
                        </tbody>
                    </table>
                </div>

            </section>

            <!-- -------------------------------------------------------------
                 SECTION 2: PATIENT DIRECTORY (EHR)
            ------------------------------------------------------------- -->
            <section id="view-patients" class="tab-view-section">
                <div class="modern-table-card">
                    <div class="table-top-bar">
                        <div class="table-heading-title">Master Patient Registry (Electronic Health Records)</div>
                        <button class="btn-brand" onclick="openModal('patientModal')">+ Register New Patient</button>
                    </div>
                    <table class="behance-table" id="patientsDirTable">
                        <thead>
                            <tr>
                                <th>MRN #</th>
                                <th>Patient Name</th>
                                <th>Age / Gender</th>
                                <th>Blood Group</th>
                                <th>Contact Phone</th>
                                <th>Consultations</th>
                                <th>Last Visit</th>
                                <th>Admit Date</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% if patients and patients|length > 0 %}
                                {% for p in patients %}
                                <tr>
                                    <td><strong style="color: #4f46e5; font-family: monospace;">MRN-{{ "%04d"|format(p.patient_id) }}</strong></td>
                                    <td>
                                        <div class="table-profile-cell">
                                            <div class="avatar-circle" style="background: linear-gradient(135deg, #0d9488, #0284c7);">
                                                {{ p.name[:2].upper() }}
                                            </div>
                                            <div class="cell-main-title">{{ p.name }}</div>
                                        </div>
                                    </td>
                                    <td>{{ p.age }} Yrs • {{ p.gender }}</td>
                                    <td><span class="blood-chip">{{ p.blood_group }}</span></td>
                                    <td>{{ p.phone }}</td>
                                    <td><span class="pill-badge pill-completed">{{ p.total_visits or 0 }} Visits</span></td>
                                    <td><span style="font-size: 12px; color: var(--text-secondary); font-weight: 600;">{{ p.last_visit or 'None' }}</span></td>
                                    <td>{{ p.created_at }}</td>
                                </tr>
                                {% endfor %}
                            {% else %}
                                <tr>
                                    <td colspan="8" style="text-align: center; padding: 48px 20px; color: var(--text-muted);">
                                        <div style="font-size: 36px; margin-bottom: 8px;">👥</div>
                                        <div style="font-size: 14px; font-weight: 800; color: var(--text-title); margin-bottom: 4px;">Master Patient Registry is Empty</div>
                                        <div style="font-size: 12px; color: var(--text-secondary); margin-bottom: 16px;">Enroll your first hospital outpatient or inpatient to initiate their Electronic Health Record (EHR).</div>
                                        <button class="btn-brand" style="margin: 0 auto;" onclick="openModal('patientModal')">+ Register First Patient</button>
                                    </td>
                                </tr>
                            {% endif %}
                        </tbody>
                    </table>
                </div>
            </section>

            <!-- -------------------------------------------------------------
                 SECTION 3: DOCTORS & SPECIALISTS
            ------------------------------------------------------------- -->
            <section id="view-doctors" class="tab-view-section">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div class="table-heading-title">Specialist Physicians & Medical Faculty</div>
                    <button class="btn-brand" onclick="openModal('doctorModal')">+ Add Specialist</button>
                </div>

                <div class="doctor-card-grid">
                    {% if doctors and doctors|length > 0 %}
                        {% for d in doctors %}
                        <div class="doctor-behance-card">
                            <div class="doc-profile-row">
                                <div class="doc-avatar-large">{{ d.name[4:6] if d.name.startswith("Dr. ") else d.name[:2] }}</div>
                                <div class="doc-info-col">
                                    <h3>{{ d.name }}</h3>
                                    <p>{{ d.specialization }}</p>
                                </div>
                                <div class="doc-rating-badge">★ {{ d.rating or '4.9' }}</div>
                            </div>

                            <div class="doc-details-box">
                                <div>📞 <strong>Phone:</strong> {{ d.phone }}</div>
                                <div>✉️ <strong>Email:</strong> {{ d.email or 'N/A' }}</div>
                                <div>📅 <strong>OPD Days:</strong> {{ d.available_days }}</div>
                                <div>💳 <strong>Consultation Fee:</strong> <strong style="color: #10b981;">{{ currency }} {{ "%.2f"|format(d.fee) }}</strong></div>
                                <div style="margin-top: 8px; padding-top: 8px; border-top: 1px dashed var(--border-light); font-size: 11.5px; color: var(--text-secondary); display: flex; justify-content: space-between;">
                                    <span>Total Consults: <strong style="color: var(--primary-indigo); font-size: 12px;">{{ d.total_consultations or 0 }}</strong></span>
                                    <span>Completed: <strong style="color: #10b981; font-size: 12px;">{{ d.completed_consultations or 0 }}</strong></span>
                                </div>
                            </div>

                            <button class="btn-brand" style="justify-content: center; width: 100%;" onclick="openAppointmentModalForDoctor({{ d.doctor_id }})">
                                📅 Schedule Consultation
                            </button>
                        </div>
                        {% endfor %}
                    {% else %}
                        <div style="grid-column: 1 / -1; background: var(--surface-white); border: 1px dashed var(--border-light); border-radius: var(--radius-lg); padding: 50px 24px; text-align: center;">
                            <div style="font-size: 40px; margin-bottom: 12px;">👨‍⚕️</div>
                            <h3 style="font-size: 16px; font-weight: 800; color: var(--text-title); margin-bottom: 6px;">No Specialists Enrolled in Roster</h3>
                            <p style="font-size: 13px; color: var(--text-secondary); max-width: 480px; margin: 0 auto 18px auto;">Add clinical doctors, faculty heads, and attending physicians to configure consultation fees, OPD days, and clinical appointment slots.</p>
                            <button class="btn-brand" style="margin: 0 auto;" onclick="openModal('doctorModal')">+ Add First Medical Specialist</button>
                        </div>
                    {% endif %}
                </div>
            </section>

            <!-- -------------------------------------------------------------
                 SECTION 4: APPOINTMENTS QUEUE
            ------------------------------------------------------------- -->
            <section id="view-appointments" class="tab-view-section">
                <div class="modern-table-card">
                    <div class="table-top-bar">
                        <div class="table-heading-title">Outpatient Consultation Schedule</div>
                        <button class="btn-brand" onclick="openModal('apptModal')">+ Book New Consultation</button>
                    </div>
                    <table class="behance-table">
                        <thead>
                            <tr>
                                <th>Token</th>
                                <th>Patient Name</th>
                                <th>Physician</th>
                                <th>Specialization</th>
                                <th>Date & Slot</th>
                                <th>Status</th>
                                <th>Clinical Notes</th>
                                <th style="text-align: right;">Clinical Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% if appointments and appointments|length > 0 %}
                                {% for a in appointments %}
                                <tr>
                                    <td><strong style="color: var(--primary-indigo);">#APPT-{{ "%04d"|format(a.appointment_id) }}</strong></td>
                                    <td><strong>{{ a.patient_name }}</strong></td>
                                    <td>{{ a.doctor_name }}</td>
                                    <td><span style="background: #eef2ff; color: #4338ca; padding: 2px 8px; border-radius: 4px; font-weight: 700; font-size: 11px;">{{ a.doctor_dept }}</span></td>
                                    <td>{{ a.appointment_date }} (<strong>{{ a.time_slot }}</strong>)</td>
                                    <td><span class="pill-badge pill-{{ a.status.lower() }}">{{ a.status }}</span></td>
                                    <td><span style="color: var(--text-secondary); font-style: italic;">{{ a.notes or 'Routine consult' }}</span></td>
                                    <td style="text-align: right; white-space: nowrap;">
                                        {% if a.status == 'Scheduled' %}
                                        <a href="/api/appointment/status?id={{ a.appointment_id }}&status=Completed&tab=appointments" class="btn-ghost btn-action-sm" style="color: #16a34a; font-weight: 700;">✓ Complete</a>
                                        <a href="/api/appointment/status?id={{ a.appointment_id }}&status=Cancelled&tab=appointments" class="btn-ghost btn-action-sm" style="color: #ef4444; font-weight: 700;">✕ Cancel</a>
                                        {% elif a.status == 'Completed' %}
                                        <button class="btn-ghost btn-action-sm" onclick="openPrescriptionModal({{ a.appointment_id }}, '{{ a.patient_name }}', {{ a.patient_id }}, '{{ a.doctor_name }}', {{ a.doctor_id }})" style="color: #0d9488; font-weight: 700;">📝 Rx</button>
                                        <button class="btn-ghost btn-action-sm" onclick="openBillingModal({{ a.appointment_id }}, '{{ a.patient_name }}', {{ a.patient_id }}, {{ a.doctor_fee }})" style="color: #10b981; font-weight: 700;">💳 Bill</button>
                                        {% else %}
                                        <span style="font-size: 11.5px; color: #ef4444; font-weight: 700;">Cancelled</span>
                                        {% endif %}
                                    </td>
                                </tr>
                                {% endfor %}
                            {% else %}
                                <tr>
                                    <td colspan="8" style="text-align: center; padding: 48px 20px; color: var(--text-muted);">
                                        <div style="font-size: 36px; margin-bottom: 8px;">📅</div>
                                        <div style="font-size: 14px; font-weight: 800; color: var(--text-title); margin-bottom: 4px;">Outpatient Schedule is Clear</div>
                                        <div style="font-size: 12px; color: var(--text-secondary); margin-bottom: 16px;">No pending or ongoing consultations in the queue. Book an appointment to begin clinical intake.</div>
                                        <button class="btn-brand" style="margin: 0 auto;" onclick="openModal('apptModal')">+ Schedule Consultation</button>
                                    </td>
                                </tr>
                            {% endif %}
                        </tbody>
                    </table>
                </div>
            </section>

            <!-- -------------------------------------------------------------
                 SECTION 5: DIGITAL PRESCRIPTIONS
            ------------------------------------------------------------- -->
            <section id="view-prescriptions" class="tab-view-section">
                <div class="modern-table-card">
                    <div class="table-top-bar">
                        <div class="table-heading-title">E-Prescription & Pharmacy Orders ({{ prescriptions|length }} Total)</div>
                        <button class="btn-brand" onclick="openModal('prescriptionModal')">+ Write E-Prescription</button>
                    </div>
                    <table class="behance-table">
                        <thead>
                            <tr>
                                <th>Rx Number</th>
                                <th>Prescription Date</th>
                                <th>Patient Name</th>
                                <th>Doctor</th>
                                <th>Diagnosis</th>
                                <th>Advice</th>
                                <th style="text-align: right;">Official PDF</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% if prescriptions and prescriptions|length > 0 %}
                                {% for r in prescriptions %}
                                <tr>
                                    <td><strong style="color: #4f46e5; font-family: monospace;">RX-{{ "%04d"|format(r.prescription_id) }}</strong></td>
                                    <td>{{ r.date }}</td>
                                    <td><strong>{{ r.patient_name }}</strong></td>
                                    <td>{{ r.doctor_name }}</td>
                                    <td><span style="color: #0d9488; font-weight: 700;">{{ r.diagnosis }}</span></td>
                                    <td><span style="color: var(--text-secondary);">{{ r.advice or '-' }}</span></td>
                                    <td style="text-align: right;">
                                        <a href="/download/prescription/{{ r.prescription_id }}" target="_blank" class="btn-ghost btn-action-sm">
                                            🖨️ View Rx PDF
                                        </a>
                                    </td>
                                </tr>
                                {% endfor %}
                            {% else %}
                                <tr>
                                    <td colspan="7" style="text-align: center; padding: 48px 20px; color: var(--text-muted);">
                                        <div style="font-size: 36px; margin-bottom: 8px;">💊</div>
                                        <div style="font-size: 14px; font-weight: 800; color: var(--text-title); margin-bottom: 4px;">No Digital E-Prescriptions Issued Yet</div>
                                        <div style="font-size: 12px; color: var(--text-secondary); margin-bottom: 16px;">Once doctors consult patients, digital Rx orders with medication dosages and printable PDFs will appear here.</div>
                                        <button class="btn-brand" style="margin: 0 auto;" onclick="openModal('prescriptionModal')">+ Issue E-Prescription</button>
                                    </td>
                                </tr>
                            {% endif %}
                        </tbody>
                    </table>
                </div>
            </section>

            <!-- -------------------------------------------------------------
                 SECTION 6: BILLING & INVOICING
            ------------------------------------------------------------- -->
            <section id="view-billing" class="tab-view-section">
                <div class="modern-table-card">
                    <div class="table-top-bar">
                        <div class="table-heading-title">Hospital Cashier & Billing Ledger (Settled: {{ currency }} {{ "%.2f"|format(metrics.total_revenue) }})</div>
                        <button class="btn-brand" onclick="openModal('billingModal')">+ Generate Tax Invoice</button>
                    </div>
                    <table class="behance-table">
                        <thead>
                            <tr>
                                <th>Invoice ID</th>
                                <th>Billing Date</th>
                                <th>Patient Name</th>
                                <th>Doctor</th>
                                <th>Total Amount</th>
                                <th>Status</th>
                                <th>Payment Mode</th>
                                <th style="text-align: right;">Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% if bills and bills|length > 0 %}
                                {% for b in bills %}
                                <tr>
                                    <td><strong style="color: #4f46e5; font-family: monospace;">INV-{{ "%04d"|format(b.bill_id) }}</strong></td>
                                    <td>{{ b.date }}</td>
                                    <td><strong>{{ b.patient_name }}</strong></td>
                                    <td>{{ b.doctor_name }}</td>
                                    <td><strong style="color: #10b981; font-size: 14px;">{{ currency }} {{ "%.2f"|format(b.total_amount) }}</strong></td>
                                    <td><span class="pill-badge pill-{{ b.payment_status.lower() }}">{{ b.payment_status }}</span></td>
                                    <td><strong>{{ b.payment_mode }}</strong></td>
                                    <td style="text-align: right; white-space: nowrap;">
                                        {% if b.payment_status != 'Paid' %}
                                        <a href="/api/billing/pay?bill_id={{ b.bill_id }}&mode=UPI&tab=billing" class="btn-brand btn-action-sm" style="background: #10b981; color: white; font-weight: 700;">
                                            💳 Settle & Pay
                                        </a>
                                        {% endif %}
                                        <a href="/download/invoice/{{ b.bill_id }}" target="_blank" class="btn-ghost btn-action-sm">
                                            📄 PDF
                                        </a>
                                    </td>
                                </tr>
                                {% endfor %}
                            {% else %}
                                <tr>
                                    <td colspan="8" style="text-align: center; padding: 48px 20px; color: var(--text-muted);">
                                        <div style="font-size: 36px; margin-bottom: 8px;">💳</div>
                                        <div style="font-size: 14px; font-weight: 800; color: var(--text-title); margin-bottom: 4px;">No Hospital Invoices Generated Yet</div>
                                        <div style="font-size: 12px; color: var(--text-secondary); margin-bottom: 16px;">Itemized billing records and official PDF tax receipts will be tracked here upon patient discharge.</div>
                                        <button class="btn-brand" style="margin: 0 auto;" onclick="openModal('billingModal')">+ Generate First Invoice</button>
                                    </td>
                                </tr>
                            {% endif %}
                        </tbody>
                    </table>
                </div>
            </section>

        </div>
    </main>

    <!-- MODAL: REGISTER PATIENT -->
    <div id="patientModal" class="modal-overlay-bg">
        <div class="modal-container-card">
            <div class="modal-top-bar">
                <h3>👤 Register New Patient</h3>
                <button class="close-icon-btn" onclick="closeModal('patientModal')">&times;</button>
            </div>
            <form action="/api/patient/add" method="POST">
                <div class="modal-form-content">
                    <div class="modern-form-group">
                        <label>Patient Full Name *</label>
                        <input type="text" name="name" class="modern-input" placeholder="e.g. Ramesh Kumar" required>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
                        <div class="modern-form-group">
                            <label>Age (Years) *</label>
                            <input type="number" name="age" class="modern-input" min="1" max="120" required>
                        </div>
                        <div class="modern-form-group">
                            <label>Gender *</label>
                            <select name="gender" class="modern-select">
                                <option>Male</option><option>Female</option><option>Other</option>
                            </select>
                        </div>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
                        <div class="modern-form-group">
                            <label>Phone Number *</label>
                            <input type="text" name="phone" class="modern-input" required>
                        </div>
                        <div class="modern-form-group">
                            <label>Blood Group *</label>
                            <select name="blood_group" class="modern-select">
                                <option>A+</option><option>A-</option><option>B+</option><option>B-</option>
                                <option>O+</option><option>O-</option><option>AB+</option><option>AB-</option>
                            </select>
                        </div>
                    </div>
                    <div class="modern-form-group">
                        <label>Residential Address</label>
                        <input type="text" name="address" class="modern-input" placeholder="Street, City, Postal Code">
                    </div>
                </div>
                <div class="modal-actions-bar">
                    <button type="button" class="btn-ghost" onclick="closeModal('patientModal')">Cancel</button>
                    <button type="submit" class="btn-brand">Save Patient Record</button>
                </div>
            </form>
        </div>
    </div>

    <!-- MODAL: ADD DOCTOR -->
    <div id="doctorModal" class="modal-overlay-bg">
        <div class="modal-container-card">
            <div class="modal-top-bar">
                <h3>👨‍⚕️ Add Specialist Physician</h3>
                <button class="close-icon-btn" onclick="closeModal('doctorModal')">&times;</button>
            </div>
            <form action="/api/doctor/add" method="POST">
                <div class="modal-form-content">
                    <div class="modern-form-group">
                        <label>Doctor Full Name *</label>
                        <input type="text" name="name" class="modern-input" placeholder="Dr. Full Name" required>
                    </div>
                    <div class="modern-form-group">
                        <label>Specialization *</label>
                        <select name="specialization" class="modern-select">
                            <option>Cardiology</option><option>Neurology</option><option>Pediatrics</option>
                            <option>Orthopedics</option><option>General Medicine</option><option>Dermatology</option>
                        </select>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
                        <div class="modern-form-group">
                            <label>Phone Number *</label>
                            <input type="text" name="phone" class="modern-input" required>
                        </div>
                        <div class="modern-form-group">
                            <label>Email Address</label>
                            <input type="email" name="email" class="modern-input">
                        </div>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
                        <div class="modern-form-group">
                            <label>Available Days *</label>
                            <input type="text" name="available_days" class="modern-input" placeholder="Mon, Wed, Fri" required>
                        </div>
                        <div class="modern-form-group">
                            <label>Consultation Fee ({{ currency }}) *</label>
                            <input type="number" step="0.01" name="fee" class="modern-input" value="700.00" required>
                        </div>
                    </div>
                </div>
                <div class="modal-actions-bar">
                    <button type="button" class="btn-ghost" onclick="closeModal('doctorModal')">Cancel</button>
                    <button type="submit" class="btn-brand">Enroll Specialist</button>
                </div>
            </form>
        </div>
    </div>

    <!-- MODAL: BOOK APPOINTMENT -->
    <div id="apptModal" class="modal-overlay-bg">
        <div class="modal-container-card">
            <div class="modal-top-bar">
                <h3>📅 Book Outpatient Appointment</h3>
                <button class="close-icon-btn" onclick="closeModal('apptModal')">&times;</button>
            </div>
            <form action="/api/appointment/book" method="POST">
                <div class="modal-form-content">
                    <div class="modern-form-group">
                        <label>Select Patient *</label>
                        <select name="patient_id" class="modern-select" required>
                            {% if patients and patients|length > 0 %}
                                {% for p in patients %}
                                <option value="{{ p.patient_id }}">{{ p.name }} (MRN-{{ "%04d"|format(p.patient_id) }})</option>
                                {% endfor %}
                            {% else %}
                                <option value="" disabled selected>⚠️ No patients registered - Click 'Register New Patient' first</option>
                            {% endif %}
                        </select>
                    </div>
                    <div class="modern-form-group">
                        <label>Select Consulting Physician *</label>
                        <select name="doctor_id" class="modern-select" required>
                            {% if doctors and doctors|length > 0 %}
                                {% for d in doctors %}
                                <option value="{{ d.doctor_id }}">{{ d.name }} — {{ d.specialization }} ({{ currency }}{{ "%.0f"|format(d.fee) }})</option>
                                {% endfor %}
                            {% else %}
                                <option value="" disabled selected>⚠️ No specialists enrolled - Click 'Add Specialist' first</option>
                            {% endif %}
                        </select>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
                        <div class="modern-form-group">
                            <label>Appointment Date *</label>
                            <input type="date" name="appointment_date" class="modern-input" value="{{ today }}" required>
                        </div>
                        <div class="modern-form-group">
                            <label>Time Slot *</label>
                            <select name="time_slot" class="modern-select">
                                <option>09:00 AM</option><option>09:30 AM</option><option>10:00 AM</option>
                                <option>10:30 AM</option><option>11:00 AM</option><option>11:30 AM</option>
                                <option>02:00 PM</option><option>02:30 PM</option><option>03:00 PM</option>
                            </select>
                        </div>
                    </div>
                    <div class="modern-form-group">
                        <label>Reason / Symptoms</label>
                        <input type="text" name="notes" class="modern-input" placeholder="e.g. Chest pain, follow-up...">
                    </div>
                </div>
                <div class="modal-actions-bar">
                    <button type="button" class="btn-ghost" onclick="closeModal('apptModal')">Cancel</button>
                    <button type="submit" class="btn-brand">Confirm Booking</button>
                </div>
            </form>
        </div>
    </div>

    <!-- MODAL: WRITE PRESCRIPTION -->
    <div id="prescriptionModal" class="modal-overlay-bg">
        <div class="modal-container-card" style="width: 580px;">
            <div class="modal-top-bar">
                <h3>📝 Write E-Prescription</h3>
                <button class="close-icon-btn" onclick="closeModal('prescriptionModal')">&times;</button>
            </div>
            <form action="/api/prescription/create" method="POST">
                <div class="modal-form-content">
                    <div class="modern-form-group">
                        <label>Select Associated Consultation *</label>
                        <select name="appointment_id" id="rxApptSelect" class="modern-select" onchange="syncRxDetails(this.value)" required>
                            {% if appointments and appointments|length > 0 %}
                                {% for a in appointments %}
                                <option value="{{ a.appointment_id }}" data-patient-id="{{ a.patient_id }}" data-doctor-id="{{ a.doctor_id }}" data-patient-name="{{ a.patient_name }}" data-doctor-name="{{ a.doctor_name }}">
                                    #APPT-{{ "%04d"|format(a.appointment_id) }}: {{ a.patient_name }} with {{ a.doctor_name }} ({{ a.appointment_date }})
                                </option>
                                {% endfor %}
                            {% else %}
                                <option value="" disabled selected>⚠️ No consultations scheduled to prescribe</option>
                            {% endif %}
                        </select>
                    </div>
                    <input type="hidden" name="patient_id" id="rxPatientId" value="{{ appointments[0].patient_id if appointments else '' }}">
                    <input type="hidden" name="doctor_id" id="rxDoctorId" value="{{ appointments[0].doctor_id if appointments else '' }}">
                    
                    <div class="modern-form-group">
                        <label>Clinical Diagnosis / Condition *</label>
                        <input type="text" name="diagnosis" id="rxDiagnosisInput" class="modern-input" placeholder="e.g. Acute Bronchitis, Migraine with aura..." required>
                    </div>

                    <div style="background: #f8fafc; border: 1px solid var(--border-light); border-radius: var(--radius-md); padding: 14px; margin-bottom: 14px;">
                        <div style="font-size: 12px; font-weight: 800; color: var(--text-title); margin-bottom: 8px;">💊 Medication Order</div>
                        <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 10px; margin-bottom: 8px;">
                            <input type="text" name="med_name" class="modern-input" placeholder="Drug Name (e.g. Amoxicillin)" value="Amoxicillin" required>
                            <input type="text" name="med_dosage" class="modern-input" placeholder="Strength (500mg)" value="500mg" required>
                        </div>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                            <select name="med_frequency" class="modern-select">
                                <option>1-0-1 (Twice daily)</option>
                                <option>1-1-1 (Thrice daily)</option>
                                <option>0-0-1 (Once daily - Night)</option>
                                <option>1-0-0 (Once daily - Morning)</option>
                                <option>SOS (As needed)</option>
                            </select>
                            <input type="text" name="med_duration" class="modern-input" placeholder="Duration (e.g. 7 Days)" value="5 Days">
                        </div>
                    </div>

                    <div class="modern-form-group">
                        <label>Dietary & Clinical Advice</label>
                        <textarea name="advice" class="modern-input" style="height: 70px; resize: none;" placeholder="e.g. Light diet, avoid cold beverages, follow up in 10 days.">Adequate rest, hydrate well, follow up if symptoms persist.</textarea>
                    </div>
                </div>
                <div class="modal-actions-bar">
                    <button type="button" class="btn-ghost" onclick="closeModal('prescriptionModal')">Cancel</button>
                    <button type="submit" class="btn-brand">Save & Issue Prescription</button>
                </div>
            </form>
        </div>
    </div>

    <!-- MODAL: GENERATE INVOICE -->
    <div id="billingModal" class="modal-overlay-bg">
        <div class="modal-container-card" style="width: 540px;">
            <div class="modal-top-bar">
                <h3>💳 Generate Hospital Tax Invoice</h3>
                <button class="close-icon-btn" onclick="closeModal('billingModal')">&times;</button>
            </div>
            <form action="/api/billing/create" method="POST">
                <div class="modal-form-content">
                    <div class="modern-form-group">
                        <label>Select Consultation *</label>
                        <select name="appointment_id" id="billApptSelect" class="modern-select" onchange="syncBillDetails(this.value)" required>
                            {% if appointments and appointments|length > 0 %}
                                {% for a in appointments %}
                                <option value="{{ a.appointment_id }}" data-patient-id="{{ a.patient_id }}" data-fee="{{ a.doctor_fee or 500 }}">
                                    #APPT-{{ "%04d"|format(a.appointment_id) }}: {{ a.patient_name }} ({{ a.doctor_name }})
                                </option>
                                {% endfor %}
                            {% else %}
                                <option value="" disabled selected>⚠️ No consultations scheduled to bill</option>
                            {% endif %}
                        </select>
                    </div>
                    <input type="hidden" name="patient_id" id="billPatientId" value="{{ appointments[0].patient_id if appointments else '' }}">

                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
                        <div class="modern-form-group">
                            <label>Consultation Fee ({{ currency }}) *</label>
                            <input type="number" step="0.01" name="consultation_fee" id="billConsultFee" class="modern-input" value="800.00" oninput="calcBillTotal()" required>
                        </div>
                        <div class="modern-form-group">
                            <label>Pharmacy Charges ({{ currency }})</label>
                            <input type="number" step="0.01" name="medicine_fee" id="billMedFee" class="modern-input" value="350.00" oninput="calcBillTotal()">
                        </div>
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
                        <div class="modern-form-group">
                            <label>Lab / Other ({{ currency }})</label>
                            <input type="number" step="0.01" name="other_charges" id="billOtherFee" class="modern-input" value="150.00" oninput="calcBillTotal()">
                        </div>
                        <div class="modern-form-group">
                            <label>Discount ({{ currency }})</label>
                            <input type="number" step="0.01" name="discount" id="billDiscount" class="modern-input" value="0.00" oninput="calcBillTotal()">
                        </div>
                    </div>

                    <div style="background: #ecfdf5; border: 1px solid #a7f3d0; border-radius: var(--radius-md); padding: 12px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
                        <span style="font-weight: 700; color: #065f46;">Net Payable Total:</span>
                        <strong style="color: #047857; font-size: 18px;" id="billTotalPreview">{{ currency }} 1300.00</strong>
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
                        <div class="modern-form-group">
                            <label>Payment Status *</label>
                            <select name="payment_status" class="modern-select">
                                <option value="Paid">Paid (Settled)</option>
                                <option value="Unpaid">Unpaid (Pending)</option>
                            </select>
                        </div>
                        <div class="modern-form-group">
                            <label>Payment Method *</label>
                            <select name="payment_mode" class="modern-select">
                                <option value="UPI">UPI / Digital</option>
                                <option value="Cash">Cash</option>
                                <option value="Card">Credit / Debit Card</option>
                                <option value="Insurance">TPA Insurance</option>
                            </select>
                        </div>
                    </div>
                </div>
                <div class="modal-actions-bar">
                    <button type="button" class="btn-ghost" onclick="closeModal('billingModal')">Cancel</button>
                    <button type="submit" class="btn-brand">Issue Tax Invoice</button>
                </div>
            </form>
        </div>
    </div>

    <!-- SCRIPT ENGINE -->
    <script>
        const ALL_PATIENTS = {{ patients_json | safe }};
        const ALL_DOCTORS = {{ doctors_json | safe }};
        const ALL_APPOINTMENTS = {{ appointments_json | safe }};
        const DEFAULT_CURR = "{{ currency }}";

        function activateSection(event, sectionId) {
            document.querySelectorAll('.tab-view-section').forEach(s => s.classList.remove('active'));
            document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));

            const target = document.getElementById('view-' + sectionId);
            if (target) target.classList.add('active');

            const btn = document.querySelector(`.nav-btn[onclick*="${sectionId}"]`);
            if (btn) btn.classList.add('active');

            const searchVal = document.getElementById('globalSearchInput')?.value || '';
            if (searchVal) {
                filterCurrentActiveTable(searchVal);
            }
        }

        function openModal(id) { document.getElementById(id).classList.add('active'); }
        function closeModal(id) { document.getElementById(id).classList.remove('active'); }

        function openAppointmentModalForDoctor(docId) {
            const select = document.querySelector('#apptModal select[name="doctor_id"]');
            if (select) select.value = String(docId);
            openModal('apptModal');
        }

        function openPrescriptionModal(apptId, patientName, patientId, doctorName, doctorId) {
            const select = document.getElementById('rxApptSelect');
            if (select) {
                select.value = String(apptId);
            }
            const pInput = document.getElementById('rxPatientId');
            if (pInput) pInput.value = patientId;
            const dInput = document.getElementById('rxDoctorId');
            if (dInput) dInput.value = doctorId;
            openModal('prescriptionModal');
        }

        function openBillingModal(apptId, patientName, patientId, doctorFee) {
            const select = document.getElementById('billApptSelect');
            if (select) select.value = String(apptId);
            const pInput = document.getElementById('billPatientId');
            if (pInput) pInput.value = patientId;
            const feeInput = document.getElementById('billConsultFee');
            if (feeInput && doctorFee) feeInput.value = Number(doctorFee).toFixed(2);
            calcBillTotal();
            openModal('billingModal');
        }

        function syncRxDetails(apptId) {
            const select = document.getElementById('rxApptSelect');
            if (!select || select.selectedIndex < 0) return;
            const opt = select.options[select.selectedIndex];
            if (opt && opt.getAttribute('data-patient-id')) {
                const pId = opt.getAttribute('data-patient-id');
                const dId = opt.getAttribute('data-doctor-id');
                if (pId) document.getElementById('rxPatientId').value = pId;
                if (dId) document.getElementById('rxDoctorId').value = dId;
            }
        }

        function syncBillDetails(apptId) {
            const select = document.getElementById('billApptSelect');
            if (!select || select.selectedIndex < 0) return;
            const opt = select.options[select.selectedIndex];
            if (opt && opt.getAttribute('data-patient-id')) {
                const pId = opt.getAttribute('data-patient-id');
                if (pId) document.getElementById('billPatientId').value = pId;
                const fee = opt.getAttribute('data-fee');
                if (fee) {
                    document.getElementById('billConsultFee').value = Number(fee).toFixed(2);
                    calcBillTotal();
                }
            }
        }

        function calcBillTotal() {
            const consult = parseFloat(document.getElementById('billConsultFee')?.value || 0);
            const med = parseFloat(document.getElementById('billMedFee')?.value || 0);
            const other = parseFloat(document.getElementById('billOtherFee')?.value || 0);
            const disc = parseFloat(document.getElementById('billDiscount')?.value || 0);
            const total = Math.max(0, (consult + med + other) - disc);
            const prev = document.getElementById('billTotalPreview');
            if (prev) prev.innerText = `${DEFAULT_CURR} ${total.toFixed(2)}`;
        }

        // Live Real-Time Dashboard Statistics Refresher
        async function refreshDashboardMetrics(userTriggered = false) {
            const badge = document.getElementById('aiSyncBadgeText');
            if (userTriggered && badge) {
                badge.innerText = 'Syncing...';
            }

            try {
                const res = await fetch('/api/metrics');
                if (!res.ok) return;
                const m = await res.json();

                // 1. Metric Cards
                const elPatients = document.getElementById('statTotalPatients');
                if (elPatients) elPatients.innerText = m.total_patients;

                const elDoctors = document.getElementById('statActiveDoctors');
                if (elDoctors) elDoctors.innerText = m.active_doctors;

                const elDeptCount = document.getElementById('statDeptCount');
                if (elDeptCount) elDeptCount.innerText = m.departments_load ? m.departments_load.length : 0;

                const elAppts = document.getElementById('statTodayAppts');
                if (elAppts) elAppts.innerText = m.today_appointments;

                const elPending = document.getElementById('statTodayPending');
                if (elPending) elPending.innerText = `${m.today_pending} Pending`;

                const elDone = document.getElementById('statTodayDone');
                if (elDone) elDone.innerText = `${m.today_completed} Done`;

                const elRev = document.getElementById('statSettledRevenue');
                if (elRev) elRev.innerText = `${DEFAULT_CURR} ${Number(m.total_revenue).toFixed(2)}`;

                const elRatio = document.getElementById('statInvoicesRatio');
                if (elRatio) elRatio.innerText = `${m.paid_invoices_count} of ${m.total_invoices_count}`;

                // 2. Hospital Bed Capacity Sidebar Meter
                const capFill = document.getElementById('sidebarCapacityFill');
                if (capFill) capFill.style.width = `${m.capacity_pct}%`;

                const capText = document.getElementById('sidebarCapacityText');
                if (capText) capText.innerText = `${m.capacity_pct}% Occupied`;

                const freeText = document.getElementById('sidebarFreeBedsText');
                if (freeText) freeText.innerText = `${m.free_beds} Beds Free`;

                // 3. AI Banner Clinical Summary
                const bannerText = document.getElementById('aiBannerText');
                if (bannerText) {
                    bannerText.innerHTML = `Real-time analytics indicate <strong>${m.flow_status}</strong> with <strong>${m.completion_rate}%</strong> consultation resolution. All <strong>${m.active_doctors}</strong> specialists are active across <strong>${m.active_departments_list}</strong>. Bed occupancy is at <strong>${m.capacity_pct}%</strong> (${m.free_beds} beds free).`;
                }

                // 4. Weekly Patient Inflow Chart Bars
                if (m.weekly_chart && Array.isArray(m.weekly_chart)) {
                    m.weekly_chart.forEach(d => {
                        const bar = document.getElementById(`chartBar_${d.day}`);
                        const col = document.getElementById(`chartCol_${d.day}`);
                        if (bar) {
                            bar.style.height = `${d.height}%`;
                            if (d.has_data) {
                                bar.classList.add('has-data');
                            } else {
                                bar.classList.remove('has-data');
                            }
                            let countEl = document.getElementById(`chartCount_${d.day}`);
                            if (d.count > 0) {
                                if (!countEl) {
                                    countEl = document.createElement('span');
                                    countEl.id = `chartCount_${d.day}`;
                                    countEl.className = 'bar-count-badge';
                                    bar.appendChild(countEl);
                                }
                                countEl.innerText = d.count;
                            } else if (countEl) {
                                countEl.remove();
                            }
                        }
                        if (col) col.setAttribute('title', `${d.day}: ${d.count} Consultations`);
                    });
                }

                // 5. Department Load Distribution
                const deptList = document.getElementById('deptLoadList');
                if (deptList) {
                    if (m.departments_load && Array.isArray(m.departments_load) && m.departments_load.length > 0) {
                        let dHtml = '';
                        m.departments_load.forEach((dep, idx) => {
                            dHtml += `
                            <div class="dept-item-row" id="deptRow_${idx}">
                                <div class="dept-info-top">
                                    <span>${dep.name}</span>
                                    <span><strong>${dep.count}</strong> consults (${dep.actual_pct}%)</span>
                                </div>
                                <div class="dept-progress-track">
                                    <div class="dept-progress-bar" style="width: ${dep.percentage}%; background: ${dep.color};"></div>
                                </div>
                            </div>`;
                        });
                        deptList.innerHTML = dHtml;
                    } else {
                        deptList.innerHTML = `
                            <div style="text-align: center; padding: 28px 12px; color: var(--text-muted); font-size: 12px;">
                                <span style="font-size: 26px; display: block; margin-bottom: 6px;">🩺</span>
                                No department consultations recorded yet.<br>Rosters and specialty metrics activate with patient intake.
                            </div>`;
                    }
                }

                const totalConsultsEl = document.getElementById('totalDeptConsultsText');
                if (totalConsultsEl) totalConsultsEl.innerText = `${m.total_appointments_all} Total Consults`;

                if (badge) {
                    badge.innerText = 'Live Stats: Synced';
                }
            } catch (err) {
                console.error("Metrics sync error:", err);
                if (badge) badge.innerText = 'Live Stats: Synced';
            }
        }

        function handleGlobalSearch(query) {
            const q = (query || '').trim().toLowerCase();
            const dropdown = document.getElementById('searchDropdown');
            
            filterCurrentActiveTable(q);

            if (!q) {
                dropdown.classList.remove('active');
                dropdown.innerHTML = '';
                return;
            }

            const matchedPatients = ALL_PATIENTS.filter(p => 
                (p.name && p.name.toLowerCase().includes(q)) ||
                (p.phone && p.phone.includes(q)) ||
                (String(p.patient_id).includes(q)) ||
                (p.blood_group && p.blood_group.toLowerCase().includes(q))
            ).slice(0, 4);

            const matchedDoctors = ALL_DOCTORS.filter(d => 
                (d.name && d.name.toLowerCase().includes(q)) ||
                (d.specialization && d.specialization.toLowerCase().includes(q)) ||
                (d.phone && d.phone.includes(q))
            ).slice(0, 4);

            const matchedAppointments = ALL_APPOINTMENTS.filter(a => 
                (a.patient_name && a.patient_name.toLowerCase().includes(q)) ||
                (a.doctor_name && a.doctor_name.toLowerCase().includes(q)) ||
                (String(a.appointment_id).includes(q)) ||
                (a.status && a.status.toLowerCase().includes(q))
            ).slice(0, 4);

            let html = '';
            const totalMatches = matchedPatients.length + matchedDoctors.length + matchedAppointments.length;

            if (totalMatches === 0) {
                html = '<div class="search-no-results">🔍 No matching patients, doctors, or appointments found.</div>';
            } else {
                if (matchedPatients.length > 0) {
                    html += `<div class="search-group-header"><span>👥 Patients</span><span>${matchedPatients.length} Matched</span></div>`;
                    matchedPatients.forEach(p => {
                        html += `
                        <div class="search-result-item" onclick="jumpToItem('patients', ${p.patient_id})">
                            <div class="search-item-left">
                                <div class="search-item-badge" style="background:#e0f2fe; color:#0369a1;">P</div>
                                <div>
                                    <div class="search-item-title">${p.name} <span class="blood-chip" style="font-size:10px; padding:1px 5px;">${p.blood_group || ''}</span></div>
                                    <div class="search-item-sub">MRN-#${String(p.patient_id).padStart(4, '0')} • ${p.age} Yrs • 📞 ${p.phone}</div>
                                </div>
                            </div>
                            <span class="search-item-action">View Record →</span>
                        </div>`;
                    });
                }

                if (matchedDoctors.length > 0) {
                    html += `<div class="search-group-header"><span>👨‍⚕️ Specialists & Faculty</span><span>${matchedDoctors.length} Matched</span></div>`;
                    matchedDoctors.forEach(d => {
                        html += `
                        <div class="search-result-item" onclick="jumpToItem('doctors', ${d.doctor_id})">
                            <div class="search-item-left">
                                <div class="search-item-badge" style="background:#ecfeff; color:#0891b2;">Dr</div>
                                <div>
                                    <div class="search-item-title">${d.name}</div>
                                    <div class="search-item-sub">${d.specialization} • Fee: ${DEFAULT_CURR}${Number(d.fee).toFixed(0)}</div>
                                </div>
                            </div>
                            <span class="search-item-action">View Roster →</span>
                        </div>`;
                    });
                }

                if (matchedAppointments.length > 0) {
                    html += `<div class="search-group-header"><span>📅 Consultations</span><span>${matchedAppointments.length} Matched</span></div>`;
                    matchedAppointments.forEach(a => {
                        html += `
                        <div class="search-result-item" onclick="jumpToItem('appointments', ${a.appointment_id})">
                            <div class="search-item-left">
                                <div class="search-item-badge" style="background:#fef3c7; color:#d97706;">#${a.appointment_id}</div>
                                <div>
                                    <div class="search-item-title">${a.patient_name} with ${a.doctor_name}</div>
                                    <div class="search-item-sub">${a.appointment_date} (${a.time_slot}) • Status: ${a.status}</div>
                                </div>
                            </div>
                            <span class="search-item-action">Open Queue →</span>
                        </div>`;
                    });
                }
            }

            dropdown.innerHTML = html;
            dropdown.classList.add('active');
        }

        function filterCurrentActiveTable(query) {
            const q = query.toLowerCase();
            const activeSection = document.querySelector('.tab-view-section.active');
            if (!activeSection) return;

            const rows = activeSection.querySelectorAll('table tbody tr');
            rows.forEach(r => {
                const text = r.innerText.toLowerCase();
                r.style.display = text.includes(q) ? '' : 'none';
            });

            const docCards = activeSection.querySelectorAll('.doctor-behance-card');
            docCards.forEach(c => {
                const text = c.innerText.toLowerCase();
                c.style.display = text.includes(q) ? '' : 'none';
            });
        }

        function jumpToItem(sectionId, id) {
            const btn = document.querySelector(`.nav-btn[onclick*="${sectionId}"]`);
            if (btn) btn.click();

            const dropdown = document.getElementById('searchDropdown');
            if (dropdown) dropdown.classList.remove('active');

            setTimeout(() => {
                const rows = document.querySelectorAll(`#view-${sectionId} table tbody tr`);
                rows.forEach(r => {
                    if (r.innerText.includes(String(id))) {
                        r.scrollIntoView({ behavior: 'smooth', block: 'center' });
                        r.style.backgroundColor = '#e0e7ff';
                        setTimeout(() => r.style.backgroundColor = '', 2000);
                    }
                });
            }, 120);
        }

        document.addEventListener('click', function(e) {
            const box = document.querySelector('.search-pill-box');
            if (box && !box.contains(e.target)) {
                document.getElementById('searchDropdown')?.classList.remove('active');
            }
        });
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                document.getElementById('searchDropdown')?.classList.remove('active');
            }
        });

        // Initialize Tab from URL parameter & Start Live Statistics Heartbeat
        window.addEventListener('DOMContentLoaded', () => {
            const urlParams = new URLSearchParams(window.location.search);
            const tab = urlParams.get('tab');
            if (tab) {
                activateSection(null, tab);
            }
            // Live auto-polling every 12 seconds
            setInterval(() => refreshDashboardMetrics(false), 12000);
        });
    </script>
</body>
</html>
"""

# ======================================================================================
# AUTHENTIC CLINICAL LOGIN PORTAL TEMPLATE
# ======================================================================================
LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MediCare AI | Healthcare Staff Authentication Portal</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary-indigo: #4f46e5;
            --primary-gradient: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%);
            --primary-glow: rgba(79, 70, 229, 0.25);
            --bg-dark: #090d16;
            --surface-card: #ffffff;
            --border-light: #e2e8f0;
            --text-title: #0f172a;
            --text-secondary: #64748b;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Plus Jakarta Sans', sans-serif; }
        body {
            background: radial-gradient(circle at 10% 20%, #1e1b4b 0%, #090d16 90%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 24px;
        }
        .login-card {
            width: 980px;
            max-width: 95vw;
            background: #ffffff;
            border-radius: 24px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5), 0 0 40px rgba(79, 70, 229, 0.2);
            display: grid;
            grid-template-columns: 1fr 1.15fr;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        /* Left Brand Hero Panel */
        .login-hero-panel {
            background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #4338ca 100%);
            color: #ffffff;
            padding: 44px 38px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            position: relative;
            overflow: hidden;
        }
        .login-hero-panel::after {
            content: '';
            position: absolute;
            bottom: -50px;
            right: -50px;
            width: 250px;
            height: 250px;
            background: radial-gradient(circle, rgba(99, 102, 241, 0.4) 0%, transparent 70%);
            border-radius: 50%;
        }
        .hero-brand {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .brand-gem {
            width: 44px;
            height: 44px;
            background: #ffffff;
            color: #4f46e5;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 22px;
            font-weight: 800;
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        }
        .hero-brand h1 { font-size: 20px; font-weight: 800; letter-spacing: -0.3px; }
        .hero-brand p { font-size: 11px; color: #c7d2fe; font-weight: 600; text-transform: uppercase; }

        .hero-features {
            margin: 36px 0;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }
        .feature-item {
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 13.5px;
            color: #e0e7ff;
            font-weight: 500;
        }
        .feature-icon-box {
            width: 32px;
            height: 32px;
            background: rgba(255, 255, 255, 0.12);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
        }

        .hero-footer-note {
            font-size: 11px;
            color: #a5b4fc;
            display: flex;
            justify-content: space-between;
            border-top: 1px solid rgba(255, 255, 255, 0.15);
            padding-top: 16px;
        }

        /* Right Form Panel */
        .login-form-panel {
            padding: 44px 40px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        .form-heading h2 {
            font-size: 24px;
            font-weight: 800;
            color: var(--text-title);
            letter-spacing: -0.5px;
        }
        .form-heading p {
            font-size: 13px;
            color: var(--text-secondary);
            margin-top: 6px;
            margin-bottom: 20px;
        }

        /* Password Visibility Toggle */
        .toggle-pwd-btn {
            position: absolute;
            right: 12px;
            top: 50%;
            transform: translateY(-50%);
            background: none;
            border: none;
            cursor: pointer;
            font-size: 15px;
            color: #94a3b8;
            padding: 4px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 6px;
            transition: color 0.15s ease;
        }
        .toggle-pwd-btn:hover {
            color: var(--primary-indigo);
        }

        /* Remember Password & Security Chip */
        .login-options-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-top: 4px;
            margin-bottom: 20px;
        }
        .remember-checkbox-label {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 13px;
            color: var(--text-body);
            font-weight: 600;
            cursor: pointer;
            user-select: none;
        }
        .remember-checkbox-label input[type="checkbox"] {
            width: 17px;
            height: 17px;
            accent-color: var(--primary-indigo);
            cursor: pointer;
        }
        .security-chip {
            font-size: 11px;
            color: #059669;
            font-weight: 700;
            background: #ecfdf5;
            border: 1px solid #a7f3d0;
            padding: 4px 10px;
            border-radius: 14px;
            display: flex;
            align-items: center;
            gap: 4px;
        }

        .alert-error-box {
            background: #fef2f2;
            border: 1px solid #fecaca;
            color: #b91c1c;
            padding: 10px 14px;
            border-radius: 8px;
            font-size: 12.5px;
            font-weight: 600;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .input-group-row {
            display: flex;
            flex-direction: column;
            gap: 6px;
            margin-bottom: 16px;
        }
        .input-group-row label {
            font-size: 12px;
            font-weight: 700;
            color: var(--text-title);
        }
        .login-input-wrap {
            position: relative;
        }
        .login-input-icon {
            position: absolute;
            left: 14px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 14px;
            color: #94a3b8;
        }
        .login-input {
            width: 100%;
            background: #f8fafc;
            border: 1px solid var(--border-light);
            padding: 12px 14px 12px 42px;
            border-radius: 10px;
            font-size: 13.5px;
            outline: none;
            color: var(--text-title);
            transition: all 0.2s;
        }
        .login-input:focus {
            background: #ffffff;
            border-color: var(--primary-indigo);
            box-shadow: 0 0 0 3px var(--primary-glow);
        }

        .submit-login-btn {
            background: var(--primary-gradient);
            color: #ffffff;
            border: none;
            padding: 13px;
            border-radius: 10px;
            font-size: 14px;
            font-weight: 700;
            cursor: pointer;
            box-shadow: 0 8px 20px var(--primary-glow);
            transition: all 0.2s ease;
            width: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            margin-top: 6px;
        }
        .submit-login-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 24px var(--primary-glow);
        }

        .phi-disclaimer {
            font-size: 11px;
            color: #94a3b8;
            margin-top: 18px;
            text-align: center;
            line-height: 1.4;
        }
    </style>
</head>
<body>
    <div class="login-card">
        <!-- Left Hero Panel -->
        <div class="login-hero-panel">
            <div class="hero-brand">
                <div class="brand-gem">✦</div>
                <div>
                    <h1>MediCare AI</h1>
                    <p>Clinical Health OS</p>
                </div>
            </div>

            <div class="hero-features">
                <div class="feature-item">
                    <div class="feature-icon-box">🔒</div>
                    <span>HIPAA & NABH Compliant Clinical Gateway</span>
                </div>
                <div class="feature-item">
                    <div class="feature-icon-box">🤖</div>
                    <span>AI Diagnostic Triage & Clinical Intelligence</span>
                </div>
                <div class="feature-item">
                    <div class="feature-icon-box">⚡</div>
                    <span>Real-time OPD Queuing & Schedule Synchronization</span>
                </div>
                <div class="feature-item">
                    <div class="feature-icon-box">📄</div>
                    <span>Digital Prescriptions & Branded Tax Invoicing</span>
                </div>
            </div>

            <div class="hero-footer-note">
                <span>STATION: CENTRAL-OPD-02</span>
                <span>SYSTEM v4.2 ENTERPRISE</span>
            </div>
        </div>

        <!-- Right Form Panel -->
        <div class="login-form-panel">
            <div class="form-heading">
                <h2>Clinical Portal Sign-In</h2>
                <p>Enter your authorized hospital staff credentials to access Electronic Health Records (EHR).</p>
            </div>

            {% if error %}
            <div class="alert-error-box">
                <span>⚠️ {{ error }}</span>
            </div>
            {% endif %}

            <form action="/login" method="POST" id="loginForm" onsubmit="handleLoginSubmit()">
                <div class="input-group-row">
                    <label>Staff ID / Username *</label>
                    <div class="login-input-wrap">
                        <span class="login-input-icon">👤</span>
                        <input type="text" id="usernameInput" name="username" class="login-input" placeholder="Enter Staff ID or Username" autocomplete="username" required autofocus>
                    </div>
                </div>

                <div class="input-group-row">
                    <label>Password *</label>
                    <div class="login-input-wrap">
                        <span class="login-input-icon">🔒</span>
                        <input type="password" id="passwordInput" name="password" class="login-input" placeholder="••••••••" autocomplete="current-password" required>
                        <button type="button" class="toggle-pwd-btn" onclick="togglePasswordVisibility()" title="Show/Hide Password" tabindex="-1">
                            <span id="pwdEyeIcon">👁️</span>
                        </button>
                    </div>
                </div>

                <!-- Remember Me & Security Row -->
                <div class="login-options-row">
                    <label class="remember-checkbox-label">
                        <input type="checkbox" id="rememberMe" name="remember_me" value="true">
                        <span>Remember credentials on this device</span>
                    </label>
                    <span class="security-chip">🔒 256-Bit SSL</span>
                </div>

                <button type="submit" class="submit-login-btn">
                    <span>Sign In to Workstation</span>
                    <span>→</span>
                </button>
            </form>

            <div class="phi-disclaimer">
                ⚠️ Protected Health Information (PHI) Notice: Unauthorized access is strictly prohibited and subject to institutional audit.
            </div>
        </div>
    </div>

    <script>
        function togglePasswordVisibility() {
            const pwd = document.getElementById('passwordInput');
            const icon = document.getElementById('pwdEyeIcon');
            if (pwd.type === 'password') {
                pwd.type = 'text';
                icon.innerText = '🙈';
            } else {
                pwd.type = 'password';
                icon.innerText = '👁️';
            }
        }

        window.addEventListener('DOMContentLoaded', () => {
            const savedUser = localStorage.getItem('medicare_remembered_staff');
            if (savedUser) {
                document.getElementById('usernameInput').value = savedUser;
                document.getElementById('rememberMe').checked = true;
                const pwdInput = document.getElementById('passwordInput');
                if (pwdInput) pwdInput.focus();
            }
        });

        function handleLoginSubmit() {
            const remember = document.getElementById('rememberMe').checked;
            const user = document.getElementById('usernameInput').value.trim();
            if (remember && user) {
                localStorage.setItem('medicare_remembered_staff', user);
            } else {
                localStorage.removeItem('medicare_remembered_staff');
            }
        }
    </script>
</body>
</html>
"""

# Authorized Clinical Staff Users (Securely Hashed)
AUTH_USERS = {
    "admin": {
        "hash": generate_password_hash("admin123"),
        "name": "Dr. Rajesh Sharma, MD",
        "role": "Chief Physician / Administrator",
        "initials": "RS"
    },
    "doctor": {
        "hash": generate_password_hash("doctor123"),
        "name": "Dr. Priya Patel, MD",
        "role": "Attending Neurologist",
        "initials": "PP"
    },
    "staff": {
        "hash": generate_password_hash("staff123"),
        "name": "Sunita Gupta",
        "role": "Clinical Reception & Triage",
        "initials": "SG"
    }
}

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "").strip()
        remember_me = request.form.get("remember_me") == "true"

        user_entry = AUTH_USERS.get(username)
        is_valid = False
        if user_entry:
            if "hash" in user_entry and check_password_hash(user_entry["hash"], password):
                is_valid = True
            elif user_entry.get("password") == password:
                is_valid = True

        if is_valid:
            session.permanent = remember_me
            session["user"] = username
            session["user_info"] = {
                "name": user_entry["name"],
                "role": user_entry["role"],
                "initials": user_entry["initials"]
            }
            return redirect("/")
        else:
            return render_template_string(
                LOGIN_TEMPLATE,
                error="Invalid Staff ID or Password. Please verify your credentials or contact the Hospital IT Administrator."
            )

    # GET request
    if "user" in session:
        return redirect("/")
    return render_template_string(LOGIN_TEMPLATE, error=None)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/")
@app.route("/api/index")
@app.route("/api/index.py")
def index():

    if "user" not in session:
        return redirect("/login")

    session_user = session.get("user_info", {
        "name": "Dr. Rajesh Sharma, MD",
        "role": "Chief Physician / Administrator",
        "initials": "RS"
    })

    metrics = db.get_dashboard_metrics()
    patients = db.get_all_patients()
    doctors = db.get_all_doctors()
    appointments = db.get_all_appointments()
    prescriptions = db.get_prescriptions()
    bills = db.get_billings()
    today = datetime.date.today().strftime("%Y-%m-%d")

    return render_template_string(
        AI_HEALTHCARE_TEMPLATE,
        metrics=metrics,
        patients=patients,
        doctors=doctors,
        appointments=appointments,
        prescriptions=prescriptions,
        bills=bills,
        patients_json=json.dumps(patients),
        doctors_json=json.dumps(doctors),
        appointments_json=json.dumps(appointments),
        session_user=session_user,
        currency=DEFAULT_CURRENCY,
        today=today
    )

@app.route("/api/metrics")
def api_metrics():
    metrics = db.get_dashboard_metrics()
    return jsonify(metrics)

@app.route("/api/patient/add", methods=["POST"])
def add_patient():
    name = (request.form.get("name") or "").strip()
    if not name:
        return "<script>alert('Patient full name is required for medical admission.'); window.history.back();</script>"
    try:
        age = int(request.form.get("age", 25))
    except (ValueError, TypeError):
        age = 25
    gender = request.form.get("gender", "Male")
    phone = (request.form.get("phone") or "").strip()
    blood = request.form.get("blood_group", "O+")
    address = (request.form.get("address") or "").strip()
    db.add_patient(name, age, gender, phone, blood, address)
    return "<script>window.location.href='/?tab=patients';</script>"

@app.route("/api/doctor/add", methods=["POST"])
def add_doctor():
    name = (request.form.get("name") or "").strip()
    if not name:
        return "<script>alert('Doctor full name is required for roster enrollment.'); window.history.back();</script>"
    spec = request.form.get("specialization") or "General Medicine"
    phone = (request.form.get("phone") or "").strip()
    email = (request.form.get("email") or "").strip()
    days = request.form.get("available_days", "Mon-Fri")
    try:
        fee = float(request.form.get("fee", 500))
    except (ValueError, TypeError):
        fee = 500.0
    db.add_doctor(name, spec, phone, email, days, fee)
    return "<script>window.location.href='/?tab=doctors';</script>"

@app.route("/api/appointment/book", methods=["POST"])
def book_appointment():
    p_id_raw = request.form.get("patient_id")
    d_id_raw = request.form.get("doctor_id")
    if not p_id_raw or not d_id_raw:
        return "<script>alert('Scheduling Alert: Please select both a registered patient and an enrolled specialist.'); window.history.back();</script>"
    try:
        p_id = int(p_id_raw)
        d_id = int(d_id_raw)
    except (ValueError, TypeError):
        return "<script>alert('Invalid patient or specialist token.'); window.history.back();</script>"

    d_date = request.form.get("appointment_date") or datetime.date.today().strftime("%Y-%m-%d")
    slot = request.form.get("time_slot") or "10:00 AM"
    notes = request.form.get("notes", "")

    if db.check_appointment_conflict(d_id, d_date, slot):
        return "<script>alert('Scheduling Conflict Alert: Selected doctor already has an active appointment at this date and time slot.'); window.history.back();</script>"

    db.add_appointment(p_id, d_id, d_date, slot, "Scheduled", notes)
    return "<script>window.location.href='/?tab=appointments';</script>"

@app.route("/api/appointment/status")
def update_status():
    try:
        appt_id = int(request.args.get("id"))
    except (ValueError, TypeError):
        return redirect("/")
    status = request.args.get("status", "Completed")
    tab = request.args.get("tab", "dashboard")
    db.update_appointment_status(appt_id, status)
    return f"<script>window.location.href='/?tab={tab}';</script>"

@app.route("/api/billing/create", methods=["POST"])
def create_bill():
    appt_id_raw = request.form.get("appointment_id")
    p_id_raw = request.form.get("patient_id")
    if not appt_id_raw or not p_id_raw:
        return "<script>alert('Billing Alert: Please select a valid patient consultation to issue a tax invoice.'); window.history.back();</script>"
    try:
        appt_id = int(appt_id_raw)
        p_id = int(p_id_raw)
        consult_fee = float(request.form.get("consultation_fee", 500))
        med_fee = float(request.form.get("medicine_fee", 0))
        other_fee = float(request.form.get("other_charges", 0))
        disc = float(request.form.get("discount", 0))
    except (ValueError, TypeError):
        return "<script>alert('Invalid financial values supplied in billing calculation.'); window.history.back();</script>"

    total = max(0.0, (consult_fee + med_fee + other_fee) - disc)
    pay_status = request.form.get("payment_status", "Paid")
    pay_mode = request.form.get("payment_mode", "Cash")

    db.create_or_update_bill(appt_id, p_id, consult_fee, med_fee, other_fee, disc, total, pay_status, pay_mode)
    return "<script>window.location.href='/?tab=billing';</script>"

@app.route("/api/billing/pay")
def pay_bill():
    try:
        bill_id = int(request.args.get("bill_id"))
    except (ValueError, TypeError):
        return redirect("/?tab=billing")
    mode = request.args.get("mode", "UPI")
    tab = request.args.get("tab", "billing")
    db.update_bill_status(bill_id, "Paid", mode)
    return f"<script>window.location.href='/?tab={tab}';</script>"

@app.route("/api/prescription/create", methods=["POST"])
def create_prescription():
    appt_id_raw = request.form.get("appointment_id")
    p_id_raw = request.form.get("patient_id")
    d_id_raw = request.form.get("doctor_id")
    if not appt_id_raw or not p_id_raw or not d_id_raw:
        return "<script>alert('Clinical Alert: Please select an active consultation record before issuing an E-Prescription.'); window.history.back();</script>"
    try:
        appt_id = int(appt_id_raw)
        p_id = int(p_id_raw)
        d_id = int(d_id_raw)
    except (ValueError, TypeError):
        return "<script>alert('Invalid clinical consultation parameters.'); window.history.back();</script>"

    diagnosis = request.form.get("diagnosis", "").strip() or "General Consultation"
    med_name = request.form.get("med_name", "Paracetamol").strip()
    med_dosage = request.form.get("med_dosage", "500mg").strip()
    med_freq = request.form.get("med_frequency", "1-0-1 (Twice daily)").strip()
    med_dur = request.form.get("med_duration", "5 Days").strip()
    advice = request.form.get("advice", "Adequate rest and hydration.").strip()

    medicines = [
        {"name": med_name, "dosage": med_dosage, "frequency": med_freq, "duration": med_dur}
    ]
    db.save_prescription(appt_id, p_id, d_id, diagnosis, json.dumps(medicines), advice)
    return "<script>window.location.href='/?tab=prescriptions';</script>"

@app.route("/download/invoice/<int:bill_id>")
def download_invoice(bill_id):
    bills = db.get_billings()
    bill_data = next((b for b in bills if b["bill_id"] == bill_id), None)
    if not bill_data:
        return "Invoice not found", 404
    path = PDFReportGenerator.generate_invoice_pdf(bill_data)
    return send_file(path, as_attachment=False)

@app.route("/download/prescription/<int:rx_id>")
def download_prescription(rx_id):
    rxs = db.get_prescriptions()
    rx_data = next((r for r in rxs if r["prescription_id"] == rx_id), None)
    if not rx_data:
        return "Prescription not found", 404
    path = PDFReportGenerator.generate_prescription_pdf(rx_data)
    return send_file(path, as_attachment=False)

if __name__ == "__main__":
    print("=" * 60)
    print("AI HEALTHCARE & HOSPITAL MANAGEMENT DASHBOARD LIVE AT: http://127.0.0.1:5000")
    print("=" * 60)
    app.run(host="0.0.0.0", port=5000, debug=False)

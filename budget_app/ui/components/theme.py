"""Shared NiceGUI theme."""

from __future__ import annotations

from nicegui import ui


def add_theme() -> None:
    ui.add_head_html(
        """
        <style>
            body { background: #eef2f7; color: #111827; overflow-x: hidden; }
            .q-page { background: radial-gradient(circle at 10% 0%, #dff7f1 0, transparent 24%), radial-gradient(circle at 92% 8%, #ffe4e6 0, transparent 22%), #eef2f7; }
            .bp-shell { width: 100%; max-width: none; margin: 0; padding: 0 clamp(20px, 2.4vw, 48px); }
            .bp-header { background: rgba(255, 255, 255, .94); border-bottom: 1px solid #dbe3ef; box-shadow: 0 10px 30px rgb(15 23 42 / 0.06); backdrop-filter: blur(12px); }
            .bp-nav { background: rgba(255, 255, 255, .92); border-bottom: 1px solid #dbe3ef; }
            .bp-nav-link { color: #4b5563; padding: 20px 18px; border-bottom: 4px solid transparent; text-decoration: none; white-space: nowrap; font-size: 20px; line-height: 28px; font-weight: 700; min-height: 68px; display: inline-flex; align-items: center; }
            .bp-nav-link .q-icon { font-size: 28px; }
            .bp-nav-link:hover { color: #111827; border-color: #fb7185; }
            .bp-nav-active { color: #0f766e; border-color: #0f766e; }
            .bp-page { width: 100%; max-width: none; margin: 0; padding: 22px clamp(20px, 2.4vw, 48px) 28px; }
            .bp-card { background: rgba(255, 255, 255, .96); border: 1px solid #dbe3ef; border-radius: 8px; box-shadow: 0 14px 30px -24px rgb(15 23 42 / .5); }
            .bp-dashboard-panel { background: rgba(255, 255, 255, .9); border: 1px solid #dbe3ef; border-radius: 8px; box-shadow: 0 24px 42px -32px rgb(15 23 42 / .45); }
            .bp-card-hover { transition: box-shadow 160ms ease, transform 160ms ease; }
            .bp-card-hover:hover { box-shadow: 0 12px 18px -12px rgb(17 24 39 / 0.25); transform: translateY(-1px); }
            .bp-muted { color: #6b7280; }
            .bp-title { font-size: 30px; line-height: 38px; font-weight: 750; color: #111827; letter-spacing: 0; }
            .bp-section-title { font-size: 20px; line-height: 28px; font-weight: 700; color: #111827; letter-spacing: 0; }
            .bp-page, .bp-card, .q-field, .q-table, .q-btn { font-size: 16px; }
            .q-field__label, .q-table th { font-size: 14px; }
            .q-btn { font-weight: 650; border-radius: 8px; }
            .q-card { min-width: 0; }
            .bp-table .q-table__top, .bp-table thead tr { background: #f9fafb; }
            .bp-table th { color: #6b7280; text-transform: uppercase; letter-spacing: .04em; font-weight: 700; }
            .bp-table tbody tr:hover { background: #f9fafb; }
            .bp-table .q-table__card { box-shadow: none; }
            .bp-positive { color: #15803d; }
            .bp-warning { color: #b45309; }
            .bp-negative { color: #b91c1c; }
            .bp-blue { color: #1d4ed8; }
            .bp-money { font-variant-numeric: tabular-nums; white-space: nowrap; text-align: right; }
            .bp-stat-card { min-height: 116px; }
            .bp-stat-value { font-variant-numeric: tabular-nums; white-space: nowrap; overflow-wrap: anywhere; }
            .bp-hero-stat { background: linear-gradient(135deg, #0f766e, #2563eb 58%, #e11d48); color: #fff; border: 0; overflow: hidden; }
            .bp-hero-stat .q-icon { opacity: .9; }
            .bp-account-strip { display: grid; grid-template-columns: minmax(260px, .9fr) minmax(0, 1.7fr); gap: 18px; width: 100%; align-items: stretch; }
            .bp-account-total { background: linear-gradient(135deg, #111827, #0f766e); color: #fff; border-radius: 8px; padding: 22px; min-height: 160px; display: flex; flex-direction: column; justify-content: space-between; }
            .bp-account-list { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; width: 100%; }
            .bp-account-mini { background: #f8fafc; border: 1px solid #e5e7eb; border-radius: 8px; padding: 14px; min-width: 0; }
            .bp-account-mini-value { font-size: 22px; line-height: 28px; font-weight: 800; font-variant-numeric: tabular-nums; overflow-wrap: anywhere; }
            .bp-grid-desktop { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 18px; width: 100%; }
            .bp-kpi-grid { display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 16px; width: 100%; align-items: stretch; }
            .bp-two-col { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 20px; width: 100%; align-items: start; }
            .bp-pill { border-radius: 999px; padding: 4px 10px; font-size: 12px; font-weight: 700; display: inline-flex; align-items: center; gap: 4px; }
            .bp-income-pill { background: #dcfce7; color: #166534; }
            .bp-expense-pill { background: #fee2e2; color: #991b1b; }
            .bp-bank-pill { background: #dbeafe; color: #1d4ed8; }
            .bp-cash-pill { background: #fef3c7; color: #92400e; }
            .bp-primary-btn { background: #2563eb; color: #fff; }
            .bp-secondary-btn { background: #eef2f7; color: #374151; }
            .bp-danger-btn { background: #dc2626; color: #fff; }
            .bp-envelope-card { border-left: 5px solid #2563eb; min-height: 155px; }
            .bp-envelope-ok { border-left-color: #16a34a; }
            .bp-envelope-warning { border-left-color: #f59e0b; }
            .bp-envelope-danger { border-left-color: #dc2626; }
            .bp-progress { width: 100%; background: #e5e7eb; border-radius: 999px; height: 10px; overflow: hidden; }
            .bp-progress-fill { height: 10px; border-radius: 999px; }
            .bp-progress-ok { background: #16a34a; }
            .bp-progress-warning { background: #f59e0b; }
            .bp-progress-danger { background: #dc2626; }
            .bp-segmented .q-radio { border: 1px solid #d1d5db; border-radius: 8px; padding: 8px 12px; background: #fff; min-width: 130px; justify-content: center; }
            .bp-month-card { min-height: 116px; position: relative; overflow: hidden; }
            .bp-month-value { font-size: 28px; line-height: 34px; font-weight: 800; text-align: center; }
            .bp-month-arrow { opacity: .25; transition: opacity 140ms ease, transform 140ms ease; }
            .bp-month-card:hover .bp-month-arrow { opacity: 1; transform: scale(1.04); }
            .bp-compact-metrics { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; }
            .bp-metric-box { background: #f8fafc; border: 1px solid #e5e7eb; border-radius: 8px; padding: 8px 10px; min-width: 0; }
            .bp-metric-box .bp-money { font-size: 14px; text-align: left; overflow-wrap: anywhere; white-space: normal; }
            @media print {
                .bp-header, .bp-nav, .q-btn { display: none !important; }
                .bp-page { max-width: none; padding: 0; }
                .bp-card { box-shadow: none; break-inside: avoid; }
            }
            input::-webkit-outer-spin-button,
            input::-webkit-inner-spin-button { -webkit-appearance: none; margin: 0; }
            input[type=number] { -moz-appearance: textfield; }
            @media (max-width: 980px) {
                .bp-two-col { grid-template-columns: 1fr; }
                .bp-account-strip { grid-template-columns: 1fr; }
                .bp-kpi-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
                .bp-nav-link { font-size: 18px; line-height: 26px; min-height: 62px; padding: 18px 14px; }
            }
            @media (max-width: 700px) {
                .bp-shell, .bp-page { padding-left: 16px; padding-right: 16px; }
                .bp-kpi-grid, .bp-grid-desktop { grid-template-columns: 1fr; }
                .bp-nav-link { font-size: 17px; line-height: 24px; min-height: 58px; padding: 16px 12px; }
                .bp-nav-link .q-icon { font-size: 24px; }
            }
        </style>
        """,
        shared=True,
    )

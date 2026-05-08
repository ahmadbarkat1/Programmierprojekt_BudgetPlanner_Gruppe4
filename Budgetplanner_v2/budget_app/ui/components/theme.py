"""Shared NiceGUI theme."""

from __future__ import annotations

from nicegui import ui


def add_theme() -> None:
    ui.add_head_html(
        """
        <style>
            body { background: #f6f7f9; color: #111827; }
            .q-page { background: #f6f7f9; }
            .bp-shell { max-width: 1320px; margin: 0 auto; padding: 0 28px; }
            .bp-header { background: #fff; border-bottom: 1px solid #e5e7eb; box-shadow: 0 1px 2px rgb(0 0 0 / 0.04); }
            .bp-nav { background: #fff; border-bottom: 1px solid #e5e7eb; }
            .bp-nav-link { color: #4b5563; padding: 15px 8px; border-bottom: 3px solid transparent; text-decoration: none; white-space: nowrap; }
            .bp-nav-link:hover { color: #111827; border-color: #d1d5db; }
            .bp-nav-active { color: #1d4ed8; border-color: #2563eb; }
            .bp-page { max-width: 1320px; margin: 0 auto; padding: 30px 28px 42px; }
            .bp-card { background: #fff; border: 1px solid #e5e7eb; border-radius: 8px; box-shadow: 0 1px 2px rgb(0 0 0 / 0.04); }
            .bp-card-hover { transition: box-shadow 160ms ease, transform 160ms ease; }
            .bp-card-hover:hover { box-shadow: 0 12px 18px -12px rgb(17 24 39 / 0.25); transform: translateY(-1px); }
            .bp-muted { color: #6b7280; }
            .bp-title { font-size: 30px; line-height: 38px; font-weight: 750; color: #111827; letter-spacing: 0; }
            .bp-section-title { font-size: 20px; line-height: 28px; font-weight: 700; color: #111827; letter-spacing: 0; }
            .bp-page, .bp-card, .q-field, .q-table, .q-btn { font-size: 16px; }
            .q-field__label, .q-table th { font-size: 14px; }
            .q-btn { font-weight: 650; border-radius: 8px; }
            .bp-table .q-table__top, .bp-table thead tr { background: #f9fafb; }
            .bp-table th { color: #6b7280; text-transform: uppercase; letter-spacing: .04em; font-weight: 700; }
            .bp-table tbody tr:hover { background: #f9fafb; }
            .bp-table .q-table__card { box-shadow: none; }
            .bp-positive { color: #15803d; }
            .bp-warning { color: #b45309; }
            .bp-negative { color: #b91c1c; }
            .bp-blue { color: #1d4ed8; }
            .bp-money { font-variant-numeric: tabular-nums; white-space: nowrap; text-align: right; }
            .bp-stat-card { min-height: 128px; }
            .bp-stat-value { font-variant-numeric: tabular-nums; white-space: nowrap; }
            .bp-hero-stat { background: linear-gradient(135deg, #0f766e, #2563eb); color: #fff; border: 0; }
            .bp-grid-desktop { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 22px; width: 100%; }
            .bp-two-col { display: grid; grid-template-columns: minmax(360px, 0.85fr) minmax(520px, 1.15fr); gap: 24px; width: 100%; align-items: start; }
            .bp-pill { border-radius: 999px; padding: 4px 10px; font-size: 12px; font-weight: 700; display: inline-flex; align-items: center; gap: 4px; }
            .bp-income-pill { background: #dcfce7; color: #166534; }
            .bp-expense-pill { background: #fee2e2; color: #991b1b; }
            .bp-bank-pill { background: #dbeafe; color: #1d4ed8; }
            .bp-cash-pill { background: #fef3c7; color: #92400e; }
            .bp-primary-btn { background: #2563eb; color: #fff; }
            .bp-secondary-btn { background: #eef2f7; color: #374151; }
            .bp-danger-btn { background: #dc2626; color: #fff; }
            .bp-envelope-card { border-left: 5px solid #2563eb; min-height: 205px; }
            .bp-envelope-ok { border-left-color: #16a34a; }
            .bp-envelope-warning { border-left-color: #f59e0b; }
            .bp-envelope-danger { border-left-color: #dc2626; }
            .bp-progress { width: 100%; background: #e5e7eb; border-radius: 999px; height: 10px; overflow: hidden; }
            .bp-progress-fill { height: 10px; border-radius: 999px; }
            .bp-progress-ok { background: #16a34a; }
            .bp-progress-warning { background: #f59e0b; }
            .bp-progress-danger { background: #dc2626; }
            .bp-segmented .q-radio { border: 1px solid #d1d5db; border-radius: 8px; padding: 8px 12px; background: #fff; min-width: 130px; justify-content: center; }
            input::-webkit-outer-spin-button,
            input::-webkit-inner-spin-button { -webkit-appearance: none; margin: 0; }
            input[type=number] { -moz-appearance: textfield; }
            @media (max-width: 980px) {
                .bp-two-col { grid-template-columns: 1fr; }
            }
            @media (max-width: 700px) {
                .bp-shell, .bp-page { padding-left: 16px; padding-right: 16px; }
            }
        </style>
        """,
        shared=True,
    )

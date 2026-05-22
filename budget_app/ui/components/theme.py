"""Shared NiceGUI theme."""

from __future__ import annotations

from nicegui import ui


def add_theme() -> None:
    ui.add_head_html(
        """
        <style>
            body { background: #e6edf7; color: #111827; overflow-x: hidden; }
            .q-page { background: radial-gradient(circle at 8% 0%, #bff3e7 0, transparent 25%), radial-gradient(circle at 92% 7%, #ffcdd7 0, transparent 24%), radial-gradient(circle at 58% 105%, #dbeafe 0, transparent 28%), #e6edf7; }
            .bp-shell { width: 100%; max-width: none; margin: 0; padding: 0 clamp(20px, 2.4vw, 48px); }
            .bp-header { background: rgba(255, 255, 255, .88); border-bottom: 1px solid #dbe3ef; box-shadow: 0 10px 30px rgb(15 23 42 / 0.08); backdrop-filter: blur(14px); }
            .bp-brand-icon { font-size: 46px; }
            .bp-brand-title { font-size: 34px; line-height: 42px; font-weight: 900; letter-spacing: 0; }
            .bp-nav { background: rgba(255, 255, 255, .86); border-bottom: 1px solid #dbe3ef; backdrop-filter: blur(12px); }
            .bp-nav-link { color: #374151; padding: 22px 22px; border-bottom: 5px solid transparent; text-decoration: none; white-space: nowrap; font-size: 22px; line-height: 30px; font-weight: 800; min-height: 76px; display: inline-flex; align-items: center; }
            .bp-nav-link .q-icon { font-size: 30px; }
            .bp-nav-link:hover { color: #111827; border-color: #fb7185; }
            .bp-nav-active { color: #0f766e; border-color: #0f766e; }
            .bp-page { width: 100%; max-width: none; margin: 0; padding: 22px clamp(20px, 2.4vw, 48px) 28px; }
            .bp-card { background: rgba(255, 255, 255, .9); border: 1px solid #d3deec; border-radius: 8px; box-shadow: 0 18px 34px -28px rgb(15 23 42 / .55); }
            .bp-dashboard-panel { background: linear-gradient(135deg, rgba(255,255,255,.9), rgba(240,253,250,.86)); border: 1px solid #cbdfea; border-radius: 8px; box-shadow: 0 24px 42px -32px rgb(15 23 42 / .45); }
            .bp-card-hover { transition: box-shadow 160ms ease, transform 160ms ease; }
            .bp-card-hover:hover { box-shadow: 0 12px 18px -12px rgb(17 24 39 / 0.25); transform: translateY(-1px); }
            .bp-muted { color: #6b7280; }
            .bp-title { font-size: 34px; line-height: 42px; font-weight: 800; color: #111827; letter-spacing: 0; }
            .bp-section-title { font-size: 23px; line-height: 31px; font-weight: 800; color: #111827; letter-spacing: 0; }
            .bp-page, .bp-card, .q-field, .q-table, .q-btn, .q-radio, .q-checkbox { font-size: 20px; }
            .q-field__label, .q-table th { font-size: 18px; }
            .q-field__native, .q-field__input { font-size: 20px; }
            .q-table tbody td { font-size: 19px; }
            .q-table th { font-weight: 850; }
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
            .bp-stat-card { min-height: 158px; }
            .bp-stat-card .text-sm { font-size: 17px; line-height: 24px; }
            .bp-stat-card .text-xs { font-size: 15px; line-height: 22px; }
            .bp-stat-card .text-2xl { font-size: 34px; line-height: 40px; }
            .bp-stat-value { font-variant-numeric: tabular-nums; white-space: nowrap; overflow-wrap: anywhere; }
            .bp-hero-stat { background: linear-gradient(135deg, #0f766e, #2563eb 58%, #e11d48); color: #fff; border: 0; overflow: hidden; }
            .bp-hero-stat .q-icon { opacity: .9; }
            .bp-account-strip { display: grid; grid-template-columns: minmax(260px, .9fr) minmax(0, 1.7fr); gap: 18px; width: 100%; align-items: stretch; }
            .bp-account-total { background: linear-gradient(135deg, #111827, #0f766e); color: #fff; border-radius: 8px; padding: 22px; min-height: 160px; display: flex; flex-direction: column; justify-content: space-between; }
            .bp-account-list { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; width: 100%; }
            .bp-account-mini { background: #f8fafc; border: 1px solid #e5e7eb; border-radius: 8px; padding: 14px; min-width: 0; }
            .bp-account-mini-value { font-size: 22px; line-height: 28px; font-weight: 800; font-variant-numeric: tabular-nums; overflow-wrap: anywhere; }
            .bp-grid-desktop { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 18px; width: 100%; }
            .bp-kpi-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 18px; width: 100%; align-items: stretch; }
            .bp-two-col { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 20px; width: 100%; align-items: start; }
            .bp-dashboard-charts { display: grid; grid-template-columns: minmax(300px, .75fr) minmax(520px, 1.25fr); gap: 20px; width: 100%; align-items: start; }
            .bp-chart-card {
                height: 540px;
                overflow: hidden;
            }
            .bp-chart-header {
                min-height: 54px;
                margin-bottom: 12px;
            }
            .bp-chart-canvas {
                height: 435px;
                min-height: 435px;
            }
            .bp-chart-canvas-compact {
                height: 360px;
                min-height: 360px;
            }
            .bp-chart-caption {
                min-height: 34px;
                margin-bottom: 8px;
                font-size: 22px;
                line-height: 30px;
            }
            .bp-pill { border-radius: 999px; padding: 4px 10px; font-size: 16px; font-weight: 800; display: inline-flex; align-items: center; gap: 4px; }
            .bp-income-pill { background: #dcfce7; color: #166534; }
            .bp-expense-pill { background: #fee2e2; color: #991b1b; }
            .bp-bank-pill { background: #dbeafe; color: #1d4ed8; }
            .bp-cash-pill { background: #fef3c7; color: #92400e; }
            .bp-primary-btn { background: #2563eb; color: #fff; }
            .bp-secondary-btn { background: #eef2f7; color: #374151; }
            .bp-danger-btn { background: #dc2626; color: #fff; }
            .bp-header-action {
                width: 150px;
                min-width: 150px;
                height: 48px;
                min-height: 48px;
                padding: 0 16px !important;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                line-height: 1;
                vertical-align: middle;
            }
            .bp-header-action .q-btn__content {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                gap: 10px;
                flex-wrap: nowrap;
                white-space: nowrap;
                width: 100%;
            }
            .bp-header-action .q-icon {
                width: 24px;
                min-width: 24px;
                height: 24px;
                font-size: 24px;
                line-height: 24px;
                margin: 0;
            }
            .bp-darkmode-btn {
                width: 170px;
                min-width: 170px;
            }
            .bp-envelope-card { border-left: 5px solid #2563eb; min-height: 155px; }
            .bp-envelope-ok { border-left-color: #16a34a; }
            .bp-envelope-warning { border-left-color: #f59e0b; }
            .bp-envelope-danger { border-left-color: #dc2626; }
            .bp-progress { width: 100%; background: #e5e7eb; border-radius: 999px; height: 10px; overflow: hidden; }
            .bp-progress-fill { height: 10px; border-radius: 999px; }
            .bp-progress-ok { background: #16a34a; }
            .bp-progress-warning { background: #f59e0b; }
            .bp-progress-danger { background: #dc2626; }
            .bp-type-toggle { display: inline-flex; gap: 8px; box-shadow: none; border-radius: 8px; overflow: visible; }
            .bp-type-option {
                min-width: 150px;
                min-height: 56px;
                border-radius: 8px !important;
                border: 2px solid transparent !important;
                font-weight: 850;
                box-shadow: none !important;
            }
            .bp-type-income,
            .bp-type-expense {
                background: #e5e7eb !important;
                border-color: #cbd5e1 !important;
                color: #64748b !important;
                box-shadow: none !important;
            }
            .bp-type-income.is-active {
                background: #16a34a !important;
                border-color: #16a34a !important;
                color: #ffffff !important;
                box-shadow: 0 0 0 3px rgb(22 163 74 / .24), 0 10px 18px -14px rgb(21 128 61 / .75) !important;
            }
            .bp-type-expense.is-active {
                background: #dc2626 !important;
                border-color: #dc2626 !important;
                color: #ffffff !important;
                box-shadow: 0 0 0 3px rgb(220 38 38 / .24), 0 10px 18px -14px rgb(185 28 28 / .75) !important;
            }
            .bp-type-toggle .q-btn,
            .bp-type-toggle .q-btn-group .q-btn {
                min-width: 150px;
                min-height: 56px;
                border-radius: 8px !important;
                border: 2px solid transparent !important;
                font-weight: 850;
                box-shadow: none !important;
            }
            .bp-type-toggle .q-btn:first-child,
            .bp-type-toggle .q-btn:nth-of-type(1),
            .bp-type-toggle .q-btn-group .q-btn:first-child {
                background: #e5e7eb !important;
                border-color: #cbd5e1 !important;
                color: #64748b !important;
            }
            .bp-type-toggle .q-btn:first-child.bg-primary,
            .bp-type-toggle .q-btn:nth-of-type(1).bg-primary,
            .bp-type-toggle .q-btn:nth-of-type(1).q-btn--active,
            .bp-type-toggle .q-btn:first-child[aria-pressed="true"],
            .bp-type-toggle .q-btn-group .q-btn:first-child.bg-primary,
            .bp-type-toggle .q-btn-group .q-btn:first-child[aria-pressed="true"] {
                background: #16a34a !important;
                border-color: #16a34a !important;
                color: #ffffff !important;
                box-shadow: 0 0 0 3px rgb(22 163 74 / .24) !important;
            }
            .bp-type-toggle .q-btn:last-child,
            .bp-type-toggle .q-btn:nth-of-type(2),
            .bp-type-toggle .q-btn-group .q-btn:last-child {
                background: #e5e7eb !important;
                border-color: #cbd5e1 !important;
                color: #64748b !important;
            }
            .bp-type-toggle .q-btn:last-child.bg-primary,
            .bp-type-toggle .q-btn:nth-of-type(2).bg-primary,
            .bp-type-toggle .q-btn:nth-of-type(2).q-btn--active,
            .bp-type-toggle .q-btn:last-child[aria-pressed="true"],
            .bp-type-toggle .q-btn-group .q-btn:last-child.bg-primary,
            .bp-type-toggle .q-btn-group .q-btn:last-child[aria-pressed="true"] {
                background: #dc2626 !important;
                border-color: #dc2626 !important;
                color: #ffffff !important;
                box-shadow: 0 0 0 3px rgb(220 38 38 / .24) !important;
            }
            .bp-type-toggle .bp-type-income.is-active {
                background: #15803d !important;
                border-color: #16a34a !important;
                color: #ffffff !important;
            }
            .bp-type-toggle .bp-type-expense.is-active {
                background: #dc2626 !important;
                border-color: #b91c1c !important;
                color: #ffffff !important;
            }
            .bp-type-toggle .bp-type-option {
                opacity: 1;
                transition: background-color 140ms ease, border-color 140ms ease, box-shadow 140ms ease, opacity 140ms ease, transform 140ms ease;
            }
            .bp-type-toggle .bp-type-income:not(.is-active),
            .bp-type-toggle .bp-type-expense:not(.is-active) {
                background: #e5e7eb !important;
                border-color: #cbd5e1 !important;
                color: #64748b !important;
                box-shadow: none !important;
                transform: none;
            }
            .bp-type-toggle .bp-type-income.is-active {
                background: #15803d !important;
                border-color: #22c55e !important;
                color: #ffffff !important;
                box-shadow: 0 0 0 3px rgb(34 197 94 / .24), 0 10px 18px -14px rgb(21 128 61 / .75) !important;
                transform: translateY(-1px);
            }
            .bp-type-toggle .bp-type-expense.is-active {
                background: #dc2626 !important;
                border-color: #ef4444 !important;
                color: #ffffff !important;
                box-shadow: 0 0 0 3px rgb(248 113 113 / .24), 0 10px 18px -14px rgb(185 28 28 / .75) !important;
                transform: translateY(-1px);
            }
            .bp-recurring-card {
                width: min(100%, 520px);
                background: #f8fafc;
                border: 1px solid #dbe3ef;
                color: #111827;
            }
            .bp-recurring-card .q-checkbox__label {
                color: #111827;
                font-weight: 700;
            }
            .bp-recurring-card .q-field__control {
                background: #ffffff;
            }
            .bp-type-toggle {
                display: inline-flex;
                gap: 0;
                padding: 0;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                background: #ffffff;
                box-shadow: 0 2px 5px rgb(15 23 42 / .16);
                overflow: hidden;
            }
            .bp-type-toggle-compact {
                width: max-content;
                max-width: max-content;
                justify-self: start;
            }
            .bp-type-toggle .bp-type-option,
            .bp-type-toggle .bp-type-income,
            .bp-type-toggle .bp-type-expense,
            .bp-type-toggle .bp-type-income:not(.is-active),
            .bp-type-toggle .bp-type-expense:not(.is-active) {
                min-width: 150px;
                min-height: 48px;
                border: 0 !important;
                border-radius: 0 !important;
                background: #ffffff !important;
                color: #111827 !important;
                box-shadow: none !important;
                transform: none;
                opacity: 1;
            }
            .bp-type-toggle .bp-type-option:first-child {
                border-radius: 7px 0 0 7px !important;
            }
            .bp-type-toggle .bp-type-option:last-child {
                border-radius: 0 7px 7px 0 !important;
            }
            .bp-type-toggle .bp-type-option.is-active,
            .bp-type-toggle .bp-type-income.is-active,
            .bp-type-toggle .bp-type-expense.is-active {
                background: #5a9bd8 !important;
                color: #ffffff !important;
                border: 0 !important;
                box-shadow: none !important;
                transform: none;
            }
            .bp-month-card { min-height: 158px; position: relative; overflow: hidden; background: #5a9bd8 !important; color: #fff; border-color: #4f8fca; box-shadow: 0 10px 18px -12px rgb(37 99 235 / .55); }
            .bp-month-card .bp-muted, .bp-month-card .text-gray-900 { color: #eef6ff !important; }
            .bp-month-value { font-size: 34px; line-height: 40px; font-weight: 850; text-align: center; color: #fff !important; }
            .bp-month-arrow { opacity: .96; background: rgba(255,255,255,.95); color: #2f7fc2; transition: opacity 140ms ease, transform 140ms ease; box-shadow: 0 10px 20px -16px rgb(15 23 42 / .6); }
            .bp-month-card:hover .bp-month-arrow { opacity: 1; transform: scale(1.08); }
            .bp-compact-metrics { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; }
            .bp-metric-box { background: #f8fafc; border: 1px solid #e5e7eb; border-radius: 8px; padding: 8px 10px; min-width: 0; }
            .bp-metric-box .bp-money { font-size: 16px; text-align: left; overflow-wrap: anywhere; white-space: normal; }
            @media print {
                .bp-header, .bp-nav, .q-btn { display: none !important; }
                @page { size: A4 landscape; margin: 8mm; }
                body, .q-page { background: #fff !important; }
                .bp-page { max-width: none; padding: 0; gap: 12px; }
                .bp-card, .bp-dashboard-panel { box-shadow: none; break-inside: avoid; page-break-inside: avoid; background: #fff !important; overflow: visible !important; }
                .bp-dashboard-charts { grid-template-columns: repeat(2, minmax(0, 1fr)) !important; gap: 10px; align-items: stretch; }
                .bp-two-col, .bp-account-strip { grid-template-columns: 1fr !important; gap: 12px; }
                .bp-grid-desktop, .bp-kpi-grid { grid-template-columns: repeat(2, minmax(0, 1fr)) !important; gap: 10px; }
                .bp-card.p-6, .bp-dashboard-panel.p-5 { padding: 12px !important; }
                .bp-dashboard-charts [style*="height"], .bp-dashboard-charts .h-96, .bp-chart-canvas, .bp-chart-canvas-compact { height: 300px !important; min-height: 300px !important; }
                canvas, svg { max-width: 100% !important; }
                .q-table__bottom { display: none !important; }
            }
            input::-webkit-outer-spin-button,
            input::-webkit-inner-spin-button { -webkit-appearance: none; margin: 0; }
            input[type=number] { -moz-appearance: textfield; }
            @media (max-width: 980px) {
                .bp-two-col, .bp-dashboard-charts { grid-template-columns: 1fr; }
                .bp-account-strip { grid-template-columns: 1fr; }
                .bp-kpi-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
                .bp-nav-link { font-size: 19px; line-height: 27px; min-height: 64px; padding: 18px 15px; }
            }
            @media (max-width: 700px) {
                .bp-shell, .bp-page { padding-left: 16px; padding-right: 16px; }
                .bp-header-action { width: 48px; min-width: 48px; padding: 0 !important; }
                .bp-darkmode-btn { width: 48px; min-width: 48px; }
                .bp-header-action .q-btn__content span:not(.q-icon) { display: none; }
                .bp-kpi-grid, .bp-grid-desktop { grid-template-columns: 1fr; }
                .bp-nav-link { font-size: 17px; line-height: 24px; min-height: 58px; padding: 16px 12px; }
                .bp-nav-link .q-icon { font-size: 24px; }
            }
        </style>
        <script>
            window.bpUpdateDarkModeButtons = (isDark) => {
                document.querySelectorAll('.bp-darkmode-btn').forEach((button) => {
                    const icon = button.querySelector('.q-icon');
                    const label = Array.from(button.querySelectorAll('.q-btn__content span')).find((element) => !element.classList.contains('q-icon'));
                    if (icon) {
                        icon.textContent = isDark ? 'light_mode' : 'dark_mode';
                    }
                    if (label) {
                        label.textContent = isDark ? 'Lightmode' : 'Darkmode';
                    }
                    button.setAttribute('aria-label', isDark ? 'Lightmode aktivieren' : 'Darkmode aktivieren');
                });
            };
            window.addEventListener('load', () => {
                const isDark = localStorage.getItem('bpDarkMode') === '1';
                if (isDark) {
                    document.body.classList.add('bp-dark');
                }
                window.bpUpdateDarkModeButtons(isDark);
                if (sessionStorage.getItem('bpPrintAfterLoad') === '1') {
                    sessionStorage.removeItem('bpPrintAfterLoad');
                    window.setTimeout(() => window.print(), 650);
                }
            });
        </script>
        <style>
            body.bp-dark { background: #08111f; color: #e5edf7; }
            body.bp-dark .q-page { background: radial-gradient(circle at 8% 0%, #083f3c 0, transparent 25%), radial-gradient(circle at 92% 8%, #3b164f 0, transparent 24%), radial-gradient(circle at 55% 110%, #102a55 0, transparent 28%), #08111f; }
            body.bp-dark .bp-header, body.bp-dark .bp-nav { background: rgba(8, 17, 31, .88); border-color: #1e3554; box-shadow: 0 16px 36px rgb(0 0 0 / .32); }
            body.bp-dark .bp-brand-title, body.bp-dark .bp-title, body.bp-dark .bp-section-title, body.bp-dark .text-gray-900 { color: #f8fafc !important; }
            body.bp-dark .bp-brand-icon { color: #5eead4 !important; }
            body.bp-dark .bp-page, body.bp-dark .bp-card, body.bp-dark .q-field, body.bp-dark .q-table { color: #e5edf7; }
            body.bp-dark .bp-card { background: rgba(15, 23, 42, .86); border-color: #27415f; box-shadow: 0 18px 38px -24px rgb(0 0 0 / .85); }
            body.bp-dark .bp-dashboard-panel { background: linear-gradient(135deg, rgba(15,23,42,.9), rgba(11,59,62,.78)); border-color: #28556a; }
            body.bp-dark .bp-muted { color: #aebfd2; }
            body.bp-dark .bp-nav-link { color: #cbd5e1; }
            body.bp-dark .bp-nav-link:hover { color: #f8fafc; border-color: #60a5fa; }
            body.bp-dark .bp-nav-active { color: #5eead4; border-color: #5eead4; }
            body.bp-dark .bp-primary-btn { background: #3b82f6; color: #fff; }
            body.bp-dark .bp-secondary-btn { background: #1d4f7a; color: #f8fafc; border: 1px solid #3b82f6; }
            body.bp-dark .bp-danger-btn { background: #b91c1c; color: #fff; }
            body.bp-dark .bp-positive { color: #4ade80; }
            body.bp-dark .bp-warning { color: #fbbf24; }
            body.bp-dark .bp-negative { color: #f87171; }
            body.bp-dark .bp-blue { color: #93c5fd; }
            body.bp-dark .bp-account-total { background: linear-gradient(135deg, #06111f, #0f766e); }
            body.bp-dark .bp-account-mini, body.bp-dark .bp-metric-box { background: rgba(15, 23, 42, .92); border-color: #334e68; }
            body.bp-dark .bp-table { background: rgba(15,23,42,.92); }
            body.bp-dark .bp-table .q-table__top, body.bp-dark .bp-table thead tr { background: #102033; }
            body.bp-dark .bp-table tbody tr:hover { background: #172b43; }
            body.bp-dark .bp-table th { color: #aebfd2; }
            body.bp-dark .q-table tbody td { color: #e5edf7; border-color: #253950; }
            body.bp-dark .q-field__control { background: rgba(15, 23, 42, .7); color: #e5edf7; }
            body.bp-dark .q-field__native, body.bp-dark .q-field__input, body.bp-dark .q-field__label { color: #e5edf7; }
            body.bp-dark .q-field__marginal { color: #aebfd2; }
            body.bp-dark .q-menu, body.bp-dark .q-dialog .q-card { background: #111f32; color: #e5edf7; }
            body.bp-dark .bp-income-pill { background: #064e3b; color: #bbf7d0; }
            body.bp-dark .bp-expense-pill { background: #7f1d1d; color: #fecaca; }
            body.bp-dark .bp-bank-pill { background: #1e3a8a; color: #bfdbfe; }
            body.bp-dark .bp-cash-pill { background: #78350f; color: #fde68a; }
            body.bp-dark .bp-type-income,
            body.bp-dark .bp-type-expense { background: #334155 !important; border-color: #475569 !important; color: #cbd5e1 !important; }
            body.bp-dark .bp-type-income.is-active { background: #22c55e !important; border-color: #22c55e !important; color: #052e16 !important; }
            body.bp-dark .bp-type-expense.is-active { background: #ef4444 !important; border-color: #ef4444 !important; color: #ffffff !important; }
            body.bp-dark .bp-type-toggle .q-btn:first-child,
            body.bp-dark .bp-type-toggle .q-btn:nth-of-type(1),
            body.bp-dark .bp-type-toggle .q-btn-group .q-btn:first-child { background: #334155 !important; border-color: #475569 !important; color: #cbd5e1 !important; }
            body.bp-dark .bp-type-toggle .q-btn:first-child.bg-primary,
            body.bp-dark .bp-type-toggle .q-btn:nth-of-type(1).bg-primary,
            body.bp-dark .bp-type-toggle .q-btn:nth-of-type(1).q-btn--active,
            body.bp-dark .bp-type-toggle .q-btn:first-child[aria-pressed="true"],
            body.bp-dark .bp-type-toggle .q-btn-group .q-btn:first-child.bg-primary,
            body.bp-dark .bp-type-toggle .q-btn-group .q-btn:first-child[aria-pressed="true"] { background: #22c55e !important; border-color: #22c55e !important; color: #052e16 !important; }
            body.bp-dark .bp-type-toggle .q-btn:last-child,
            body.bp-dark .bp-type-toggle .q-btn:nth-of-type(2),
            body.bp-dark .bp-type-toggle .q-btn-group .q-btn:last-child { background: #334155 !important; border-color: #475569 !important; color: #cbd5e1 !important; }
            body.bp-dark .bp-type-toggle .q-btn:last-child.bg-primary,
            body.bp-dark .bp-type-toggle .q-btn:nth-of-type(2).bg-primary,
            body.bp-dark .bp-type-toggle .q-btn:nth-of-type(2).q-btn--active,
            body.bp-dark .bp-type-toggle .q-btn:last-child[aria-pressed="true"],
            body.bp-dark .bp-type-toggle .q-btn-group .q-btn:last-child.bg-primary,
            body.bp-dark .bp-type-toggle .q-btn-group .q-btn:last-child[aria-pressed="true"] { background: #ef4444 !important; border-color: #ef4444 !important; color: #ffffff !important; }
            body.bp-dark .bp-type-toggle .bp-type-income.is-active { background: #22c55e !important; border-color: #22c55e !important; color: #052e16 !important; }
            body.bp-dark .bp-type-toggle .bp-type-expense.is-active { background: #ef4444 !important; border-color: #ef4444 !important; color: #ffffff !important; }
            body.bp-dark .bp-type-toggle .bp-type-option { opacity: 1; }
            body.bp-dark .bp-type-toggle .bp-type-income:not(.is-active),
            body.bp-dark .bp-type-toggle .bp-type-expense:not(.is-active) {
                background: #334155 !important;
                border-color: #475569 !important;
                color: #cbd5e1 !important;
                box-shadow: none !important;
                transform: none;
            }
            body.bp-dark .bp-type-toggle .bp-type-income.is-active {
                background: #16a34a !important;
                border-color: #86efac !important;
                color: #ffffff !important;
                box-shadow: 0 0 0 3px rgb(74 222 128 / .28), 0 12px 20px -14px rgb(34 197 94 / .85) !important;
            }
            body.bp-dark .bp-type-toggle .bp-type-expense.is-active {
                background: #ef4444 !important;
                border-color: #fca5a5 !important;
                color: #ffffff !important;
                box-shadow: 0 0 0 3px rgb(248 113 113 / .30), 0 12px 20px -14px rgb(239 68 68 / .85) !important;
            }
            body.bp-dark .bp-recurring-card {
                background: #14263d;
                border: 1px solid #3b82f6;
                color: #eaf2ff;
                box-shadow: 0 16px 30px -24px rgb(0 0 0 / .9);
            }
            body.bp-dark .bp-recurring-card .bp-muted { color: #bfd4ec; }
            body.bp-dark .bp-recurring-card .q-checkbox__label { color: #f8fafc; }
            body.bp-dark .bp-recurring-card .q-checkbox__inner { color: #93c5fd; }
            body.bp-dark .bp-recurring-card .q-field__control {
                background: #0f1e31;
                border-color: #426281;
                color: #f8fafc;
            }
            body.bp-dark .bp-recurring-card .q-field__native,
            body.bp-dark .bp-recurring-card .q-field__input,
            body.bp-dark .bp-recurring-card .q-field__label,
            body.bp-dark .bp-recurring-card .q-field__marginal {
                color: #f8fafc;
            }
            body.bp-dark .bp-type-toggle {
                border-color: #172033;
                background: #071223;
                box-shadow: 0 2px 6px rgb(0 0 0 / .42);
            }
            body.bp-dark .bp-type-toggle .bp-type-option,
            body.bp-dark .bp-type-toggle .bp-type-income,
            body.bp-dark .bp-type-toggle .bp-type-expense,
            body.bp-dark .bp-type-toggle .bp-type-income:not(.is-active),
            body.bp-dark .bp-type-toggle .bp-type-expense:not(.is-active) {
                background: #071223 !important;
                color: #e5edf7 !important;
                border: 0 !important;
                box-shadow: none !important;
                transform: none;
                opacity: 1;
            }
            body.bp-dark .bp-type-toggle .bp-type-option.is-active,
            body.bp-dark .bp-type-toggle .bp-type-income.is-active,
            body.bp-dark .bp-type-toggle .bp-type-expense.is-active {
                background: #5a9bd8 !important;
                color: #ffffff !important;
                border: 0 !important;
                box-shadow: none !important;
                transform: none;
            }
            body.bp-dark .bp-month-card { background: #1d4f7a !important; border-color: #3b82f6; }
            body.bp-dark .bp-month-card .bp-muted, body.bp-dark .bp-month-card .text-gray-900, body.bp-dark .bp-month-value { color: #eff6ff !important; }
            body.bp-dark .bp-month-arrow { background: #0f172a; color: #93c5fd; border: 1px solid #3b82f6; }
            body.bp-dark .bp-progress { background: #24364d; }
            body.bp-dark .bg-blue-50 { background: #102a55 !important; }
            body.bp-dark .border-blue-200 { border-color: #2563eb !important; }
            body.bp-dark .text-blue-900 { color: #bfdbfe !important; }
            body.bp-dark .bg-red-50 { background: #450a0a !important; }
            body.bp-dark .border-red-200 { border-color: #dc2626 !important; }
            body.bp-dark .text-red-900 { color: #fecaca !important; }
            body.bp-dark .bg-amber-50 { background: #422006 !important; }
            body.bp-dark .border-amber-200 { border-color: #b45309 !important; }
            body.bp-dark .text-amber-800 { color: #fde68a !important; }
        </style>
        """,
        shared=True,
    )

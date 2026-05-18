"""Dashboard page."""

from __future__ import annotations

from collections import defaultdict

from nicegui import ui

from ...utils.date_utils import current_year_month, month_name, month_short_label, previous_months
from ...utils.format_utils import money
from ..components.cards import envelope_card, stat_card
from ..components.layout import empty_state, month_nav_card, page_container, page_title
from ..components.tables import transaction_table
from ..controllers import FinanceController
from .shared import account_balance


def _chart_number_formatter() -> str:
    return "(value) => Number(value).toLocaleString('de-CH')"


def register_overview_page(controller: FinanceController) -> None:
    @ui.page("/")
    def dashboard_page(year: int | None = None, month: int | None = None) -> None:
        current_year, current_month = current_year_month()
        year = year or current_year
        month = month or current_month
        data = controller.dashboard_data(year=year, month=month)
        all_transactions = controller.list_recent_transactions()
        accounts = controller.list_accounts()
        total_account_balance = sum(account_balance(account, all_transactions) for account in accounts)
        total_budget = sum(status.budget.limit_chf for status in data.budget_statuses)
        budgeted_category_ids = {status.budget.category_id for status in data.budget_statuses}
        budgeted_expenses = sum(
            transaction.amount_chf
            for transaction in data.transactions
            if transaction.transaction_type == "expense" and transaction.category_id in budgeted_category_ids
        )
        unbudgeted_expenses = sum(
            transaction.amount_chf
            for transaction in data.transactions
            if transaction.transaction_type == "expense" and transaction.category_id not in budgeted_category_ids
        )
        total_budget_remaining = total_budget - budgeted_expenses
        current_usage = (budgeted_expenses / total_budget * 100) if total_budget else 0
        monthly_comparison = []
        for comparison_year, comparison_month in previous_months(year, month):
            month_data = controller.dashboard_data(year=comparison_year, month=comparison_month)
            monthly_comparison.append(
                {
                    "month": month_short_label(comparison_year, comparison_month),
                    "income": round(month_data.overview.total_income_chf, 2),
                    "expenses": round(month_data.overview.total_expenses_chf, 2),
                }
            )

        with page_container("/"):
            page_title("Übersicht", "Dein Budgetstatus für den aktuellen Monat auf einen Blick.")

            with ui.card().classes("bp-card bp-hero-stat w-full p-7"):
                with ui.row().classes("w-full items-center justify-between gap-6"):
                    with ui.column().classes("gap-1"):
                        ui.label("Noch verfügbares Monatsbudget").classes("text-base text-blue-100")
                        ui.label(money(total_budget_remaining)).classes("text-5xl font-bold bp-stat-value")
                        ui.label(month_name(year, month)).classes("text-3xl font-bold text-blue-50")
                    ui.icon("savings").classes("text-7xl text-blue-100")

            if total_budget and total_budget_remaining < 0:
                with ui.element("div").classes("bg-red-50 border border-red-200 rounded-lg p-4 w-full"):
                    ui.label(f"Gesamtbudget um {money(abs(total_budget_remaining))} überschritten.").classes("font-semibold text-red-900")
            elif unbudgeted_expenses:
                with ui.element("div").classes("bg-amber-50 border border-amber-200 rounded-lg p-4 w-full"):
                    ui.label(
                        f"{money(unbudgeted_expenses)} Ausgaben liegen in Kategorien ohne Budget und werden nicht vom verfügbaren Budget abgezogen."
                    ).classes("text-sm text-amber-800")

            with ui.element("div").classes("bp-kpi-grid"):
                month_nav_card("/", year, month)
                stat_card("Einnahmen", money(data.overview.total_income_chf), "trending_up", "green", month_name(year, month))
                stat_card("Ausgaben", money(data.overview.total_expenses_chf), "trending_down", "red", month_name(year, month))
                stat_card("Kontostand", money(total_account_balance), "account_balance_wallet", "blue", "über alle Konten")
                stat_card("Budgetverbrauch", f"{current_usage:.0f}%", "percent", "amber" if current_usage >= 80 else "green")

            with ui.element("div").classes("bp-dashboard-panel w-full p-5"):
                with ui.row().classes("w-full items-center justify-between gap-4 mb-4"):
                    with ui.column().classes("gap-1"):
                        ui.label("Kontenübersicht").classes("bp-section-title")
                        ui.label("Schneller Blick darauf, wo dein Geld gerade liegt.").classes("bp-muted")
                    ui.button("Konten verwalten", icon="account_balance_wallet", on_click=lambda: ui.navigate.to("/accounts")).classes("bp-secondary-btn")
                if not accounts:
                    empty_state("account_balance_wallet", "Keine Konten vorhanden.", "Erstelle dein erstes Konto, damit dein Dashboard aussagekräftig wird.", "Konto erfassen", lambda: ui.navigate.to("/accounts"))
                else:
                    with ui.element("div").classes("bp-account-strip"):
                        with ui.element("div").classes("bp-account-total"):
                            with ui.column().classes("gap-1"):
                                ui.label("Gesamt verfügbar").classes("text-sm text-teal-100")
                                ui.label(money(total_account_balance)).classes("text-4xl font-bold bp-stat-value")
                            with ui.row().classes("items-center justify-between"):
                                ui.label(f"{len(accounts)} Konten").classes("text-teal-100")
                                ui.icon("payments").classes("text-4xl text-teal-100")
                        with ui.element("div").classes("bp-account-list"):
                            for account in accounts:
                                balance = account_balance(account, all_transactions)
                                is_cash = account.account_type == "Bargeld"
                                icon = "payments" if is_cash else "account_balance"
                                pill = "bp-cash-pill" if is_cash else "bp-bank-pill"
                                with ui.element("div").classes("bp-account-mini"):
                                    with ui.row().classes("w-full items-start justify-between gap-3 no-wrap"):
                                        with ui.column().classes("gap-1"):
                                            ui.label(account.name).classes("font-bold text-gray-900")
                                            ui.label(account.account_type).classes(f"bp-pill {pill}")
                                        ui.icon(icon).classes("text-2xl bp-muted")
                                    ui.label(money(balance)).classes(f"bp-account-mini-value mt-4 {'bp-positive' if balance >= 0 else 'bp-negative'}")

            with ui.element("div").classes("bp-two-col"):
                with ui.card().classes("bp-card w-full p-6"):
                    ui.label("Ausgaben nach Kategorie").classes("bp-section-title mb-4")
                    category_totals: dict[str, float] = defaultdict(float)
                    for transaction in data.transactions:
                        if transaction.transaction_type == "expense":
                            category_totals[transaction.category.name] += transaction.amount_chf
                    if category_totals:
                        ui.echart(
                            {
                                "tooltip": {"trigger": "item"},
                                "legend": {"bottom": 0},
                                "series": [
                                    {
                                        "type": "pie",
                                        "radius": ["45%", "72%"],
                                        "label": {"show": False},
                                        "data": [{"name": name, "value": round(value, 2)} for name, value in category_totals.items()],
                                    }
                                ],
                            }
                        ).classes("h-80 w-full")
                    else:
                        empty_state("pie_chart", "Noch keine Transaktionen erfasst.", "Erfasse deine erste Ausgabe.", "Ausgabe erfassen", lambda: ui.navigate.to("/transactions"))

                with ui.card().classes("bp-card w-full p-6"):
                    ui.label("Einnahmen vs. Ausgaben").classes("bp-section-title mb-4")
                    ui.echart(
                        {
                            "tooltip": {"trigger": "axis", ":valueFormatter": _chart_number_formatter()},
                            "legend": {"bottom": 0},
                            "grid": {"left": 52, "right": 24, "top": 24, "bottom": 58},
                            "xAxis": {"type": "category", "data": [item["month"] for item in monthly_comparison]},
                            "yAxis": {"type": "value", "axisLabel": {":formatter": _chart_number_formatter()}},
                            "series": [
                                {"name": "Einnahmen", "type": "bar", "itemStyle": {"color": "#16a34a"}, "data": [item["income"] for item in monthly_comparison]},
                                {"name": "Ausgaben", "type": "bar", "itemStyle": {"color": "#dc2626"}, "data": [item["expenses"] for item in monthly_comparison]},
                            ],
                        }
                    ).classes("h-80 w-full")

            with ui.card().classes("bp-card w-full p-6"):
                with ui.row().classes("w-full items-center justify-between"):
                    ui.label("Budgetstatus").classes("bp-section-title")
                    ui.button("Budget planen", icon="inventory_2", on_click=lambda: ui.navigate.to("/budget")).classes("bp-secondary-btn")
                if not data.budget_statuses:
                    empty_state("inventory_2", "Lege dein erstes Budget fest.", "Umschläge machen sichtbar, wie viel je Kategorie noch frei ist.", "Budget erfassen", lambda: ui.navigate.to("/budget"))
                else:
                    with ui.element("div").classes("bp-grid-desktop mt-4"):
                        for status in data.budget_statuses:
                            envelope_card(status)

            with ui.card().classes("bp-card w-full p-6"):
                ui.label("Letzte Transaktionen im aktuellen Monat").classes("bp-section-title mb-4")
                transaction_table(data.transactions[:10], "Noch keine Transaktionen erfasst.")

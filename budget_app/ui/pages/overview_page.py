"""Dashboard page."""

from __future__ import annotations

from calendar import monthrange
from collections import defaultdict

from nicegui import ui

from ...utils.date_utils import current_year_month, month_name, month_short_label, previous_month, previous_months
from ...utils.format_utils import money
from ..components.cards import envelope_card, progress_bar, stat_card
from ..components.layout import empty_state, month_nav_card, page_container, page_title
from ..components.tables import transaction_table
from ..controllers import FinanceController
from .shared import account_balance


def _chart_number_formatter() -> str:
    return "(value) => Number(value).toLocaleString('de-CH')"


def _expense_progress_options(controller: FinanceController, year: int, month: int) -> dict:
    comparison_months = []
    cursor_year, cursor_month = year, month
    for _ in range(3):
        cursor_year, cursor_month = previous_month(cursor_year, cursor_month)
        comparison_months.append((cursor_year, cursor_month))
    comparison_months.reverse()

    day_count = monthrange(year, month)[1]
    days = list(range(1, day_count + 1))
    previous_cumulative: list[list[float]] = []
    for comparison_year, comparison_month in comparison_months:
        month_data = controller.dashboard_data(year=comparison_year, month=comparison_month)
        cumulative = []
        running_total = 0.0
        transactions_by_day: dict[int, float] = defaultdict(float)
        for transaction in month_data.transactions:
            if transaction.transaction_type == "expense":
                transactions_by_day[transaction.transaction_date.day] += transaction.amount_chf
        comparison_day_count = monthrange(comparison_year, comparison_month)[1]
        for day in days:
            if day <= comparison_day_count:
                running_total += transactions_by_day.get(day, 0.0)
            cumulative.append(round(running_total, 2))
        previous_cumulative.append(cumulative)

    average_cumulative = [
        round(sum(month_values[day_index] for month_values in previous_cumulative) / len(previous_cumulative), 2)
        for day_index in range(day_count)
    ]

    current_data = controller.dashboard_data(year=year, month=month)
    current_by_day: dict[int, float] = defaultdict(float)
    max_actual_day = 0
    for transaction in current_data.transactions:
        if transaction.transaction_type == "expense":
            current_by_day[transaction.transaction_date.day] += transaction.amount_chf
            max_actual_day = max(max_actual_day, transaction.transaction_date.day)
    current_cumulative: list[float | None] = []
    running_total = 0.0
    for day in days:
        if max_actual_day and day <= max_actual_day:
            running_total += current_by_day.get(day, 0.0)
            current_cumulative.append(round(running_total, 2))
        else:
            current_cumulative.append(None)

    return {
        "backgroundColor": "transparent",
        "tooltip": {"trigger": "axis", ":valueFormatter": _chart_number_formatter()},
        "legend": {"top": 2, "left": 0, "textStyle": {"fontSize": 14, "color": "#4b5563"}},
        "grid": {"left": 64, "right": 26, "top": 82, "bottom": 56},
        "xAxis": {
            "type": "category",
            "name": "Tag im Monat",
            "nameLocation": "middle",
            "nameGap": 34,
            "data": [str(day) for day in days],
            "axisLine": {"lineStyle": {"color": "#cbd5e1"}},
            "axisTick": {"show": False},
            "axisLabel": {"color": "#64748b", "interval": 4},
        },
        "yAxis": {
            "type": "value",
            "name": "Kumulierte Ausgaben (CHF)",
            "nameLocation": "middle",
            "nameGap": 48,
            "axisLine": {"show": False},
            "axisTick": {"show": False},
            "axisLabel": {"color": "#64748b", ":formatter": _chart_number_formatter()},
            "splitLine": {"lineStyle": {"color": "#e5e7eb", "type": "dashed"}},
        },
        "series": [
            {
                "name": "Üblicherweise pro Monat",
                "type": "line",
                "smooth": True,
                "showSymbol": False,
                "lineStyle": {"width": 7, "color": "#6b7280", "cap": "round"},
                "itemStyle": {"color": "#6b7280"},
                "data": average_cumulative,
            },
            {
                "name": f"{max_actual_day or 1}. {month_name(year, month).split()[0]}",
                "type": "line",
                "smooth": True,
                "connectNulls": False,
                "symbolSize": 16,
                "lineStyle": {"width": 5, "color": "#0284c7", "cap": "round"},
                "itemStyle": {"color": "#0284c7", "borderColor": "#fff", "borderWidth": 3},
                "data": current_cumulative,
            },
        ],
    }


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

        with page_container("/", controller):
            page_title("Übersicht", "Dein Budgetstatus für den aktuellen Monat auf einen Blick.")

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
                stat_card("Noch verfügbares Monatsbudget", money(total_budget_remaining), "savings", "green" if total_budget_remaining >= 0 else "red", month_name(year, month))
                stat_card("Einnahmen", money(data.overview.total_income_chf), "trending_up", "green", month_name(year, month))
                stat_card("Ausgaben", money(data.overview.total_expenses_chf), "trending_down", "red", month_name(year, month))

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

            with ui.element("div").classes("bp-dashboard-charts"):
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
                                        "radius": ["48%", "82%"],
                                        "center": ["50%", "44%"],
                                        "label": {"show": False},
                                        "data": [{"name": name, "value": round(value, 2)} for name, value in category_totals.items()],
                                    }
                                ],
                            }
                        ).classes("h-96 w-full")
                    else:
                        empty_state("pie_chart", "Noch keine Transaktionen erfasst.", "Erfasse deine erste Ausgabe.", "Ausgabe erfassen", lambda: ui.navigate.to("/transactions"))

                with ui.card().classes("bp-card w-full p-6"):
                    with ui.row().classes("w-full items-center justify-between gap-4 mb-4"):
                        ui.label("Einnahmen vs. Ausgaben").classes("bp-section-title")
                        chart_mode = ui.toggle({"bars": "Vergleich", "lines": "Ausgabenverlauf"}, value="bars").props("toggle-color=primary")
                    chart_area = ui.column().classes("w-full")

                    def render_income_expense_chart() -> None:
                        chart_area.clear()
                        with chart_area:
                            if chart_mode.value == "lines":
                                ui.label(f"Im {month_name(year, month).split()[0]} haben Sie bis jetzt {money(data.overview.total_expenses_chf)} ausgegeben").classes("text-2xl font-bold text-gray-900 mb-1")
                                ui.echart(_expense_progress_options(controller, year, month)).classes("h-96 w-full")
                                return
                            ui.echart(
                                {
                                    "tooltip": {"trigger": "axis", ":valueFormatter": _chart_number_formatter()},
                                    "legend": {"bottom": 0},
                                    "grid": {"left": 58, "right": 26, "top": 30, "bottom": 58},
                                    "xAxis": {"type": "category", "data": [item["month"] for item in monthly_comparison]},
                                    "yAxis": {"type": "value", "axisLabel": {":formatter": _chart_number_formatter()}},
                                    "series": [
                                        {"name": "Einnahmen", "type": "bar", "itemStyle": {"color": "#16a34a"}, "data": [item["income"] for item in monthly_comparison]},
                                        {"name": "Ausgaben", "type": "bar", "itemStyle": {"color": "#dc2626"}, "data": [item["expenses"] for item in monthly_comparison]},
                                    ],
                                }
                            ).classes("h-96 w-full")

                    chart_mode.on_value_change(render_income_expense_chart)
                    render_income_expense_chart()

            with ui.card().classes("bp-card w-full p-6"):
                with ui.row().classes("w-full items-center justify-between"):
                    ui.label("Budgetstatus").classes("bp-section-title")
                    ui.button("Budget planen", icon="inventory_2", on_click=lambda: ui.navigate.to("/budget")).classes("bp-secondary-btn")
                if not data.budget_statuses:
                    empty_state("inventory_2", "Lege dein erstes Budget fest.", "Umschläge machen sichtbar, wie viel je Kategorie noch frei ist.", "Budget erfassen", lambda: ui.navigate.to("/budget"))
                else:
                    with ui.element("div").classes("bp-grid-desktop mt-4"):
                        with ui.element("div").classes("bp-account-total"):
                            with ui.column().classes("gap-1"):
                                ui.label("Alle Budgets").classes("text-sm text-teal-100")
                                ui.label(money(total_budget_remaining)).classes("text-4xl font-bold bp-stat-value")
                                ui.label(f"{money(budgeted_expenses)} von {money(total_budget)} verbraucht").classes("text-teal-100")
                            progress_bar(current_usage, "danger" if total_budget_remaining < 0 else "warning" if current_usage >= 80 else "ok")
                        for status in data.budget_statuses:
                            envelope_card(status)

            with ui.card().classes("bp-card w-full p-6"):
                ui.label("Letzte Transaktionen im aktuellen Monat").classes("bp-section-title mb-4")
                sorted_transactions = sorted(data.transactions, key=lambda item: (item.transaction_date, item.id or 0), reverse=True)
                transaction_table(sorted_transactions[:10], "Noch keine Transaktionen erfasst.")

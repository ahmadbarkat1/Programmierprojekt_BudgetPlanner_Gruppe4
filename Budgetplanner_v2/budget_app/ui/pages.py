"""NiceGUI pages.

The page class owns only UI code. User actions are delegated to the controller,
which then calls services and DAOs.
"""

from __future__ import annotations

from collections import defaultdict
from datetime import date
from typing import Callable

from nicegui import ui

from ..domain.models import Account, Budget, Category, Transaction
from .controllers import FinanceController


class Pages:
    """Registers all NiceGUI routes."""

    def __init__(self, finance_controller: FinanceController) -> None:
        self._finance_controller = finance_controller

    def register(self) -> None:
        controller = self._finance_controller

        def money(value: float) -> str:
            return f"CHF {value:,.2f}".replace(",", "’")

        def month_label(year: int, month: int) -> str:
            return date(year, month, 1).strftime("%m.%Y")

        def parse_float(value: object, field_name: str) -> float:
            text = str(value or "").strip().replace("’", "").replace("'", "").replace(",", ".")
            if not text:
                raise ValueError(f"Bitte {field_name} erfassen.")
            return float(text)

        def parse_int(value: object, field_name: str) -> int:
            text = str(value or "").strip()
            if not text:
                raise ValueError(f"Bitte {field_name} erfassen.")
            return int(text)

        def number_input(label: str, placeholder: str = ""):
            return ui.input(label, placeholder=placeholder).props("inputmode=decimal").classes("w-full")

        def month_name(year: int, month: int) -> str:
            month_names = [
                "Januar",
                "Februar",
                "März",
                "April",
                "Mai",
                "Juni",
                "Juli",
                "August",
                "September",
                "Oktober",
                "November",
                "Dezember",
            ]
            return f"{month_names[month - 1]} {year}"

        def month_short_label(year: int, month: int) -> str:
            month_names = ["Jan", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"]
            return f"{month_names[month - 1]} {str(year)[-2:]}"

        def previous_months(year: int, month: int, count: int = 6) -> list[tuple[int, int]]:
            months: list[tuple[int, int]] = []
            cursor_year = year
            cursor_month = month
            for _ in range(count):
                months.append((cursor_year, cursor_month))
                cursor_month -= 1
                if cursor_month == 0:
                    cursor_month = 12
                    cursor_year -= 1
            return list(reversed(months))

        def current_month() -> tuple[int, int]:
            today = date.today()
            return today.year, today.month

        def account_balance(account: Account, transactions: list[Transaction]) -> float:
            balance = account.starting_balance_chf
            for transaction in transactions:
                if transaction.account_id != account.id:
                    continue
                if transaction.transaction_type == "income":
                    balance += transaction.amount_chf
                else:
                    balance -= transaction.amount_chf
            return round(balance, 2)

        def usage_count(items: list[Transaction], attribute: str, item_id: int | None) -> int:
            return sum(1 for item in items if getattr(item, attribute) == item_id)

        def category_type_label(category: Category) -> str:
            return "Einnahme" if category.category_type == "income" else "Ausgabe"

        def add_theme() -> None:
            ui.add_head_html(
                """
                <style>
                    body { background: #f9fafb; color: #111827; }
                    .q-page { background: #f9fafb; }
                    .bp-shell { max-width: 1280px; margin: 0 auto; padding: 0 24px; }
                    .bp-header { background: #fff; border-bottom: 1px solid #e5e7eb; box-shadow: 0 1px 2px rgb(0 0 0 / 0.04); }
                    .bp-nav { background: #fff; border-bottom: 1px solid #e5e7eb; }
                    .bp-nav-link { color: #4b5563; padding: 16px 8px; border-bottom: 2px solid transparent; text-decoration: none; white-space: nowrap; }
                    .bp-nav-link:hover { color: #111827; border-color: #d1d5db; }
                    .bp-nav-active { color: #2563eb; border-color: #3b82f6; }
                    .bp-page { max-width: 1280px; margin: 0 auto; padding: 32px 24px; }
                    .bp-card { background: #fff; border: 0; border-radius: 8px; box-shadow: 0 1px 3px rgb(0 0 0 / 0.10), 0 1px 2px rgb(0 0 0 / 0.06); }
                    .bp-card-hover { transition: box-shadow 160ms ease, transform 160ms ease; }
                    .bp-card-hover:hover { box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.10), 0 4px 6px -4px rgb(0 0 0 / 0.10); transform: translateY(-1px); }
                    .bp-muted { color: #6b7280; }
                    .bp-title { font-size: 28px; line-height: 36px; font-weight: 700; color: #111827; }
                    .bp-section-title { font-size: 21px; line-height: 30px; font-weight: 600; color: #111827; }
                    .bp-page, .bp-card, .q-field, .q-table, .q-btn { font-size: 16px; }
                    .q-field__label, .q-table th { font-size: 14px; }
                    .q-btn { font-weight: 600; }
                    .bp-table .q-table__top, .bp-table thead tr { background: #f9fafb; }
                    .bp-table th { color: #6b7280; text-transform: uppercase; letter-spacing: .04em; font-weight: 600; }
                    .bp-positive { color: #16a34a; }
                    .bp-negative { color: #dc2626; }
                    .bp-blue { color: #2563eb; }
                    .bp-money { font-variant-numeric: tabular-nums; white-space: nowrap; text-align: right; }
                    .bp-pill { border-radius: 999px; padding: 4px 10px; font-size: 12px; font-weight: 600; }
                    .bp-income-pill { background: #dcfce7; color: #166534; }
                    .bp-expense-pill { background: #fee2e2; color: #991b1b; }
                    .bp-primary-btn { background: #2563eb; color: #fff; border-radius: 8px; }
                    .bp-secondary-btn { background: #e5e7eb; color: #374151; border-radius: 8px; }
                    .bp-table tbody tr:hover { background: #f9fafb; }
                    .bp-table .q-table__card { box-shadow: none; }
                    input::-webkit-outer-spin-button,
                    input::-webkit-inner-spin-button { -webkit-appearance: none; margin: 0; }
                    input[type=number] { -moz-appearance: textfield; }
                    @media (max-width: 700px) {
                        .bp-shell, .bp-page { padding-left: 16px; padding-right: 16px; }
                    }
                </style>
                """,
                shared=True,
            )

        def navigation(active_path: str) -> None:
            nav_items = [
                ("/", "home", "Übersicht"),
                ("/budget", "trending_up", "Budget"),
                ("/transactions", "sync_alt", "Transaktionen"),
                ("/categories", "sell", "Kategorien"),
                ("/accounts", "account_balance_wallet", "Konten"),
            ]
            with ui.header(elevated=False).classes("bp-header"):
                with ui.row().classes("bp-shell w-full items-center py-4"):
                    ui.label("💰 Budget Planner").classes("text-3xl font-bold text-gray-900")
            with ui.row().classes("bp-nav w-full"):
                with ui.row().classes("bp-shell w-full gap-8 overflow-x-auto no-wrap"):
                    for path, icon, label in nav_items:
                        classes = "bp-nav-link bp-nav-active" if active_path == path else "bp-nav-link"
                        with ui.link(target=path).classes(classes):
                            with ui.row().classes("items-center gap-2 no-wrap"):
                                ui.icon(icon).classes("text-xl")
                                ui.label(label)

        def stat_card(title: str, value: str, icon: str, tone: str, subtitle: str | None = None) -> None:
            tones = {
                "green": ("bg-green-100", "text-green-600", "bp-positive"),
                "red": ("bg-red-100", "text-red-600", "bp-negative"),
                "blue": ("bg-blue-100", "text-blue-600", "bp-blue"),
                "purple": ("bg-purple-100", "text-purple-600", "text-purple-600"),
            }
            bg_class, icon_class, value_class = tones[tone]
            with ui.card().classes("bp-card w-full p-6"):
                with ui.row().classes("w-full items-start justify-between no-wrap"):
                    with ui.column().classes("gap-1"):
                        ui.label(title).classes("text-sm bp-muted")
                        ui.label(value).classes(f"text-2xl font-bold mt-2 {value_class}")
                        if subtitle:
                            ui.label(subtitle).classes("text-xs bp-muted")
                    with ui.element("div").classes(f"{bg_class} rounded-full p-3"):
                        ui.icon(icon).classes(f"text-2xl {icon_class}")

        def page_container(active_path: str) -> Callable[[], None]:
            navigation(active_path)
            return ui.column().classes("bp-page w-full gap-6")

        def progress_bar(percent: float, color_class: str) -> None:
            width = max(0, min(percent, 100))
            with ui.element("div").classes("w-full bg-gray-200 rounded-full h-2 overflow-hidden"):
                ui.element("div").classes(f"h-2 rounded-full {color_class}").style(f"width: {width:.1f}%")

        def transaction_columns(show_actions: bool = False) -> list[dict[str, str]]:
            columns: list[dict[str, str]] = [
                {"name": "date", "label": "Datum", "field": "date", "align": "left"},
                {"name": "type", "label": "Typ", "field": "type", "align": "left"},
                {"name": "category", "label": "Kategorie", "field": "category", "align": "left"},
                {"name": "account", "label": "Konto", "field": "account", "align": "left"},
                {"name": "description", "label": "Beschreibung", "field": "description", "align": "left"},
                {"name": "amount", "label": "Betrag", "field": "amount", "align": "right"},
            ]
            if show_actions:
                columns.append({"name": "actions", "label": "Aktionen", "field": "actions", "align": "right"})
            return columns

        def transaction_rows(transactions: list[Transaction]) -> list[dict[str, str]]:
            rows = []
            for transaction in transactions:
                is_income = transaction.transaction_type == "income"
                rows.append(
                    {
                        "id": transaction.id,
                        "date": transaction.transaction_date.strftime("%d.%m.%Y"),
                        "type": "Einnahme" if is_income else "Ausgabe",
                        "type_class": "bp-income-pill" if is_income else "bp-expense-pill",
                        "category": transaction.category.name,
                        "account": transaction.account.name,
                        "description": transaction.description or "-",
                        "amount": f"{'+' if is_income else '-'}{money(transaction.amount_chf)}",
                        "amount_class": "bp-positive" if is_income else "bp-negative",
                    }
                )
            return rows

        def transaction_table(
            transactions: list[Transaction],
            empty_text: str,
            on_edit: Callable[[int], None] | None = None,
            on_delete: Callable[[int], None] | None = None,
        ) -> None:
            if not transactions:
                with ui.card().classes("bp-card w-full p-8 text-center"):
                    ui.label(empty_text).classes("bp-muted")
                return
            table = ui.table(
                columns=transaction_columns(show_actions=on_edit is not None or on_delete is not None),
                rows=transaction_rows(transactions),
                row_key="id",
            ).classes("bp-card bp-table w-full").props("flat")
            table.add_slot("body-cell-type", """
                <q-td :props="props">
                    <span class="bp-pill" :class="props.row.type_class">{{ props.row.type }}</span>
                </q-td>
            """)
            table.add_slot("body-cell-amount", """
                <q-td :props="props">
                    <span class="font-semibold" :class="props.row.amount_class">{{ props.row.amount }}</span>
                </q-td>
            """)
            if on_edit is not None or on_delete is not None:
                table.add_slot("body-cell-actions", """
                    <q-td :props="props">
                        <q-btn flat dense round icon="edit" color="primary" @click="$parent.$emit('edit-row', props.row.id)" />
                        <q-btn flat dense round icon="delete" color="negative" @click="$parent.$emit('delete-row', props.row.id)" />
                    </q-td>
                """)
                if on_edit is not None:
                    table.on("edit-row", lambda event: on_edit(int(event.args)))
                if on_delete is not None:
                    table.on("delete-row", lambda event: on_delete(int(event.args)))

        def budget_for_category(budgets: list[Budget], category_id: int | None, year: int, month: int) -> Budget | None:
            return next(
                (
                    budget
                    for budget in budgets
                    if budget.category_id == category_id and budget.year == year and budget.month == month
                ),
                None,
            )

        add_theme()

        @ui.page("/")
        def dashboard_page() -> None:
            year, month = current_month()
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
            exceeded = [status for status in data.budget_statuses if status.is_exceeded]
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
                if total_budget and total_budget_remaining < 0:
                    with ui.element("div").classes("bg-red-50 border border-red-200 rounded-lg p-4 w-full"):
                        with ui.row().classes("items-start gap-3 no-wrap"):
                            ui.icon("error_outline").classes("text-red-600 text-xl mt-1")
                            with ui.column().classes("gap-1"):
                                ui.label("Gesamtbudget überschritten!").classes("font-semibold text-red-900")
                                ui.label(
                                    f"Sie haben Ihr monatliches Budget um {money(abs(total_budget_remaining))} überschritten."
                                ).classes("text-sm text-red-700")
                elif exceeded:
                    with ui.element("div").classes("bg-yellow-50 border border-yellow-200 rounded-lg p-4 w-full"):
                        with ui.row().classes("items-start gap-3 no-wrap"):
                            ui.icon("warning_amber").classes("text-yellow-600 text-xl mt-1")
                            with ui.column().classes("gap-1"):
                                ui.label("Kategorie-Budget überschritten!").classes("font-semibold text-yellow-900")
                                for status in exceeded:
                                    ui.label(
                                        f"{status.budget.category.name}: {money(abs(status.remaining_chf))} über dem Limit"
                                    ).classes("text-sm text-yellow-700")

                with ui.grid(columns="repeat(auto-fit, minmax(220px, 1fr))").classes("w-full gap-6"):
                    stat_card("Einnahmen (Monat)", money(data.overview.total_income_chf), "trending_up", "green")
                    stat_card("Ausgaben (Monat)", money(data.overview.total_expenses_chf), "trending_down", "red")
                    stat_card("Gesamtkontostand", money(total_account_balance), "account_balance_wallet", "blue")
                    stat_card("Aktueller Monat", month_name(year, month), "calendar_month", "blue")
                    stat_card(
                        "Verfügbares Budget",
                        money(total_budget_remaining),
                        "trending_up",
                        "purple" if total_budget_remaining >= 0 else "red",
                        f"Budgetierte Ausgaben: {money(budgeted_expenses)}"
                        if total_budget
                        else "Noch kein Monatsbudget",
                    )
                if unbudgeted_expenses:
                    with ui.element("div").classes("bg-yellow-50 border border-yellow-200 rounded-lg p-4 w-full"):
                        ui.label(
                            f"Hinweis: {money(unbudgeted_expenses)} Ausgaben liegen in Kategorien ohne Budget und werden "
                            "nicht vom verfügbaren Budget abgezogen."
                        ).classes("text-sm text-yellow-800")

                with ui.grid(columns="repeat(auto-fit, minmax(320px, 1fr))").classes("w-full gap-6"):
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
                                            "radius": "70%",
                                            "label": {"show": False},
                                            "labelLine": {"show": False},
                                            "data": [
                                                {"name": name, "value": round(value, 2)}
                                                for name, value in category_totals.items()
                                            ],
                                        }
                                    ],
                                }
                            ).classes("h-80 w-full")
                        else:
                            ui.label("Keine Ausgaben im aktuellen Monat.").classes("bp-muted")

                    with ui.card().classes("bp-card w-full p-6"):
                        ui.label("Einnahmen vs. Ausgaben (6 Monate)").classes("bp-section-title mb-4")
                        ui.echart(
                            {
                                "tooltip": {"trigger": "axis"},
                                "legend": {"bottom": 0},
                                "grid": {"left": 50, "right": 24, "top": 24, "bottom": 58},
                                "xAxis": {"type": "category", "data": [item["month"] for item in monthly_comparison]},
                                "yAxis": {"type": "value"},
                                "series": [
                                    {
                                        "name": "Einnahmen",
                                        "type": "bar",
                                        "itemStyle": {"color": "#16a34a"},
                                        "data": [item["income"] for item in monthly_comparison],
                                    },
                                    {
                                        "name": "Ausgaben",
                                        "type": "bar",
                                        "itemStyle": {"color": "#dc2626"},
                                        "data": [item["expenses"] for item in monthly_comparison],
                                    },
                                ],
                            }
                        ).classes("h-80 w-full")
                        rows = [
                            {
                                "month": item["month"],
                                "income": money(item["income"]),
                                "expenses": money(item["expenses"]),
                            }
                            for item in monthly_comparison
                        ]
                        ui.table(
                            columns=[
                                {"name": "month", "label": "Monat", "field": "month", "align": "left"},
                                {"name": "income", "label": "Einnahmen", "field": "income", "align": "right"},
                                {"name": "expenses", "label": "Ausgaben", "field": "expenses", "align": "right"},
                            ],
                            rows=rows,
                        ).classes("bp-table w-full mt-4").props("flat dense")

                with ui.grid(columns="repeat(auto-fit, minmax(320px, 1fr))").classes("w-full gap-6"):
                    with ui.card().classes("bp-card w-full p-6"):
                        ui.label("Kontenübersicht").classes("bp-section-title mb-4")
                        if not accounts:
                            ui.label("Keine Konten vorhanden.").classes("bp-muted")
                        else:
                            for account in accounts:
                                balance = account_balance(account, all_transactions)
                                with ui.row().classes("w-full items-center justify-between py-2 border-b border-gray-100"):
                                    ui.label(account.name).classes("font-medium")
                                    ui.label(money(balance)).classes(
                                        f"font-semibold bp-money {'bp-positive' if balance >= 0 else 'bp-negative'}"
                                    )

                    with ui.card().classes("bp-card w-full p-6"):
                        ui.label("Budgetstatus").classes("bp-section-title mb-4")
                        if not data.budget_statuses:
                            ui.label("Noch keine Budgets für diesen Monat erfasst.").classes("bp-muted")
                        else:
                            for status in data.budget_statuses:
                                percent = min((status.spent_chf / status.budget.limit_chf) * 100, 100)
                                color = "red" if status.is_exceeded else "green" if percent <= 80 else "yellow"
                                with ui.column().classes("w-full gap-2 mb-4"):
                                    with ui.row().classes("w-full justify-between"):
                                        ui.label(status.budget.category.name).classes("font-medium")
                                        ui.label(f"{money(status.spent_chf)} / {money(status.budget.limit_chf)}").classes(
                                            "text-sm bp-muted"
                                        )
                                    color_class = "bg-red-600" if color == "red" else "bg-yellow-500" if color == "yellow" else "bg-green-600"
                                    progress_bar(percent, color_class)
                                    ui.label(f"{percent:.0f}% genutzt · {money(status.remaining_chf)} Restbudget").classes(
                                        "text-xs bp-muted"
                                    )

                with ui.card().classes("bp-card w-full p-6"):
                    ui.label("Letzte Transaktionen im aktuellen Monat").classes("bp-section-title mb-4")
                    transaction_table(data.transactions[:10], "Noch keine Transaktionen in diesem Monat.")

        @ui.page("/transactions")
        def transactions_page() -> None:
            with page_container("/transactions"):
                ui.label("Transaktionen").classes("bp-title")

                accounts = controller.list_accounts()
                categories = controller.list_categories()
                account_options = {account.id: account.name for account in accounts}

                def category_options_for(transaction_type_value: str) -> dict[int, str]:
                    return {
                        category.id: category.name
                        for category in categories
                        if category.category_type == transaction_type_value
                    }

                with ui.card().classes("bp-card w-full p-6"):
                    ui.label("Neue Transaktion erfassen").classes("bp-section-title mb-4")
                    ui.label("Typ").classes("font-semibold mb-1")
                    transaction_type = ui.radio({"income": "Einnahme", "expense": "Ausgabe"}, value="expense").props(
                        "inline"
                    ).classes("text-lg mb-4")
                    with ui.grid(columns="repeat(auto-fit, minmax(220px, 1fr))").classes("w-full gap-4"):
                        amount = number_input("Betrag (CHF)", "0.00")
                        transaction_date = ui.input("Datum", value=date.today().isoformat()).props("type=date").classes(
                            "w-full"
                        )
                        account = ui.select(account_options, label="Konto").classes("w-full")
                        category = ui.select(category_options_for("expense"), label="Kategorie").classes("w-full")
                    description = ui.input("Beschreibung", placeholder="Optional").classes("w-full mt-4")
                    with ui.column().classes("gap-2 mt-4"):
                        recurring = ui.checkbox("Wiederkehrende Transaktion").props("disable")
                        recurring.tooltip("Wiederkehrende Transaktionen sind im aktuellen Datenmodell noch nicht gespeichert.")
                        ui.select(
                            {"monthly": "Monatlich", "weekly": "Wöchentlich", "yearly": "Jährlich"},
                            label="Wiederholung",
                            value="monthly",
                        ).classes("w-full max-w-sm").props("disable")

                    def update_category_options() -> None:
                        category.set_options(category_options_for(str(transaction_type.value)))
                        category.value = None

                    transaction_type.on_value_change(update_category_options)

                    def save_transaction() -> None:
                        try:
                            if account.value is None or category.value is None:
                                raise ValueError("Bitte Konto und Kategorie auswählen.")
                            controller.create_transaction(
                                amount_chf=parse_float(amount.value, "einen Betrag"),
                                transaction_type=str(transaction_type.value),
                                transaction_date=date.fromisoformat(str(transaction_date.value)),
                                description=description.value or "",
                                account_id=int(account.value),
                                category_id=int(category.value),
                            )
                        except Exception as error:
                            ui.notify(str(error), type="warning")
                            return
                        ui.notify("Transaktion gespeichert.", type="positive")
                        ui.navigate.to("/transactions")

                    with ui.row().classes("gap-3 mt-4"):
                        ui.button("Speichern", on_click=save_transaction).classes("bp-primary-btn")
                        ui.button("Abbrechen", on_click=lambda: ui.navigate.to("/transactions")).classes("bp-secondary-btn")

                transactions = controller.list_recent_transactions()
                with ui.card().classes("bp-card w-full p-4"):
                    with ui.row().classes("items-center gap-2 mb-3"):
                        ui.icon("filter_alt").classes("bp-muted")
                        ui.label("Filter").classes("font-semibold")
                    month_options = {
                        "": "Alle Monate",
                        **{
                            transaction.transaction_date.strftime("%Y-%m"): month_name(
                                transaction.transaction_date.year,
                                transaction.transaction_date.month,
                            )
                            for transaction in transactions
                        },
                    }
                    with ui.grid(columns="repeat(auto-fit, minmax(180px, 1fr))").classes("w-full gap-4"):
                        filter_type = ui.select(
                            {"": "Alle Typen", "income": "Einnahmen", "expense": "Ausgaben"},
                            value="",
                        ).classes("w-full")
                        filter_category = ui.select(
                            {"": "Alle Kategorien", **{str(category.id): category.name for category in categories}},
                            value="",
                        ).classes("w-full")
                        filter_month = ui.select(month_options, value="").classes("w-full")
                        reset_button = ui.button("Filter zurücksetzen").classes("bp-secondary-btn")

                with ui.card().classes("bp-card w-full p-6"):
                    ui.label("Transaktionsliste").classes("bp-section-title mb-4")
                    transaction_list = ui.column().classes("w-full")

                    def open_delete_dialog(transaction_id: int) -> None:
                        with ui.dialog() as dialog, ui.card().classes("bp-card p-6"):
                            ui.label("Transaktion löschen?").classes("bp-section-title")
                            ui.label("Diese Aktion kann nicht rückgängig gemacht werden.").classes("bp-muted")

                            def delete_transaction() -> None:
                                try:
                                    controller.delete_transaction(transaction_id)
                                except Exception as error:
                                    ui.notify(str(error), type="warning")
                                    return
                                ui.notify("Transaktion gelöscht.", type="positive")
                                ui.navigate.to("/transactions")

                            with ui.row().classes("gap-3 mt-4"):
                                ui.button("Löschen", icon="delete", on_click=delete_transaction).classes("bg-red-600 text-white rounded-lg")
                                ui.button("Abbrechen", on_click=dialog.close).classes("bp-secondary-btn")
                        dialog.open()

                    def open_edit_dialog(transaction_id: int) -> None:
                        transaction = next(item for item in transactions if item.id == transaction_id)
                        with ui.dialog() as dialog, ui.card().classes("bp-card p-6 w-full max-w-3xl"):
                            ui.label("Transaktion bearbeiten").classes("bp-section-title mb-4")
                            edit_type = ui.radio(
                                {"income": "Einnahme", "expense": "Ausgabe"},
                                value=transaction.transaction_type,
                            ).props("inline").classes("text-lg mb-4")
                            with ui.grid(columns="repeat(auto-fit, minmax(220px, 1fr))").classes("w-full gap-4"):
                                edit_amount = number_input("Betrag (CHF)", "0.00")
                                edit_amount.value = f"{transaction.amount_chf:.2f}"
                                edit_date = ui.input(
                                    "Datum",
                                    value=transaction.transaction_date.isoformat(),
                                ).props("type=date").classes("w-full")
                                edit_account = ui.select(account_options, label="Konto", value=transaction.account_id).classes("w-full")
                                edit_category = ui.select(
                                    category_options_for(transaction.transaction_type),
                                    label="Kategorie",
                                    value=transaction.category_id,
                                ).classes("w-full")
                            edit_description = ui.input(
                                "Beschreibung",
                                value=transaction.description,
                                placeholder="Optional",
                            ).classes("w-full mt-4")

                            def update_edit_category_options() -> None:
                                edit_category.set_options(category_options_for(str(edit_type.value)))
                                edit_category.value = None

                            edit_type.on_value_change(update_edit_category_options)

                            def save_edit() -> None:
                                try:
                                    if edit_account.value is None or edit_category.value is None:
                                        raise ValueError("Bitte Konto und Kategorie auswählen.")
                                    controller.update_transaction(
                                        transaction_id=transaction_id,
                                        amount_chf=parse_float(edit_amount.value, "einen Betrag"),
                                        transaction_type=str(edit_type.value),
                                        transaction_date=date.fromisoformat(str(edit_date.value)),
                                        description=edit_description.value or "",
                                        account_id=int(edit_account.value),
                                        category_id=int(edit_category.value),
                                    )
                                except Exception as error:
                                    ui.notify(str(error), type="warning")
                                    return
                                ui.notify("Transaktion aktualisiert.", type="positive")
                                ui.navigate.to("/transactions")

                            with ui.row().classes("gap-3 mt-4"):
                                ui.button("Speichern", icon="save", on_click=save_edit).classes("bp-primary-btn")
                                ui.button("Abbrechen", on_click=dialog.close).classes("bp-secondary-btn")
                        dialog.open()

                    def filtered_transactions() -> list[Transaction]:
                        result = transactions
                        if filter_type.value:
                            result = [item for item in result if item.transaction_type == filter_type.value]
                        if filter_category.value:
                            result = [item for item in result if str(item.category_id) == str(filter_category.value)]
                        if filter_month.value:
                            result = [
                                item
                                for item in result
                                if item.transaction_date.strftime("%Y-%m") == filter_month.value
                            ]
                        return result

                    def render_transaction_list() -> None:
                        transaction_list.clear()
                        with transaction_list:
                            transaction_table(
                                filtered_transactions(),
                                "Keine Transaktionen gefunden.",
                                on_edit=open_edit_dialog,
                                on_delete=open_delete_dialog,
                            )

                    def reset_filters() -> None:
                        filter_type.value = ""
                        filter_category.value = ""
                        filter_month.value = ""
                        render_transaction_list()

                    filter_type.on_value_change(render_transaction_list)
                    filter_category.on_value_change(render_transaction_list)
                    filter_month.on_value_change(render_transaction_list)
                    reset_button.on_click(reset_filters)
                    render_transaction_list()

        @ui.page("/categories")
        def categories_page() -> None:
            transactions = controller.list_recent_transactions()
            with page_container("/categories"):
                ui.label("Kategorien verwalten").classes("bp-title")

                with ui.card().classes("bp-card w-full p-6"):
                    ui.label("Neue Kategorie erstellen").classes("bp-section-title mb-4")
                    category_name = ui.input("Kategoriename", placeholder="z.B. Lebensmittel, Transport").classes(
                        "w-full max-w-2xl"
                    )
                    category_type = ui.radio({"income": "Einnahme", "expense": "Ausgabe"}, value="expense").props("inline")

                    def save_category() -> None:
                        try:
                            controller.create_category(category_name.value or "", str(category_type.value))
                        except Exception as error:
                            ui.notify(str(error), type="warning")
                            return
                        ui.notify("Kategorie gespeichert.", type="positive")
                        ui.navigate.to("/categories")

                    with ui.row().classes("gap-3"):
                        ui.button("Erstellen", on_click=save_category).classes("bp-primary-btn")
                        ui.button("Abbrechen", on_click=lambda: ui.navigate.to("/categories")).classes("bp-secondary-btn")

                categories = controller.list_categories()
                rows = [
                    {
                        "name": category.name,
                        "type": category_type_label(category),
                        "type_class": "bp-income-pill" if category.category_type == "income" else "bp-expense-pill",
                        "usage": f"{usage_count(transactions, 'category_id', category.id)} Transaktionen",
                        "id": category.id,
                        "category_type": category.category_type,
                    }
                    for category in categories
                ]
                category_table = ui.table(
                    columns=[
                        {"name": "name", "label": "Kategoriename", "field": "name", "align": "left"},
                        {"name": "type", "label": "Typ", "field": "type", "align": "left"},
                        {"name": "usage", "label": "Verwendungen", "field": "usage", "align": "left"},
                        {"name": "actions", "label": "Aktionen", "field": "actions", "align": "right"},
                    ],
                    rows=rows,
                    row_key="id",
                ).classes("bp-card bp-table w-full").props("flat")
                category_table.add_slot("body-cell-type", """
                    <q-td :props="props">
                        <span class="bp-pill" :class="props.row.type_class">{{ props.row.type }}</span>
                    </q-td>
                """)
                category_table.add_slot("body-cell-actions", """
                    <q-td :props="props">
                        <q-btn flat dense round icon="edit" color="primary" @click="$parent.$emit('edit-category', props.row.id)" />
                        <q-btn flat dense round icon="delete" color="negative" @click="$parent.$emit('delete-category', props.row.id)" />
                    </q-td>
                """)

                def open_edit_category_dialog(category_id: int) -> None:
                    category = next(item for item in categories if item.id == category_id)
                    with ui.dialog() as dialog, ui.card().classes("bp-card p-6 w-full max-w-2xl"):
                        ui.label("Kategorie bearbeiten").classes("bp-section-title mb-4")
                        edit_name = ui.input("Kategoriename", value=category.name).classes("w-full")
                        edit_type = ui.radio(
                            {"income": "Einnahme", "expense": "Ausgabe"},
                            value=category.category_type,
                        ).props("inline").classes("text-lg mt-4")

                        def save_category_edit() -> None:
                            try:
                                controller.update_category(
                                    category_id=category_id,
                                    name=edit_name.value or "",
                                    category_type=str(edit_type.value),
                                )
                            except Exception as error:
                                ui.notify(str(error), type="warning")
                                return
                            ui.notify("Kategorie aktualisiert.", type="positive")
                            ui.navigate.to("/categories")

                        with ui.row().classes("gap-3 mt-4"):
                            ui.button("Speichern", icon="save", on_click=save_category_edit).classes("bp-primary-btn")
                            ui.button("Abbrechen", on_click=dialog.close).classes("bp-secondary-btn")
                    dialog.open()

                def open_delete_category_dialog(category_id: int) -> None:
                    with ui.dialog() as dialog, ui.card().classes("bp-card p-6"):
                        ui.label("Kategorie löschen?").classes("bp-section-title")
                        ui.label("Kategorien können nur gelöscht werden, wenn sie nicht verwendet werden.").classes("bp-muted")

                        def delete_category() -> None:
                            try:
                                controller.delete_category(category_id)
                            except Exception as error:
                                ui.notify(str(error), type="warning")
                                return
                            ui.notify("Kategorie gelöscht.", type="positive")
                            ui.navigate.to("/categories")

                        with ui.row().classes("gap-3 mt-4"):
                            ui.button("Löschen", icon="delete", on_click=delete_category).classes("bg-red-600 text-white rounded-lg")
                            ui.button("Abbrechen", on_click=dialog.close).classes("bp-secondary-btn")
                    dialog.open()

                category_table.on("edit-category", lambda event: open_edit_category_dialog(int(event.args)))
                category_table.on("delete-category", lambda event: open_delete_category_dialog(int(event.args)))

        @ui.page("/accounts")
        def accounts_page() -> None:
            transactions = controller.list_recent_transactions()
            with page_container("/accounts"):
                ui.label("Konten verwalten").classes("bp-title")

                with ui.card().classes("bp-card w-full p-6"):
                    ui.label("Neues Konto erstellen").classes("bp-section-title mb-4")
                    with ui.grid(columns="repeat(auto-fit, minmax(240px, 1fr))").classes("w-full gap-4"):
                        name = ui.input("Kontoname", placeholder="z.B. Girokonto, Sparkonto").classes("w-full")
                        account_type = ui.select(
                            ["Bankkonto", "Bargeld"],
                            label="Kontotyp",
                            value="Bankkonto",
                        ).classes("w-full")
                        starting_balance = number_input("Startsaldo (CHF)", "0.00")

                    def save_account() -> None:
                        try:
                            controller.create_account(
                                name.value or "",
                                account_type.value or "",
                                parse_float(starting_balance.value, "einen Startsaldo"),
                            )
                        except Exception as error:
                            ui.notify(str(error), type="warning")
                            return
                        ui.notify("Konto gespeichert.", type="positive")
                        ui.navigate.to("/accounts")

                    with ui.row().classes("gap-3 mt-4"):
                        ui.button("Erstellen", on_click=save_account).classes("bp-primary-btn")
                        ui.button("Abbrechen", on_click=lambda: ui.navigate.to("/accounts")).classes("bp-secondary-btn")

                accounts = controller.list_accounts()
                if accounts:
                    with ui.grid(columns="repeat(auto-fit, minmax(280px, 1fr))").classes("w-full gap-6"):
                        for account in accounts:
                            balance = account_balance(account, transactions)
                            count = usage_count(transactions, "account_id", account.id)
                            with ui.card().classes("bp-card bp-card-hover w-full p-6"):
                                with ui.row().classes("w-full items-start justify-between no-wrap mb-4"):
                                    with ui.row().classes("items-center gap-3 no-wrap"):
                                        with ui.element("div").classes("bg-blue-100 rounded-full p-3"):
                                            ui.icon("account_balance_wallet").classes("text-blue-600 text-2xl")
                                        with ui.column().classes("gap-0"):
                                            ui.label(account.name).classes("font-semibold text-lg text-gray-900")
                                            ui.label(f"{count} Transaktionen").classes("text-xs bp-muted")
                                    ui.icon("lock").classes("text-gray-300")
                                ui.label("Startsaldo").classes("text-xs bp-muted")
                                ui.label(money(account.starting_balance_chf)).classes("text-sm text-gray-700 mb-3")
                                ui.separator()
                                ui.label("Aktueller Saldo").classes("text-xs bp-muted mt-3")
                                ui.label(money(balance)).classes(
                                    f"text-2xl font-bold {'bp-positive' if balance >= 0 else 'bp-negative'}"
                                )
                    total_start = sum(account.starting_balance_chf for account in accounts)
                    total_balance = sum(account_balance(account, transactions) for account in accounts)
                    with ui.element("div").classes("bg-blue-600 rounded-lg shadow-lg p-6 text-white w-full"):
                        ui.label("Gesamtübersicht").classes("text-lg font-semibold mb-4")
                        with ui.grid(columns="repeat(auto-fit, minmax(180px, 1fr))").classes("w-full gap-6"):
                            with ui.column().classes("gap-1"):
                                ui.label("Anzahl Konten").classes("text-blue-100 text-sm")
                                ui.label(str(len(accounts))).classes("text-3xl font-bold")
                            with ui.column().classes("gap-1"):
                                ui.label("Gesamter Startsaldo").classes("text-blue-100 text-sm")
                                ui.label(money(total_start)).classes("text-3xl font-bold")
                            with ui.column().classes("gap-1"):
                                ui.label("Aktueller Gesamtsaldo").classes("text-blue-100 text-sm")
                                ui.label(money(total_balance)).classes("text-3xl font-bold")
                else:
                    with ui.card().classes("bp-card w-full p-12 text-center"):
                        ui.icon("account_balance_wallet").classes("text-gray-300 text-6xl")
                        ui.label("Keine Konten vorhanden").classes("bp-muted")

        @ui.page("/budget")
        def budget_page() -> None:
            year, month = current_month()
            month_transactions = controller.dashboard_data(year=year, month=month).transactions
            with page_container("/budget"):
                ui.label("Budget verwalten").classes("bp-title")

                expense_categories = controller.list_categories(category_type="expense")
                category_options = {category.id: category.name for category in expense_categories}
                current_budgets = controller.list_budgets(year=year, month=month)
                current_budget_limit = sum(budget.limit_chf for budget in current_budgets)
                current_expenses = sum(
                    transaction.amount_chf
                    for transaction in month_transactions
                    if transaction.transaction_type == "expense"
                )
                current_remaining = round(current_budget_limit - current_expenses, 2)
                current_usage = (current_expenses / current_budget_limit * 100) if current_budget_limit else 0

                with ui.card().classes("bp-card w-full p-6"):
                    ui.label("Budgets pro Kategorie").classes("bp-section-title mb-4")
                    with ui.grid(columns="repeat(auto-fit, minmax(220px, 1fr))").classes("w-full gap-4"):
                        budget_month = number_input("Monat", "1-12")
                        budget_year = number_input("Jahr", "2026")
                        limit = number_input("Limit pro Kategorie (CHF)", "0.00")
                        budget_category = ui.select(category_options, label="Ausgabenkategorie").classes("w-full")

                    def save_budget() -> None:
                        try:
                            if budget_category.value is None:
                                raise ValueError("Bitte eine Ausgabenkategorie auswählen.")
                            controller.create_budget(
                                month=parse_int(budget_month.value, "einen Monat"),
                                year=parse_int(budget_year.value, "ein Jahr"),
                                limit_chf=parse_float(limit.value, "ein Budgetlimit"),
                                category_id=int(budget_category.value),
                            )
                        except Exception as error:
                            ui.notify(str(error), type="warning")
                            return
                        ui.notify("Budget gespeichert.", type="positive")
                        ui.navigate.to("/budget")

                    with ui.row().classes("gap-3 mt-4"):
                        ui.button("Speichern", on_click=save_budget).classes("bp-primary-btn")
                        ui.button("Abbrechen", on_click=lambda: ui.navigate.to("/budget")).classes("bp-secondary-btn")

                with ui.grid(columns="repeat(auto-fit, minmax(220px, 1fr))").classes("w-full gap-6"):
                    stat_card("Budgetlimit", money(current_budget_limit), "account_balance_wallet", "blue")
                    stat_card("Ausgaben", money(current_expenses), "trending_down", "red")
                    stat_card(
                        "Verbleibend",
                        money(current_remaining),
                        "savings",
                        "green" if current_remaining >= 0 else "red",
                    )
                    stat_card(
                        "Verbrauch",
                        f"{current_usage:.0f}%",
                        "percent",
                        "red" if current_usage > 100 else "purple" if current_usage > 80 else "green",
                    )

                budgets = controller.list_budgets()
                with ui.card().classes("bp-card w-full p-6"):
                    ui.label("Budgets nach Kategorie").classes("bp-section-title mb-4")
                    if not budgets:
                        with ui.column().classes("w-full items-center gap-2 py-8"):
                            ui.icon("trending_up").classes("text-gray-300 text-6xl")
                            ui.label("Kein Budget festgelegt").classes("bp-muted")
                    else:
                        with ui.column().classes("w-full gap-4"):
                            for budget in budgets:
                                relevant_transactions = (
                                    month_transactions
                                    if budget.year == year and budget.month == month
                                    else controller.dashboard_data(year=budget.year, month=budget.month).transactions
                                )
                                spent = sum(
                                    transaction.amount_chf
                                    for transaction in relevant_transactions
                                    if transaction.transaction_type == "expense"
                                    and transaction.category_id == budget.category_id
                                )
                                remaining = round(budget.limit_chf - spent, 2)
                                percent = (spent / budget.limit_chf * 100) if budget.limit_chf else 0
                                status = "Überschritten" if remaining < 0 else "Warnung" if percent > 80 else "OK"
                                tone = (
                                    "text-red-600"
                                    if remaining < 0
                                    else "text-yellow-600"
                                    if percent > 80
                                    else "text-green-600"
                                )
                                with ui.element("div").classes("border border-gray-200 rounded-lg p-4 w-full"):
                                    with ui.row().classes("w-full items-start justify-between gap-4"):
                                        with ui.column().classes("gap-1"):
                                            ui.label(
                                                f"{budget.category.name} - {month_label(budget.year, budget.month)}"
                                            ).classes("text-lg font-semibold")
                                            ui.label(f"Limit: {money(budget.limit_chf)}").classes("text-sm bp-muted")
                                        ui.label(status).classes(f"font-semibold {tone}")
                                    with ui.grid(columns="repeat(auto-fit, minmax(160px, 1fr))").classes("w-full gap-4 mt-4"):
                                        ui.label(f"Ausgaben: {money(spent)}").classes("text-sm bp-muted")
                                        ui.label(f"Verbleibend: {money(remaining)}").classes(
                                            f"text-sm font-semibold {tone}"
                                        )
                                        ui.label(f"Verbrauch: {percent:.1f}%").classes("text-sm bp-muted")
                                    color_class = (
                                        "bg-red-600"
                                        if remaining < 0
                                        else "bg-yellow-500"
                                        if percent > 80
                                        else "bg-green-600"
                                    )
                                    progress_bar(percent, color_class)

        @ui.page("/settings")
        def settings_redirect_page() -> None:
            ui.navigate.to("/accounts")

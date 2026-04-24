"""NiceGUI pages.

The page class owns only UI code. User actions are delegated to the controller,
which then calls services and DAOs.
"""

from __future__ import annotations

from datetime import date

from nicegui import ui

from .controllers import FinanceController


class Pages:
    """Registers all NiceGUI routes."""

    def __init__(self, finance_controller: FinanceController) -> None:
        self._finance_controller = finance_controller

    def register(self) -> None:
        controller = self._finance_controller

        def money(value: float) -> str:
            return f"CHF {value:,.2f}".replace(",", "'")

        def navigation() -> None:
            with ui.header().classes("bg-slate-900 text-white"):
                with ui.row().classes("w-full items-center justify-between"):
                    ui.label("Budgetplanner").classes("text-xl font-bold")
                    with ui.row().classes("gap-2"):
                        ui.link("Dashboard", "/").classes("text-white")
                        ui.link("Transaktionen", "/transactions").classes("text-white")
                        ui.link("Stammdaten", "/settings").classes("text-white")

        @ui.page("/")
        def dashboard_page() -> None:
            navigation()
            today = date.today()
            data = controller.dashboard_data(year=today.year, month=today.month)

            ui.markdown(f"## Finanzuebersicht {today.month:02d}/{today.year}")
            with ui.grid(columns=3).classes("w-full gap-4"):
                with ui.card().classes("w-full"):
                    ui.label("Einnahmen").classes("text-sm text-slate-500")
                    ui.label(money(data.overview.total_income_chf)).classes("text-2xl font-bold text-green-700")
                with ui.card().classes("w-full"):
                    ui.label("Ausgaben").classes("text-sm text-slate-500")
                    ui.label(money(data.overview.total_expenses_chf)).classes("text-2xl font-bold text-red-700")
                with ui.card().classes("w-full"):
                    ui.label("Saldo").classes("text-sm text-slate-500")
                    ui.label(money(data.overview.balance_chf)).classes("text-2xl font-bold")

            ui.markdown("### Budgetstatus")
            if not data.budget_statuses:
                ui.label("Noch keine Budgets fuer diesen Monat erfasst.")
            else:
                columns = [
                    {"name": "category", "label": "Kategorie", "field": "category", "align": "left"},
                    {"name": "limit", "label": "Budget", "field": "limit", "align": "right"},
                    {"name": "spent", "label": "Ausgegeben", "field": "spent", "align": "right"},
                    {"name": "remaining", "label": "Restbudget", "field": "remaining", "align": "right"},
                    {"name": "status", "label": "Status", "field": "status", "align": "left"},
                ]
                rows = []
                for status in data.budget_statuses:
                    rows.append(
                        {
                            "category": status.budget.category.name,
                            "limit": money(status.budget.limit_chf),
                            "spent": money(status.spent_chf),
                            "remaining": money(status.remaining_chf),
                            "status": "Ueberschritten" if status.is_exceeded else "OK",
                        }
                    )
                ui.table(columns=columns, rows=rows).classes("w-full")

            ui.markdown("### Letzte Transaktionen im aktuellen Monat")
            if not data.transactions:
                ui.label("Noch keine Transaktionen in diesem Monat.")
            else:
                rows = [
                    {
                        "date": transaction.transaction_date.strftime("%d.%m.%Y"),
                        "type": "Einnahme" if transaction.transaction_type == "income" else "Ausgabe",
                        "category": transaction.category.name,
                        "account": transaction.account.name,
                        "amount": money(transaction.amount_chf),
                        "description": transaction.description,
                    }
                    for transaction in data.transactions[:10]
                ]
                ui.table(
                    columns=[
                        {"name": "date", "label": "Datum", "field": "date"},
                        {"name": "type", "label": "Typ", "field": "type"},
                        {"name": "category", "label": "Kategorie", "field": "category"},
                        {"name": "account", "label": "Konto", "field": "account"},
                        {"name": "amount", "label": "Betrag", "field": "amount", "align": "right"},
                        {"name": "description", "label": "Beschreibung", "field": "description"},
                    ],
                    rows=rows,
                ).classes("w-full")

        @ui.page("/transactions")
        def transactions_page() -> None:
            navigation()
            ui.markdown("## Transaktionen erfassen")

            accounts = controller.list_accounts()
            categories = controller.list_categories()
            account_options = {account.id: account.name for account in accounts}
            category_options = {category.id: f"{category.name} ({category.category_type})" for category in categories}

            with ui.card().classes("w-full max-w-3xl"):
                amount = ui.number("Betrag in CHF", value=0.0, min=0.01, step=0.05).classes("w-full")
                transaction_type = ui.select(
                    {"income": "Einnahme", "expense": "Ausgabe"},
                    label="Typ",
                    value="expense",
                ).classes("w-full")
                transaction_date = (
                    ui.input("Datum", value=date.today().isoformat())
                    .props("type=date")
                    .classes("w-full")
                )
                account = ui.select(account_options, label="Konto").classes("w-full")
                category = ui.select(category_options, label="Kategorie").classes("w-full")
                description = ui.input("Beschreibung").classes("w-full")

                def save_transaction() -> None:
                    try:
                        if account.value is None or category.value is None:
                            raise ValueError("Bitte Konto und Kategorie auswaehlen.")
                        controller.create_transaction(
                            amount_chf=float(amount.value),
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

                ui.button("Speichern", on_click=save_transaction).props("color=primary")

            ui.markdown("## Alle Transaktionen")
            transactions = controller.list_recent_transactions()
            if not transactions:
                ui.label("Noch keine Transaktionen erfasst.")
                return
            rows = [
                {
                    "date": transaction.transaction_date.strftime("%d.%m.%Y"),
                    "type": "Einnahme" if transaction.transaction_type == "income" else "Ausgabe",
                    "category": transaction.category.name,
                    "account": transaction.account.name,
                    "amount": money(transaction.amount_chf),
                    "description": transaction.description,
                }
                for transaction in transactions
            ]
            ui.table(
                columns=[
                    {"name": "date", "label": "Datum", "field": "date"},
                    {"name": "type", "label": "Typ", "field": "type"},
                    {"name": "category", "label": "Kategorie", "field": "category"},
                    {"name": "account", "label": "Konto", "field": "account"},
                    {"name": "amount", "label": "Betrag", "field": "amount", "align": "right"},
                    {"name": "description", "label": "Beschreibung", "field": "description"},
                ],
                rows=rows,
            ).classes("w-full")

        @ui.page("/settings")
        def settings_page() -> None:
            navigation()
            ui.markdown("## Stammdaten und Budgets")

            with ui.tabs().classes("w-full") as tabs:
                account_tab = ui.tab("Konten")
                category_tab = ui.tab("Kategorien")
                budget_tab = ui.tab("Budgets")

            with ui.tab_panels(tabs, value=account_tab).classes("w-full"):
                with ui.tab_panel(account_tab):
                    name = ui.input("Kontoname").classes("w-full max-w-xl")
                    account_type = ui.select(
                        ["Bankkonto", "Bargeld", "Sparkonto", "Kreditkarte"],
                        label="Kontotyp",
                        value="Bankkonto",
                    ).classes("w-full max-w-xl")
                    starting_balance = ui.number("Startsaldo in CHF", value=0.0, step=0.05).classes("w-full max-w-xl")

                    def save_account() -> None:
                        try:
                            controller.create_account(name.value or "", account_type.value or "", float(starting_balance.value))
                        except Exception as error:
                            ui.notify(str(error), type="warning")
                            return
                        ui.notify("Konto gespeichert.", type="positive")
                        ui.navigate.to("/settings")

                    ui.button("Konto speichern", on_click=save_account).props("color=primary")

                with ui.tab_panel(category_tab):
                    category_name = ui.input("Kategoriename").classes("w-full max-w-xl")
                    category_type = ui.select(
                        {"income": "Einnahme", "expense": "Ausgabe"},
                        label="Kategorietyp",
                        value="expense",
                    ).classes("w-full max-w-xl")

                    def save_category() -> None:
                        try:
                            controller.create_category(category_name.value or "", str(category_type.value))
                        except Exception as error:
                            ui.notify(str(error), type="warning")
                            return
                        ui.notify("Kategorie gespeichert.", type="positive")
                        ui.navigate.to("/settings")

                    ui.button("Kategorie speichern", on_click=save_category).props("color=primary")

                with ui.tab_panel(budget_tab):
                    today = date.today()
                    expense_categories = controller.list_categories(category_type="expense")
                    category_options = {category.id: category.name for category in expense_categories}
                    month = ui.number("Monat", value=today.month, min=1, max=12, step=1).classes("w-full max-w-xl")
                    year = ui.number("Jahr", value=today.year, min=2000, max=2100, step=1).classes("w-full max-w-xl")
                    limit = ui.number("Budgetlimite in CHF", value=0.0, min=0.01, step=0.05).classes("w-full max-w-xl")
                    budget_category = ui.select(category_options, label="Ausgabenkategorie").classes("w-full max-w-xl")

                    def save_budget() -> None:
                        try:
                            if budget_category.value is None:
                                raise ValueError("Bitte eine Ausgabenkategorie auswaehlen.")
                            controller.create_budget(
                                month=int(month.value),
                                year=int(year.value),
                                limit_chf=float(limit.value),
                                category_id=int(budget_category.value),
                            )
                        except Exception as error:
                            ui.notify(str(error), type="warning")
                            return
                        ui.notify("Budget gespeichert.", type="positive")
                        ui.navigate.to("/settings")

                    ui.button("Budget speichern", on_click=save_budget).props("color=primary")

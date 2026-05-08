"""Transactions page."""

from __future__ import annotations

from datetime import date

from nicegui import ui

from ...utils.date_utils import month_name
from ...utils.format_utils import parse_float, parse_int
from ..components.forms import number_input, type_segmented
from ..components.layout import page_container, page_title
from ..components.tables import transaction_table
from ..controllers import FinanceController


RECURRENCE_OPTIONS = {
    "weekly": "Wöchentlich",
    "monthly": "Monatlich",
    "quarterly": "Quartalsweise",
    "yearly": "Jährlich",
}


def register_transactions_page(controller: FinanceController) -> None:
    @ui.page("/transactions")
    def transactions_page() -> None:
        accounts = controller.list_accounts()
        categories = controller.list_categories()
        account_options = {account.id: account.name for account in accounts}

        def category_options_for(transaction_type_value: str) -> dict[int, str]:
            return {category.id: category.name for category in categories if category.category_type == transaction_type_value}

        with page_container("/transactions"):
            page_title("Transaktionen", "Erfasse Einnahmen und Ausgaben mit passenden Kategorien und Konten.")

            with ui.card().classes("bp-card w-full p-6"):
                ui.label("Neue Transaktion erfassen").classes("bp-section-title mb-4")
                ui.label("Typ").classes("font-semibold mb-2")
                transaction_type = type_segmented("expense")
                with ui.grid(columns="repeat(4, minmax(180px, 1fr))").classes("w-full gap-4 mt-4"):
                    amount = number_input("Betrag (CHF)", "0.00")
                    transaction_date = ui.input("Datum", value=date.today().isoformat()).props("type=date").classes("w-full")
                    account = ui.select(account_options, label="Konto").classes("w-full")
                    category = ui.select(category_options_for("expense"), label="Kategorie").classes("w-full")
                description = ui.input("Beschreibung", placeholder="Optional").classes("w-full mt-4")

                with ui.element("div").classes("bg-gray-50 border border-gray-200 rounded-lg p-4 mt-5"):
                    recurring = ui.checkbox("Wiederkehrende Transaktion")
                    ui.label("Ideal für Miete, Lohn, Abos oder quartalsweise Zahlungen.").classes("text-sm bp-muted")
                    with ui.grid(columns="repeat(2, minmax(180px, 1fr))").classes("w-full gap-4 mt-3"):
                        recurrence = ui.select(RECURRENCE_OPTIONS, label="Wiederholung", value="monthly").classes("w-full")
                        occurrences = number_input("Anzahl Buchungen", "z.B. 6", 6)

                def update_category_options() -> None:
                    category.set_options(category_options_for(str(transaction_type.value)))
                    category.value = None

                transaction_type.on_value_change(update_category_options)

                def save_transaction() -> None:
                    try:
                        if account.value is None or category.value is None:
                            raise ValueError("Bitte Konto und Kategorie auswählen.")
                        common = {
                            "amount_chf": parse_float(amount.value, "einen Betrag"),
                            "transaction_type": str(transaction_type.value),
                            "transaction_date": date.fromisoformat(str(transaction_date.value)),
                            "description": description.value or "",
                            "account_id": int(account.value),
                            "category_id": int(category.value),
                        }
                        if recurring.value:
                            created = controller.create_recurring_transactions(
                                **common,
                                frequency=str(recurrence.value),
                                occurrences=parse_int(occurrences.value, "eine Anzahl Buchungen"),
                            )
                            ui.notify(f"{len(created)} wiederkehrende Transaktionen gespeichert.", type="positive")
                        else:
                            controller.create_transaction(**common)
                            ui.notify("Transaktion gespeichert.", type="positive")
                    except Exception as error:
                        ui.notify(str(error), type="warning")
                        return
                    ui.navigate.to("/transactions")

                with ui.row().classes("gap-3 mt-5"):
                    ui.button("Speichern", icon="save", on_click=save_transaction).classes("bp-primary-btn")
                    ui.button("Abbrechen", on_click=lambda: ui.navigate.to("/transactions")).classes("bp-secondary-btn")

            transactions = controller.list_recent_transactions()
            with ui.card().classes("bp-card w-full p-4"):
                with ui.row().classes("items-center gap-2 mb-3"):
                    ui.icon("filter_alt").classes("bp-muted")
                    ui.label("Filter").classes("font-semibold")
                month_options = {
                    "": "Alle Monate",
                    **{
                        transaction.transaction_date.strftime("%Y-%m"): month_name(transaction.transaction_date.year, transaction.transaction_date.month)
                        for transaction in transactions
                    },
                }
                with ui.grid(columns="repeat(4, minmax(170px, 1fr))").classes("w-full gap-4"):
                    filter_type = ui.select({"": "Alle Typen", "income": "Einnahmen", "expense": "Ausgaben"}, value="").classes("w-full")
                    filter_category = ui.select({"": "Alle Kategorien", **{str(category.id): category.name for category in categories}}, value="").classes("w-full")
                    filter_month = ui.select(month_options, value="").classes("w-full")
                    reset_button = ui.button("Filter zurücksetzen", icon="restart_alt").classes("bp-secondary-btn")

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
                            ui.button("Löschen", icon="delete", on_click=delete_transaction).classes("bp-danger-btn")
                            ui.button("Abbrechen", on_click=dialog.close).classes("bp-secondary-btn")
                    dialog.open()

                def open_edit_dialog(transaction_id: int) -> None:
                    transaction = next(item for item in transactions if item.id == transaction_id)
                    with ui.dialog() as dialog, ui.card().classes("bp-card p-6 w-full max-w-3xl"):
                        ui.label("Transaktion bearbeiten").classes("bp-section-title mb-4")
                        edit_type = type_segmented(transaction.transaction_type)
                        with ui.grid(columns="repeat(4, minmax(170px, 1fr))").classes("w-full gap-4 mt-4"):
                            edit_amount = number_input("Betrag (CHF)", "0.00", f"{transaction.amount_chf:.2f}")
                            edit_date = ui.input("Datum", value=transaction.transaction_date.isoformat()).props("type=date").classes("w-full")
                            edit_account = ui.select(account_options, label="Konto", value=transaction.account_id).classes("w-full")
                            edit_category = ui.select(category_options_for(transaction.transaction_type), label="Kategorie", value=transaction.category_id).classes("w-full")
                        edit_description = ui.input("Beschreibung", value=transaction.description, placeholder="Optional").classes("w-full mt-4")

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

                def filtered_transactions():
                    result = transactions
                    if filter_type.value:
                        result = [item for item in result if item.transaction_type == filter_type.value]
                    if filter_category.value:
                        result = [item for item in result if str(item.category_id) == str(filter_category.value)]
                    if filter_month.value:
                        result = [item for item in result if item.transaction_date.strftime("%Y-%m") == filter_month.value]
                    return result

                def render_transaction_list() -> None:
                    transaction_list.clear()
                    with transaction_list:
                        transaction_table(filtered_transactions(), "Keine Transaktionen gefunden.", on_edit=open_edit_dialog, on_delete=open_delete_dialog)

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

"""Accounts page."""

from __future__ import annotations

from nicegui import ui

from ...utils.format_utils import money, parse_float
from ..components.forms import number_input
from ..components.layout import empty_state, page_container, page_title
from ..controllers import FinanceController
from .shared import account_balance, usage_count


ACCOUNT_TYPES = ["Bankkonto", "Bargeld"]


def register_accounts_page(controller: FinanceController) -> None:
    @ui.page("/accounts")
    def accounts_page() -> None:
        transactions = controller.list_recent_transactions()
        accounts = controller.list_accounts()
        with page_container("/accounts", controller):
            page_title("Konten", "Verwalte Bankkonto und Bargeld mit klarem aktuellem Saldo.")

            with ui.card().classes("bp-card w-full p-6"):
                ui.label("Neues Konto erstellen").classes("bp-section-title mb-4")
                with ui.grid(columns="repeat(3, minmax(220px, 1fr))").classes("w-full gap-4"):
                    name = ui.input("Kontoname", placeholder="z.B. Girokonto, Sparkonto").classes("w-full")
                    account_type = ui.select(ACCOUNT_TYPES, label="Kontotyp", value="Bankkonto").classes("w-full")
                    starting_balance = number_input("Startsaldo (CHF)", "0.00")

                def save_account() -> None:
                    try:
                        controller.create_account(name.value or "", account_type.value or "", parse_float(starting_balance.value, "einen Startsaldo"))
                    except Exception as error:
                        ui.notify(str(error), type="warning")
                        return
                    ui.notify("Konto gespeichert.", type="positive")
                    ui.navigate.to("/accounts")

                with ui.row().classes("gap-3 mt-4"):
                    ui.button("Erstellen", icon="add", on_click=save_account).classes("bp-primary-btn")
                    ui.button("Abbrechen", on_click=lambda: ui.navigate.to("/accounts")).classes("bp-secondary-btn")

            if not accounts:
                empty_state("account_balance_wallet", "Keine Konten vorhanden.", "Erstelle dein erstes Bank- oder Bargeldkonto.")
                return

            total_start = sum(account.starting_balance_chf for account in accounts)
            total_balance = sum(account_balance(account, transactions) for account in accounts)
            with ui.element("div").classes("bp-dashboard-panel w-full p-5"):
                ui.label("Gesamtübersicht").classes("bp-section-title mb-4")
                with ui.element("div").classes("bp-account-strip"):
                    with ui.element("div").classes("bp-account-total"):
                        with ui.column().classes("gap-1"):
                            ui.label("Aktueller Gesamtsaldo").classes("text-sm text-teal-100")
                            ui.label(money(total_balance)).classes("text-4xl font-bold bp-stat-value")
                        ui.label(f"{len(accounts)} Konten aktiv").classes("text-teal-100")
                    with ui.grid(columns="repeat(2, minmax(180px, 1fr))").classes("w-full gap-4"):
                        with ui.column().classes("bp-account-mini gap-1"):
                            ui.label("Anzahl Konten").classes("bp-muted")
                            ui.label(str(len(accounts))).classes("bp-account-mini-value")
                        with ui.column().classes("bp-account-mini gap-1"):
                            ui.label("Gesamter Startsaldo").classes("bp-muted")
                            ui.label(money(total_start)).classes("bp-account-mini-value")

            def open_edit_account_dialog(account_id: int) -> None:
                account_to_edit = next(account for account in accounts if account.id == account_id)
                with ui.dialog() as dialog, ui.card().classes("bp-card p-6 w-full max-w-2xl"):
                    ui.label("Konto bearbeiten").classes("bp-section-title mb-4")
                    with ui.grid(columns="repeat(3, minmax(180px, 1fr))").classes("w-full gap-4"):
                        edit_name = ui.input("Kontoname", value=account_to_edit.name).classes("w-full")
                        edit_type = ui.select(ACCOUNT_TYPES, label="Kontotyp", value=account_to_edit.account_type if account_to_edit.account_type in ACCOUNT_TYPES else "Bankkonto").classes("w-full")
                        edit_starting_balance = number_input("Startsaldo (CHF)", "0.00", f"{account_to_edit.starting_balance_chf:.2f}")

                    def save_account_edit() -> None:
                        try:
                            controller.update_account(
                                account_id=account_id,
                                name=edit_name.value or "",
                                account_type=edit_type.value or "",
                                starting_balance_chf=parse_float(edit_starting_balance.value, "einen Startsaldo"),
                            )
                        except Exception as error:
                            ui.notify(str(error), type="warning")
                            return
                        ui.notify("Konto aktualisiert.", type="positive")
                        ui.navigate.to("/accounts")

                    with ui.row().classes("gap-3 mt-4"):
                        ui.button("Speichern", icon="save", on_click=save_account_edit).classes("bp-primary-btn")
                        ui.button("Abbrechen", on_click=dialog.close).classes("bp-secondary-btn")
                dialog.open()

            def open_delete_account_dialog(account_id: int) -> None:
                with ui.dialog() as dialog, ui.card().classes("bp-card p-6"):
                    ui.label("Konto löschen?").classes("bp-section-title")
                    ui.label("Dieses Konto wird nur gelöscht, wenn keine Transaktionen damit verknüpft sind.").classes("bp-muted")

                    def delete_account() -> None:
                        try:
                            controller.delete_account(account_id)
                        except Exception as error:
                            ui.notify(str(error), type="warning")
                            return
                        ui.notify("Konto gelöscht.", type="positive")
                        ui.navigate.to("/accounts")

                    with ui.row().classes("gap-3 mt-4"):
                        ui.button("Löschen", icon="delete", on_click=delete_account).classes("bp-danger-btn")
                        ui.button("Abbrechen", on_click=dialog.close).classes("bp-secondary-btn")
                dialog.open()

            with ui.element("div").classes("bp-grid-desktop"):
                for account in accounts:
                    balance = account_balance(account, transactions)
                    count = usage_count(transactions, "account_id", account.id)
                    is_cash = account.account_type == "Bargeld"
                    icon = "payments" if is_cash else "account_balance"
                    pill = "bp-cash-pill" if is_cash else "bp-bank-pill"
                    icon_bg = "bg-amber-100 text-amber-700" if is_cash else "bg-blue-100 text-blue-700"
                    with ui.card().classes("bp-card bp-card-hover w-full p-6"):
                        with ui.row().classes("w-full items-start justify-between gap-3 no-wrap"):
                            with ui.row().classes("items-center gap-3 no-wrap"):
                                with ui.element("div").classes(f"{icon_bg} rounded-full p-3"):
                                    ui.icon(icon).classes("text-2xl")
                                with ui.column().classes("gap-1"):
                                    ui.label(account.name).classes("font-bold text-lg text-gray-900")
                                    ui.label(account.account_type).classes(f"bp-pill {pill}")
                            with ui.row().classes("gap-1 no-wrap"):
                                ui.button(icon="edit", on_click=lambda account_id=account.id: open_edit_account_dialog(account_id)).props("flat dense round color=primary")
                                ui.button(icon="delete", on_click=lambda account_id=account.id: open_delete_account_dialog(account_id)).props("flat dense round color=negative")
                        ui.label("Aktueller Saldo").classes("text-xs bp-muted mt-6")
                        ui.label(money(balance)).classes(f"text-3xl font-bold bp-money {'bp-positive' if balance >= 0 else 'bp-negative'}")
                        ui.separator().classes("my-4")
                        with ui.row().classes("w-full justify-between"):
                            ui.label("Startsaldo").classes("bp-muted")
                            ui.label(money(account.starting_balance_chf)).classes("font-semibold bp-money")
                        with ui.row().classes("w-full justify-between"):
                            ui.label("Transaktionen").classes("bp-muted")
                            ui.label(str(count)).classes("font-semibold")

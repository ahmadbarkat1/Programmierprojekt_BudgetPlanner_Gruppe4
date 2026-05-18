"""Budget page."""

from __future__ import annotations

from nicegui import ui

from ...utils.date_utils import current_year_month, month_name
from ...utils.format_utils import money, parse_float, parse_int
from ..components.cards import envelope_card, progress_bar, stat_card
from ..components.forms import number_input
from ..components.layout import empty_state, month_nav_card, page_container, page_title
from ..controllers import FinanceController


def register_budget_page(controller: FinanceController) -> None:
    @ui.page("/budget")
    def budget_page(year: int | None = None, month: int | None = None) -> None:
        current_year, current_month = current_year_month()
        year = year or current_year
        month = month or current_month
        data = controller.dashboard_data(year=year, month=month)
        expense_categories = controller.list_categories(category_type="expense")
        category_options = {category.id: category.name for category in expense_categories}
        current_budgets = controller.list_budgets(year=year, month=month)
        current_budget_limit = sum(budget.limit_chf for budget in current_budgets)
        current_expenses = sum(transaction.amount_chf for transaction in data.transactions if transaction.transaction_type == "expense")
        current_remaining = round(current_budget_limit - current_expenses, 2)
        current_usage = (current_expenses / current_budget_limit * 100) if current_budget_limit else 0

        with page_container("/budget", controller):
            page_title("Budget", "Plane dein Monatsbudget nach Kategorie und sieh sofort, wo du noch Luft hast.")

            with ui.element("div").classes("bp-kpi-grid"):
                month_nav_card("/budget", year, month)
                stat_card("Budget", money(current_budget_limit), "inventory_2", "blue", month_name(year, month))
                stat_card("Ausgaben", money(current_expenses), "trending_down", "red", month_name(year, month))
                stat_card("Verbleibend", money(current_remaining), "savings", "green" if current_remaining >= 0 else "red", month_name(year, month))

            with ui.element("div").classes("bp-two-col"):
                with ui.card().classes("bp-card w-full p-6"):
                    ui.label("Budget nach Kategorie erfassen").classes("bp-section-title mb-2")
                    ui.label("Jahr und Monat werden automatisch aus dem Systemdatum vorbelegt.").classes("bp-muted mb-4")
                    with ui.grid(columns="repeat(2, minmax(0, 1fr))").classes("w-full gap-4"):
                        budget_month = number_input("Monat", "1-12", month)
                        budget_year = number_input("Jahr", str(year), year)
                    budget_category = ui.select(category_options, label="Ausgabenkategorie").classes("w-full")
                    limit = number_input("Betrag (CHF)", "0.00")

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

                    with ui.row().classes("gap-3 mt-5"):
                        ui.button("Speichern", icon="save", on_click=save_budget).classes("bp-primary-btn")
                        ui.button("Abbrechen", on_click=lambda: ui.navigate.to("/budget")).classes("bp-secondary-btn")

                with ui.card().classes("bp-card w-full p-6"):
                    ui.label("Budget vom Vormonat übernehmen").classes("bp-section-title mb-2")
                    ui.label("Du kannst die Budgets aus dem Vormonat übernehmen und danach anpassen.").classes("bp-muted")
                    copy_month = number_input("Zielmonat", "1-12", month)
                    copy_year = number_input("Zieljahr", str(year), year)

                    def copy_previous_budget() -> None:
                        try:
                            copied = controller.copy_previous_month_budget(
                                year=parse_int(copy_year.value, "ein Zieljahr"),
                                month=parse_int(copy_month.value, "einen Zielmonat"),
                            )
                        except Exception as error:
                            ui.notify(str(error), type="warning")
                            return
                        ui.notify(f"{len(copied)} Budget-Umschläge übernommen.", type="positive")
                        ui.navigate.to("/budget")

                    ui.button("Budget vom Vormonat übernehmen", icon="content_copy", on_click=copy_previous_budget).classes("bp-primary-btn mt-4")

            def open_edit_budget_dialog(budget_id: int) -> None:
                budget_to_edit = next(status.budget for status in data.budget_statuses if status.budget.id == budget_id)
                with ui.dialog() as dialog, ui.card().classes("bp-card p-6 w-full max-w-2xl"):
                    ui.label("Budget bearbeiten").classes("bp-section-title mb-4")
                    with ui.grid(columns="repeat(2, minmax(0, 1fr))").classes("w-full gap-4"):
                        edit_month = number_input("Monat", "1-12", budget_to_edit.month)
                        edit_year = number_input("Jahr", str(budget_to_edit.year), budget_to_edit.year)
                    edit_category = ui.select(category_options, label="Ausgabenkategorie", value=budget_to_edit.category_id).classes("w-full")
                    edit_limit = number_input("Betrag (CHF)", "0.00", f"{budget_to_edit.limit_chf:.2f}")

                    def save_budget_edit() -> None:
                        try:
                            if edit_category.value is None:
                                raise ValueError("Bitte eine Ausgabenkategorie auswählen.")
                            controller.update_budget(
                                budget_id=budget_id,
                                month=parse_int(edit_month.value, "einen Monat"),
                                year=parse_int(edit_year.value, "ein Jahr"),
                                limit_chf=parse_float(edit_limit.value, "ein Budgetlimit"),
                                category_id=int(edit_category.value),
                            )
                        except Exception as error:
                            ui.notify(str(error), type="warning")
                            return
                        ui.notify("Budget aktualisiert.", type="positive")
                        ui.navigate.to(f"/budget?year={year}&month={month}")

                    with ui.row().classes("gap-3 mt-5"):
                        ui.button("Speichern", icon="save", on_click=save_budget_edit).classes("bp-primary-btn")
                        ui.button("Abbrechen", on_click=dialog.close).classes("bp-secondary-btn")
                dialog.open()

            def open_delete_budget_dialog(budget_id: int) -> None:
                budget_to_delete = next(status.budget for status in data.budget_statuses if status.budget.id == budget_id)
                with ui.dialog() as dialog, ui.card().classes("bp-card p-6"):
                    ui.label(f"Budget '{budget_to_delete.category.name}' löschen?").classes("bp-section-title")
                    ui.label("Das Budget wird gelöscht. Bereits erfasste Transaktionen bleiben erhalten.").classes("bp-muted")

                    def delete_budget() -> None:
                        try:
                            controller.delete_budget(budget_id)
                        except Exception as error:
                            ui.notify(str(error), type="warning")
                            return
                        ui.notify("Budget gelöscht.", type="positive")
                        ui.navigate.to(f"/budget?year={year}&month={month}")

                    with ui.row().classes("gap-3 mt-4"):
                        ui.button("Löschen", icon="delete", on_click=delete_budget).classes("bp-danger-btn")
                        ui.button("Abbrechen", on_click=dialog.close).classes("bp-secondary-btn")
                dialog.open()

            with ui.card().classes("bp-card w-full p-6"):
                ui.label("Budgets für diesen Monat").classes("bp-section-title")
                if not data.budget_statuses:
                    empty_state("inventory_2", "Noch keine Budgets für diesen Monat.", "Lege dein erstes Budget fest oder übernimm den Vormonat.")
                else:
                    with ui.element("div").classes("bp-grid-desktop mt-4"):
                        with ui.element("div").classes("bp-account-total"):
                            with ui.column().classes("gap-1"):
                                ui.label("Alle Budgets").classes("text-sm text-teal-100")
                                ui.label(money(current_remaining)).classes("text-4xl font-bold bp-stat-value")
                                ui.label(f"{money(current_expenses)} von {money(current_budget_limit)} verbraucht").classes("text-teal-100")
                            progress_bar(current_usage, "danger" if current_remaining < 0 else "warning" if current_usage >= 80 else "ok")
                        for status in data.budget_statuses:
                            envelope_card(status, on_edit=open_edit_budget_dialog, on_delete=open_delete_budget_dialog)

            budgets = controller.list_budgets()
            with ui.expansion("Erfasste Budgets", icon="table_chart", value=True).classes("bp-card w-full p-2"):
                if not budgets:
                    empty_state("inventory_2", "Kein Budget festgelegt.", "Lege dein erstes Budget fest.")
                else:
                    budget_table_area = ui.column().classes("w-full")

                    columns = [
                        {"name": "period", "label": "Monat", "field": "period", "align": "left"},
                        {"name": "category", "label": "Kategorie", "field": "category", "align": "left"},
                        {"name": "limit", "label": "Budget", "field": "limit", "align": "right"},
                        {"name": "spent", "label": "Verbrauch", "field": "spent", "align": "right"},
                        {"name": "remaining", "label": "Verbleibend", "field": "remaining", "align": "right"},
                        {"name": "status", "label": "Auslastung", "field": "status", "align": "right"},
                    ]
                    rows = []
                    for budget in budgets:
                        month_data = controller.dashboard_data(year=budget.year, month=budget.month)
                        spent = sum(
                            transaction.amount_chf
                            for transaction in month_data.transactions
                            if transaction.transaction_type == "expense" and transaction.category_id == budget.category_id
                        )
                        remaining = round(budget.limit_chf - spent, 2)
                        percent = (spent / budget.limit_chf * 100) if budget.limit_chf else 0
                        rows.append(
                            {
                                "period": f"{budget.month:02d}.{budget.year}",
                                "category": budget.category.name,
                                "limit": money(budget.limit_chf),
                                "spent": money(spent),
                                "remaining": money(remaining),
                                "status": f"{percent:.0f}%",
                                "status_class": "bp-negative" if remaining < 0 else "bp-warning" if percent >= 80 else "bp-positive",
                            }
                        )

                    def render_table(table_rows: list[dict[str, str]]) -> None:
                        table = ui.table(columns=columns, rows=table_rows).classes("bp-table w-full").props("flat")
                        table.add_slot(
                            "body-cell-status",
                            """
                            <q-td :props="props">
                                <span class="font-semibold" :class="props.row.status_class">{{ props.row.status }}</span>
                            </q-td>
                            """,
                        )

                    def render_budget_tables() -> None:
                        budget_table_area.clear()
                        with budget_table_area:
                            grouped: dict[str, list[dict[str, str]]] = {}
                            for row in rows:
                                grouped.setdefault(row["period"], []).append(row)
                            for period, period_rows in grouped.items():
                                ui.label(period).classes("text-lg font-bold text-gray-900 mt-4")
                                render_table(period_rows)

                    render_budget_tables()

    @ui.page("/settings")
    def settings_redirect_page() -> None:
        ui.navigate.to("/accounts")

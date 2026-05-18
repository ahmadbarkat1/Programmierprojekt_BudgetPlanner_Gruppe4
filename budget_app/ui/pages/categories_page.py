"""Categories page."""

from __future__ import annotations

from nicegui import ui

from ..components.forms import type_segmented
from ..components.layout import empty_state, page_container, page_title
from ..controllers import FinanceController
from .shared import category_type_label, usage_count


def register_categories_page(controller: FinanceController) -> None:
    @ui.page("/categories")
    def categories_page() -> None:
        transactions = controller.list_recent_transactions()
        categories = controller.list_categories()
        with page_container("/categories", controller):
            page_title("Kategorien", "Ordne Einnahmen und Ausgaben sauber deinen Budgets zu.")

            with ui.card().classes("bp-card w-full p-6"):
                ui.label("Neue Kategorie erstellen").classes("bp-section-title mb-4")
                with ui.grid(columns="340px minmax(320px, 1fr)").classes("w-full max-w-5xl gap-6 items-center"):
                    category_type = type_segmented("expense")
                    category_name = ui.input("Kategoriename", placeholder="z.B. Lebensmittel, Transport").classes("w-full")

                def save_category() -> None:
                    try:
                        controller.create_category(category_name.value or "", str(category_type.value))
                    except Exception as error:
                        ui.notify(str(error), type="warning")
                        return
                    ui.notify("Kategorie gespeichert.", type="positive")
                    ui.navigate.to("/categories")

                with ui.row().classes("gap-3 mt-4"):
                    ui.button("Erstellen", icon="add", on_click=save_category).classes("bp-primary-btn")
                    ui.button("Abbrechen", on_click=lambda: ui.navigate.to("/categories")).classes("bp-secondary-btn")

            if not categories:
                empty_state("sell", "Noch keine Kategorien vorhanden.", "Erstelle Einnahme- und Ausgabekategorien, um Transaktionen sauber einzuordnen.")
                return

            rows = [
                {
                    "name": category.name,
                    "type": category_type_label(category),
                    "type_class": "bp-income-pill" if category.category_type == "income" else "bp-expense-pill",
                    "usage": f"{usage_count(transactions, 'category_id', category.id)} Transaktionen",
                    "id": category.id,
                }
                for category in categories
            ]
            table = ui.table(
                columns=[
                    {"name": "name", "label": "Kategoriename", "field": "name", "align": "left"},
                    {"name": "type", "label": "Typ", "field": "type", "align": "left"},
                    {"name": "usage", "label": "Verwendungen", "field": "usage", "align": "left"},
                    {"name": "actions", "label": "Aktionen", "field": "actions", "align": "right"},
                ],
                rows=rows,
                row_key="id",
            ).classes("bp-card bp-table w-full").props("flat")
            table.add_slot(
                "body-cell-type",
                """
                <q-td :props="props">
                    <span class="bp-pill" :class="props.row.type_class">{{ props.row.type }}</span>
                </q-td>
                """,
            )
            table.add_slot(
                "body-cell-actions",
                """
                <q-td :props="props">
                    <q-btn flat dense round icon="edit" color="primary" @click="$parent.$emit('edit-category', props.row.id)" />
                    <q-btn flat dense round icon="delete" color="negative" @click="$parent.$emit('delete-category', props.row.id)" />
                </q-td>
                """,
            )

            def open_edit_category_dialog(category_id: int) -> None:
                category = next(item for item in categories if item.id == category_id)
                with ui.dialog() as dialog, ui.card().classes("bp-card p-6 w-full max-w-2xl"):
                    ui.label("Kategorie bearbeiten").classes("bp-section-title mb-4")
                    edit_name = ui.input("Kategoriename", value=category.name).classes("w-full")
                    edit_type = type_segmented(category.category_type)

                    def save_category_edit() -> None:
                        try:
                            controller.update_category(category_id=category_id, name=edit_name.value or "", category_type=str(edit_type.value))
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
                category = next(item for item in categories if item.id == category_id)
                with ui.dialog() as dialog, ui.card().classes("bp-card p-6"):
                    ui.label(f"Kategorie '{category.name}' löschen?").classes("bp-section-title")
                    ui.label(
                        "Kategorien können nur gelöscht werden, wenn keine Transaktionen oder Budgets damit verbunden sind. "
                        "Zugehörige Transaktionen bleiben geschützt und verhindern das Löschen."
                    ).classes("bp-muted")

                    def delete_category() -> None:
                        try:
                            controller.delete_category(category_id)
                        except Exception as error:
                            ui.notify(str(error), type="warning")
                            return
                        ui.notify("Kategorie gelöscht.", type="positive")
                        ui.navigate.to("/categories")

                    with ui.row().classes("gap-3 mt-4"):
                        ui.button("Löschen", icon="delete", on_click=delete_category).classes("bp-danger-btn")
                        ui.button("Abbrechen", on_click=dialog.close).classes("bp-secondary-btn")
                dialog.open()

            table.on("edit-category", lambda event: open_edit_category_dialog(int(event.args)))
            table.on("delete-category", lambda event: open_delete_category_dialog(int(event.args)))

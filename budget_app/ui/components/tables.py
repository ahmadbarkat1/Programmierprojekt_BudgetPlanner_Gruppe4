"""Shared table components."""

from __future__ import annotations

from collections.abc import Callable

from nicegui import ui

from ...domain.models import Transaction
from ...utils.format_utils import money
from .layout import empty_state


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
    empty_cta: str | None = None,
    empty_cta_action: Callable[[], None] | None = None,
    empty_icon: str = "receipt_long",
) -> None:
    if not transactions:
        empty_state(
            empty_icon,
            empty_text,
            "Erfasse deine erste Einnahme oder Ausgabe, damit die Übersicht lebendig wird.",
            empty_cta,
            empty_cta_action,
        )
        return
    columns: list[dict[str, str]] = [
        {"name": "date", "label": "Datum", "field": "date", "align": "left"},
        {"name": "type", "label": "Typ", "field": "type", "align": "left"},
        {"name": "category", "label": "Kategorie", "field": "category", "align": "left"},
        {"name": "account", "label": "Konto", "field": "account", "align": "left"},
        {"name": "description", "label": "Beschreibung", "field": "description", "align": "left"},
        {"name": "amount", "label": "Betrag", "field": "amount", "align": "right"},
    ]
    if on_edit is not None or on_delete is not None:
        columns.append({"name": "actions", "label": "Aktionen", "field": "actions", "align": "right"})
    table = ui.table(columns=columns, rows=transaction_rows(transactions), row_key="id").classes("bp-card bp-table w-full").props("flat")
    table.add_slot(
        "body-cell-type",
        """
        <q-td :props="props">
            <span class="bp-pill" :class="props.row.type_class">{{ props.row.type }}</span>
        </q-td>
        """,
    )
    table.add_slot(
        "body-cell-amount",
        """
        <q-td :props="props">
            <span class="font-semibold" :class="props.row.amount_class">{{ props.row.amount }}</span>
        </q-td>
        """,
    )
    if on_edit is not None or on_delete is not None:
        table.add_slot(
            "body-cell-actions",
            """
            <q-td :props="props">
                <q-btn flat dense round icon="edit" color="primary" @click="$parent.$emit('edit-row', props.row.id)" />
                <q-btn flat dense round icon="delete" color="negative" @click="$parent.$emit('delete-row', props.row.id)" />
            </q-td>
            """,
        )
        if on_edit is not None:
            table.on("edit-row", lambda event: on_edit(int(event.args)))
        if on_delete is not None:
            table.on("delete-row", lambda event: on_delete(int(event.args)))

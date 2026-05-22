"""Form helpers."""

from __future__ import annotations

from collections.abc import Callable

from nicegui import ui


def number_input(label: str, placeholder: str = "", value: object | None = None):
    field = ui.input(label, placeholder=placeholder, value=value).props("inputmode=decimal").classes("w-full")
    return field


class TypeSegmented:
    ACTIVE_INCOME_STYLE = (
        "background-color: #22c55e !important; "
        "color: #ffffff !important; "
        "border: 4px solid #16a34a !important; "
        "box-shadow: 0 0 0 3px rgba(34, 197, 94, .24) !important;"
    )
    ACTIVE_EXPENSE_STYLE = (
        "background-color: #ef4444 !important; "
        "color: #ffffff !important; "
        "border: 4px solid #dc2626 !important; "
        "box-shadow: 0 0 0 3px rgba(239, 68, 68, .24) !important;"
    )
    INACTIVE_STYLE = (
        "background-color: #5b9bd5 !important; "
        "color: #ffffff !important; "
        "border: 4px solid #5b9bd5 !important; "
        "box-shadow: none !important;"
    )

    def __init__(self, value: str = "expense") -> None:
        self.value = value if value in {"income", "expense"} else "expense"
        self._callbacks: list[Callable[[], None]] = []
        with ui.row().classes("bp-type-toggle bp-type-toggle-compact"):
            self.income_button = ui.button("EINNAHME", on_click=lambda: self.set_value("income")).props("unelevated").classes("bp-type-option bp-type-income")
            self.expense_button = ui.button("AUSGABE", on_click=lambda: self.set_value("expense")).props("unelevated").classes("bp-type-option bp-type-expense")
        self.update_transaction_type_buttons()

    def set_value(self, value: str) -> None:
        if value not in {"income", "expense"}:
            return
        self.value = value
        self.update_transaction_type_buttons()
        for callback in self._callbacks:
            callback()

    def on_value_change(self, callback: Callable[[], None]) -> "TypeSegmented":
        self._callbacks.append(callback)
        return self

    def update_transaction_type_buttons(self) -> None:
        self.income_button.classes(remove="is-active")
        self.expense_button.classes(remove="is-active")
        if self.value == "income":
            self.income_button.classes(add="is-active")
            self.income_button.style(replace=self.ACTIVE_INCOME_STYLE)
            self.expense_button.style(replace=self.INACTIVE_STYLE)
        else:
            self.expense_button.classes(add="is-active")
            self.income_button.style(replace=self.INACTIVE_STYLE)
            self.expense_button.style(replace=self.ACTIVE_EXPENSE_STYLE)


def type_segmented(value: str = "income"):
    return TypeSegmented(value)

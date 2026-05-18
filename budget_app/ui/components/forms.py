"""Form helpers."""

from __future__ import annotations

from collections.abc import Callable

from nicegui import ui


def number_input(label: str, placeholder: str = "", value: object | None = None):
    field = ui.input(label, placeholder=placeholder, value=value).props("inputmode=decimal").classes("w-full")
    return field


class TypeSegmented:
    def __init__(self, value: str = "expense") -> None:
        self.value = value
        self._callbacks: list[Callable[[], None]] = []
        with ui.row().classes("bp-type-toggle"):
            self.income_button = ui.button("Einnahme", on_click=lambda: self.set_value("income")).props("unelevated").classes("bp-type-option bp-type-income")
            self.expense_button = ui.button("Ausgabe", on_click=lambda: self.set_value("expense")).props("unelevated").classes("bp-type-option bp-type-expense")
        self._refresh()

    def set_value(self, value: str) -> None:
        self.value = value
        self._refresh()
        for callback in self._callbacks:
            callback()

    def on_value_change(self, callback: Callable[[], None]) -> "TypeSegmented":
        self._callbacks.append(callback)
        return self

    def _refresh(self) -> None:
        self.income_button.classes(add="is-active" if self.value == "income" else None, remove="is-active" if self.value != "income" else None)
        self.expense_button.classes(add="is-active" if self.value == "expense" else None, remove="is-active" if self.value != "expense" else None)


def type_segmented(value: str = "expense"):
    return TypeSegmented(value)

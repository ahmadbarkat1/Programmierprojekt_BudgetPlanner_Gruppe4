"""Form helpers."""

from __future__ import annotations

from nicegui import ui


def number_input(label: str, placeholder: str = "", value: object | None = None):
    field = ui.input(label, placeholder=placeholder, value=value).props("inputmode=decimal").classes("w-full")
    return field


def type_segmented(value: str = "expense"):
    return ui.radio({"income": "Einnahme", "expense": "Ausgabe"}, value=value).props("inline").classes("bp-segmented")

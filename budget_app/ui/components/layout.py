"""Shared layout helpers."""

from __future__ import annotations

import csv
import zipfile
from io import BytesIO, StringIO
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import date
from typing import Iterable

from nicegui import ui

from ...services.pdf_export_service import export_budgetplanner_pdf
from ...utils.date_utils import current_year_month, month_name, next_month, previous_month
from ..controllers import FinanceController


def navigation(active_path: str, controller: FinanceController | None = None) -> None:
    nav_items = [
        ("/", "home", "Übersicht"),
        ("/accounts", "account_balance_wallet", "Konten"),
        ("/categories", "sell", "Kategorien"),
        ("/budget", "inventory_2", "Budget"),
        ("/transactions", "sync_alt", "Transaktionen"),
    ]
    with ui.header(elevated=False).classes("bp-header"):
        with ui.row().classes("bp-shell w-full items-center justify-between py-4"):
            with ui.row().classes("items-center gap-4 no-wrap"):
                ui.icon("account_balance_wallet").classes("bp-brand-icon text-teal-700")
                ui.label("Budget Planner").classes("bp-brand-title text-gray-900")
            with ui.row().classes("items-center gap-3 no-wrap"):
                ui.button("Darkmode", icon="dark_mode", on_click=toggle_dark_mode).classes("bp-secondary-btn bp-header-action bp-darkmode-btn")
                import_button = ui.button("Import", icon="upload_file", on_click=lambda: open_import_dialog(controller, active_path)).classes("bp-secondary-btn bp-header-action")
                ui.button("Export", icon="ios_share", on_click=lambda: open_export_dialog(active_path, controller)).classes("bp-secondary-btn bp-header-action")
                help_button = ui.button(icon="help_outline", on_click=open_help_dialog).props("round").classes("bp-secondary-btn bp-help-btn")
    with ui.row().classes("bp-nav w-full"):
        with ui.row().classes("bp-shell w-full gap-8 overflow-x-auto no-wrap"):
            for path, icon, label in nav_items:
                classes = "bp-nav-link bp-nav-active" if active_path == path else "bp-nav-link"
                with ui.link(target=path).classes(classes):
                    with ui.row().classes("items-center gap-2 no-wrap"):
                        ui.icon(icon).classes("text-xl")
                        ui.label(label)


def page_container(active_path: str, controller: FinanceController | None = None):
    navigation(active_path, controller)
    return ui.column().classes("bp-page w-full gap-6")


def open_export_dialog(active_path: str, controller: FinanceController | None) -> None:
    current_year, current_month = current_year_month()
    month_options = _export_month_options(controller, current_year, current_month)
    with ui.dialog() as dialog, ui.card().classes("bp-card p-6 w-full max-w-2xl"):
        ui.label("Export").classes("bp-section-title")
        ui.label("Wähle Datenbereiche, Format und bei Bedarf den Monat für Budgets und Transaktionen.").classes("bp-muted mb-3")
        export_format = ui.select({"csv": "CSV", "pdf": "PDF"}, label="Exportformat", value=None).classes("w-full")
        export_month = ui.select(month_options, label="Monat", value=f"{current_year}-{current_month:02d}").classes("w-full")

        with ui.element("div").classes("bp-export-options mt-4"):
            overview_area = ui.checkbox("Übersicht", value=True)
            accounts_area = ui.checkbox("Konten", value=True)
            categories_area = ui.checkbox("Kategorien", value=True)
            budgets_area = ui.checkbox("Budgets", value=True)
            transactions_area = ui.checkbox("Transaktionen", value=True)
            all_areas = ui.checkbox("Alle", value=True)

        area_checkboxes = {
            "overview": overview_area,
            "accounts": accounts_area,
            "categories": categories_area,
            "budgets": budgets_area,
            "transactions": transactions_area,
        }

        syncing_all_area = {"active": False}

        def select_all_areas() -> None:
            if syncing_all_area["active"]:
                return
            syncing_all_area["active"] = True
            try:
                for checkbox in area_checkboxes.values():
                    checkbox.value = bool(all_areas.value)
            finally:
                syncing_all_area["active"] = False

        def sync_all_area_state() -> None:
            if syncing_all_area["active"]:
                return
            syncing_all_area["active"] = True
            try:
                all_areas.value = all(bool(checkbox.value) for checkbox in area_checkboxes.values())
            finally:
                syncing_all_area["active"] = False

        all_areas.on_value_change(select_all_areas)
        for checkbox in area_checkboxes.values():
            checkbox.on_value_change(sync_all_area_state)

        def run_export() -> None:
            if controller is None:
                ui.notify("Export ist auf dieser Seite nicht verfügbar.", type="warning")
                return
            selected_areas = _selected_export_areas(
                overview=bool(overview_area.value),
                accounts=bool(accounts_area.value),
                categories=bool(categories_area.value),
                budgets=bool(budgets_area.value),
                transactions=bool(transactions_area.value),
                all_selected=bool(all_areas.value),
            )
            if not selected_areas:
                ui.notify("Bitte wähle mindestens einen Bereich für den Export aus.", type="warning")
                return
            if not export_format.value:
                ui.notify("Bitte wähle ein Exportformat aus.", type="warning")
                return
            selected_year, selected_month = [int(value) for value in str(export_month.value).split("-")]
            export_selected_data(controller, selected_areas, str(export_format.value), selected_year, selected_month)
            dialog.close()

        with ui.row().classes("gap-3 mt-5"):
            ui.button("Exportieren", icon="download", on_click=run_export).classes("bp-primary-btn")
            ui.button("Abbrechen", on_click=dialog.close).classes("bp-secondary-btn")
    dialog.open()


def toggle_dark_mode() -> None:
    ui.run_javascript(
        """
        document.body.classList.toggle('bp-dark');
        const isDark = document.body.classList.contains('bp-dark');
        localStorage.setItem('bpDarkMode', isDark ? '1' : '0');
        window.bpUpdateDarkModeButtons?.(isDark);
        """
    )


def open_help_dialog() -> None:
    with ui.dialog() as dialog, ui.card().classes("bp-card bp-help-dialog p-6 w-full max-w-2xl"):
        with ui.row().classes("w-full items-start justify-between gap-4 no-wrap"):
            with ui.column().classes("gap-1"):
                ui.label("Hilfe").classes("bp-section-title")
                ui.label("Kurzüberblick für den Budget Planner.").classes("bp-muted")
            ui.button(icon="close", on_click=dialog.close).props("flat round").classes("bp-help-close")

        with ui.element("div").classes("bp-help-list mt-4"):
            with ui.element("div").classes("bp-help-item"):
                ui.icon("savings").classes("bp-help-icon")
                with ui.column().classes("gap-1"):
                    ui.label("Envelope-System").classes("font-bold")
                    ui.label(
                        "Der Budget Planner arbeitet wie ein Couvert-System: Für jede Ausgabenkategorie legen Sie ein eigenes Monatsbudget fest. "
                        "Jede Ausgabe wird einem Couvert zugeordnet, damit sofort sichtbar ist, wie viel pro Kategorie noch verfügbar ist."
                    ).classes("bp-muted")
            with ui.element("div").classes("bp-help-item"):
                ui.icon("dashboard").classes("bp-help-icon")
                with ui.column().classes("gap-1"):
                    ui.label("Übersicht").classes("font-bold")
                    ui.label("Hier sehen Sie Budgetstatus, Kontostände, Ausgaben nach Kategorie und Monatsvergleiche.").classes("bp-muted")
            with ui.element("div").classes("bp-help-item"):
                ui.icon("account_balance_wallet").classes("bp-help-icon")
                with ui.column().classes("gap-1"):
                    ui.label("Konten").classes("font-bold")
                    ui.label("Verwalten Sie Bankkonten, Bargeld oder Sparkonten und behalten Sie Ihre aktuellen Kontostände im Blick.").classes("bp-muted")
            with ui.element("div").classes("bp-help-item"):
                ui.icon("sell").classes("bp-help-icon")
                with ui.column().classes("gap-1"):
                    ui.label("Kategorien").classes("font-bold")
                    ui.label("Erstellen Sie Kategorien für Einnahmen und Ausgaben, damit Transaktionen sauber eingeordnet werden können.").classes("bp-muted")
            with ui.element("div").classes("bp-help-item"):
                ui.icon("inventory_2").classes("bp-help-icon")
                with ui.column().classes("gap-1"):
                    ui.label("Budget").classes("font-bold")
                    ui.label(
                        "Legen Sie pro Kategorie ein Monatsbudget fest und erkennen Sie schnell, wo noch Spielraum bleibt "
                        "oder welches Kategorie-Budget bereits überschritten wurde."
                    ).classes("bp-muted")
            with ui.element("div").classes("bp-help-item"):
                ui.icon("sync_alt").classes("bp-help-icon")
                with ui.column().classes("gap-1"):
                    ui.label("Transaktionen").classes("font-bold")
                    ui.label("Erfassen Sie Einnahmen oder Ausgaben und ordnen Sie diese einem Konto und einer Kategorie zu.").classes("bp-muted")
            with ui.element("div").classes("bp-help-item"):
                ui.icon("upload_file").classes("bp-help-icon")
                with ui.column().classes("gap-1"):
                    ui.label("Import und Export").classes("font-bold")
                    ui.label("Importieren Sie CSV-Daten oder exportieren Sie Monatsdaten als CSV oder Druckansicht.").classes("bp-muted")
            with ui.element("div").classes("bp-help-item"):
                ui.icon("support_agent").classes("bp-help-icon")
                with ui.column().classes("gap-1"):
                    ui.label("Kontakt").classes("font-bold")
                    ui.label("Bei weiteren Fragen wenden Sie sich an unser Supportteam: support@budgetplanner.ch").classes("bp-muted")

        with ui.row().classes("justify-end mt-5"):
            ui.button("Verstanden", icon="check", on_click=dialog.close).classes("bp-primary-btn")
    dialog.open()


def open_import_dialog(controller: FinanceController | None, active_path: str = "/") -> None:
    with ui.dialog() as dialog, ui.card().classes("bp-card p-6 w-full max-w-xl"):
        ui.label("CSV Import").classes("bp-section-title")
        ui.label("Importiert Konten, Kategorien, Budgets oder Transaktionen aus CSV-Dateien. ZIP-Dateien mit mehreren CSVs werden ebenfalls unterstützt.").classes("bp-muted mb-3")
        with ui.element("div").classes("bg-blue-50 border border-blue-200 rounded-lg p-4"):
            ui.label("Erwartete Transaktions-Spalten").classes("font-bold text-blue-900")
            ui.label("Datum; Typ; Kategorie; Konto; Beschreibung; Betrag CHF").classes("text-blue-900")
            ui.label("Tipp: Exportierte CSV- oder ZIP-Dateien können direkt wieder importiert werden.").classes("text-blue-900")

        async def handle_upload(event) -> None:
            try:
                result = await import_uploaded_data(event.file, controller)
            except Exception as error:
                ui.notify(str(error), type="warning")
                return
            _show_import_result(result)
            dialog.close()
            ui.navigate.to(active_path)

        ui.upload(on_upload=handle_upload, label="CSV oder ZIP Datei auswählen", auto_upload=True).props("accept=.csv,.zip text/csv application/zip").classes("w-full mt-4")
        with ui.row().classes("gap-3 mt-5"):
            ui.button("Schliessen", icon="close", on_click=dialog.close).classes("bp-secondary-btn")
    dialog.open()


@dataclass
class ImportResult:
    accounts_created: int = 0
    accounts_updated: int = 0
    categories_created: int = 0
    categories_updated: int = 0
    budgets_created: int = 0
    budgets_updated: int = 0
    transactions_created: int = 0
    transactions_updated: int = 0
    skipped: int = 0
    errors: list[str] = field(default_factory=list)

    def merge(self, other: "ImportResult") -> None:
        self.accounts_created += other.accounts_created
        self.accounts_updated += other.accounts_updated
        self.categories_created += other.categories_created
        self.categories_updated += other.categories_updated
        self.budgets_created += other.budgets_created
        self.budgets_updated += other.budgets_updated
        self.transactions_created += other.transactions_created
        self.transactions_updated += other.transactions_updated
        self.skipped += other.skipped
        self.errors.extend(other.errors)


async def import_uploaded_data(file, controller: FinanceController | None) -> ImportResult:
    if controller is None:
        raise ValueError("Import ist aktuell nicht verfügbar.")
    content = await _read_upload_bytes(file)
    filename = str(getattr(file, "filename", "") or "").lower()
    result = ImportResult()
    if filename.endswith(".zip") or content.startswith(b"PK"):
        with zipfile.ZipFile(BytesIO(content)) as archive:
            csv_names = [name for name in archive.namelist() if name.lower().endswith(".csv") and not name.endswith("/")]
            for name in _ordered_import_filenames(csv_names):
                text = archive.read(name).decode("utf-8-sig")
                result.merge(import_csv_text(text, controller, source_name=name))
        return result
    result.merge(import_csv_text(content.decode("utf-8-sig"), controller, source_name=filename or "CSV-Datei"))
    return result


async def _read_upload_bytes(file) -> bytes:
    if hasattr(file, "read"):
        data = await file.read()
        if isinstance(data, str):
            return data.encode("utf-8")
        return data
    if hasattr(file, "text"):
        return (await file.text("utf-8-sig")).encode("utf-8-sig")
    raise ValueError("Die Datei konnte nicht gelesen werden.")


def _ordered_import_filenames(names: list[str]) -> list[str]:
    priority = {"account": 0, "konto": 0, "konten": 0, "categor": 1, "kategorie": 1, "budget": 2, "transaction": 3, "transaktion": 3}

    def sort_key(name: str) -> tuple[int, str]:
        lowered = name.lower()
        for marker, index in priority.items():
            if marker in lowered:
                return index, lowered
        return 9, lowered

    return sorted(names, key=sort_key)


def import_csv_text(text: str, controller: FinanceController, source_name: str = "CSV-Datei") -> ImportResult:
    sample = text[:1024]
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=";,")
    except csv.Error:
        dialect = csv.excel
        dialect.delimiter = ";"
    reader = csv.DictReader(StringIO(text), dialect=dialect)
    if not reader.fieldnames:
        raise ValueError(f"{source_name}: Die CSV-Datei enthält keine Kopfzeile.")
    rows = list(reader)
    area = _detect_import_area(reader.fieldnames)
    if area == "accounts":
        return import_accounts_rows(rows, controller, source_name)
    if area == "categories":
        return import_categories_rows(rows, controller, source_name)
    if area == "budgets":
        return import_budgets_rows(rows, controller, source_name)
    if area == "transactions":
        return import_transactions_rows(rows, controller, source_name)
    raise ValueError(f"{source_name}: Die Spalten konnten keinem Importbereich zugeordnet werden.")


def _detect_import_area(fieldnames: list[str]) -> str:
    headers = {_normalize_header(fieldname) for fieldname in fieldnames}
    if {"kontoname", "kontotyp"}.issubset(headers) or {"konto", "kontotyp"}.issubset(headers):
        return "accounts"
    if "kategoriename" in headers or ("kategorie" in headers and "typ" in headers and "datum" not in headers):
        return "categories"
    if {"monat", "jahr", "kategorie"}.issubset(headers) and ("limitchf" in headers or "limit" in headers or "budget" in headers):
        return "budgets"
    if {"datum", "typ", "kategorie", "konto"}.issubset(headers):
        return "transactions"
    return "unknown"


def import_accounts_rows(rows: list[dict[str, object]], controller: FinanceController, source_name: str = "Konten") -> ImportResult:
    result = ImportResult()
    user_id = controller.default_user().id
    accounts_by_name = {_normalize_key(account.name): account for account in controller.list_accounts()}
    for line_number, row in enumerate(rows, start=2):
        normalized = _normalize_row(row)
        try:
            name = _required_text(normalized, ["kontoname", "konto", "name"], "Kontoname")
            account_type = _text_value(normalized, ["kontotyp", "typ"], "Bankkonto") or "Bankkonto"
            starting_balance = _parse_import_amount(_text_value(normalized, ["startsaldochf", "startsaldo", "saldo", "betragchf"], "0"))
            existing = accounts_by_name.get(_normalize_key(name))
            if existing is None:
                created = controller.account_service.create_account(name, account_type, starting_balance, user_id)
                accounts_by_name[_normalize_key(created.name)] = created
                result.accounts_created += 1
            else:
                if existing.account_type != account_type or round(existing.starting_balance_chf, 2) != round(starting_balance, 2):
                    updated = controller.account_service.update_account(existing.id, name, account_type, starting_balance)
                    accounts_by_name[_normalize_key(updated.name)] = updated
                    result.accounts_updated += 1
        except Exception as error:
            _record_import_error(result, source_name, line_number, error)
    return result


def import_categories_rows(rows: list[dict[str, object]], controller: FinanceController, source_name: str = "Kategorien") -> ImportResult:
    result = ImportResult()
    user_id = controller.default_user().id
    categories_by_name = {_normalize_key(category.name): category for category in controller.list_categories()}
    for line_number, row in enumerate(rows, start=2):
        normalized = _normalize_row(row)
        try:
            name = _required_text(normalized, ["kategoriename", "kategorie", "name"], "Kategoriename")
            category_type = _parse_type(_required_text(normalized, ["typ", "kategorietyp"], "Typ"))
            existing = categories_by_name.get(_normalize_key(name))
            if existing is None:
                created = controller.category_service.create_category(name, category_type, user_id)
                categories_by_name[_normalize_key(created.name)] = created
                result.categories_created += 1
            else:
                if existing.category_type != category_type:
                    updated = controller.category_service.update_category(existing.id, name, category_type)
                    categories_by_name[_normalize_key(updated.name)] = updated
                    result.categories_updated += 1
        except Exception as error:
            _record_import_error(result, source_name, line_number, error)
    return result


def import_budgets_rows(rows: list[dict[str, object]], controller: FinanceController, source_name: str = "Budgets") -> ImportResult:
    result = ImportResult()
    user_id = controller.default_user().id
    categories_by_name = {_normalize_key(category.name): category for category in controller.list_categories()}
    for line_number, row in enumerate(rows, start=2):
        normalized = _normalize_row(row)
        try:
            month = _parse_int_value(_required_text(normalized, ["monat", "month"], "Monat"), "Monat")
            year = _parse_int_value(_required_text(normalized, ["jahr", "year"], "Jahr"), "Jahr")
            category_name = _required_text(normalized, ["kategorie", "kategoriename"], "Kategorie")
            limit = _parse_import_amount(_required_text(normalized, ["limitchf", "limit", "budget", "betragchf"], "Limit CHF"))
            category = categories_by_name.get(_normalize_key(category_name))
            if category is None:
                raise ValueError(f"Kategorie '{category_name}' existiert nicht.")
            existing = controller.budget_service.budget_dao.get_by_category_month(user_id, category.id, year, month)
            if existing is None:
                controller.budget_service.create_budget(month=month, year=year, limit_chf=limit, user_id=user_id, category_id=category.id)
                result.budgets_created += 1
            else:
                if round(existing.limit_chf, 2) != round(limit, 2):
                    controller.budget_service.update_budget(existing.id, month=month, year=year, limit_chf=limit, category_id=category.id)
                    result.budgets_updated += 1
        except Exception as error:
            _record_import_error(result, source_name, line_number, error)
    return result


def import_transactions_rows(rows: list[dict[str, object]], controller: FinanceController, source_name: str = "Transaktionen") -> ImportResult:
    result = ImportResult()
    accounts_by_name = {_normalize_key(account.name): account for account in controller.list_accounts()}
    categories_by_name = {_normalize_key(category.name): category for category in controller.list_categories()}
    existing_transactions = {
        _transaction_natural_key(transaction): transaction
        for transaction in controller.list_recent_transactions(limit=10000)
    }
    for line_number, row in enumerate(rows, start=2):
        normalized = _normalize_row(row)
        try:
            transaction_date = _parse_import_date(_required_text(normalized, ["datum", "date"], "Datum"))
            raw_type = _text_value(normalized, ["typ", "type"], "")
            amount = _parse_import_amount(_required_text(normalized, ["betragchf", "betrag", "amount"], "Betrag CHF"))
            transaction_type = _parse_type(raw_type, amount)
            category_name = _required_text(normalized, ["kategorie", "kategoriename"], "Kategorie")
            account_name = _required_text(normalized, ["konto", "kontoname"], "Konto")
            description = _text_value(normalized, ["beschreibung", "description"], "")
            account = accounts_by_name.get(_normalize_key(account_name))
            if account is None:
                raise ValueError(f"Konto '{account_name}' existiert nicht.")
            category = categories_by_name.get(_normalize_key(category_name))
            if category is None:
                raise ValueError(f"Kategorie '{category_name}' existiert nicht.")
            if category.category_type != transaction_type:
                raise ValueError(f"Kategorie '{category_name}' passt nicht zum Typ '{transaction_type}'.")
            normalized_amount = abs(amount)
            key = (transaction_date, description.strip().lower(), account.id, category.id, transaction_type)
            existing = existing_transactions.get(key)
            if existing is None:
                created = controller.create_transaction(
                    amount_chf=normalized_amount,
                    transaction_type=transaction_type,
                    transaction_date=transaction_date,
                    description=description,
                    account_id=account.id,
                    category_id=category.id,
                )
                existing_transactions[_transaction_natural_key(created)] = created
                result.transactions_created += 1
            else:
                if round(existing.amount_chf, 2) != round(normalized_amount, 2):
                    updated = controller.update_transaction(
                        transaction_id=existing.id,
                        amount_chf=normalized_amount,
                        transaction_type=transaction_type,
                        transaction_date=transaction_date,
                        description=description,
                        account_id=account.id,
                        category_id=category.id,
                    )
                    existing_transactions[_transaction_natural_key(updated)] = updated
                    result.transactions_updated += 1
                else:
                    result.skipped += 1
        except Exception as error:
            _record_import_error(result, source_name, line_number, error)
    return result


async def _import_transactions_csv(file, controller: FinanceController | None) -> tuple[int, int]:
    result = await import_uploaded_data(file, controller)
    return result.transactions_created + result.transactions_updated, result.skipped + len(result.errors)


def _show_import_result(result: ImportResult) -> None:
    summary_parts = []
    if result.accounts_created or result.accounts_updated:
        summary_parts.append(f"{result.accounts_created} Konten importiert, {result.accounts_updated} aktualisiert")
    if result.categories_created or result.categories_updated:
        summary_parts.append(f"{result.categories_created} Kategorien importiert, {result.categories_updated} aktualisiert")
    if result.budgets_created or result.budgets_updated:
        summary_parts.append(f"{result.budgets_created} Budgets importiert, {result.budgets_updated} aktualisiert")
    if result.transactions_created or result.transactions_updated:
        summary_parts.append(f"{result.transactions_created} Transaktionen importiert, {result.transactions_updated} aktualisiert")
    if result.skipped:
        summary_parts.append(f"{result.skipped} unverändert übersprungen")
    if not summary_parts:
        summary_parts.append("Keine neuen oder geänderten Datensätze importiert")
    if result.errors:
        preview = "; ".join(result.errors[:3])
        more = f" (+{len(result.errors) - 3} weitere)" if len(result.errors) > 3 else ""
        ui.notify(f"{' | '.join(summary_parts)} | {len(result.errors)} Zeile(n) fehlerhaft: {preview}{more}", type="warning", multi_line=True)
        return
    ui.notify(" | ".join(summary_parts), type="positive", multi_line=True)


def _record_import_error(result: ImportResult, source_name: str, line_number: int, error: Exception) -> None:
    result.errors.append(f"{source_name} Zeile {line_number}: {error}")


def _normalize_header(value: object) -> str:
    return (
        str(value or "")
        .strip()
        .casefold()
        .replace(" ", "")
        .replace("_", "")
        .replace("-", "")
        .replace("(", "")
        .replace(")", "")
    )


def _normalize_key(value: object) -> str:
    return str(value or "").strip().casefold()


def _normalize_row(row: dict[str, object]) -> dict[str, object]:
    return {_normalize_header(key): value for key, value in row.items()}


def _text_value(row: dict[str, object], keys: list[str], default: str = "") -> str:
    for key in keys:
        normalized_key = _normalize_header(key)
        if normalized_key in row and row[normalized_key] is not None:
            return str(row[normalized_key]).strip()
    return default


def _required_text(row: dict[str, object], keys: list[str], label: str) -> str:
    value = _text_value(row, keys)
    if not value:
        raise ValueError(f"{label} fehlt.")
    return value


def _parse_type(value: object, amount: float | None = None) -> str:
    text = str(value or "").strip().casefold()
    if text in {"income", "einnahme", "einnahmen"}:
        return "income"
    if text in {"expense", "ausgabe", "ausgaben"}:
        return "expense"
    if amount is not None:
        return "expense" if amount < 0 else "income"
    raise ValueError(f"Typ '{value}' ist ungültig.")


def _parse_int_value(value: object, label: str) -> int:
    try:
        return int(str(value).strip())
    except ValueError as error:
        raise ValueError(f"{label} ist ungültig.") from error


def _transaction_natural_key(transaction) -> tuple[date, str, int, int, str]:
    return (
        transaction.transaction_date,
        transaction.description.strip().lower(),
        transaction.account_id,
        transaction.category_id,
        transaction.transaction_type,
    )


def _parse_import_date(value: object) -> date:
    text = str(value or "").strip()
    if not text:
        raise ValueError("Datum fehlt.")
    if "." in text:
        day, month, year = [int(part) for part in text.split(".")]
        return date(year, month, day)
    return date.fromisoformat(text)


def _parse_import_amount(value: object) -> float:
    text = str(value or "").strip().replace("CHF", "").replace("chf", "").replace("’", "").replace("'", "").replace(" ", "").replace(",", ".")
    if not text:
        raise ValueError("Betrag fehlt.")
    return float(text)


def _export_month_options(controller: FinanceController | None, default_year: int, default_month: int) -> dict[str, str]:
    options = {f"{default_year}-{default_month:02d}": month_name(default_year, default_month)}
    if controller is not None:
        for transaction in controller.list_recent_transactions():
            key = transaction.transaction_date.strftime("%Y-%m")
            options[key] = month_name(transaction.transaction_date.year, transaction.transaction_date.month)
    return dict(sorted(options.items(), reverse=True))


def _selected_export_areas(
    *,
    overview: bool,
    accounts: bool,
    categories: bool,
    budgets: bool,
    transactions: bool,
    all_selected: bool,
) -> list[str]:
    if all_selected:
        return ["overview", "accounts", "categories", "budgets", "transactions"]
    selected = []
    if overview:
        selected.append("overview")
    if accounts:
        selected.append("accounts")
    if categories:
        selected.append("categories")
    if budgets:
        selected.append("budgets")
    if transactions:
        selected.append("transactions")
    return selected


def export_selected_data(controller: FinanceController, areas: list[str], export_format: str, year: int, month: int) -> None:
    if export_format == "csv":
        csv_files = {}
        if "overview" in areas:
            csv_files["uebersicht_export.csv"] = export_overview_csv(controller, year, month)
        if "accounts" in areas:
            csv_files["konten_export.csv"] = export_accounts_csv(controller)
        if "categories" in areas:
            csv_files["kategorien_export.csv"] = export_categories_csv(controller)
        if "budgets" in areas:
            csv_files["budgets_export.csv"] = export_budgets_csv(controller, year, month)
        if "transactions" in areas:
            csv_files["transaktionen_export.csv"] = export_transactions_csv(controller, year, month)
        if len(csv_files) == 1:
            filename, content = next(iter(csv_files.items()))
            ui.download(content, filename=filename, media_type="text/csv")
        else:
            ui.download(create_export_zip(csv_files), filename=f"budgetplanner_export_{year}_{month:02d}.zip", media_type="application/zip")
        ui.notify("Export erstellt.", type="positive")
        return
    if export_format == "pdf":
        ui.download(
            export_selected_data_pdf(controller, areas, year, month),
            filename=f"budgetplanner_export_{year}_{month:02d}.pdf",
            media_type="application/pdf",
        )
        ui.notify("PDF-Bericht erstellt.", type="positive")
        return
    ui.notify("Bitte wähle ein Exportformat aus.", type="warning")


def _csv_download_bytes(rows: Iterable[Iterable[object]]) -> bytes:
    output = StringIO()
    writer = csv.writer(output, delimiter=";")
    for row in rows:
        writer.writerow(row)
    return output.getvalue().encode("utf-8-sig")


def export_overview_csv(controller: FinanceController, year: int, month: int) -> bytes:
    data = controller.dashboard_data(year=year, month=month)
    rows = [["Bereich", "Wert", "Betrag CHF"]]
    rows.append(["Monat", month_name(year, month), ""])
    rows.append(["Einnahmen", "", f"{data.overview.total_income_chf:.2f}"])
    rows.append(["Ausgaben", "", f"{data.overview.total_expenses_chf:.2f}"])
    rows.append(["Saldo", "", f"{data.overview.balance_chf:.2f}"])
    for status in data.budget_statuses:
        rows.append([f"Budget {status.budget.category.name}", "Limit", f"{status.budget.limit_chf:.2f}"])
        rows.append([f"Budget {status.budget.category.name}", "Verbraucht", f"{status.spent_chf:.2f}"])
        rows.append([f"Budget {status.budget.category.name}", "Rest", f"{status.remaining_chf:.2f}"])
    return _csv_download_bytes(rows)


def export_accounts_csv(controller: FinanceController) -> bytes:
    rows = [["Kontoname", "Kontotyp", "Startsaldo CHF"]]
    for account in controller.list_accounts():
        rows.append([account.name, account.account_type, f"{account.starting_balance_chf:.2f}"])
    return _csv_download_bytes(rows)


def export_categories_csv(controller: FinanceController) -> bytes:
    rows = [["Kategoriename", "Typ"]]
    for category in controller.list_categories():
        rows.append([category.name, "Einnahme" if category.category_type == "income" else "Ausgabe"])
    return _csv_download_bytes(rows)


def export_budgets_csv(controller: FinanceController, year: int, month: int) -> bytes:
    rows = [["Monat", "Jahr", "Kategorie", "Limit CHF"]]
    for budget in controller.list_budgets(year=year, month=month):
        rows.append([budget.month, budget.year, budget.category.name, f"{budget.limit_chf:.2f}"])
    return _csv_download_bytes(rows)


def export_transactions_csv(controller: FinanceController, year: int, month: int) -> bytes:
    user = controller.default_user()
    transactions = controller.transaction_service.list_for_month(year=year, month=month, user_id=user.id)
    rows = [["Datum", "Typ", "Kategorie", "Konto", "Beschreibung", "Betrag CHF"]]
    for transaction in transactions:
        signed_amount = transaction.amount_chf if transaction.transaction_type == "income" else -transaction.amount_chf
        rows.append(
            [
                transaction.transaction_date.isoformat(),
                "Einnahme" if transaction.transaction_type == "income" else "Ausgabe",
                transaction.category.name,
                transaction.account.name,
                transaction.description,
                f"{signed_amount:.2f}",
            ]
        )
    return _csv_download_bytes(rows)


def create_export_zip(csv_files: dict[str, bytes]) -> bytes:
    archive = BytesIO()
    with zipfile.ZipFile(archive, mode="w", compression=zipfile.ZIP_DEFLATED) as zip_file:
        for filename, content in csv_files.items():
            zip_file.writestr(filename, content)
    return archive.getvalue()


def export_selected_data_pdf(controller: FinanceController, areas: list[str], year: int, month: int) -> bytes:
    return export_budgetplanner_pdf(controller, areas, year, month)


def _build_overview_pdf_page(controller: FinanceController, year: int, month: int) -> bytes:
    data = controller.dashboard_data(year=year, month=month)
    category_totals: dict[str, float] = defaultdict(float)
    for transaction in data.transactions:
        if transaction.transaction_type == "expense":
            category_totals[transaction.category.name] += transaction.amount_chf

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

    average_cumulative, current_cumulative = _expense_progress_pdf_series(controller, year, month)
    commands = [
        _pdf_rect(0, 0, 842, 595, "#f8fafc"),
        _pdf_text(34, 558, f"Übersicht - {month_name(year, month)}", 19, True, "#111827"),
        _pdf_text(34, 538, "Alle wichtigen Budget-Grafiken kompakt auf einer Seite.", 10, False, "#64748b"),
    ]

    _draw_category_pdf_chart(commands, 34, 318, 252, 205, category_totals)
    _draw_monthly_pdf_chart(commands, 304, 318, 504, 205, monthly_comparison)
    _draw_progress_pdf_chart(commands, 34, 50, 774, 238, average_cumulative, current_cumulative)
    return "\n".join(commands).encode("latin-1", "replace")


def _expense_progress_pdf_series(controller: FinanceController, year: int, month: int) -> tuple[list[float], list[float | None]]:
    comparison_months = []
    cursor_year, cursor_month = year, month
    for _ in range(3):
        cursor_year, cursor_month = previous_month(cursor_year, cursor_month)
        comparison_months.append((cursor_year, cursor_month))
    comparison_months.reverse()

    day_count = monthrange(year, month)[1]
    days = list(range(1, day_count + 1))
    previous_cumulative: list[list[float]] = []
    for comparison_year, comparison_month in comparison_months:
        month_data = controller.dashboard_data(year=comparison_year, month=comparison_month)
        transactions_by_day: dict[int, float] = defaultdict(float)
        for transaction in month_data.transactions:
            if transaction.transaction_type == "expense":
                transactions_by_day[transaction.transaction_date.day] += transaction.amount_chf
        comparison_day_count = monthrange(comparison_year, comparison_month)[1]
        running_total = 0.0
        cumulative = []
        for day in days:
            if day <= comparison_day_count:
                running_total += transactions_by_day.get(day, 0.0)
            cumulative.append(round(running_total, 2))
        previous_cumulative.append(cumulative)

    average_cumulative = [
        round(sum(month_values[day_index] for month_values in previous_cumulative) / len(previous_cumulative), 2)
        for day_index in range(day_count)
    ]

    current_data = controller.dashboard_data(year=year, month=month)
    current_by_day: dict[int, float] = defaultdict(float)
    max_actual_day = 0
    for transaction in current_data.transactions:
        if transaction.transaction_type == "expense":
            current_by_day[transaction.transaction_date.day] += transaction.amount_chf
            max_actual_day = max(max_actual_day, transaction.transaction_date.day)

    current_cumulative: list[float | None] = []
    running_total = 0.0
    for day in days:
        if max_actual_day and day <= max_actual_day:
            running_total += current_by_day.get(day, 0.0)
            current_cumulative.append(round(running_total, 2))
        else:
            current_cumulative.append(None)
    return average_cumulative, current_cumulative


def _draw_category_pdf_chart(commands: list[str], x: float, y: float, width: float, height: float, category_totals: dict[str, float]) -> None:
    commands.extend(_pdf_panel(x, y, width, height, "Ausgaben nach Kategorie"))
    if not category_totals:
        commands.append(_pdf_text(x + 18, y + height / 2, "Keine Ausgaben vorhanden.", 11, False, "#64748b"))
        return

    chart_items = sorted(category_totals.items(), key=lambda item: item[1], reverse=True)[:6]
    max_value = max(value for _, value in chart_items) or 1
    colors = ["#b6dc29", "#555b7d", "#fb923c", "#0ea5e9", "#facc15", "#f06292"]
    bar_x = x + 94
    bar_max_width = width - 132
    start_y = y + height - 62
    for index, (name, value) in enumerate(chart_items):
        row_y = start_y - index * 23
        bar_width = max(4, bar_max_width * value / max_value)
        commands.append(_pdf_text(x + 16, row_y + 2, _short_pdf_label(name, 13), 9, False, "#475569"))
        commands.append(_pdf_rect(bar_x, row_y, bar_width, 11, colors[index % len(colors)]))
        commands.append(_pdf_text(bar_x + bar_max_width + 8, row_y + 1, _money_pdf(value), 8, False, "#64748b"))


def _draw_monthly_pdf_chart(commands: list[str], x: float, y: float, width: float, height: float, monthly_comparison: list[dict[str, float | str]]) -> None:
    commands.extend(_pdf_panel(x, y, width, height, "Einnahmen vs. Ausgaben"))
    if not monthly_comparison:
        commands.append(_pdf_text(x + 18, y + height / 2, "Keine Monatsdaten vorhanden.", 11, False, "#64748b"))
        return

    chart_x = x + 50
    chart_y = y + 42
    chart_width = width - 72
    chart_height = height - 84
    max_value = max(max(float(item["income"]), float(item["expenses"])) for item in monthly_comparison) or 1
    _draw_pdf_grid(commands, chart_x, chart_y, chart_width, chart_height, max_value)
    group_width = chart_width / len(monthly_comparison)
    bar_width = min(18, group_width * 0.24)
    for index, item in enumerate(monthly_comparison):
        base_x = chart_x + index * group_width + group_width / 2
        income_height = chart_height * float(item["income"]) / max_value
        expense_height = chart_height * float(item["expenses"]) / max_value
        commands.append(_pdf_rect(base_x - bar_width - 2, chart_y, bar_width, income_height, "#16a34a"))
        commands.append(_pdf_rect(base_x + 2, chart_y, bar_width, expense_height, "#dc2626"))
        commands.append(_pdf_text(base_x - 14, chart_y - 18, str(item["month"]), 8, False, "#64748b"))
    _draw_pdf_legend(commands, x + width - 180, y + height - 28, [("Einnahmen", "#16a34a"), ("Ausgaben", "#dc2626")])


def _draw_progress_pdf_chart(
    commands: list[str],
    x: float,
    y: float,
    width: float,
    height: float,
    average_cumulative: list[float],
    current_cumulative: list[float | None],
) -> None:
    commands.extend(_pdf_panel(x, y, width, height, "Ausgabenverlauf"))
    chart_x = x + 56
    chart_y = y + 48
    chart_width = width - 88
    chart_height = height - 96
    all_values = average_cumulative + [value for value in current_cumulative if value is not None]
    max_value = max(all_values) if all_values else 1
    _draw_pdf_grid(commands, chart_x, chart_y, chart_width, chart_height, max_value)

    average_points = _line_points(average_cumulative, chart_x, chart_y, chart_width, chart_height, max_value)
    current_points = _line_points(current_cumulative, chart_x, chart_y, chart_width, chart_height, max_value)
    commands.append(_pdf_polyline(average_points, "#6b7280", 3.2))
    commands.append(_pdf_polyline(current_points, "#0284c7", 2.8))
    for point in current_points[:: max(1, len(current_points) // 12)]:
        commands.append(_pdf_circle(point[0], point[1], 2.8, "#ffffff", "#0284c7"))

    day_count = len(average_cumulative)
    for day in [1, 6, 11, 16, 21, 26, day_count]:
        if day <= day_count:
            tick_x = chart_x + (day - 1) / max(day_count - 1, 1) * chart_width
            commands.append(_pdf_text(tick_x - 4, chart_y - 19, str(day), 8, False, "#64748b"))
    commands.append(_pdf_text(chart_x + chart_width / 2 - 34, y + 18, "Tag im Monat", 9, True, "#64748b"))
    commands.append(_pdf_text(x + 18, chart_y + chart_height / 2, "Ausgabe (CHF)", 9, True, "#64748b"))
    _draw_pdf_legend(commands, x + 18, y + height - 30, [("Durchschnitt letzte 3 Monate", "#6b7280"), ("Aktuelle Ausgaben", "#0284c7")])


def _append_pdf_section(lines: list[tuple[str, int, bool]], title: str, rows: list[list[object]]) -> None:
    lines.append((title, 14, True))
    if len(rows) == 1:
        lines.append(("Keine Daten vorhanden.", 10, False))
        lines.append(("", 10, False))
        return
    for index, row in enumerate(rows):
        lines.append((" | ".join(str(value) for value in row), 10, index == 0))
    lines.append(("", 10, False))


def _pdf_panel(x: float, y: float, width: float, height: float, title: str) -> list[str]:
    return [
        _pdf_rect(x, y, width, height, "#ffffff"),
        _pdf_stroke_rect(x, y, width, height, "#dbeafe", 1),
        _pdf_text(x + 14, y + height - 24, title, 12, True, "#111827"),
    ]


def _draw_pdf_grid(commands: list[str], x: float, y: float, width: float, height: float, max_value: float) -> None:
    commands.append(_pdf_line([(x, y), (x + width, y)], "#94a3b8", 0.7))
    for index in range(1, 5):
        grid_y = y + height * index / 4
        value = max_value * index / 4
        commands.append(_pdf_line([(x, grid_y), (x + width, grid_y)], "#e2e8f0", 0.45))
        commands.append(_pdf_text(x - 42, grid_y - 3, _compact_number_pdf(value), 7, False, "#64748b"))


def _draw_pdf_legend(commands: list[str], x: float, y: float, items: list[tuple[str, str]]) -> None:
    cursor_x = x
    for label, color in items:
        commands.append(_pdf_rect(cursor_x, y - 3, 10, 7, color))
        commands.append(_pdf_text(cursor_x + 14, y - 3, label, 8, False, "#475569"))
        cursor_x += 112


def _line_points(values: list[float | None], x: float, y: float, width: float, height: float, max_value: float) -> list[tuple[float, float]]:
    if not values:
        return []
    points = []
    divisor = max(len(values) - 1, 1)
    for index, value in enumerate(values):
        if value is None:
            continue
        points.append((x + index / divisor * width, y + float(value) / max_value * height))
    return points


def _short_pdf_label(value: str, max_length: int) -> str:
    return value if len(value) <= max_length else f"{value[: max_length - 1]}."


def _money_pdf(value: float) -> str:
    return f"CHF {value:,.0f}".replace(",", "'")


def _compact_number_pdf(value: float) -> str:
    return f"{value:,.0f}".replace(",", "'")


def _hex_to_pdf_rgb(color: str) -> tuple[float, float, float]:
    value = color.lstrip("#")
    return int(value[0:2], 16) / 255, int(value[2:4], 16) / 255, int(value[4:6], 16) / 255


def _pdf_rect(x: float, y: float, width: float, height: float, color: str) -> str:
    r, g, b = _hex_to_pdf_rgb(color)
    return f"{r:.3f} {g:.3f} {b:.3f} rg {x:.1f} {y:.1f} {width:.1f} {height:.1f} re f"


def _pdf_stroke_rect(x: float, y: float, width: float, height: float, color: str, line_width: float) -> str:
    r, g, b = _hex_to_pdf_rgb(color)
    return f"{r:.3f} {g:.3f} {b:.3f} RG {line_width:.1f} w {x:.1f} {y:.1f} {width:.1f} {height:.1f} re S"


def _pdf_line(points: list[tuple[float, float]], color: str, line_width: float) -> str:
    if len(points) < 2:
        return ""
    r, g, b = _hex_to_pdf_rgb(color)
    first_x, first_y = points[0]
    segments = [f"{first_x:.1f} {first_y:.1f} m"]
    segments.extend(f"{point_x:.1f} {point_y:.1f} l" for point_x, point_y in points[1:])
    return f"{r:.3f} {g:.3f} {b:.3f} RG {line_width:.1f} w {' '.join(segments)} S"


def _pdf_polyline(points: list[tuple[float, float]], color: str, line_width: float) -> str:
    return _pdf_line(points, color, line_width)


def _pdf_circle(x: float, y: float, radius: float, fill_color: str, stroke_color: str) -> str:
    fill_r, fill_g, fill_b = _hex_to_pdf_rgb(fill_color)
    stroke_r, stroke_g, stroke_b = _hex_to_pdf_rgb(stroke_color)
    left = x - radius
    bottom = y - radius
    size = radius * 2
    return (
        f"{fill_r:.3f} {fill_g:.3f} {fill_b:.3f} rg {stroke_r:.3f} {stroke_g:.3f} {stroke_b:.3f} RG 1 w "
        f"{left:.1f} {bottom:.1f} {size:.1f} {size:.1f} re B"
    )


def _pdf_text(x: float, y: float, text: str, font_size: int, is_bold: bool, color: str) -> str:
    font = "F2" if is_bold else "F1"
    r, g, b = _hex_to_pdf_rgb(color)
    return f"{r:.3f} {g:.3f} {b:.3f} rg BT /{font} {font_size} Tf {x:.1f} {y:.1f} Td ({_pdf_escape(text)}) Tj ET"


def _build_simple_pdf(lines: list[tuple[str, int, bool]]) -> bytes:
    return _build_pdf_pages(_build_simple_pdf_streams(lines))


def _build_simple_pdf_streams(lines: list[tuple[str, int, bool]]) -> list[bytes]:
    margin_x = 38
    y_start = 552
    y_min = 42
    streams: list[bytes] = []
    page_commands: list[str] = []
    y = y_start

    def flush_page() -> None:
        nonlocal page_commands
        if not page_commands:
            return
        streams.append("\n".join(page_commands).encode("latin-1", "replace"))
        page_commands = []

    for raw_text, font_size, is_bold in lines:
        for text in _wrap_pdf_line(str(raw_text), max_chars=132):
            line_height = max(font_size + 5, 14)
            if y - line_height < y_min:
                flush_page()
                y = y_start
            font = "F2" if is_bold else "F1"
            page_commands.append(f"BT /{font} {font_size} Tf {margin_x} {y} Td ({_pdf_escape(text)}) Tj ET")
            y -= line_height
    flush_page()
    return streams


def _build_pdf_pages(page_streams: list[bytes]) -> bytes:
    page_width = 842
    page_height = 595
    objects: list[bytes | None] = [None]
    objects.extend([b"", b"", b"<< /Type /Font /Subtype /Type1 /BaseFont /Courier >>", b"<< /Type /Font /Subtype /Type1 /BaseFont /Courier-Bold >>"])
    page_ids: list[int] = []
    if not page_streams:
        page_streams = [_pdf_text(38, 552, "Keine Exportdaten vorhanden.", 12, False, "#111827").encode("latin-1")]
    for stream in page_streams:
        objects.append(b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n" + stream + b"\nendstream")
        current_content_id = len(objects) - 1
        page = (
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {page_width} {page_height}] "
            f"/Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> /Contents {current_content_id} 0 R >>"
        ).encode("ascii")
        objects.append(page)
        page_ids.append(len(objects) - 1)
    kids = " ".join(f"{page_id} 0 R" for page_id in page_ids)
    objects[1] = b"<< /Type /Catalog /Pages 2 0 R >>"
    objects[2] = f"<< /Type /Pages /Kids [{kids}] /Count {len(page_ids)} >>".encode("ascii")
    return _serialize_pdf(objects)


def _wrap_pdf_line(text: str, max_chars: int) -> list[str]:
    if not text:
        return [""]
    parts = []
    current = ""
    for word in text.split():
        if len(current) + len(word) + 1 <= max_chars:
            current = f"{current} {word}".strip()
        else:
            parts.append(current)
            current = word
    if current:
        parts.append(current)
    return parts or [""]


def _pdf_escape(text: str) -> str:
    cleaned = text.replace("’", "'").replace("–", "-")
    cleaned = cleaned.encode("latin-1", "replace").decode("latin-1")
    return cleaned.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _serialize_pdf(objects: list[bytes | None]) -> bytes:
    pdf = BytesIO()
    pdf.write(b"%PDF-1.4\n")
    offsets = [0]
    for object_id, content in enumerate(objects[1:], start=1):
        offsets.append(pdf.tell())
        pdf.write(f"{object_id} 0 obj\n".encode("ascii"))
        pdf.write(content or b"")
        pdf.write(b"\nendobj\n")
    xref_offset = pdf.tell()
    pdf.write(f"xref\n0 {len(objects)}\n".encode("ascii"))
    pdf.write(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.write(f"{offset:010d} 00000 n \n".encode("ascii"))
    pdf.write(
        f"trailer\n<< /Size {len(objects)} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n".encode("ascii")
    )
    return pdf.getvalue()


def _download_transactions_csv(controller: FinanceController, year: int, month: int) -> None:
    csv_bytes = export_transactions_csv(controller, year, month)
    ui.download(csv_bytes, filename=f"budgetplanner_{year}_{month:02d}_transaktionen.csv", media_type="text/csv")
    ui.notify(f"CSV für {month_name(year, month)} exportiert.", type="positive")


def _print_selected_month(active_path: str, year: int, month: int) -> None:
    if active_path in {"/", "/budget"}:
        target = f"{active_path}?year={year}&month={month}"
        ui.run_javascript(
            f"""
            sessionStorage.setItem('bpPrintAfterLoad', '1');
            window.location.href = {target!r};
            """
        )
        return
    ui.run_javascript("window.print()")


def page_title(title: str, subtitle: str) -> None:
    with ui.column().classes("gap-1"):
        ui.label(title).classes("bp-title")
        ui.label(subtitle).classes("bp-muted")


def month_nav_card(path: str, year: int, month: int) -> None:
    previous_year, previous_month_value = previous_month(year, month)
    next_year, next_month_value = next_month(year, month)
    previous_target = f"{path}?year={previous_year}&month={previous_month_value}"
    next_target = f"{path}?year={next_year}&month={next_month_value}"
    with ui.card().classes("bp-card bp-month-card w-full p-5"):
        with ui.row().classes("w-full h-full items-center justify-between gap-3 no-wrap"):
            ui.button(icon="chevron_left", on_click=lambda: ui.navigate.to(previous_target)).props("flat round").classes("bp-month-arrow")
            with ui.column().classes("items-center gap-1"):
                ui.label(month_name(year, month)).classes("bp-month-value text-gray-900")
            ui.button(icon="chevron_right", on_click=lambda: ui.navigate.to(next_target)).props("flat round").classes("bp-month-arrow")


def empty_state(icon: str, title: str, description: str, cta: str | None = None, on_click: Callable[[], None] | None = None) -> None:
    with ui.element("div").classes("w-full p-10 text-center"):
        ui.icon(icon).classes("text-gray-300 text-6xl")
        ui.label(title).classes("text-lg font-semibold text-gray-800")
        ui.label(description).classes("bp-muted")
        if cta and on_click:
            ui.button(cta, on_click=on_click).classes("bp-primary-btn mt-3")

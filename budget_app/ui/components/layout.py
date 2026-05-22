"""Shared layout helpers."""

from __future__ import annotations

import csv
from io import StringIO
from collections.abc import Callable
from datetime import date

from nicegui import ui

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
                import_button = ui.button("Import", icon="upload_file", on_click=lambda: open_import_dialog(controller)).classes("bp-secondary-btn bp-header-action")
                import_button.tooltip("CSV-Import ist vorbereitet: Später kannst du hier Kontoauszüge hochladen und automatisch als Transaktionen übernehmen.")
                ui.button("Export", icon="ios_share", on_click=lambda: open_export_dialog(active_path, controller)).classes("bp-secondary-btn bp-header-action")
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
    with ui.dialog() as dialog, ui.card().classes("bp-card p-6 w-full max-w-xl"):
        ui.label("Export").classes("bp-section-title")
        ui.label("Wähle Exportart und Monat.").classes("bp-muted mb-3")
        export_type = ui.select({"pdf": "PDF Export", "csv": "CSV Export"}, label="Exportart", value="pdf").classes("w-full")
        export_month = ui.select(month_options, label="Monat", value=f"{current_year}-{current_month:02d}").classes("w-full")

        def run_export() -> None:
            selected_year, selected_month = [int(value) for value in str(export_month.value).split("-")]
            if export_type.value == "csv":
                if controller is None:
                    ui.notify("CSV-Export ist auf dieser Seite nicht verfügbar.", type="warning")
                    return
                _download_transactions_csv(controller, selected_year, selected_month)
                dialog.close()
                return
            _print_selected_month(active_path, selected_year, selected_month)
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


def open_import_dialog(controller: FinanceController | None) -> None:
    with ui.dialog() as dialog, ui.card().classes("bp-card p-6 w-full max-w-xl"):
        ui.label("CSV Import").classes("bp-section-title")
        ui.label("Importiert Transaktionen aus einer CSV-Datei im BudgetPlanner-Format.").classes("bp-muted mb-3")
        with ui.element("div").classes("bg-blue-50 border border-blue-200 rounded-lg p-4"):
            ui.label("Erwartete Spalten").classes("font-bold text-blue-900")
            ui.label("Datum; Typ; Kategorie; Konto; Beschreibung; Betrag CHF").classes("text-blue-900")
            ui.label("Tipp: Der CSV-Export dieser App kann direkt wieder importiert werden.").classes("text-blue-900")

        async def handle_upload(event) -> None:
            try:
                imported_count, skipped_count = await _import_transactions_csv(event.file, controller)
            except Exception as error:
                ui.notify(str(error), type="warning")
                return
            ui.notify(f"{imported_count} Transaktionen importiert, {skipped_count} übersprungen.", type="positive")
            dialog.close()

        ui.upload(on_upload=handle_upload, label="CSV Datei auswählen", auto_upload=True).props("accept=.csv text/csv").classes("w-full mt-4")
        with ui.row().classes("gap-3 mt-5"):
            ui.button("Schliessen", icon="close", on_click=dialog.close).classes("bp-secondary-btn")
    dialog.open()


async def _import_transactions_csv(file, controller: FinanceController | None) -> tuple[int, int]:
    text = await file.text("utf-8-sig")
    sample = text[:1024]
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=";,")
    except csv.Error:
        dialect = csv.excel
        dialect.delimiter = ";"
    reader = csv.DictReader(StringIO(text), dialect=dialect)
    if not reader.fieldnames:
        raise ValueError("Die CSV-Datei enthält keine Kopfzeile.")

    if controller is None:
        raise ValueError("Import ist aktuell nicht verfügbar.")

    accounts = {account.name.strip().lower(): account for account in controller.list_accounts()}
    categories = {category.name.strip().lower(): category for category in controller.list_categories()}
    existing = {
        (
            transaction.transaction_date,
            transaction.description.strip().lower(),
            round(transaction.amount_chf, 2),
            transaction.transaction_type,
        )
        for transaction in controller.list_recent_transactions(limit=5000)
    }

    imported_count = 0
    skipped_count = 0
    for row in reader:
        normalized = {str(key or "").strip().lower(): value for key, value in row.items()}
        try:
            transaction_date = _parse_import_date(normalized.get("datum", ""))
            raw_type = str(normalized.get("typ", "")).strip().lower()
            category_name = str(normalized.get("kategorie", "")).strip()
            account_name = str(normalized.get("konto", "")).strip()
            description = str(normalized.get("beschreibung", "")).strip()
            amount = _parse_import_amount(normalized.get("betrag chf", normalized.get("betrag", "")))
            transaction_type = "income" if raw_type in {"einnahme", "income"} or amount > 0 else "expense"
            account = accounts[account_name.lower()]
            category = categories[category_name.lower()]
            dedupe_key = (transaction_date, description.lower(), round(abs(amount), 2), transaction_type)
            if dedupe_key in existing:
                skipped_count += 1
                continue
            controller.create_transaction(
                amount_chf=abs(amount),
                transaction_type=transaction_type,
                transaction_date=transaction_date,
                description=description,
                account_id=account.id,
                category_id=category.id,
            )
            existing.add(dedupe_key)
            imported_count += 1
        except Exception:
            skipped_count += 1
            continue
    return imported_count, skipped_count


def _parse_import_date(value: object) -> date:
    text = str(value or "").strip()
    if not text:
        raise ValueError("Datum fehlt.")
    if "." in text:
        day, month, year = [int(part) for part in text.split(".")]
        return date(year, month, day)
    return date.fromisoformat(text)


def _parse_import_amount(value: object) -> float:
    text = str(value or "").strip().replace("CHF", "").replace("’", "").replace("'", "").replace(",", ".")
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


def _download_transactions_csv(controller: FinanceController, year: int, month: int) -> None:
    user = controller.default_user()
    transactions = controller.transaction_service.list_for_month(year=year, month=month, user_id=user.id)
    output = StringIO()
    writer = csv.writer(output, delimiter=";")
    writer.writerow(["Datum", "Typ", "Kategorie", "Konto", "Beschreibung", "Betrag CHF"])
    for transaction in transactions:
        signed_amount = transaction.amount_chf if transaction.transaction_type == "income" else -transaction.amount_chf
        writer.writerow(
            [
                transaction.transaction_date.isoformat(),
                "Einnahme" if transaction.transaction_type == "income" else "Ausgabe",
                transaction.category.name,
                transaction.account.name,
                transaction.description,
                f"{signed_amount:.2f}",
            ]
        )
    csv_bytes = output.getvalue().encode("utf-8-sig")
    ui.download(csv_bytes, filename=f"budgetplanner_{year}_{month:02d}_transaktionen.csv", media_type="text/csv")
    ui.notify(f"CSV für {month_name(year, month)} exportiert: {len(transactions)} Transaktionen.", type="positive")


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
                ui.label("Monat").classes("text-sm bp-muted")
                ui.label(month_name(year, month)).classes("bp-month-value text-gray-900")
            ui.button(icon="chevron_right", on_click=lambda: ui.navigate.to(next_target)).props("flat round").classes("bp-month-arrow")


def empty_state(icon: str, title: str, description: str, cta: str | None = None, on_click: Callable[[], None] | None = None) -> None:
    with ui.element("div").classes("w-full p-10 text-center"):
        ui.icon(icon).classes("text-gray-300 text-6xl")
        ui.label(title).classes("text-lg font-semibold text-gray-800")
        ui.label(description).classes("bp-muted")
        if cta and on_click:
            ui.button(cta, on_click=on_click).classes("bp-primary-btn mt-3")

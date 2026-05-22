"""Shared layout helpers."""

from __future__ import annotations

import csv
import zipfile
from io import BytesIO, StringIO
from collections.abc import Callable
from datetime import date
from typing import Iterable

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
                help_button = ui.button(icon="help_outline", on_click=open_help_dialog).props("round").classes("bp-secondary-btn bp-help-btn")
                help_button.tooltip("Hilfe und Anleitung öffnen")
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
            accounts_area = ui.checkbox("Konten")
            categories_area = ui.checkbox("Kategorien")
            budgets_area = ui.checkbox("Budgets")
            transactions_area = ui.checkbox("Transaktionen", value=True)
            all_areas = ui.checkbox("Alle")

        area_checkboxes = {
            "accounts": accounts_area,
            "categories": categories_area,
            "budgets": budgets_area,
            "transactions": transactions_area,
        }

        def select_all_areas() -> None:
            if all_areas.value:
                for checkbox in area_checkboxes.values():
                    checkbox.value = True

        def sync_all_area_state() -> None:
            all_areas.value = all(bool(checkbox.value) for checkbox in area_checkboxes.values())

        all_areas.on_value_change(select_all_areas)
        for checkbox in area_checkboxes.values():
            checkbox.on_value_change(sync_all_area_state)

        def run_export() -> None:
            if controller is None:
                ui.notify("Export ist auf dieser Seite nicht verfügbar.", type="warning")
                return
            selected_areas = _selected_export_areas(
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


def _selected_export_areas(
    *,
    accounts: bool,
    categories: bool,
    budgets: bool,
    transactions: bool,
    all_selected: bool,
) -> list[str]:
    if all_selected:
        return ["accounts", "categories", "budgets", "transactions"]
    selected = []
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
    lines: list[tuple[str, int, bool]] = [
        ("Budget Planner Exportbericht", 16, True),
        (f"Monat: {month_name(year, month)}", 11, False),
        ("", 10, False),
    ]
    if "accounts" in areas:
        account_rows = [["Kontoname", "Kontotyp", "Startsaldo CHF"]]
        account_rows.extend([[account.name, account.account_type, f"{account.starting_balance_chf:.2f}"] for account in controller.list_accounts()])
        _append_pdf_section(lines, "Konten", account_rows)
    if "categories" in areas:
        category_rows = [["Kategoriename", "Typ"]]
        category_rows.extend([[category.name, "Einnahme" if category.category_type == "income" else "Ausgabe"] for category in controller.list_categories()])
        _append_pdf_section(lines, "Kategorien", category_rows)
    if "budgets" in areas:
        budget_rows = [["Monat", "Jahr", "Kategorie", "Limit CHF"]]
        budget_rows.extend([[budget.month, budget.year, budget.category.name, f"{budget.limit_chf:.2f}"] for budget in controller.list_budgets(year=year, month=month)])
        _append_pdf_section(lines, "Budgets", budget_rows)
    if "transactions" in areas:
        user = controller.default_user()
        transactions = controller.transaction_service.list_for_month(year=year, month=month, user_id=user.id)
        transaction_rows = [["Datum", "Typ", "Kategorie", "Konto", "Beschreibung", "Betrag CHF"]]
        for transaction in transactions:
            signed_amount = transaction.amount_chf if transaction.transaction_type == "income" else -transaction.amount_chf
            transaction_rows.append(
                [
                    transaction.transaction_date.isoformat(),
                    "Einnahme" if transaction.transaction_type == "income" else "Ausgabe",
                    transaction.category.name,
                    transaction.account.name,
                    transaction.description,
                    f"{signed_amount:.2f}",
                ]
            )
        _append_pdf_section(lines, "Transaktionen", transaction_rows)
    return _build_simple_pdf(lines)


def _append_pdf_section(lines: list[tuple[str, int, bool]], title: str, rows: list[list[object]]) -> None:
    lines.append((title, 14, True))
    if len(rows) == 1:
        lines.append(("Keine Daten vorhanden.", 10, False))
        lines.append(("", 10, False))
        return
    for index, row in enumerate(rows):
        lines.append((" | ".join(str(value) for value in row), 10, index == 0))
    lines.append(("", 10, False))


def _build_simple_pdf(lines: list[tuple[str, int, bool]]) -> bytes:
    page_width = 842
    page_height = 595
    margin_x = 38
    y_start = 552
    y_min = 42
    objects: list[bytes | None] = [None]
    objects.extend([b"", b"", b"<< /Type /Font /Subtype /Type1 /BaseFont /Courier >>", b"<< /Type /Font /Subtype /Type1 /BaseFont /Courier-Bold >>"])
    page_ids: list[int] = []
    content_id = 0
    page_commands: list[str] = []
    y = y_start

    def flush_page() -> None:
        nonlocal page_commands
        if not page_commands:
            return
        stream = "\n".join(page_commands).encode("latin-1", "replace")
        objects.append(b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n" + stream + b"\nendstream")
        current_content_id = len(objects) - 1
        page = (
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {page_width} {page_height}] "
            f"/Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> /Contents {current_content_id} 0 R >>"
        ).encode("ascii")
        objects.append(page)
        page_ids.append(len(objects) - 1)
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
    if not page_ids:
        page_ids.append(5)
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

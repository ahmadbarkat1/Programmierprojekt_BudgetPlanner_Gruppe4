from io import BytesIO
from zipfile import ZipFile

from budget_app.application import BudgetPlannerApplication
from budget_app.data_access.db import Database
from budget_app.ui.components.layout import (
    _selected_export_areas,
    create_export_zip,
    export_accounts_csv,
    export_budgets_csv,
    export_categories_csv,
    export_overview_csv,
    export_selected_data_pdf,
    export_transactions_csv,
)


def test_export_csv_templates_include_headers():
    app = BudgetPlannerApplication(database=Database(database_url="sqlite:///:memory:"))
    controller = app.finance_controller

    assert export_accounts_csv(controller).decode("utf-8-sig").splitlines()[0] == "Kontoname;Kontotyp;Startsaldo CHF"
    assert export_categories_csv(controller).decode("utf-8-sig").splitlines()[0] == "Kategoriename;Typ"
    assert export_budgets_csv(controller, 2026, 5).decode("utf-8-sig").splitlines()[0] == "Monat;Jahr;Kategorie;Limit CHF"
    assert export_transactions_csv(controller, 2026, 5).decode("utf-8-sig").splitlines()[0] == "Datum;Typ;Kategorie;Konto;Beschreibung;Betrag CHF"
    assert export_overview_csv(controller, 2026, 5).decode("utf-8-sig").splitlines()[0] == "Bereich;Wert;Betrag CHF"


def test_create_export_zip_contains_selected_csv_files():
    archive = create_export_zip(
        {
            "konten_export.csv": b"Kontoname;Kontotyp;Startsaldo CHF\n",
            "kategorien_export.csv": b"Kategoriename;Typ\n",
            "budgets_export.csv": b"Monat;Jahr;Kategorie;Limit CHF\n",
        }
    )

    with ZipFile(BytesIO(archive)) as zip_file:
        assert sorted(zip_file.namelist()) == ["budgets_export.csv", "kategorien_export.csv", "konten_export.csv"]


def test_pdf_export_returns_pdf_bytes_for_all_areas():
    app = BudgetPlannerApplication(database=Database(database_url="sqlite:///:memory:"))

    pdf = export_selected_data_pdf(app.finance_controller, ["overview", "accounts", "categories", "budgets", "transactions"], 2026, 5)

    assert pdf.startswith(b"%PDF-")


def test_selected_export_areas_validates_empty_and_all_selection():
    assert _selected_export_areas(overview=False, accounts=False, categories=False, budgets=False, transactions=False, all_selected=False) == []
    assert _selected_export_areas(overview=False, accounts=False, categories=False, budgets=False, transactions=False, all_selected=True) == [
        "overview",
        "accounts",
        "categories",
        "budgets",
        "transactions",
    ]

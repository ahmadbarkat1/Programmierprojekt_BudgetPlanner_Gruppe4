from budget_app.application import BudgetPlannerApplication
from budget_app.data_access.db import Database
from budget_app.ui.components.layout import import_csv_text


def _app():
    return BudgetPlannerApplication(database=Database(database_url="sqlite:///:memory:"))


def test_import_creates_new_account_from_csv():
    app = _app()

    result = import_csv_text("Kontoname;Kontotyp;Startsaldo CHF\nJuni Konto;Bankkonto;250.00\n", app.finance_controller, "konten.csv")

    assert result.accounts_created == 1
    assert any(account.name == "Juni Konto" for account in app.finance_controller.list_accounts())


def test_import_creates_new_category_from_csv():
    app = _app()

    result = import_csv_text("Kategoriename;Typ\nJuni Kategorie;Ausgabe\n", app.finance_controller, "kategorien.csv")

    category = next(category for category in app.finance_controller.list_categories() if category.name == "Juni Kategorie")
    assert result.categories_created == 1
    assert category.category_type == "expense"


def test_import_updates_existing_june_budget():
    app = _app()
    category = app.finance_controller.create_category("Juni Budget", "expense")

    first = import_csv_text("Monat;Jahr;Kategorie;Limit CHF\n6;2026;Juni Budget;400.00\n", app.finance_controller, "budgets.csv")
    second = import_csv_text("Monat;Jahr;Kategorie;Limit CHF\n6;2026;Juni Budget;800.00\n", app.finance_controller, "budgets.csv")

    budget = next(budget for budget in app.finance_controller.list_budgets(year=2026, month=6) if budget.category_id == category.id)
    assert first.budgets_created == 1
    assert second.budgets_updated == 1
    assert budget.limit_chf == 800.0


def test_import_transactions_accepts_income_expense_and_positive_or_negative_expenses():
    app = _app()
    account = app.finance_controller.create_account("Importkonto", "Bankkonto", 0)
    income_category = app.finance_controller.create_category("Import Einkommen", "income")
    expense_category = app.finance_controller.create_category("Import Ausgabe", "expense")
    app.finance_controller.create_budget(month=6, year=2026, limit_chf=500, category_id=expense_category.id)

    result = import_csv_text(
        "\n".join(
            [
                "Datum;Typ;Kategorie;Konto;Beschreibung;Betrag CHF",
                "2026-06-01;income;Import Einkommen;Importkonto;Lohn;1000.00",
                "2026-06-02;Einnahme;Import Einkommen;Importkonto;Bonus;50.00",
                "2026-06-03;expense;Import Ausgabe;Importkonto;Essen;25.00",
                "2026-06-04;Ausgabe;Import Ausgabe;Importkonto;Miete;-300.00",
                "2026-06-05;Ausgabe;Import Ausgabe;Importkonto;Transport;30.00",
            ]
        ),
        app.finance_controller,
        "transaktionen.csv",
    )

    imported = [
        transaction
        for transaction in app.finance_controller.transaction_service.list_for_month(year=2026, month=6, user_id=app.finance_controller.default_user().id)
        if transaction.account_id == account.id
    ]
    assert result.transactions_created == 5
    assert {transaction.transaction_type for transaction in imported} == {"income", "expense"}
    assert sorted(transaction.amount_chf for transaction in imported if transaction.transaction_type == "expense") == [25.0, 30.0, 300.0]


def test_import_reports_missing_dependencies_instead_of_silent_skip():
    app = _app()

    result = import_csv_text(
        "Monat;Jahr;Kategorie;Limit CHF\n6;2026;Fehlende Kategorie;500.00\n",
        app.finance_controller,
        "budgets.csv",
    )

    assert result.budgets_created == 0
    assert len(result.errors) == 1
    assert "Fehlende Kategorie" in result.errors[0]

from datetime import date

from budget_app.application import BudgetPlannerApplication
from budget_app.data_access.dao import AccountDAO, BudgetDAO, CategoryDAO, TransactionDAO, UserDAO
from budget_app.data_access.db import Database
from budget_app.services.account_service import AccountService
from budget_app.services.budget_service import BudgetService
from budget_app.services.category_service import CategoryService
from budget_app.services.transaction_service import TransactionService


def test_create_transaction_with_sqlite_memory_database():
    database = Database(database_url="sqlite:///:memory:")
    database.init_schema_and_seed()
    engine = database.engine

    user = UserDAO(engine).get_default_user()
    account_service = AccountService(AccountDAO(engine))
    category_service = CategoryService(CategoryDAO(engine))
    transaction_service = TransactionService(
        transaction_dao=TransactionDAO(engine),
        account_dao=AccountDAO(engine),
        category_dao=CategoryDAO(engine),
    )

    account = account_service.create_account("Testkonto", "Bankkonto", 0.0, user.id)
    category = category_service.create_category("Testausgabe", "expense", user.id)
    transaction = transaction_service.create_transaction(
        amount_chf=42.5,
        transaction_type="expense",
        transaction_date=date(2026, 4, 24),
        description="Integrationstest",
        account_id=account.id,
        category_id=category.id,
    )

    assert transaction.id is not None
    assert transaction.amount_chf == 42.5


def test_budget_can_be_created_for_expense_category():
    database = Database(database_url="sqlite:///:memory:")
    database.init_schema_and_seed()
    engine = database.engine

    user = UserDAO(engine).get_default_user()
    category = CategoryService(CategoryDAO(engine)).create_category("Haushalt", "expense", user.id)
    budget = BudgetService(BudgetDAO(engine), CategoryDAO(engine)).create_budget(
        month=4,
        year=2026,
        limit_chf=300.0,
        user_id=user.id,
        category_id=category.id,
    )

    assert budget.id is not None
    assert budget.limit_chf == 300.0


def test_application_workflow_creates_budgeted_expense_and_dashboard_status():
    app = BudgetPlannerApplication(database=Database(database_url="sqlite:///:memory:"))

    account = app.finance_controller.create_account("Ferienkonto", "Bankkonto", 500.0)
    category = app.finance_controller.create_category("Reisen", "expense")
    budget = app.finance_controller.create_budget(
        month=5,
        year=2026,
        limit_chf=300.0,
        category_id=category.id,
    )
    transaction = app.finance_controller.create_transaction(
        amount_chf=180.0,
        transaction_type="expense",
        transaction_date=date(2026, 5, 18),
        description="Zugticket",
        account_id=account.id,
        category_id=category.id,
    )

    dashboard = app.finance_controller.dashboard_data(year=2026, month=5)
    travel_status = next(status for status in dashboard.budget_statuses if status.budget.id == budget.id)

    assert transaction.id is not None
    assert dashboard.overview.total_expenses_chf == 180.0
    assert travel_status.spent_chf == 180.0
    assert travel_status.remaining_chf == 120.0
    assert travel_status.is_exceeded is False


def test_application_workflow_creates_recurring_budgeted_expenses():
    app = BudgetPlannerApplication(database=Database(database_url="sqlite:///:memory:"))

    account = app.finance_controller.create_account("Haushaltskonto", "Bankkonto", 1000.0)
    category = app.finance_controller.create_category("Fitness", "expense")
    app.finance_controller.create_budget(month=5, year=2026, limit_chf=100.0, category_id=category.id)
    june_budget = app.finance_controller.create_budget(month=6, year=2026, limit_chf=100.0, category_id=category.id)

    transactions = app.finance_controller.create_recurring_transactions(
        amount_chf=45.0,
        transaction_type="expense",
        transaction_date=date(2026, 5, 18),
        description="Abo",
        account_id=account.id,
        category_id=category.id,
        frequency="monthly",
        occurrences=2,
    )

    june_dashboard = app.finance_controller.dashboard_data(year=2026, month=6)
    june_status = next(status for status in june_dashboard.budget_statuses if status.budget.id == june_budget.id)

    assert [transaction.transaction_date for transaction in transactions] == [date(2026, 5, 18), date(2026, 6, 18)]
    assert [transaction.description for transaction in transactions] == ["Abo", "Abo (2/2)"]
    assert june_dashboard.overview.total_expenses_chf == 45.0
    assert june_status.remaining_chf == 55.0

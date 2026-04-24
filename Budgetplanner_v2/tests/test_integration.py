from datetime import date

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


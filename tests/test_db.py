from datetime import date

from sqlmodel import SQLModel

from budget_app.data_access.dao import AccountDAO, CategoryDAO, TransactionDAO, UserDAO
from budget_app.data_access.db import Database
from budget_app.domain.models import Transaction


def test_seeded_database_contains_demo_accounts_and_categories():
    database = Database(database_url="sqlite:///:memory:")
    database.init_schema_and_seed()
    engine = database.engine

    user = UserDAO(engine).get_default_user()
    account_names = {account.name for account in AccountDAO(engine).list_for_user(user.id)}
    category_names = {category.name for category in CategoryDAO(engine).list_for_user(user.id)}

    assert {"Studentenkonto", "Bargeld"}.issubset(account_names)
    assert {"Nebenjob", "Nachhilfe", "Fast Food", "Ausgang", "Padel"}.issubset(category_names)


def test_saving_transaction_persists_it_for_recent_query():
    database = Database(database_url="sqlite:///:memory:")
    database.init_schema_and_seed()
    engine = database.engine

    user = UserDAO(engine).get_default_user()
    account = AccountDAO(engine).list_for_user(user.id)[0]
    income_category = CategoryDAO(engine).list_for_user(user.id, category_type="income")[0]
    transaction_dao = TransactionDAO(engine)

    saved = transaction_dao.create(
        Transaction(
            amount_chf=125.75,
            transaction_type="income",
            transaction_date=date(2026, 5, 1),
            description="Persistenztest",
            account_id=account.id,
            category_id=income_category.id,
        )
    )

    recent_transactions = transaction_dao.list_recent()

    assert saved.id is not None
    assert saved.id in [transaction.id for transaction in recent_transactions]
    assert any(transaction.description == "Persistenztest" for transaction in recent_transactions)


def test_empty_database_returns_no_recent_transactions():
    database = Database(database_url="sqlite:///:memory:")
    SQLModel.metadata.create_all(database.engine)

    assert TransactionDAO(database.engine).list_recent() == []


def test_monthly_transaction_query_returns_only_matching_month():
    database = Database(database_url="sqlite:///:memory:")
    database.init_schema_and_seed()
    engine = database.engine

    user = UserDAO(engine).get_default_user()
    account = AccountDAO(engine).list_for_user(user.id)[0]
    expense_category = CategoryDAO(engine).list_for_user(user.id, category_type="expense")[0]
    transaction_dao = TransactionDAO(engine)
    transaction_dao.create(
        Transaction(
            amount_chf=20.0,
            transaction_type="expense",
            transaction_date=date(2026, 4, 30),
            description="April",
            account_id=account.id,
            category_id=expense_category.id,
        )
    )
    may_transaction = transaction_dao.create(
        Transaction(
            amount_chf=30.0,
            transaction_type="expense",
            transaction_date=date(2026, 5, 1),
            description="Mai",
            account_id=account.id,
            category_id=expense_category.id,
        )
    )

    may_transactions = transaction_dao.list_for_month(year=2026, month=5, user_id=user.id)

    assert may_transaction.id in [transaction.id for transaction in may_transactions]
    assert all(transaction.transaction_date.month == 5 for transaction in may_transactions)
    assert all(transaction.transaction_date.year == 2026 for transaction in may_transactions)

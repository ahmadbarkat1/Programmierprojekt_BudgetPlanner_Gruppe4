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

    assert {"Bankkonto", "Bargeld"}.issubset(account_names)
    assert {"Lohn", "Lebensmittel", "Miete"}.issubset(category_names)


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
    assert [transaction.id for transaction in recent_transactions] == [saved.id]
    assert recent_transactions[0].description == "Persistenztest"


def test_empty_database_returns_no_recent_transactions():
    database = Database(database_url="sqlite:///:memory:")
    SQLModel.metadata.create_all(database.engine)

    assert TransactionDAO(database.engine).list_recent() == []

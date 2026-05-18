import pytest
from datetime import date

from budget_app.services.transaction_service import TransactionService
from budget_app.data_access.dao import AccountDAO, CategoryDAO, TransactionDAO
from budget_app.data_access.db import Database


def setup_services():
    db = Database(database_url="sqlite:///:memory:")
    db.init_schema_and_seed()
    engine = db.engine

    return TransactionService(
        transaction_dao=TransactionDAO(engine),
        account_dao=AccountDAO(engine),
        category_dao=CategoryDAO(engine),
    )


def test_transaction_invalid_amount():
    service = setup_services()

    with pytest.raises(ValueError):
        service.create_transaction(
            amount_chf=0,
            transaction_type="expense",
            transaction_date=date.today(),
            description="Test",
            account_id=1,
            category_id=1,
        )


def test_transaction_invalid_type():
    service = setup_services()

    with pytest.raises(ValueError):
        service.create_transaction(
            amount_chf=10,
            transaction_type="invalid",
            transaction_date=date.today(),
            description="Test",
            account_id=1,
            category_id=1,
        )

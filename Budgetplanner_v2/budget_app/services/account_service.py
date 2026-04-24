"""Account use cases."""

from __future__ import annotations

from typing import List

from ..data_access.dao import AccountDAO
from ..domain.models import Account


class AccountService:
    """Business operations for accounts."""

    def __init__(self, account_dao: AccountDAO) -> None:
        self.account_dao = account_dao

    def create_account(self, name: str, account_type: str, starting_balance_chf: float, user_id: int) -> Account:
        if not name.strip():
            raise ValueError("Der Kontoname darf nicht leer sein.")
        return self.account_dao.create(
            Account(
                name=name.strip(),
                account_type=account_type.strip() or "Bankkonto",
                starting_balance_chf=round(float(starting_balance_chf), 2),
                user_id=user_id,
            )
        )

    def list_accounts(self, user_id: int) -> List[Account]:
        return self.account_dao.list_for_user(user_id)


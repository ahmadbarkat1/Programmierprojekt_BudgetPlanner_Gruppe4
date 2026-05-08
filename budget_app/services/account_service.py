"""Account use cases."""

from __future__ import annotations

from typing import List

from ..data_access.dao import AccountDAO
from ..domain.models import Account


class AccountService:
    """Business operations for accounts."""

    VALID_TYPES = {"Bankkonto", "Bargeld"}

    def __init__(self, account_dao: AccountDAO) -> None:
        self.account_dao = account_dao

    def create_account(self, name: str, account_type: str, starting_balance_chf: float, user_id: int) -> Account:
        if not name.strip():
            raise ValueError("Der Kontoname darf nicht leer sein.")
        cleaned_type = account_type.strip() or "Bankkonto"
        if cleaned_type not in self.VALID_TYPES:
            raise ValueError("Kontotyp muss 'Bankkonto' oder 'Bargeld' sein.")
        return self.account_dao.create(
            Account(
                name=name.strip(),
                account_type=cleaned_type,
                starting_balance_chf=round(float(starting_balance_chf), 2),
                user_id=user_id,
            )
        )

    def list_accounts(self, user_id: int) -> List[Account]:
        return self.account_dao.list_for_user(user_id)

    def update_account(self, account_id: int, name: str, account_type: str, starting_balance_chf: float) -> Account:
        if not name.strip():
            raise ValueError("Der Kontoname darf nicht leer sein.")
        cleaned_type = account_type.strip() or "Bankkonto"
        if cleaned_type not in self.VALID_TYPES:
            raise ValueError("Kontotyp muss 'Bankkonto' oder 'Bargeld' sein.")
        return self.account_dao.update(
            account_id=account_id,
            name=name.strip(),
            account_type=cleaned_type,
            starting_balance_chf=round(float(starting_balance_chf), 2),
        )

    def delete_account(self, account_id: int) -> None:
        if self.account_dao.has_transactions(account_id):
            raise ValueError("Dieses Konto kann nicht gelöscht werden, da bereits Transaktionen damit verknüpft sind.")
        self.account_dao.delete(account_id)

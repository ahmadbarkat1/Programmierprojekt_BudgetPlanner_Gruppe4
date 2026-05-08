"""NiceGUI page registration."""

from __future__ import annotations

from ..components.theme import add_theme
from ..controllers import FinanceController
from .accounts_page import register_accounts_page
from .budget_page import register_budget_page
from .categories_page import register_categories_page
from .overview_page import register_overview_page
from .transactions_page import register_transactions_page


class Pages:
    """Registers all NiceGUI routes."""

    def __init__(self, finance_controller: FinanceController) -> None:
        self._finance_controller = finance_controller

    def register(self) -> None:
        add_theme()
        register_overview_page(self._finance_controller)
        register_budget_page(self._finance_controller)
        register_transactions_page(self._finance_controller)
        register_categories_page(self._finance_controller)
        register_accounts_page(self._finance_controller)

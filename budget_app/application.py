"""NiceGUI app wiring.

Object-oriented entrypoint: ``BudgetPlannerApplication`` wires dependencies and
runs NiceGUI. This follows the same composition-root idea as the Pizzeria
reference project.
"""

from __future__ import annotations

import socket
from typing import Optional

from nicegui import ui

from .data_access.dao import AccountDAO, BudgetDAO, CategoryDAO, TransactionDAO, UserDAO
from .data_access.db import Database
from .services.account_service import AccountService
from .services.budget_service import BudgetService
from .services.category_service import CategoryService
from .services.finance_service import FinanceService
from .services.transaction_service import TransactionService
from .ui.controllers import FinanceController
from .ui.pages import Pages


def _find_available_port(host: str, preferred_port: int, attempts: int = 50) -> int:
    """Return ``preferred_port`` or the next free port.

    NiceGUI exits with an error if the selected port is already occupied. A
    small preflight check keeps local development smooth when an old server is
    still running.
    """
    for port in range(preferred_port, preferred_port + attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind((host, port))
            except OSError:
                continue
            return port
    raise RuntimeError(f"Kein freier Port zwischen {preferred_port} und {preferred_port + attempts - 1} gefunden.")


class BudgetPlannerApplication:
    """Application composition root."""

    def __init__(self, database: Optional[Database] = None) -> None:
        self.database = database or Database()
        self.database.init_schema_and_seed()
        engine = self.database.engine

        self.user_dao = UserDAO(engine)
        self.account_dao = AccountDAO(engine)
        self.category_dao = CategoryDAO(engine)
        self.transaction_dao = TransactionDAO(engine)
        self.budget_dao = BudgetDAO(engine)

        self.account_service = AccountService(account_dao=self.account_dao)
        self.category_service = CategoryService(category_dao=self.category_dao)
        self.transaction_service = TransactionService(
            transaction_dao=self.transaction_dao,
            account_dao=self.account_dao,
            category_dao=self.category_dao,
            budget_dao=self.budget_dao,
        )
        self.budget_service = BudgetService(
            budget_dao=self.budget_dao,
            category_dao=self.category_dao,
        )
        self.finance_service = FinanceService()

        self.finance_controller = FinanceController(
            user_dao=self.user_dao,
            account_service=self.account_service,
            category_service=self.category_service,
            transaction_service=self.transaction_service,
            budget_service=self.budget_service,
            finance_service=self.finance_service,
        )
        self.pages = Pages(finance_controller=self.finance_controller)

    def run(self, host: str = "0.0.0.0", port: int = 8080, reload: bool = False) -> None:
        """Run the NiceGUI application."""
        self.pages.register()
        available_port = _find_available_port(host, port)
        if available_port != port:
            print(f"Port {port} ist bereits belegt. Starte Budget Planner stattdessen auf Port {available_port}.")
        ui.run(host=host, port=available_port, reload=reload, title="Budget Planner")

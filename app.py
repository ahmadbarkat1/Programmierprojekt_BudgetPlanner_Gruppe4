"""Compatibility entrypoint for running the app with ``python app.py``."""

from budget_app.application import BudgetPlannerApplication


if __name__ == "__main__":
    BudgetPlannerApplication().run()


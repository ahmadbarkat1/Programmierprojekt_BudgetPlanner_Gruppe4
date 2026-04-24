"""Run the Budgetplanner app with ``python -m budget_app``."""

from .application import BudgetPlannerApplication


def main() -> None:
    app = BudgetPlannerApplication()
    app.run()


if __name__ == "__main__":
    main()


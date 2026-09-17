"""Feature calculations shared by training, evaluation and prediction."""


def loan_to_income_ratio(loan_amount, annual_income):
    """Return the unrounded ratio for numbers or pandas Series.

    Callers must supply positive income. Multiply by 100 only for display.
    """
    return loan_amount / annual_income

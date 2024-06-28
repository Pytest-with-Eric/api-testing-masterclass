def calculate_interest_only_payment(
    loan_amount: float, annual_interest_rate: float
) -> float:
    """
    Calculate the monthly interest payment for an interest-only mortgage.

    :param loan_amount: The total loan amount (principal).
    :param annual_interest_rate: The annual interest rate as a percentage.
    :return: Monthly interest payment.
    """
    monthly_interest_rate = annual_interest_rate / 100 / 12
    return loan_amount * monthly_interest_rate


def calculate_repayment_mortgage_payment(
    loan_amount: float, annual_interest_rate: float, loan_term_years: int
) -> float:
    """
    Calculate the monthly payment for a repayment mortgage.

    :param loan_amount: The total loan amount (principal).
    :param annual_interest_rate: The annual interest rate as a percentage.
    :param loan_term_years: The term of the loan in years.
    :return: Monthly payment for the full term of the loan.
    """
    monthly_interest_rate = annual_interest_rate / 100 / 12
    total_payments = loan_term_years * 12
    if monthly_interest_rate == 0:  # This avoids division by zero if interest rate is 0
        return loan_amount / total_payments
    monthly_payment = (
        loan_amount
        * (monthly_interest_rate * (1 + monthly_interest_rate) ** total_payments)
        / ((1 + monthly_interest_rate) ** total_payments - 1)
    )
    return monthly_payment

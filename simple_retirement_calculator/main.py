def calculate_retirement_plan(
    current_age,
    retirement_age,
    life_expectancy,
    monthly_expenses,
    current_savings,
    investment_return,
    current_investment=0,
    monthly_saving_to_invest=0,
    inflation_rate=3
):
    """
    Calculates retirement plan details based on the provided inputs.
    This function implements the calculation logic based on financial principles.

    Args:
        current_age: Current age (years).
        retirement_age: Desired retirement age (years).
        life_expectancy: Expected life expectancy (years).
        monthly_expenses: Expected monthly expenses after retirement (Baht).
        current_savings: Current savings (Baht).
        investment_return: Expected annual investment return (percentage, e.g., 5 for 5%).
        inflation_rate: Expected annual inflation rate (percentage, e.g., 3 for 3%).
        current_investment:  Current amount invested (Baht), defaults to 0.
        monthly_saving_to_invest: Additional monthly amount to invest (Baht), defaults to 0.


    Returns:
        A dictionary containing the calculated retirement plan details,
        including:
        - total_expenses: Estimated total expenses during retirement (Baht).
        - required_savings: Estimated total savings needed at retirement (Baht).
        - additional_savings_needed:  Additional savings required, given current savings and investments (Baht).
        - monthly_savings_required: Estimated monthly savings required to reach the goal (Baht).
        - yearly_savings_required: Equivalent of monthly_savings_required expressed annually (Baht).
        - status: a string indicating if retirement is feasible ("achievable", "needs review")

        Returns None if input validation fails.

    Raises:
      None.

    """

    # --- Input Validation ---
    if not all(
        isinstance(arg, (int, float))
        for arg in [
            current_age,
            retirement_age,
            life_expectancy,
            monthly_expenses,
            current_savings,
            investment_return,
            inflation_rate,
            current_investment,
            monthly_saving_to_invest,
        ]
    ):
        print("Error: All input values must be numeric.")
        return None

    if not (
        20 <= current_age < retirement_age <= 85
        and retirement_age < life_expectancy <= 100
    ):
        print(
            "Error: Invalid age values. Please ensure 20 <= current_age < retirement_age <= 85 and retirement_age < life_expectancy <= 100"
        )
        return None

    if not (0 <= inflation_rate <= 100 and 0 <= investment_return <= 100):
        print(
            "Error: Invalid rate values. Please ensure 0 <= inflation_rate <= 100 and 0 <= investment_rate <= 100"
        )
        return None

    if not (
        current_savings >= 0
        and current_investment >= 0
        and monthly_saving_to_invest >= 0
        and monthly_expenses >= 0
    ):
        print(
            "Error: Invalid values. Please ensure current_savings >= 0 and current_investment >= 0 and monthly_saving_to_invest >=0 and monthly_expenses >=0"
        )
        return None

    # --- Calculation Logic ---
    years_to_retirement = retirement_age - current_age
    years_in_retirement = life_expectancy - retirement_age
    monthly_return = (1 + (investment_return / 100)) ** (1 / 12) - 1
    monthly_inflation = (1 + (inflation_rate / 100)) ** (1 / 12) - 1

    # 1. Calculate total expenses during retirement (taking inflation into account).
    total_expenses = 0
    for year in range(years_in_retirement):
        yearly_expenses = 0
        for month in range(12):
            yearly_expenses += monthly_expenses * (
                (1 + monthly_inflation) ** (year * 12 + month)
            )
        total_expenses += yearly_expenses

    # 2. Calculate the required savings at retirement.
    required_savings = 0
    for year in range(years_in_retirement):
        for month in range(12):
            required_savings += (
                monthly_expenses
                * ((1 + monthly_inflation) ** (year * 12 + month))
                / ((1 + monthly_return) ** (year * 12 + month))
            )

    # 3. Calculate future value of current savings and investment.
    future_value_savings = current_savings * (1 + monthly_return) ** (
        years_to_retirement * 12
    )
    future_value_investment = current_investment * (1 + monthly_return) ** (
        years_to_retirement * 12
    )

    # 4. Calculate the future value of monthly contributions
    future_value_monthly_saving = 0
    if monthly_return > 0:  # avoid division by zero
        future_value_monthly_saving = monthly_saving_to_invest * (
            ((1 + monthly_return) ** (years_to_retirement * 12) - 1) / monthly_return
        )
    else:
        future_value_monthly_saving = (
            monthly_saving_to_invest * years_to_retirement * 12
        )

    # 5. Calculate the additional savings needed.
    additional_savings_needed = required_savings - (
        future_value_savings + future_value_investment + future_value_monthly_saving
    )
    additional_savings_needed = max(
        0, additional_savings_needed
    )  # Ensure it's not negative

    # 6. Calculate the required monthly savings to reach the goal, if additional savings are needed.
    monthly_savings_required = 0

    if additional_savings_needed > 0:
        if monthly_return > 0:
            monthly_savings_required = additional_savings_needed * (
                monthly_return
                / (((1 + monthly_return) ** (years_to_retirement * 12) - 1))
            )
        else:
            monthly_savings_required = additional_savings_needed / (
                years_to_retirement * 12
            )

    yearly_savings_required = monthly_savings_required * 12
    # 7. Determine Retirement Plan Status (achievable, need_review)
    if monthly_savings_required <= monthly_saving_to_invest:
        status = "achievable"
    else:
        status = "needs review"

    return {
        "total_expenses": round(total_expenses, 2),
        "required_savings": round(required_savings, 2),
        "additional_savings_needed": round(additional_savings_needed, 2),
        "monthly_savings_required": round(monthly_savings_required, 2),
        "yearly_savings_required": round(yearly_savings_required, 2),
        "status": status,
    }

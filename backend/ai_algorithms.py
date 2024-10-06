import math

def projected_safe_contribution(income, savings, debt, savings_goal, dependents, marital_status, leeway_percentage=0):
    basic_living_expense_rate = 0.50
    min_debt_payment_rate = 0.10
    cost_per_dependent = 1000
    marital_status_expense_rate = {
        "Single": 0,
        "Married": 0.05,
        "Divorced": 0.15
    }

    savings_buffer_multiplier = 3

    basic_living_expenses = income * basic_living_expense_rate
    debt_payment = debt * min_debt_payment_rate
    dependent_expenses = dependents * cost_per_dependent
    marital_expenses = income * marital_status_expense_rate.get(marital_status, 0)

    total_essential_expenses = basic_living_expenses + debt_payment + dependent_expenses + marital_expenses

    disposable_income = income - total_essential_expenses

    savings_buffer = total_essential_expenses * savings_buffer_multiplier

    if (savings > savings_buffer):
        available_savings = savings - savings_buffer
    else:
        available_savings = 0

    contribution_factor = 0.30
    safe_contribution = max(0, disposable_income * contribution_factor)

    savings_contribution_limit = available_savings * 0.10

    total_contribution = safe_contribution + savings_contribution_limit

    leeway_contribution = total_contribution * (1 + leeway_percentage / 100)

    max_allowed_contribution = income * 0.15
    final_contribution = min(leeway_contribution, max_allowed_contribution)

    return final_contribution

def calculate_fair_score(monthly_income, monthly_debt_payments, current_savings, current_debt, savings_goal, max_dti_threshold=50, max_sir_threshold=200):
    weight_dti = 0.4
    weight_sir = 0.4
    weight_din = 0.2

    dti = (monthly_debt_payments / monthly_income) * 100

    sir = (current_savings / monthly_income) * 100 if monthly_income > 0 else 0

    din = math.log(1 + (current_debt / monthly_income)) if monthly_income > 0 else 0

    score = max(0, 100 - (dti * weight_dti) + (sir * weight_sir) - (din * weight_din))

    return score

def calculate_contribution_adjustment(user_contribution, projected_contribution):
    if user_contribution >= projected_contribution:
        contribution_ratio = user_contribution / projected_contribution
        return min(10, 5 * contribution_ratio)
    else:
        contribution_ratio = user_contribution / projected_contribution
        return max(-10, -5 * (1 - contribution_ratio))

def calculate_timeliness_adjustment(on_time_payments, total_payments):
    if total_payments == 0:
        return 0
    payment_timeliness_ratio = on_time_payments / total_payments
    return min(15, max(-15, 30 * (payment_timeliness_ratio - 0.5)))

def calculate_loan_repayment_adjustment(loan_taken, loan_repaid, loan_amount, projected_contribution):
    if loan_taken:
        loan_ratio = loan_amount / projected_contribution
        if loan_repaid:
            return min(15, 10 * loan_ratio)
        else:
            return max(-20, -15 * loan_ratio)
    return 0

def update_user_score(previous_score, user_contribution, projected_contribution, on_time_payments, total_payments, loan_taken=False, loan_repaid=False, loan_amount=0):
    contribution_adjustment = calculate_contribution_adjustment(user_contribution, projected_contribution)
    timeliness_adjustment = calculate_timeliness_adjustment(on_time_payments, total_payments)
    loan_adjustment = calculate_loan_repayment_adjustment(loan_taken, loan_repaid, loan_amount, projected_contribution)
    
    new_score = previous_score + contribution_adjustment + timeliness_adjustment + loan_adjustment
    new_score = max(0, min(new_score, 100))
    
    return new_score

def calculate_contribution_adjustment(user_contribution, projected_contribution):
    if user_contribution >= projected_contribution:
        contribution_ratio = user_contribution / projected_contribution
        return min(10, 5 * contribution_ratio)
    else:
        contribution_ratio = user_contribution / projected_contribution
        return max(-10, -5 * (1 - contribution_ratio))

def calculate_timeliness_adjustment(on_time_payments, total_payments):
    if total_payments == 0:
        return 0
    payment_timeliness_ratio = on_time_payments / total_payments
    return min(15, max(-15, 30 * (payment_timeliness_ratio - 0.5)))

def calculate_loan_repayment_adjustment(loan_taken, loan_repaid, loan_amount, projected_contribution):
    if loan_taken:
        loan_ratio = loan_amount / projected_contribution
        if loan_repaid:
            return min(15, 10 * loan_ratio)
        else:
            return max(-20, -15 * loan_ratio)
    return 0

def update_user_score(previous_score, user_contribution, projected_contribution, on_time_payments, total_payments, loan_taken=False, loan_repaid=False, loan_amount=0):
    contribution_adjustment = calculate_contribution_adjustment(user_contribution, projected_contribution)
    timeliness_adjustment = calculate_timeliness_adjustment(on_time_payments, total_payments)
    loan_adjustment = calculate_loan_repayment_adjustment(loan_taken, loan_repaid, loan_amount, projected_contribution)
    
    new_score = previous_score + contribution_adjustment + timeliness_adjustment + loan_adjustment
    new_score = max(0, min(new_score, 100))
    
    return new_score

def calculate_max_loan_amount(user_score, monthly_income):
    if user_score < 35:
        return 0
    elif user_score < 50:
        return monthly_income * 0.5
    elif user_score < 70:
        min_loan_factor = 0.5
        max_loan_factor = 1
        scaling_factor = (user_score - 50) / 20
    elif user_score < 90:
        min_loan_factor = 1
        max_loan_factor = 2
        scaling_factor = (user_score - 70) / 20
    else:
        min_loan_factor = 2
        max_loan_factor = 3
        scaling_factor = (user_score - 90) / 10

    loan_factor = min_loan_factor + scaling_factor * (max_loan_factor - min_loan_factor)
    return monthly_income * loan_factor

def check_loan_eligibility(user_score, monthly_income, desired_loan_amount):
    max_loan_amount = calculate_max_loan_amount(user_score, monthly_income)
    if desired_loan_amount <= max_loan_amount:
        return True, max_loan_amount
    else:
        return False, max_loan_amount

def calculate_final_payment_with_leeway(initial_payment, leeway_percentage=15):
    leeway_payment = initial_payment * (1 + leeway_percentage / 100)
    return leeway_payment

def calculate_months_needed(loan_amount, final_payment):
    if final_payment > 0:
        months_needed = loan_amount / final_payment
    else:
        months_needed = float('inf')
    return months_needed

def calculate_loan_repayment_no_interest(loan_amount, loan_term_years):
    num_payments = loan_term_years * 12
    return loan_amount / num_payments



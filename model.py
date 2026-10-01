from __future__ import annotations

from dataclasses import dataclass, asdict
from math import inf
from typing import Dict, Iterable


@dataclass(frozen=True)
class MarketInputs:
    market: str
    monthly_qualified_sessions: float
    checkout_conversion_pct: float
    checkout_uplift_pct: float
    payment_approval_pct: float
    approval_uplift_pp: float
    average_order_value_gbp: float
    indirect_tax_pct: float
    prices_tax_inclusive: bool
    refund_chargeback_pct: float
    gross_margin_pct: float
    payment_processing_pct: float
    service_fee_pct: float
    monthly_operating_cost_gbp: float
    setup_cost_gbp: float


def _pct(value: float) -> float:
    return value / 100.0


def calculate_market(inputs: MarketInputs) -> Dict[str, float | str]:
    """Calculate transparent market-entry economics for one scenario.

    The function deliberately does not create an opaque market score. All outputs
    are direct financial consequences of the supplied assumptions.
    """
    if inputs.monthly_qualified_sessions < 0:
        raise ValueError("monthly_qualified_sessions cannot be negative")
    if inputs.average_order_value_gbp < 0:
        raise ValueError("average_order_value_gbp cannot be negative")
    if inputs.monthly_operating_cost_gbp < 0 or inputs.setup_cost_gbp < 0:
        raise ValueError("fixed costs cannot be negative")

    bounded_pct_fields = {
        "checkout_conversion_pct": inputs.checkout_conversion_pct,
        "payment_approval_pct": inputs.payment_approval_pct,
        "indirect_tax_pct": inputs.indirect_tax_pct,
        "refund_chargeback_pct": inputs.refund_chargeback_pct,
        "gross_margin_pct": inputs.gross_margin_pct,
        "payment_processing_pct": inputs.payment_processing_pct,
        "service_fee_pct": inputs.service_fee_pct,
    }
    for name, value in bounded_pct_fields.items():
        if value < 0 or value > 100:
            raise ValueError(f"{name} must be between 0 and 100")

    base_checkout = _pct(inputs.checkout_conversion_pct)
    adjusted_checkout = base_checkout * (1 + _pct(inputs.checkout_uplift_pct))
    adjusted_checkout = max(0.0, min(1.0, adjusted_checkout))

    adjusted_approval = _pct(inputs.payment_approval_pct) + _pct(inputs.approval_uplift_pp)
    adjusted_approval = max(0.0, min(1.0, adjusted_approval))

    monthly_payment_attempts = inputs.monthly_qualified_sessions * adjusted_checkout
    monthly_orders = monthly_payment_attempts * adjusted_approval
    monthly_gmv = monthly_orders * inputs.average_order_value_gbp

    tax_rate = _pct(inputs.indirect_tax_pct)
    if inputs.prices_tax_inclusive:
        monthly_revenue_ex_tax = monthly_gmv / (1 + tax_rate)
    else:
        monthly_revenue_ex_tax = monthly_gmv

    monthly_net_revenue = monthly_revenue_ex_tax * (1 - _pct(inputs.refund_chargeback_pct))
    monthly_gross_profit = monthly_net_revenue * _pct(inputs.gross_margin_pct)

    monthly_payment_cost = monthly_gmv * _pct(inputs.payment_processing_pct)
    monthly_service_cost = monthly_gmv * _pct(inputs.service_fee_pct)
    monthly_variable_costs = monthly_payment_cost + monthly_service_cost

    monthly_contribution = (
        monthly_gross_profit
        - monthly_variable_costs
        - inputs.monthly_operating_cost_gbp
    )
    annual_contribution_before_setup = monthly_contribution * 12
    year_1_net_contribution = annual_contribution_before_setup - inputs.setup_cost_gbp

    effective_contribution_margin = 0.0
    if monthly_gmv > 0:
        effective_contribution_margin = (
            monthly_gross_profit - monthly_variable_costs
        ) / monthly_gmv

    if effective_contribution_margin > 0:
        break_even_monthly_gmv = inputs.monthly_operating_cost_gbp / effective_contribution_margin
    else:
        break_even_monthly_gmv = inf

    if monthly_contribution > 0:
        payback_months = inputs.setup_cost_gbp / monthly_contribution
    else:
        payback_months = inf

    return {
        "Market": inputs.market,
        "Adjusted checkout conversion %": adjusted_checkout * 100,
        "Adjusted approval %": adjusted_approval * 100,
        "Monthly payment attempts": monthly_payment_attempts,
        "Monthly orders": monthly_orders,
        "Monthly GMV £": monthly_gmv,
        "Monthly revenue ex tax £": monthly_revenue_ex_tax,
        "Monthly net revenue £": monthly_net_revenue,
        "Monthly gross profit £": monthly_gross_profit,
        "Monthly variable fees £": monthly_variable_costs,
        "Monthly contribution £": monthly_contribution,
        "Annual contribution before setup £": annual_contribution_before_setup,
        "Year 1 net contribution £": year_1_net_contribution,
        "Effective contribution margin %": effective_contribution_margin * 100,
        "Break-even monthly GMV £": break_even_monthly_gmv,
        "Payback months": payback_months,
    }


def run_sensitivity(inputs: MarketInputs) -> list[Dict[str, float | str]]:
    """Three transparent scenarios around the user-supplied base case."""
    scenarios = {
        "Downside": {
            "sessions_multiplier": 0.80,
            "checkout_uplift_multiplier": 0.50,
            "approval_uplift_multiplier": 0.50,
        },
        "Base": {
            "sessions_multiplier": 1.00,
            "checkout_uplift_multiplier": 1.00,
            "approval_uplift_multiplier": 1.00,
        },
        "Upside": {
            "sessions_multiplier": 1.20,
            "checkout_uplift_multiplier": 1.50,
            "approval_uplift_multiplier": 1.50,
        },
    }

    out = []
    base = asdict(inputs)
    for name, params in scenarios.items():
        scenario_data = dict(base)
        scenario_data["monthly_qualified_sessions"] *= params["sessions_multiplier"]
        scenario_data["checkout_uplift_pct"] *= params["checkout_uplift_multiplier"]
        scenario_data["approval_uplift_pp"] *= params["approval_uplift_multiplier"]
        result = calculate_market(MarketInputs(**scenario_data))
        result["Scenario"] = name
        out.append(result)
    return out


def calculate_portfolio(rows: Iterable[MarketInputs]) -> list[Dict[str, float | str]]:
    return [calculate_market(row) for row in rows]

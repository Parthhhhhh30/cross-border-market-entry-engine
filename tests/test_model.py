import math

import pytest

from model import MarketInputs, calculate_market, run_sensitivity


def base_inputs(**overrides):
    data = dict(
        market="Test",
        monthly_qualified_sessions=100000,
        checkout_conversion_pct=4.0,
        checkout_uplift_pct=10.0,
        payment_approval_pct=90.0,
        approval_uplift_pp=2.0,
        average_order_value_gbp=100.0,
        indirect_tax_pct=20.0,
        prices_tax_inclusive=True,
        refund_chargeback_pct=2.0,
        gross_margin_pct=80.0,
        payment_processing_pct=3.0,
        service_fee_pct=4.0,
        monthly_operating_cost_gbp=5000.0,
        setup_cost_gbp=20000.0,
    )
    data.update(overrides)
    return MarketInputs(**data)


def test_core_math_is_reproducible():
    result = calculate_market(base_inputs())
    assert result["Monthly payment attempts"] == pytest.approx(4400)
    assert result["Monthly orders"] == pytest.approx(4048)
    assert result["Monthly GMV £"] == pytest.approx(404800)
    assert result["Monthly revenue ex tax £"] == pytest.approx(337333.333333, rel=1e-6)


def test_tax_inclusive_revenue_is_lower_than_gmv():
    result = calculate_market(base_inputs())
    assert result["Monthly revenue ex tax £"] < result["Monthly GMV £"]


def test_tax_exclusive_revenue_equals_gmv_before_refunds():
    result = calculate_market(base_inputs(prices_tax_inclusive=False))
    assert result["Monthly revenue ex tax £"] == pytest.approx(result["Monthly GMV £"])


def test_payback_is_infinite_when_contribution_non_positive():
    result = calculate_market(base_inputs(monthly_operating_cost_gbp=1_000_000))
    assert math.isinf(result["Payback months"])


def test_percentage_bounds_are_enforced():
    with pytest.raises(ValueError):
        calculate_market(base_inputs(gross_margin_pct=101))


def test_sensitivity_has_three_named_scenarios():
    rows = run_sensitivity(base_inputs())
    assert [x["Scenario"] for x in rows] == ["Downside", "Base", "Upside"]
    assert rows[0]["Year 1 net contribution £"] < rows[1]["Year 1 net contribution £"] < rows[2]["Year 1 net contribution £"]


def test_higher_service_fee_reduces_contribution():
    low = calculate_market(base_inputs(service_fee_pct=2.0))
    high = calculate_market(base_inputs(service_fee_pct=8.0))
    assert high["Monthly contribution £"] < low["Monthly contribution £"]


def test_break_even_gmv_covers_recurring_operating_cost():
    result = calculate_market(base_inputs())
    margin = result["Effective contribution margin %"] / 100
    assert result["Break-even monthly GMV £"] * margin == pytest.approx(5000.0)

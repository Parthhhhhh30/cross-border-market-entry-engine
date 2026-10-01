from __future__ import annotations

import math

import pandas as pd
import streamlit as st

from data import load_market_context
from model import MarketInputs, calculate_portfolio, run_sensitivity

st.set_page_config(page_title="Cross-Border Market Entry Decision Engine", page_icon="🌍", layout="wide")

st.title("Cross-Border Market Entry Decision Engine")
st.caption("Scenario-based decision support for a hypothetical UK digital-services merchant. Public market data provides context; merchant-specific assumptions drive the economics.")
st.info("Portfolio model only — not tax or legal advice. There is no opaque country score; every comparison comes from visible assumptions.")

@st.cache_data(ttl=21600)
def get_context():
    return load_market_context(use_live=True)

context = get_context()
base_assumptions = pd.read_csv("assumptions.csv")

with st.sidebar:
    st.header("Merchant assumptions")
    base_checkout = st.number_input("Baseline checkout conversion %", 0.1, 100.0, 4.0, 0.1)
    base_approval = st.number_input("Baseline payment approval %", 0.1, 100.0, 92.0, 0.1)
    aov = st.number_input("Average order value £", 1.0, 10000.0, 79.0, 1.0)
    gross_margin = st.number_input("Gross margin % of net revenue", 0.0, 100.0, 78.0, 1.0)
    refunds = st.number_input("Refund + chargeback rate %", 0.0, 100.0, 3.0, 0.1)
    processing = st.number_input("Payment processing % of GMV", 0.0, 100.0, 2.9, 0.1)
    service_fee = st.number_input("Platform / MoR service fee % of GMV", 0.0, 100.0, 4.0, 0.1)
    prices_tax_inclusive = st.toggle("Customer price is tax-inclusive", value=True)
    st.caption("Service fee is an editable scenario assumption — it is not Outpost pricing.")

st.subheader("1. Market-specific assumptions")
st.caption("These six rows are synthetic merchant assumptions, not public facts. Edit them to test demand, localisation, setup cost or tax-mix hypotheses.")

editable = st.data_editor(
    base_assumptions,
    hide_index=True,
    use_container_width=True,
    num_rows="fixed",
    column_config={
        "Monthly qualified sessions": st.column_config.NumberColumn(min_value=0, step=5000),
        "Checkout uplift %": st.column_config.NumberColumn(format="%.1f%%"),
        "Approval uplift pp": st.column_config.NumberColumn(format="%.1f pp"),
        "Setup cost £": st.column_config.NumberColumn(format="£%d"),
        "Monthly operating cost £": st.column_config.NumberColumn(format="£%d"),
        "Model tax %": st.column_config.NumberColumn(format="%.1f%%"),
    },
)

market_inputs = [
    MarketInputs(
        market=row["Market"],
        monthly_qualified_sessions=float(row["Monthly qualified sessions"]),
        checkout_conversion_pct=float(base_checkout),
        checkout_uplift_pct=float(row["Checkout uplift %"]),
        payment_approval_pct=float(base_approval),
        approval_uplift_pp=float(row["Approval uplift pp"]),
        average_order_value_gbp=float(aov),
        indirect_tax_pct=float(row["Model tax %"]),
        prices_tax_inclusive=bool(prices_tax_inclusive),
        refund_chargeback_pct=float(refunds),
        gross_margin_pct=float(gross_margin),
        payment_processing_pct=float(processing),
        service_fee_pct=float(service_fee),
        monthly_operating_cost_gbp=float(row["Monthly operating cost £"]),
        setup_cost_gbp=float(row["Setup cost £"]),
    )
    for _, row in editable.iterrows()
]

results = pd.DataFrame(calculate_portfolio(market_inputs))
context_merge = context[["Market", "Population", "Population year", "GDP per capita US$", "GDP per capita US$ year", "Internet use %", "Internet use % year", "Digital payment adoption %", "Digital payment adoption year", "Indirect tax label", "Tax treatment note", "Official tax source"]].copy()
results = results.merge(context_merge, on="Market", how="left")

finite_payback = results[results["Payback months"].map(math.isfinite)]
best_contribution_row = results.loc[results["Year 1 net contribution £"].idxmax()]
fastest_row = finite_payback.loc[finite_payback["Payback months"].idxmin()] if not finite_payback.empty else None

st.subheader("2. Decision output under the current scenario")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Highest Year-1 contribution", best_contribution_row["Market"], f"£{best_contribution_row['Year 1 net contribution £']:,.0f}")
if fastest_row is not None:
    c2.metric("Fastest setup payback", fastest_row["Market"], f"{fastest_row['Payback months']:.1f} months")
else:
    c2.metric("Fastest setup payback", "No market", "Contribution ≤ 0")
c3.metric("Markets contribution-positive", f"{int((results['Monthly contribution £'] > 0).sum())}/{len(results)}")
c4.metric("Scenario AOV", f"£{aov:,.0f}", "Tax treatment is editable")

st.caption(f"Under these assumptions, {best_contribution_row['Market']} produces the highest Year-1 net contribution. That is a scenario result, not a universal market recommendation.")

comparison = results[["Market", "Monthly GMV £", "Monthly net revenue £", "Monthly contribution £", "Year 1 net contribution £", "Break-even monthly GMV £", "Payback months", "Adjusted checkout conversion %", "Adjusted approval %"]].copy()
comparison["Payback months"] = comparison["Payback months"].replace([math.inf], pd.NA)
st.dataframe(comparison.sort_values("Year 1 net contribution £", ascending=False), hide_index=True, use_container_width=True)
st.bar_chart(results.set_index("Market")[["Year 1 net contribution £", "Monthly contribution £"]])

st.subheader("3. Public market context")
context_display = results[["Market", "Population", "Population year", "GDP per capita US$", "GDP per capita US$ year", "Internet use %", "Internet use % year", "Digital payment adoption %", "Digital payment adoption year", "Indirect tax label"]].copy()
st.dataframe(context_display, hide_index=True, use_container_width=True)
st.caption("Population, GDP per capita and internet-use data load from the World Bank API when available, with a checked fallback snapshot. Findex is left blank when unavailable rather than fabricated.")

selected_market = st.selectbox("Sensitivity market", editable["Market"].tolist(), index=0)
selected_input = next(x for x in market_inputs if x.market == selected_market)
sensitivity = pd.DataFrame(run_sensitivity(selected_input))

st.subheader(f"4. Sensitivity — {selected_market}")
st.caption("Downside = -20% sessions and half the assumed conversion/approval uplifts. Upside = +20% sessions and 1.5× the assumed uplifts.")
sens_display = sensitivity[["Scenario", "Monthly GMV £", "Monthly contribution £", "Year 1 net contribution £", "Payback months"]].copy()
sens_display["Payback months"] = sens_display["Payback months"].replace([math.inf], pd.NA)
st.dataframe(sens_display, hide_index=True, use_container_width=True)
st.bar_chart(sensitivity.set_index("Scenario")[["Year 1 net contribution £"]])

with st.expander("Tax / operating context and sources"):
    for _, row in context.iterrows():
        st.markdown(f"**{row['Market']} — {row['Indirect tax label']}**")
        st.write(row["Tax treatment note"])
        st.caption(row["Official tax source"])

with st.expander("How the model calculates economics"):
    st.markdown("""
- **Successful orders** = qualified sessions × adjusted checkout conversion × adjusted payment approval.
- **GMV** = successful orders × AOV.
- If prices are tax-inclusive, **revenue ex tax** = GMV ÷ (1 + model tax rate).
- **Net revenue** subtracts the refund/chargeback assumption.
- **Gross profit** = net revenue × gross margin.
- **Monthly contribution** = gross profit − payment fees − service/MoR fees − market operating cost.
- **Year-1 net contribution** = 12 × monthly contribution − setup cost.
- **Payback** = setup cost ÷ positive monthly contribution.
- **Break-even monthly GMV** is the GMV required to cover recurring market operating cost at the scenario's effective contribution margin.
""")

st.caption("Independent portfolio project. Synthetic merchant assumptions. Not an official Outpost product, integration, pricing model, tax calculation or legal opinion.")

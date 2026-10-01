# Outpost application evidence

**Live demo:** https://cross-border-market-entry-engine.streamlit.app/

**Source:** https://github.com/Parthhhhhh30/cross-border-market-entry-engine

## Short project answer

I built a cross-border market-entry decision engine for a hypothetical UK digital-services merchant. Instead of hiding a recommendation inside a weighted country score, it separates public market context from merchant-specific assumptions and models the operating economics directly: funnel conversion, payment approval, GMV, indirect-tax treatment, gross contribution, setup cost, break-even GMV and payback. The dashboard compares six markets and lets an operator change assumptions and immediately see how the decision changes, including downside/base/upside sensitivity. Public context is refreshed from World Bank data where available, while tax notes come from official EU and government sources.

## What this demonstrates

- financial / unit-economics modelling
- market-entry thinking
- assumption discipline
- sensitivity analysis
- public-data integration
- transparent decision support rather than black-box scoring
- ability to turn strategy work into an interactive operating tool

## 90-second demo flow

1. Explain the decision: which market should a UK digital merchant enter next under a specific operating scenario?
2. Show that public data and merchant assumptions are visibly separated.
3. Change one market's monthly qualified sessions or setup cost and show the Year-1 contribution / payback move immediately.
4. Open the market comparison and state that the displayed leader is conditional on the current assumptions, not a universal ranking.
5. Select one market and show downside/base/upside sensitivity.
6. Close on what you would add in production: merchant-owned demand data, processor approval data, actual fee schedules, FX and jurisdiction-specific tax logic.

## Claims boundary

Safe claims:
- working deterministic decision model
- six-market comparison
- public World Bank data integration with fallback
- official tax-context references
- unit economics, break-even, payback and sensitivity
- automated tests and Streamlit runtime smoke test
- public deployed dashboard

Do not claim:
- that the model determines legal/tax obligations
- that the synthetic merchant assumptions are real market forecasts
- that the service-fee assumption represents Outpost pricing
- that the highest-contribution market is universally the best market

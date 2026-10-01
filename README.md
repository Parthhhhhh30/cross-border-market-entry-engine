# Cross-Border Market Entry Decision Engine

A scenario-based market-entry model for a hypothetical UK digital-services merchant. The project is designed as strategy/operations evidence: it combines public market context with explicit merchant economics instead of producing a black-box country score.

> Independent portfolio work. Not an official Outpost product, integration, pricing model, tax calculation or legal opinion.

## What it answers

Given a specific merchant scenario, how do candidate markets compare on:

- monthly GMV
- revenue after indirect-tax treatment and refunds
- gross contribution
- recurring operating contribution
- Year-1 contribution after setup cost
- break-even monthly GMV
- setup-cost payback
- downside/base/upside sensitivity

The answer changes when the assumptions change.

## Markets

- Germany
- France
- Netherlands
- Canada
- Australia
- United States

## Public context

The app attempts to load the latest available values from the World Bank V2 API for:

- population (`SP.POP.TOTL`)
- GDP per capita (`NY.GDP.PCAP.CD`)
- individuals using the internet (`IT.NET.USER.ZS`)
- Global Findex made-or-received digital payments (`g20.any`, source 14) when returned for the selected economy

No API key is required for the World Bank V2 Indicators API. A checked snapshot in `market_context.csv` keeps the dashboard usable if the API is unavailable.

Tax context uses official public sources. EU standard VAT rates are modelled as 19% Germany, 20% France and 21% Netherlands. Australia uses 10% GST. Canada and the US use clearly-labelled editable illustrative effective-rate assumptions because the actual rate depends on customer location and other facts.

## Model

```text
Qualified sessions
    x checkout conversion
    x payment approval
= successful orders
    x AOV
= GMV
    -> remove indirect tax if price is tax-inclusive
    -> remove refunds / chargebacks
    -> apply gross margin
    -> subtract payment + service fees
    -> subtract recurring market operating cost
= monthly contribution
```

Then:

- Year-1 net contribution = 12 × monthly contribution − setup cost
- Payback = setup cost ÷ positive monthly contribution
- Break-even monthly GMV = recurring operating cost ÷ effective contribution margin

See `ASSUMPTIONS.md` for the full boundary.

## Why there is no market score

Population, GDP per capita and internet adoption are useful context, but combining them with tax complexity, expected conversion, setup effort and fees into one arbitrary weighted score would hide judgement. This project keeps context visible and lets the scenario economics speak directly.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Test

```bash
pip install pytest
pytest -q
```

## Repository structure

```text
app.py                  Streamlit dashboard
model.py                deterministic financial model
data.py                 World Bank loader + fallback logic
market_context.csv      checked public-data fallback + tax notes
assumptions.csv         synthetic merchant demo assumptions
ASSUMPTIONS.md          model boundary and formulas
ARCHITECTURE.md         design / control rationale
OUTPOST.md              application answer + demo script
.github/workflows/      CI tests
```

## Sources

- World Bank Indicators API / World Development Indicators
- World Bank Global Findex
- European Commission / Your Europe VAT guidance
- European Commission VAT One Stop Shop guidance
- Canada Revenue Agency digital-economy GST/HST guidance
- Australian Taxation Office digital products / services GST guidance
- US Small Business Administration state/local sales-tax guidance

Source URLs are also stored alongside the market context used by the dashboard.

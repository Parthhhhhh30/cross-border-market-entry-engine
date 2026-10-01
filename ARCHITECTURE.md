# Architecture

```text
Official public data
World Bank + government/EU tax sources
                |
                v
        Market context layer
                |
                |  kept separate from assumptions
                v
Synthetic / user-editable merchant assumptions
                |
                v
       Deterministic Python model
 funnel -> GMV -> net revenue -> contribution
          -> break-even -> payback
                |
                +---------------------+
                |                     |
                v                     v
       Market comparison        Sensitivity cases
                |                     |
                +----------+----------+
                           v
                 One-screen Streamlit UI
```

## Design principles

### No opaque market score

The engine does not claim that a country with a larger population, higher GDP per capita or higher internet adoption is universally better. Public context is displayed beside the financial outputs. The economic comparison changes when the merchant assumptions change.

### Deterministic economics

Every financial output can be traced to a formula in `model.py`. No LLM participates in the calculation.

### Explicit uncertainty

The model exposes assumptions that usually get buried in a spreadsheet: qualified traffic, checkout uplift, payment approval uplift, indirect-tax rate, setup cost and recurring operating cost.

### Graceful public-data fallback

The deployed app attempts to refresh selected World Bank indicators through the unauthenticated V2 API. If the API is unavailable it falls back to the checked snapshot in `market_context.csv`. It never fabricates missing Findex payment-adoption values.

### Scope control

Tax information is context, not tax advice. Canada and the US use editable illustrative effective-rate assumptions because their actual rate depends on customer location and other facts.

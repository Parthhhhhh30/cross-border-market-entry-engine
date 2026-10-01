# Model assumptions

## Scenario boundary

The demo assumes a hypothetical UK business selling taxable digital services directly to consumers in six candidate markets. It is not intended to model every product, entity structure, tax registration status or customer type.

## Public data vs merchant assumptions

Public context is intentionally kept separate from the financial model.

**Public context:** population, GDP per capita, internet adoption and, when available from the API, digital-payment adoption. Tax notes come from official government / EU sources.

**Synthetic merchant assumptions:** monthly qualified sessions, conversion uplift, approval uplift, AOV, margin, refunds, processing fees, service/MoR fee, setup cost and recurring operating cost.

The synthetic figures demonstrate the engine. They are not estimates of Outpost customers, Outpost pricing or actual merchant performance.

## Formula choices

The model decomposes the funnel instead of using one conversion-rate black box:

1. qualified sessions
2. checkout conversion
3. payment approval
4. successful orders
5. GMV
6. revenue ex indirect tax
7. revenue after refunds / chargebacks
8. gross profit
9. payment + service fees
10. market operating contribution
11. setup-cost payback

Checkout uplift is relative to the baseline checkout-conversion rate. Approval uplift is an absolute percentage-point change to the baseline approval rate. Both are capped at 100%.

## Tax handling

For Germany, France and the Netherlands, the defaults are the EU standard VAT rates. Australia uses 10% GST. Canada and the US do not have a single rate suitable for a national digital-services model, so their defaults are explicitly illustrative and editable.

If the merchant price is tax-inclusive, the model removes indirect tax from GMV before calculating merchant revenue. If pricing is tax-exclusive, GMV is treated as merchant revenue before refunds.

## What the model does not do

- tax registration determination
- place-of-supply determination
- product taxability classification
- state/province-level tax calculation
- FX forecasting
- fraud-loss modelling beyond the user-entered refund/chargeback rate
- customer-acquisition-cost modelling
- legal-entity or permanent-establishment analysis
- compliance approval

Those would require a production-grade tax/compliance system, not a portfolio decision model.

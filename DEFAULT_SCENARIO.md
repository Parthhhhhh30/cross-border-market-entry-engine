# Default demo scenario

The default scenario is deliberately synthetic. It is designed to make the decision engine useful in a demo, not to forecast actual merchant performance.

Common assumptions:

- baseline checkout conversion: 4.0%
- baseline payment approval: 92.0%
- AOV: £79
- gross margin: 78%
- refunds + chargebacks: 3%
- payment processing: 2.9% of GMV
- platform / MoR service fee: 4.0% of GMV (illustrative; not Outpost pricing)
- customer price: tax-inclusive

Market-specific assumptions are stored in `assumptions.csv` and are editable in the dashboard.

## Expected default outputs

Approximate deterministic outputs from the current defaults:

| Market | Monthly GMV | Monthly contribution | Year-1 net contribution | Payback |
|---|---:|---:|---:|---:|
| Germany | £22.2k | £7.6k | £46.1k | 5.9 months |
| France | £18.8k | £5.8k | £27.3k | 7.3 months |
| Netherlands | £9.8k | £1.6k | -£10.5k | 18.5 months |
| Canada | £17.1k | £6.1k | £35.1k | 6.2 months |
| Australia | £15.1k | £5.3k | £29.1k | 6.6 months |
| United States | £33.8k | £11.3k | £60.9k | 6.6 months |

This is intentionally not labelled a universal ranking. Under the default assumptions the US produces the highest Year-1 contribution, while Germany repays its setup cost faster. Changing demand or cost assumptions can change those outcomes immediately.

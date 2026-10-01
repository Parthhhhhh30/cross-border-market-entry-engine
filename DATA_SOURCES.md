# Data sources and evidence log

Research checked: **1 October 2026**.

## World Bank market context

The dashboard uses the World Bank V2 Indicators API, which the World Bank documents as accessible without an API key.

Series:

- `SP.POP.TOTL` — population, total
- `NY.GDP.PCAP.CD` — GDP per capita, current US$
- `IT.NET.USER.ZS` — individuals using the Internet (% of population)
- `g20.any`, source `14` — made or received a digital payment (% age 15+), Global Findex, when the API returns a value for the economy

API documentation: https://datahelpdesk.worldbank.org/knowledgebase/articles/889392

The app refreshes values from the API when possible and otherwise falls back to `market_context.csv`. Missing Findex values are left blank rather than fabricated.

## EU VAT and OSS

Official EU VAT-rate guidance:
https://europa.eu/youreurope/business/finance-and-tax/vat/vat-rules-rates/index_en.htm

Model defaults:
- Germany: 19%
- France: 20%
- Netherlands: 21%

European Commission VAT One Stop Shop guidance:
https://vat-one-stop-shop.ec.europa.eu/one-stop-shop_en

The model does not determine OSS eligibility or filing obligations.

## Canada

Canada Revenue Agency cross-border digital products and services:
https://www.canada.ca/en/revenue-agency/services/tax/businesses/topics/gst-hst-businesses/digital-economy-gsthst/charge-collect/cross-border.html

The rate depends on place of supply. The app's 13% default is an **illustrative Ontario-heavy effective-rate assumption**, not a national Canadian rate.

## Australia

Australian Taxation Office guidance:
https://www.ato.gov.au/businesses-and-organisations/international-tax-for-business/australians-doing-business-overseas-and-non-residents-doing-business-in-australia/gst-on-imported-services-and-digital-products

The model uses 10% GST as the Australian default and treats registration/taxability as outside scope.

## United States

US Small Business Administration state/local tax guidance:
https://www.sba.gov/business-guide/manage-your-business/pay-taxes

The app uses an editable **8% illustrative blended assumption**, not a claimed national sales-tax rate.

## Evidence discipline

Public facts are not converted into an opaque weighted market score. The financial model is driven only by visible merchant assumptions. Tax context is descriptive and does not determine legal obligations.

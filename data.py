from __future__ import annotations

from pathlib import Path
from typing import Dict, Tuple

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parent
FALLBACK_PATH = ROOT / "market_context.csv"

COUNTRIES = {
    "Germany": "DEU",
    "France": "FRA",
    "Netherlands": "NLD",
    "Canada": "CAN",
    "Australia": "AUS",
    "United States": "USA",
}

WDI_INDICATORS = {
    "Population": "SP.POP.TOTL",
    "GDP per capita US$": "NY.GDP.PCAP.CD",
    "Internet use %": "IT.NET.USER.ZS",
}


def _fetch_indicator(indicator: str, source: int | None = None, timeout: int = 8) -> Dict[str, Tuple[float, int]]:
    country_codes = ";".join(COUNTRIES.values())
    params = {
        "format": "json",
        "per_page": 1000,
        "date": "2020:2026",
    }
    if source is not None:
        params["source"] = source
    url = f"https://api.worldbank.org/v2/country/{country_codes}/indicator/{indicator}"
    response = requests.get(url, params=params, timeout=timeout)
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, list) or len(payload) < 2 or not payload[1]:
        return {}

    latest_by_code: Dict[str, Tuple[float, int]] = {}
    for row in payload[1]:
        value = row.get("value")
        if value is None:
            continue
        code = (row.get("countryiso3code") or "").upper()
        try:
            year = int(row.get("date"))
            numeric = float(value)
        except (TypeError, ValueError):
            continue
        if code not in latest_by_code or year > latest_by_code[code][1]:
            latest_by_code[code] = (numeric, year)
    return latest_by_code


def load_market_context(use_live: bool = True) -> pd.DataFrame:
    """Return market context, preferring live World Bank values with CSV fallback."""
    fallback = pd.read_csv(FALLBACK_PATH)
    fallback = fallback.set_index("Market", drop=False)

    if not use_live:
        return fallback.reset_index(drop=True)

    try:
        live = {label: _fetch_indicator(code) for label, code in WDI_INDICATORS.items()}
        payment = _fetch_indicator("g20.any", source=14)
    except Exception:
        return fallback.reset_index(drop=True)

    rows = []
    for market, code in COUNTRIES.items():
        base = fallback.loc[market].to_dict()
        for label in WDI_INDICATORS:
            if code in live[label]:
                value, year = live[label][code]
                base[label] = value
                base[f"{label} year"] = year
        if code in payment:
            value, year = payment[code]
            base["Digital payment adoption %"] = value
            base["Digital payment adoption year"] = year
        rows.append(base)
    return pd.DataFrame(rows)

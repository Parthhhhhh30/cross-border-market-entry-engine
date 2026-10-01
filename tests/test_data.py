from data import load_market_context


def test_fallback_has_six_markets_and_no_duplicate_market_names():
    df = load_market_context(use_live=False)
    assert len(df) == 6
    assert df["Market"].nunique() == 6
    assert set(df["Market"]) == {"Germany", "France", "Netherlands", "Canada", "Australia", "United States"}


def test_fallback_has_core_public_context():
    df = load_market_context(use_live=False)
    assert df["Population"].notna().all()
    assert df["GDP per capita US$"].notna().all()
    assert df["Internet use %"].notna().all()
    assert df["Official tax source"].str.startswith("http").all()

'''Regression tests for zero-cent competitor price handling.'''

from types import SimpleNamespace
from typing import Any

from src.merchant.services.promotion import compute_promotion_context


def _make_product(base_price: int = 1000) -> Any:
    return SimpleNamespace(
        id='prod-test',
        name='Test Product',
        base_price=base_price,
        stock_count=100,
        min_margin=0.15,
        lifecycle='mature',
        demand_velocity='flat',
    )


def test_zero_competitor_price_is_preserved(monkeypatch):
    '''A legitimate $0.00 competitor price must not be replaced by base_price.'''
    product: Any = _make_product()
    db: Any = None

    monkeypatch.setattr(
        'src.merchant.services.promotion.get_lowest_competitor_price',
        lambda _db, _product_id: 0,
    )

    context = compute_promotion_context(db, product)
    assert context['lowest_competitor_price_cents'] == 0


def test_none_competitor_price_falls_back_to_base(monkeypatch):
    '''When no competitor data exists, the context falls back to base price.'''
    product: Any = _make_product()
    db: Any = None

    monkeypatch.setattr(
        'src.merchant.services.promotion.get_lowest_competitor_price',
        lambda _db, _product_id: None,
    )

    context = compute_promotion_context(db, product)

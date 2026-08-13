from src.merchant.services.promotion import compute_promotion_context


class _FakeDB:
    def __init__(self, competitors):
        self._competitors = competitors

    def exec(self, _statement):
        class _Result:
            def all(_self):
                return self._competitors
        return _Result()


class _FakeCompetitor:
    def __init__(self, price):
        self.price = price


class _FakeProduct:
    def __init__(self):
        self.id = 'prod-1'
        self.name = 'Widget'
        self.base_price = 1000
        self.stock_count = 100
        self.min_margin = 0.2
        self.lifecycle = 'mature'
        self.demand_velocity = 'flat'


def test_zero_competitor_price_is_preserved():
    product = _FakeProduct()
    db = _FakeDB([_FakeCompetitor(0)])

    context = compute_promotion_context(db, product)

    assert context['lowest_competitor_price_cents'] == 0


def test_none_competitor_price_falls_back_to_base_price():
    product = _FakeProduct()
    db = _FakeDB([])

    context = compute_promotion_context(db, product)

    assert context['lowest_competitor_price_cents'] == product.base_price

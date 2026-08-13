from src.merchant.services.promotion import (
    PromotionAction,
    filter_allowed_actions_by_margin,
)


def test_filter_allowed_actions_by_margin_equality_boundary():
    """A discount exactly equal to the margin headroom must be allowed."""
    # min_margin 0.85 => max_discount 0.15, DISCOUNT_15_PCT sits on the boundary
    allowed = filter_allowed_actions_by_margin(0.85)
    assert PromotionAction.DISCOUNT_15_PCT.value in allowed

    # min_margin 0.90 => max_discount 0.10, 15%% exceeds the headroom
    allowed_tight = filter_allowed_actions_by_margin(0.90)
    assert PromotionAction.DISCOUNT_15_PCT.value not in allowed_tight

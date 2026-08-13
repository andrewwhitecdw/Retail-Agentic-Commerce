"""Unit tests for promotion margin filtering boundary behavior."""

from src.merchant.services.promotion import (
    PromotionAction,
    filter_allowed_actions_by_margin,
)


def test_filter_allowed_actions_by_margin_includes_exact_boundary():
    """A discount exactly equal to the margin ceiling must be allowed."""
    # min_margin=0.85 => max_discount=0.15, so DISCOUNT_15_PCT is at the boundary.
    allowed = filter_allowed_actions_by_margin(0.85)
    assert PromotionAction.DISCOUNT_15_PCT.value in allowed
    assert PromotionAction.DISCOUNT_10_PCT.value in allowed
    assert PromotionAction.DISCOUNT_5_PCT.value in allowed
    assert PromotionAction.NO_PROMO.value in allowed
    assert PromotionAction.FREE_SHIPPING.value in allowed


def test_filter_allowed_actions_by_margin_exceeds_ceiling_rejected():
    """Discounts strictly greater than the margin ceiling are rejected."""
    # min_margin=0.90 => max_discount=0.10
    allowed = filter_allowed_actions_by_margin(0.90)
    assert PromotionAction.DISCOUNT_15_PCT.value not in allowed
    assert PromotionAction.DISCOUNT_10_PCT.value in allowed
    assert PromotionAction.DISCOUNT_5_PCT.value in allowed
    assert PromotionAction.NO_PROMO.value in allowed


def test_filter_allowed_actions_by_margin_no_promo_always_present():
    """NO_PROMO fallback is always present even when all discounts excluded."""
    # min_margin=1.0 => max_discount=0.0
    allowed = filter_allowed_actions_by_margin(1.0)
    assert PromotionAction.NO_PROMO.value in allowed
    assert PromotionAction.FREE_SHIPPING.value in allowed
    assert PromotionAction.DISCOUNT_5_PCT.value not in allowed
    assert PromotionAction.DISCOUNT_10_PCT.value not in allowed

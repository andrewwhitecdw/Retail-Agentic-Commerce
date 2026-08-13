from src.merchant.services.promotion import (
    ACTION_DISCOUNT_MAP,
    filter_allowed_actions_by_margin,
)


def test_filter_allowed_actions_by_margin_includes_exact_threshold():
    """Every action whose discount equals (1 - min_margin) must be allowed."""
    for action, discount in ACTION_DISCOUNT_MAP.items():
        min_margin = 1.0 - discount
        allowed = filter_allowed_actions_by_margin(min_margin)
        assert action.value in allowed, f"{action.value} should be allowed at min_margin={min_margin}"

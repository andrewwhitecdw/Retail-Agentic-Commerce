"""Regression tests for margin validation."""

from src.merchant.services.promotion import validate_discount_against_margin


def test_validate_discount_uses_exact_float_boundary():
    """Truncation previously allowed final prices below the true float boundary."""
    base_price = 99
    min_margin = 0.15
    # 99 * 0.15 = 14.85. Discount 84 -> final 15 (OK); 85 -> final 14 (violates).
    assert validate_discount_against_margin(base_price, 84, min_margin) is True
    assert validate_discount_against_margin(base_price, 85, min_margin) is False


def test_validate_discount_integer_boundary_still_works():
    """When the boundary is an exact integer, equality must still be allowed."""
    assert validate_discount_against_margin(100, 85, 0.15) is True
    assert validate_discount_against_margin(100, 86, 0.15) is False

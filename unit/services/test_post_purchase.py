# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

import asyncio
from unittest.mock import AsyncMock

import pytest

from src.merchant.services.post_purchase import (
    PostPurchaseAgentClient,
    build_message_request,
    generate_shipping_messages_batch,
)


@pytest.mark.asyncio
async def test_generate_shipping_messages_batch_propagates_cancelled_error():
    """CancelledError from a task must not be swallowed as a fallback case."""
    client = AsyncMock(spec=PostPurchaseAgentClient)
    client.generate_message = AsyncMock(side_effect=asyncio.CancelledError())

    request = build_message_request(
        order_id="ORDER-123",
        customer_name="Alice",
        items=[{"name": "T-Shirt", "quantity": 1}],
        status="order_confirmed",
    )

    with pytest.raises(asyncio.CancelledError):
        await generate_shipping_messages_batch([request], client=client)

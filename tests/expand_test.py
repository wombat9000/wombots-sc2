import asyncio
from unittest.mock import Mock

import pytest

from .context import initial_bot_state


@pytest.mark.asyncio
async def test_expand():
    bot = initial_bot_state([])
    bot.can_build_building = Mock(return_value=True)
    expand_stub = Mock(return_value=None)
    bot.expand_now = asyncio.coroutine(expand_stub)

    success = await bot.expand()

    assert success
    expand_stub.assert_called()


@pytest.mark.asyncio
async def test_cant_expand_if_cant_build():
    bot = initial_bot_state([])
    bot.can_build_building = Mock(return_value=False)
    expand_stub = Mock(return_value=None)
    bot.expand_now = asyncio.coroutine(expand_stub)

    success = await bot.expand()

    assert not success
    expand_stub.assert_not_called()

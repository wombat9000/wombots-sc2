import asyncio
from typing import Deque
from unittest.mock import Mock

import pytest

from .context import ZergBot, Composer


@pytest.mark.asyncio
async def test_updates_multiple_bots():
    one_bot = ZergBot(Deque([]))
    two_bot = ZergBot(Deque([]))
    bots = [one_bot, two_bot]
    composer = Composer(bots)

    composer.state = Mock()

    for bot in bots:
        bot._prepare_step = Mock(return_value=None)
        on_step_stub = Mock(return_value=None)
        bot.on_step = asyncio.coroutine(on_step_stub)

        bot._prepare_first_step = Mock(return_value=None)

    iteration = 1
    await composer.on_step(iteration)

    for bot in bots:
        bot._prepare_step.assert_called_once_with(composer.state)
        bot._prepare_first_step.assert_not_called()
        on_step_stub.assert_called_once_with(iteration)


@pytest.mark.asyncio
async def test_prepare_first_step():
    one_bot = ZergBot(Deque([]))
    two_bot = ZergBot(Deque([]))
    bots = [one_bot, two_bot]
    composer = Composer(bots)

    composer.state = Mock()

    for bot in bots:
        on_step_stub = Mock(return_value=None)
        bot.on_step = asyncio.coroutine(on_step_stub)
        bot._prepare_step = Mock(return_value=None)
        bot._prepare_first_step = Mock(return_value=None)

    iteration = 0
    await composer.on_step(iteration)

    for bot in bots:
        bot._prepare_step.assert_called_once_with(composer.state)
        bot._prepare_first_step.assert_called_once()
        on_step_stub.assert_called_once_with(iteration)


@pytest.mark.asyncio
async def test_prepare_start():
    one_bot = ZergBot(Deque([]))
    two_bot = ZergBot(Deque([]))
    bots = [one_bot, two_bot]
    composer = Composer(bots)

    # composer.state = Mock()
    composer._client = Mock()
    composer.player_id = 2
    composer._game_info = Mock()
    composer._game_data = Mock()

    for bot in bots:
        bot._prepare_start = Mock(return_value=None)

    composer.on_start()

    for bot in bots:
        bot._prepare_start.assert_called_with(composer._client,
                                              composer.player_id,
                                              composer._game_info,
                                              composer._game_data)

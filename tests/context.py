import os
import sys
from unittest.mock import Mock

from sc2 import Race
from sc2 import race_worker

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from wombots.zerg_bot import *


async def async_mock(val):
    return val


def unit_mock_of(type_id: UnitTypeId):
    unit: Unit = Mock()
    unit.is_mine = Mock(return_value=True)
    unit.type_id = type_id
    return unit


def add_unit_to_bot(unit_type: UnitTypeId, bot: ZergBot, ) -> Unit:
    unit: Unit = unit_mock_of(unit_type)
    bot.units.append(unit)
    bot.workers = bot.units(race_worker[bot.race])
    return unit


def initial_bot_state(build_order) -> ZergBot:
    bot = ZergBot(Deque(build_order))

    bot.race = Race.Zerg
    bot.units = Units([], Mock())
    bot.supply_left = 10
    return bot

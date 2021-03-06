#!/usr/bin/env python3
from typing import Deque

from sc2 import run_game, maps, Race, Difficulty
from sc2.ids.unit_typeid import UnitTypeId
from sc2.player import Bot, Computer

from wombots.composed_bot import Composer
from wombots.zerg_bot import ZergBot

POOL_12_BUILD_ORDER = Deque([
    UnitTypeId.DRONE,
    UnitTypeId.OVERLORD,
    UnitTypeId.DRONE,
    UnitTypeId.DRONE,
    UnitTypeId.DRONE,
    UnitTypeId.DRONE,
    UnitTypeId.HATCHERY,
    UnitTypeId.DRONE,
    UnitTypeId.DRONE,
    UnitTypeId.EXTRACTOR,
    UnitTypeId.SPAWNINGPOOL,
    UnitTypeId.DRONE,
    UnitTypeId.DRONE,
    UnitTypeId.OVERLORD,
    UnitTypeId.OVERLORD,
    UnitTypeId.OVERLORD,
    UnitTypeId.DRONE,
    UnitTypeId.DRONE,
    UnitTypeId.DRONE,
    UnitTypeId.DRONE,
    UnitTypeId.DRONE,
    UnitTypeId.DRONE,
    UnitTypeId.DRONE,
    UnitTypeId.DRONE
])

run_game(maps.get("Abyssal Reef LE"), [
    Bot(Race.Zerg, Composer([ZergBot(POOL_12_BUILD_ORDER)])),
    Computer(Race.Protoss, Difficulty.Easy)
], realtime=True)

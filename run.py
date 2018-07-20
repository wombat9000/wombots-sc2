#!/usr/bin/env python3

from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer

from zerg_bot import ZergBot

run_game(maps.get("Abyssal Reef LE"), [
    Bot(Race.Zerg, ZergBot()),
    Computer(Race.Protoss, Difficulty.Easy)
], realtime=False)

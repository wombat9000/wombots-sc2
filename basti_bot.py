#!/usr/bin/env python3

import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.constants import *
from sc2.player import Bot, Computer

DRONE_SUPPLY = 1

class BastiBot(sc2.BotAI):


    async def on_step(self, iteration):
        larvae = self.units(UnitTypeId.LARVA)

        if larvae.exists:
            await self.maintainSupply(larvae.random)
            await self.trainDrone(larvae.random)

    async def maintainSupply(self, larva):
        if self.supply_left <= 3 and not self.already_pending(UnitTypeId.OVERLORD):
            await self.trainOverlord(larva)

    async def trainOverlord(self, larva):
        if self.can_afford(UnitTypeId.OVERLORD):
            await self.do(larva.train(UnitTypeId.OVERLORD))

    async def trainDrone(self, larva):
        if self.can_afford(UnitTypeId.DRONE) and self.supply_left >= DRONE_SUPPLY:
            await self.do(larva.train(UnitTypeId.DRONE))

run_game(maps.get("Abyssal Reef LE"), [
    Bot(Race.Zerg, BastiBot()),
    Computer(Race.Protoss, Difficulty.Easy)
], realtime=True)
import sc2
from sc2.constants import *

DRONE_SUPPLY = 1

class ZergBot(sc2.BotAI):

    async def on_step(self, iteration):
        larvae = self.units(UnitTypeId.LARVA)

        hatchery = self.units(UnitTypeId.HATCHERY).random

        if larvae.exists:
            await self.maintainSupply(larvae.random)
            await self.trainDrone(larvae.random)

        # print(dir(larvae.random))

        if self.units(UnitTypeId.SPAWNINGPOOL) < 1 and self.can_afford(UnitTypeId.SPAWNINGPOOL):
            await self.build(UnitTypeId.SPAWNINGPOOL, hatchery)

    async def maintainSupply(self, larva):
        if self.supply_left <= 3 and not self.already_pending(UnitTypeId.OVERLORD):
            await self.trainOverlord(larva)

    async def trainOverlord(self, larva):
        if self.can_afford(UnitTypeId.OVERLORD):
            await self.do(larva.train(UnitTypeId.OVERLORD))

    async def trainDrone(self, larva):
        if self.can_afford(UnitTypeId.DRONE) and self.supply_left >= DRONE_SUPPLY:
            await self.do(larva.train(UnitTypeId.DRONE))

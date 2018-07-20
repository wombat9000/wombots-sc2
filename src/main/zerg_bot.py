import sc2
from sc2.constants import *


class ZergBot(sc2.BotAI):

    async def on_step(self, iteration):
        await self.maintain_supply()
        await self.train_unit(UnitTypeId.DRONE, 1)

        hatchery = self.units(UnitTypeId.HATCHERY).random

        if len(self.units(UnitTypeId.SPAWNINGPOOL)) < 1 and self.can_afford(UnitTypeId.SPAWNINGPOOL):
            await self.build(UnitTypeId.SPAWNINGPOOL, hatchery)

    async def maintain_supply(self):
        if self.supply_left <= 3 and not self.already_pending(UnitTypeId.OVERLORD):
            await self.train_unit(UnitTypeId.OVERLORD, 0)

    def select_larvae(self):
        return self.units(UnitTypeId.LARVA)

    async def train_unit(self, unit_type, supply_cost):
        larvae = self.select_larvae()
        if larvae.exists:
            if self.can_afford(unit_type) and self.supply_left >= supply_cost:
                await self.do(larvae.random.train(unit_type))

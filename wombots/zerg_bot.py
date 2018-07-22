from typing import Deque

import sc2
from sc2.constants import *
from sc2.unit import Unit
from sc2.units import Units

SUPPLY_COST = {
    UnitTypeId.DRONE: 1,
    UnitTypeId.OVERLORD: 0
}

STRUCTURES = [
    UnitTypeId.SPAWNINGPOOL,
    UnitTypeId.EXTRACTOR,
    UnitTypeId.HATCHERY
]


class ZergBot(sc2.BotAI):

    def get_time_in_seconds(self):
        return self.state.game_loop * 0.725 * (1 / 16)

    def __init__(self, build_order: Deque[UnitTypeId]):
        self.build_order = build_order

    async def on_step(self, iteration):
        # limit bot action rate to give game time to update
        if iteration % 6 == 0:
            if self.build_order:
                await self.follow_build_order()

    async def follow_build_order(self):
        next_unit = self.build_order.popleft()

        if not self.can_afford(next_unit):
            return self.build_order.appendleft(next_unit)

        if next_unit in STRUCTURES:
            if self.workers.exists:
                hatchery = self.units(UnitTypeId.HATCHERY).random
                await self.build(next_unit, hatchery)
            else:
                return self.build_order.appendleft(next_unit)
        else:
            await self.train_unit(next_unit)

    async def maintain_supply(self):
        if self.supply_left <= 3 and not self.already_pending(UnitTypeId.OVERLORD):
            await self.train_unit(UnitTypeId.OVERLORD)

    async def train_unit(self, unit_type):
        larvae: Units = self.select_larvae()
        if larvae.exists and self.can_afford(unit_type) and self.supply_left >= SUPPLY_COST[unit_type]:
            larva: Unit = larvae.first
            await self.do(larva.train(unit_type))

    def select_larvae(self) -> Units:
        return self.units(UnitTypeId.LARVA)

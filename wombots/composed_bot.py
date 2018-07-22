from typing import List

from sc2 import BotAI


class Composer(BotAI):
    def __init__(self, bots: List[BotAI]):
        self.bots = bots

    async def on_step(self, iteration):
        for bot in self.bots:
            bot._prepare_step(self.state)

            if iteration == 0:
                bot._prepare_first_step()

            await bot.on_step(iteration)

    def on_start(self):
        for bot in self.bots:
            bot._prepare_start(self._client, self.player_id, self._game_info, self._game_data)

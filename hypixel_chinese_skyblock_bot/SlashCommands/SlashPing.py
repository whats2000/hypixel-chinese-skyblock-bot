import logging

import disnake
from disnake.ext import commands

from hypixel_chinese_skyblock_bot.Core.Common import CodExtension, get_setting_json
from hypixel_chinese_skyblock_bot.Core.Logger import Logger

bot_logger = Logger(__name__)


class SlashPingCommand(CodExtension):
    @commands.slash_command(
        guild_ids=[int(get_setting_json('ServerId'))],
        name='ping',
        description='Return the ping value from bot',
    )
    async def ping(self, inter: disnake.AppCommandInteraction):
        await inter.response.defer(ephemeral=True)

        bot_logger.log_message(logging.DEBUG, f'{inter.author.name} 用戶呼叫延遲測試命令: bot -> {self.bot.latency}')

        embed = disnake.Embed(
            title="連線延遲 ping",
            description=f'{self.bot.latency * 1000} ms',
            color=0x00ff00
        )

        embed.set_author(
            name=inter.author.name,
            icon_url=inter.author.avatar.url
        )

        await inter.edit_original_message(embed=embed)


def setup(pybot):
    pybot.add_cog(SlashPingCommand(pybot))

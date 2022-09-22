import logging

import disnake
from disnake.ext import commands
from hypixel_chinese_skyblock_bot.Core.Common import CodExtension
from hypixel_chinese_skyblock_bot.Core.Logger import Logger


class PingCommand(CodExtension):

    @commands.command()
    async def ping(self, ctx: commands.Context):
        bot_logger = Logger(__name__)

        bot_logger.log_message(logging.DEBUG, f'{ctx.message.author.name} 用戶呼叫延遲測試命令: bot -> {self.bot.latency}')

        embed = disnake.Embed(
            title='連線延遲 ping',
            description=f'{self.bot.latency * 1000} ms',
            color=0x00ff00
        )

        embed.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar.url
        )

        await ctx.send(embed=embed)

        await ctx.message.delete()


def setup(pybot):
    pybot.add_cog(PingCommand(pybot))

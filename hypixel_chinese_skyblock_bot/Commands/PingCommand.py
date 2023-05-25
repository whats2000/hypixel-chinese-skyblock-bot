import logging

import disnake
from disnake.ext import commands
from CoreFunction.Common import CodExtension
from CoreFunction.Logger import Logger
from CoreFunction.SendEmbed import set_ctx_embed_author

bot_logger = Logger(__name__)


class PingCommand(CodExtension):

    @commands.command()
    async def ping(self, ctx: commands.Context):
        bot_logger.log_message(logging.DEBUG, f'{ctx.message.author.name} 用戶呼叫延遲測試命令: bot -> {self.bot.latency}')

        embed = disnake.Embed(
            title='連線延遲 ping',
            description=f'{self.bot.latency * 1000} ms',
            color=0x00ff00
        )

        set_ctx_embed_author(embed, ctx)

        await ctx.send(embed=embed)

        await ctx.message.delete()


def setup(pybot):
    pybot.add_cog(PingCommand(pybot))

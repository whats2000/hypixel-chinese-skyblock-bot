import logging

import disnake
from disnake.ext import commands

from CoreFunction.Common import CodExtension, get_setting_json
from CoreFunction.Logger import Logger

bot_logger = Logger(__name__)


class CopyMessage(CodExtension):

    @commands.has_any_role(get_setting_json('AdminRole'))
    @commands.command()
    async def cp(self, ctx: commands.Context, args: str = None):
        bot_logger.log_message(logging.DEBUG, f'{ctx.message.author.name} 用戶呼叫複製命令')

        if args is not None:
            embed = disnake.Embed(
                title='警告',
                description=args,
                color=0xe74c3c
            )

            await ctx.send(embed=embed)

        await ctx.message.delete()


def setup(pybot):
    pybot.add_cog(CopyMessage(pybot))

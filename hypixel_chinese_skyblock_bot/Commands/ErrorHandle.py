import logging

import disnake
from disnake.ext import commands

from hypixel_chinese_skyblock_bot.Core.Common import CodExtension
from hypixel_chinese_skyblock_bot.Core.Logger import Logger


class ErrorHandle(CodExtension):
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        bot_logger = Logger(__name__)

        bot_logger.log_message(logging.ERROR, f'{ctx.message.author.name} 使用 prefix command 出現錯誤 : {error}')

        if isinstance(error, commands.CommandNotFound):
            message = '未知指令!'

        elif isinstance(error, commands.CommandOnCooldown):
            message = f'此指令在冷卻中。 請在 {round(error.retry_after, 1)} 秒後重試'

        elif isinstance(error, commands.MissingPermissions):
            message = '你沒有權限使用該指令!'

        elif isinstance(error, commands.UserInputError):
            message = '你的輸入內容有誤, 請檢查你的輸入內容!'

        else:
            message = '運行該命令時發生未知錯誤!'

        embed = disnake.Embed(
            title='錯誤狀況',
            description=message,
            color=0xe74c3c
        )

        embed.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar.url
        )

        await ctx.send(embed=embed, delete_after=20.0)

        await ctx.message.delete()


def setup(pybot):
    pybot.add_cog(ErrorHandle(pybot))

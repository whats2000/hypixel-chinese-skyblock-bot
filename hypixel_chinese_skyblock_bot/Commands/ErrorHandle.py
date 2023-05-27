import logging
import traceback

import disnake
from disnake.ext import commands

from CoreFunction.Common import CodExtension
from CoreFunction.Logger import Logger
from CoreFunction.SendEmbed import set_ctx_embed_author

bot_logger = Logger(__name__)


class ErrorHandle(CodExtension):
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        bot_logger.log_message(logging.ERROR, f'{ctx.message.author.name} 使用 prefix command 出現錯誤 : '
                                              f'[{type(error).__name__}] {error}')

        # 顯示程式錯誤位置
        # bot_logger.log_message(logging.ERROR, f'追朔位置 : '.join(traceback.format_tb(error.__traceback__)))

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

        set_ctx_embed_author(embed, ctx)

        await ctx.send(embed=embed, delete_after=20.0)

        await ctx.message.delete()


def setup(pybot):
    pybot.add_cog(ErrorHandle(pybot))

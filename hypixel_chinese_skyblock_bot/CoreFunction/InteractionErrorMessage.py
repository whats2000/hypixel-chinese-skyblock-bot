import logging
import traceback

import disnake
from disnake.ext import commands

from CoreFunction import Logger
from CoreFunction.Common import get_setting_json


async def handle_interaction_error(bot_logger: Logger,
                                   bot: commands.Bot,
                                   inter: disnake.AppCommandInteraction,
                                   error: commands.CommandError):
    if inter is not None:
        user_name = inter.author.name

        channel = inter.channel
    else:
        user_name = '未知使用者'

        channel = bot.get_channel(get_setting_json('ErrorMessageChannel'))

    bot_logger.log_message(logging.ERROR, f'{user_name} 使用交互命令出現錯誤 : [{type(error).__name__}] {error}')

    if isinstance(error, commands.CommandNotFound):
        message = '未知指令!'

    elif isinstance(error, commands.CommandOnCooldown):
        message = f'此指令在冷卻中。 請在 {round(error.retry_after, 1)} 秒後重試'

    elif isinstance(error, commands.MissingPermissions):
        message = '你沒有權限使用該指令!'

    elif isinstance(error, commands.UserInputError):
        message = '你的輸入內容有誤, 請檢查你的輸入內容!'

    elif isinstance(error, commands.CommandInvokeError):
        message = '網路壅塞中，請稍等後再嘗試'

    else:
        message = '運行該命令時發生未知錯誤!'
        bot_logger.log_message(logging.ERROR, f'追朔位置 : '.join(traceback.format_tb(error.__traceback__)))

    embed = disnake.Embed(
        title='錯誤狀況',
        description=message,
        color=0xe74c3c
    )

    if isinstance(error, commands.CommandOnCooldown):
        await inter.send(embed=embed, delete_after=20.0)

    else:
        await channel.send(embed=embed, delete_after=20.0)
import logging

import disnake
from disnake.ext import commands
from hypixel_chinese_skyblock_bot.Core.Common import CodExtension
from hypixel_chinese_skyblock_bot.Core import TranslateText
from hypixel_chinese_skyblock_bot.Core.Logger import Logger

bot_logger = Logger(__name__)


class TranslateCommand(CodExtension):

    @commands.command()
    async def translate(self, ctx: commands.Context, lang: str = None, *, args: str = None):
        if lang is not None and args is not None:
            bot_logger.log_message(logging.DEBUG, f'{ctx.message.author.name} 用戶呼叫翻譯命令')

            result = TranslateText.translate_text(None, lang, args)

            embed = disnake.Embed(
                title=result.text,
                description=f'{result.src} -> {result.dest}',
                color=0x00ff00
            )

            embed.set_author(
                name=ctx.message.author.name,
                icon_url=ctx.message.author.avatar.url
            )

            await ctx.send(embed=embed)


def setup(pybot):
    pybot.add_cog(TranslateCommand(pybot))

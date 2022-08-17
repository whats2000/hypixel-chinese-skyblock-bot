import discord
from discord.ext import commands
from hypixel_chinese_skyblock_bot.Core.Common import CodExtension
from hypixel_chinese_skyblock_bot.Core import TranslateText


class TranslateCommand(CodExtension):

    @commands.command()
    async def translate(self, ctx, lang=None, *, args=None):
        if lang is not None and args is not None:
            print(f'Info >　用戶請求翻譯 -> {ctx.message.author.name}')

            result = TranslateText.translate_text(None, lang, args)

            embed = discord.Embed(
                title=result.text,
                description=f'{result.src} -> {result.dest}',
                color=0x00ff00
            )

            embed.set_author(
                name=ctx.message.author.name,
                icon_url=ctx.message.author.avatar_url
            )

            await ctx.send(embed=embed)


def setup(pybot):
    pybot.add_cog(TranslateCommand(pybot))

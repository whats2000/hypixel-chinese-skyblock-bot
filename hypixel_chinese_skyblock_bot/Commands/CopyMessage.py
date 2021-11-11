import discord
from discord.ext import commands

from hypixel_chinese_skyblock_bot.Core.Common import CodExtension, get_setting_json


class CopyMessage(CodExtension):

    @commands.has_any_role(get_setting_json('AdminRole'))
    @commands.command()
    async def cp(self, ctx, args):
        embed = discord.Embed(
            title="警告",
            description=str(args),
            color=0xe74c3c
        )

        await ctx.send(embed=embed)

        await ctx.message.delete()


def setup(pybot):
    pybot.add_cog(CopyMessage(pybot))

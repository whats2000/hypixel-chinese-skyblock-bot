import discord
from discord.ext import commands
from hypixel_chinese_skyblock_bot.Core.Common import Cod_Extension


class Verify(Cod_Extension):

    @commands.command()
    async def verify(self, ctx):
        print('test')


def setup(pybot):
    pybot.add_cog(Verify(pybot))

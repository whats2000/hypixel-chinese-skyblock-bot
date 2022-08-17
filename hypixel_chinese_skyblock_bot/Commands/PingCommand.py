import discord
from discord.ext import commands
from hypixel_chinese_skyblock_bot.Core.Common import CodExtension


class PingCommand(CodExtension):

    @commands.command()
    async def ping(self, ctx):
        print(f'Debug > 呼叫延遲檢測 -> {self.bot.latency}')

        embed = discord.Embed(
            title='連線延遲 ping',
            description=f'{self.bot.latency * 1000} ms',
            color=0x00ff00
        )

        embed.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url
        )

        await ctx.send(embed=embed)

        await ctx.message.delete()


def setup(pybot):
    pybot.add_cog(PingCommand(pybot))

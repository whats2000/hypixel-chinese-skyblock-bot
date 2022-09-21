import disnake
from disnake.ext import commands

from hypixel_chinese_skyblock_bot.Core.Common import CodExtension, get_setting_json


class CopyMessage(CodExtension):

    @commands.has_any_role(get_setting_json('AdminRole'))
    @commands.command()
    async def cp(self, ctx: commands.Context, args: str = None):
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

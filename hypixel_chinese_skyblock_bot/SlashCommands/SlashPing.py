import discord
from dislash import slash_command
from hypixel_chinese_skyblock_bot.Core.Common import CodExtension, get_setting_json


class SlashPingCommand(CodExtension):
    @slash_command(
        guild_ids=[int(get_setting_json('ServerId'))],
        name="ping",
        description="Return the ping value from bot",
    )
    async def ping(self, inter):
        print('> 呼叫延遲檢測 -> ' + str(self.bot.latency))

        embed = discord.Embed(
            title="連線延遲 ping",
            description=str(self.bot.latency*1000)+' ms',
            color=0x00ff00
        )

        embed.set_author(
            name=inter.message.author.name,
            icon_url=inter.message.author.avatar_url
        )

        await inter.respond(embed=embed)


def setup(pybot):
    pybot.add_cog(SlashPingCommand(pybot))

import discord
from discord.ext import commands
from dislash import slash_command, OptionType
from dislash.slash_commands import Option

from hypixel_chinese_skyblock_bot.Core.Common import CodExtension, get_setting_json


class SlashEmbed(CodExtension):
    @slash_command(
        guild_ids=[int(get_setting_json('ServerId'))],
        name="embed",
        description="Build a embed",
        options=[
            Option('title', 'Makes the title of the embed', OptionType.STRING),
            Option('description', 'Makes the description', OptionType.STRING),
            Option('color', 'The color of the embed', OptionType.STRING),
            Option('picture', 'The picture of the embed', OptionType.STRING)
        ]
    )
    async def embed(self, inter, title=None, description=None, color=None, picture=None):
        if color is not None:
            try:
                color = await commands.ColorConverter().convert(inter, color)
            except:
                color = None

        else:
            color = discord.Color.default()

        emb = discord.Embed(color=color)

        if title is not None:
            emb.title = title

        if description is not None:
            emb.description = description

        if picture is not None:
            emb.set_image(url=picture)

        await inter.respond(embed=emb)


def setup(pybot):
    pybot.add_cog(SlashEmbed(pybot))

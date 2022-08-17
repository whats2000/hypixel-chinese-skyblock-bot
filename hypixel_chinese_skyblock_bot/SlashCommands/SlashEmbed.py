import discord
from discord.ext import commands
from dislash import slash_command, OptionType
from dislash.slash_commands import Option

from hypixel_chinese_skyblock_bot.Core.Common import CodExtension, get_setting_json


class SlashEmbed(CodExtension):
    @slash_command(
        guild_ids=[int(get_setting_json('ServerId'))],
        name='embed',
        description='Build a embed',
        options=[
            Option(name='title', description='Makes the title of the embed', type=OptionType.STRING),
            Option(name='description', description='Makes the description', type=OptionType.STRING),
            Option(name='color', description='The color of the embed', type=OptionType.STRING),
            Option(name='picture', description='The picture of the embed', type=OptionType.STRING)
        ]
    )
    async def embed(self, inter, title=None, description=None, color=None, picture=None):
        if color is not None:
            try:
                color = await commands.ColorConverter().convert(inter, color)
            except KeyError:
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

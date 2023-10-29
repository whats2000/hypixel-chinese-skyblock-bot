import json
import logging
import os
import re

import disnake
from disnake.ext import commands

from CoreFunction.Common import CodExtension, get_setting_json, add_role, remove_role
from CoreFunction.Logger import Logger
from CoreFunction.SendEmbed import set_inter_embed_author

bot_logger = Logger(__name__)


class RoleButton(disnake.ui.Button):
    async def callback(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer(ephemeral=True)

        bot_logger.log_message(logging.INFO, f'變更身分組 : {inter.author.name}')

        role_id = int(self.custom_id.replace("reaction_role_", ""))
        mention_role = disnake.utils.get(inter.guild.roles, id=role_id)

        if role_id not in [y.id for y in inter.author.roles]:
            await add_role(ctx=inter, role_id=role_id)

            bot_logger.log_message(logging.ERROR, f'成功新增 {self.emoji}')

            embed = disnake.Embed(
                title=f'變更稱號完成',
                description=f'成功新增 {self.emoji} {mention_role.mention}',
                color=0x00ff00
            )
        else:
            await remove_role(ctx=inter, role_id=role_id)

            bot_logger.log_message(logging.ERROR, f'成功移除 {self.emoji}')

            embed = disnake.Embed(
                title=f'變更稱號完成',
                description=f'成功移除 {self.emoji} {mention_role.mention}',
                color=0xe74c3c
            )

        set_inter_embed_author(embed, inter)

        await inter.send(embed=embed, ephemeral=True)


class RoleButtonView(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)


class SlashBuildReactionRole(CodExtension):

    def __init__(self, bot):
        super().__init__(bot)
        self.has_run_startup = False

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.has_run_startup:
            self.has_run_startup = True
            await self.reload_reaction_roles()

    @commands.has_any_role(get_setting_json('AdminRole'))
    @commands.slash_command(
        guild_ids=[int(get_setting_json('ServerId'))],
        name='send_embed',
        description='Send an already built embed'
    )
    async def send_built_embed(self, inter: disnake.AppCommandInteraction,
                               embed_name: str = commands.Param(
                                   description='Input the store embed name')
                               ):
        await inter.response.defer(ephemeral=True)

        with open(f'ReactionRoleEmbed/{embed_name}.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        button_view = RoleButtonView()

        for embed in data["embeds"]:
            embed["color"] = int(embed["color"].lstrip("#"), 16)
            embed["description"] = "\n".join(embed["description"])

            for field in embed["fields"]:
                field["value"] = "\n".join(field["value"])

                matches = re.findall(r"<:([^:]+):(\d+)> - <@&(\d+)>", field["value"])
                for emoji_name, emoji_id, role_id in matches:
                    emoji = disnake.PartialEmoji(name=emoji_name, id=int(emoji_id))
                    role = inter.guild.get_role(int(role_id))

                    button = RoleButton(
                        style=disnake.ButtonStyle.secondary,
                        label=role.name,
                        emoji=emoji,
                        custom_id=f"reaction_role_{role_id}",
                    )
                    button_view.add_item(button)

            await inter.channel.send(embed=disnake.Embed.from_dict(embed), view=button_view)

        await inter.edit_original_message('Done!')

    async def reload_reaction_roles(self):
        bot_logger.log_message(logging.INFO, f'Reactivating reaction role embed: System')

        folder_path = 'ReactionRoleEmbed/'

        file_names = [file_name for file_name in os.listdir(folder_path) if file_name.endswith('.json')]

        for file_name in file_names:
            bot_logger.log_message(logging.DEBUG, f'Setup > ReactionRoleEmbed.{file_name[:-5]}')

            with open(folder_path + file_name, "r", encoding="utf-8") as file:
                data = json.load(file)

                message_id = data["message_id"]
                channel_id = data["channel"]

                channel = await self.bot.fetch_channel(channel_id)
                message = await channel.fetch_message(message_id)

                view = RoleButtonView()

                for embed in data["embeds"]:
                    embed["color"] = int(embed["color"].lstrip("#"), 16)
                    embed["description"] = "\n".join(embed["description"])

                    for field in embed["fields"]:
                        field["value"] = "\n".join(field["value"])

                        matches = re.findall(r"<:([^:]+):(\d+)> - <@&(\d+)>", field["value"])
                        for emoji_name, emoji_id, role_id in matches:
                            emoji = disnake.PartialEmoji(name=emoji_name, id=int(emoji_id))
                            role = self.bot.guilds[0].get_role(int(role_id))

                            button = RoleButton(
                                style=disnake.ButtonStyle.secondary,
                                label=role.name,
                                emoji=emoji,
                                custom_id=f"reaction_role_{role_id}",
                            )
                            view.add_item(button)

                await message.edit(view=view)


def setup(pybot):
    pybot.add_cog(SlashBuildReactionRole(pybot))

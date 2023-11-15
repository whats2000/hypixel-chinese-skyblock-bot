import disnake
import logging

from disnake.ext import commands

from CoreFunction.Common import get_setting_json, CodExtension, add_role, remove_role
from CoreFunction.Logger import Logger

bot_logger = Logger(__name__)


class RoleAssigner(CodExtension):
    @commands.has_any_role(get_setting_json('AdminRole'))
    @commands.user_command(name="讓 TA 冷靜一下")  # Assign role
    async def assign_role(self, inter: disnake.ApplicationCommandInteraction, user: disnake.User):
        bot_logger.log_message(logging.INFO, f'Add Calm Down role to User : {inter.channel.name} | {inter.author.name}')

        role_to_assign_id = 1174176502217199687

        # Find the role in the guild
        role = inter.guild.get_role(role_to_assign_id)
        if not role:
            await inter.response.send_message(f"Role with ID `{role_to_assign_id}` not found.", ephemeral=True)
            return

        member = inter.guild.get_member(user.id)
        if not member:
            try:
                member = await inter.guild.fetch_member(user.id)
            except disnake.Forbidden:
                await inter.response.send_message("User not found in this guild.", ephemeral=True)
                return

        # Assign the role
        await member.add_roles(role)
        await inter.response.send_message(f"Assigned role to {user.mention}.", ephemeral=True)

    @commands.has_any_role(get_setting_json('AdminRole'))
    @commands.user_command(name="讓 TA 自由")  # Remove role
    async def remove_role_command(self, inter: disnake.ApplicationCommandInteraction, user: disnake.User):
        bot_logger.log_message(logging.INFO, f'Remove Calm Down role from User : {inter.channel.name} | {inter.author.name}')

        role_to_remove_id = 1174176502217199687

        # Find the role in the guild
        role = inter.guild.get_role(role_to_remove_id)
        if not role:
            await inter.response.send_message(f"Role with ID `{role_to_remove_id}` not found.", ephemeral=True)
            return

        member = inter.guild.get_member(user.id)
        if not member:
            try:
                member = await inter.guild.fetch_member(user.id)
            except disnake.Forbidden:
                await inter.response.send_message("User not found in this guild.", ephemeral=True)
                return

        # Assign the role
        await member.remove_roles(role)
        await inter.response.send_message(f"Removed role from {user.mention}.", ephemeral=True)


def setup(pybot):
    pybot.add_cog(RoleAssigner(pybot))

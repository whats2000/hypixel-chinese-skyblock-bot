import logging
import disnake
from disnake.ext import commands
from CoreFunction.Common import CodExtension, get_setting_json
from CoreFunction.Logger import Logger
from CoreFunction.SendEmbed import set_inter_embed_author

bot_logger = Logger(__name__)


class SlashLockDownChannel(CodExtension):

    @commands.has_any_role(get_setting_json('AdminRole'))
    @commands.slash_command(
        guild_ids=[int(get_setting_json('ServerId'))],
        name='lock',
        description='Lock down current channel'
    )
    async def lock_channel(self, inter: disnake.AppCommandInteraction):
        await inter.response.defer(ephemeral=True)

        bot_logger.log_message(logging.INFO, f'鎖定頻道 : {inter.channel.name} | {inter.author.name}')

        channel = inter.channel

        # Check if the channel is already locked
        if channel.overwrites_for(channel.guild.default_role).send_messages is False:
            await inter.edit_original_message("This channel is already locked.")
            return

        allowed_roles = get_setting_json('LockDownAllowRole')
        disallowed_role = get_setting_json('LockDownDisallowedRole')

        # Lock the channel by denying send_messages for @everyone role
        overwrites = channel.overwrites_for(channel.guild.default_role)
        overwrites.send_messages = False
        await channel.set_permissions(channel.guild.default_role, overwrite=overwrites)

        # Allow specified roles to send messages
        for role in channel.guild.roles:
            if role.name in allowed_roles or role.id in allowed_roles:
                overwrites = channel.overwrites_for(role)
                overwrites.send_messages = True
                await channel.set_permissions(role, overwrite=overwrites)

        # Disallow the specified roles and mute members with that role
        for role in channel.guild.roles:
            if role.name in disallowed_role or role.id in disallowed_role:
                overwrites = channel.overwrites_for(role)
                overwrites.send_messages = False
                await channel.set_permissions(role, overwrite=overwrites)

        await inter.edit_original_message("Done!")

        # Create an embed to inform players about the channel lock
        embed = disnake.Embed(
            title='Channel Locked',
            description='This channel has been locked. Only specified roles can send messages. Members with the '
                        'specified disallowed role are muted.',
            color=0x3498db
        )

        # Set the author of the embed
        set_inter_embed_author(embed, inter)

        # Send the embed to the channel
        await channel.send(embed=embed)


def setup(pybot):
    pybot.add_cog(SlashLockDownChannel(pybot))

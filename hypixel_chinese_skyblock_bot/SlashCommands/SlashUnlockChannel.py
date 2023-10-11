import logging

import disnake
from disnake.ext import commands
from CoreFunction.Common import CodExtension, get_setting_json
from CoreFunction.Logger import Logger
from CoreFunction.SendEmbed import set_inter_embed_author

bot_logger = Logger(__name__)


class SlashUnlockChannel(CodExtension):

    @commands.has_any_role(get_setting_json('AdminRole'))
    @commands.slash_command(
        guild_ids=[int(get_setting_json('ServerId'))],
        name='unlock',
        description='Unlock a locked channel'
    )
    async def unlock_channel(self, inter: disnake.AppCommandInteraction):
        await inter.response.defer(ephemeral=True)

        bot_logger.log_message(logging.INFO, f'解鎖頻道: {inter.channel.name} | {inter.author.name}')

        channel = inter.channel

        # Check if the channel is locked (i.e., send_messages for @everyone role is False)
        if channel.overwrites_for(channel.guild.default_role).send_messages is True:
            await inter.edit_original_message("This channel is not locked.")
            return

        disallowed_role = get_setting_json('LockDownDisallowedRole')

        # Reset channel permissions to allow @everyone to send messages and members with the disallowed role
        overwrites = channel.overwrites_for(channel.guild.default_role)
        overwrites.send_messages = True
        await channel.set_permissions(channel.guild.default_role, overwrite=overwrites)

        # Allow members with the disallowed role to send messages
        for role in channel.guild.roles:
            if role.name in disallowed_role or role.id in disallowed_role:
                overwrites = channel.overwrites_for(role)
                overwrites.send_messages = True
                await channel.set_permissions(role, overwrite=overwrites)

        await inter.edit_original_message("Done!")

        # Create an embed to inform players about the channel lock
        embed = disnake.Embed(
            title='Channel Unlocked',
            description='The channel has been unlocked.',
            color=0x3498db
        )

        # Set the author of the embed
        set_inter_embed_author(embed, inter)

        # Send the embed to the channel
        await channel.send(embed=embed)


def setup(pybot):
    pybot.add_cog(SlashUnlockChannel(pybot))

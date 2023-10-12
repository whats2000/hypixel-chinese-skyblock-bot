import logging

import disnake
from disnake.ext import commands
from CoreFunction.Common import CodExtension, get_setting_json, update_setting_json
from CoreFunction.Logger import Logger

bot_logger = Logger(__name__)


class SlashAutoCleanUpChannel(CodExtension):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Load cleanup settings from JSON data
        self.clean_time = get_setting_json('AutoCleanUpChannelDeleteTime')
        self.cleanup_channels = get_setting_json('AutoCleanUpChannel')
        self.allowed_roles = get_setting_json('AutoCleanUpAllowedRoles')

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        # Check if the message is in a channel with auto cleanup enabled
        if message.channel.id not in self.cleanup_channels:
            return

        # Check if the author has any allowed roles, if so, skip deletion
        if any(role.id in [allowed_role_id for allowed_role_id in self.allowed_roles] for role in
               message.author.roles):
            bot_logger.log_message(logging.INFO, f'Admin by pass : {message.content} | {message.author}')
            return

        # Retrieve the cleanup time for the specific channel
        cleanup_time = self.clean_time.get(f'{message.channel.id}', 10)

        # Ensure negative cleanup times are not processed
        if cleanup_time < 0:
            return

        bot_logger.log_message(logging.INFO, f'Delete Message : {message.content} | {message.author}')

        await message.delete(delay=cleanup_time)

    @commands.has_any_role(get_setting_json('AdminRole'))
    @commands.slash_command(
        guild_ids=[int(get_setting_json('ServerId'))],
        name='auto_clean',
        description='Change the channel to auto clean up messages after a few seconds'
    )
    async def auto_clean_channel(self,
                                 inter: disnake.AppCommandInteraction,
                                 channel: disnake.TextChannel = commands.Param(
                                     description='The channel to enable auto cleanup for'),
                                 clean_time: int = commands.Param(
                                     description='Seconds to wait before deleting messages, set to -1 to disable',
                                     default=10)):

        await inter.response.defer(ephemeral=True)

        # Add the channel to the list of channels with auto cleanup
        self.cleanup_channels.append(channel.id)
        update_setting_json('AutoCleanUpChannel', self.cleanup_channels)

        # Set the cleanup time for the specific channel
        self.clean_time[channel.id] = clean_time
        update_setting_json('AutoCleanUpChannelDeleteTime', self.clean_time)

        await inter.edit_original_message(
            f"Auto message cleanup enabled for {channel.mention}. Messages will be deleted after {clean_time} seconds.")


def setup(pybot):
    pybot.add_cog(SlashAutoCleanUpChannel(pybot))

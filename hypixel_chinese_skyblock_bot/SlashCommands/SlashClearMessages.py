import logging
import disnake
from disnake import NotFound
from disnake.ext import commands

from CoreFunction.Common import CodExtension, get_setting_json
from CoreFunction.Logger import Logger

bot_logger = Logger(__name__)


class SlashClearMessage(CodExtension):

    @commands.has_any_role(get_setting_json('AdminRole'))
    @commands.slash_command(
        guild_ids=[int(get_setting_json('ServerId'))],
        name='clear_message',
        description='Remove messages starting from the specified message ID',
    )
    async def clear_message(self,
                            inter: disnake.AppCommandInteraction,
                            message_id: str = commands.Param(
                                description='The required message ID to start clearing from'),
                            limit: int = commands.Param(description='The number of messages to clear (1-100)',
                                                        default=100)
                            ):
        if limit < 1 or limit > 100:
            await inter.response.send_message("The 'limit' parameter must be between 1 and 100.", ephemeral=True)
            return

        await inter.response.defer(ephemeral=True)

        bot_logger.log_message(logging.INFO, f'刪除信息 : {inter.channel.name} | {inter.author.name}')

        try:
            message_id = int(message_id)
            channel = inter.channel
            messages_to_clear = 0

            try:
                target_message = await channel.fetch_message(message_id)

                if target_message:
                    await inter.edit_original_message('Start Cleaning Message!')

                    async for message in channel.history(limit=None):
                        if message.id == message_id or messages_to_clear >= limit:
                            await inter.edit_original_message("Done!")
                            return
                        else:
                            await message.delete()
                            messages_to_clear += 1
            except NotFound:
                bot_logger.log_message(logging.ERROR, f'NotFound 信息 ID 找不到')
                await inter.edit_original_message("The specified message ID was not found.")

        except ValueError:
            bot_logger.log_message(logging.ERROR, f'ValueError 信息 ID 找不到')
            await inter.edit_original_message("Invalid message ID. Please provide a valid message ID.")


def setup(pybot):
    pybot.add_cog(SlashClearMessage(pybot))

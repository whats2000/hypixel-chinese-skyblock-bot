import logging
import os

import disnake
from disnake.ext import commands

from CoreFunction.Common import get_setting_json
from CoreFunction.Logger import Logger
from SlashCommands.SlashVerifyTitle import TitleDropdownView

intents_setting = disnake.Intents.default()
intents_setting.message_content = True

pybot = commands.Bot(command_prefix='sb?', intents=intents_setting)
pybot.remove_command('help')

bot_logger = Logger(__name__)


@pybot.event
async def on_ready():
    view = TitleDropdownView()

    message = await pybot.get_channel(1068042509508427807).fetch_message(1113127365971808277)

    await message.edit(view=view)

    bot_logger.log_message(logging.INFO, 'Bot is ready')


for filename in os.listdir(f'{os.getcwd()}/Commands'):
    if not filename.endswith('.py'):
        continue

    bot_logger.log_message(logging.DEBUG, f'Setup > Commands.{filename[:-3]}')

    pybot.load_extension(f'Commands.{filename[:-3]}')

for filename in os.listdir(f'{os.getcwd()}/SlashCommands'):
    if not filename.endswith('.py'):
        continue

    bot_logger.log_message(logging.DEBUG, f'Setup > SlashCommands.{filename[:-3]}')

    pybot.load_extension(f'SlashCommands.{filename[:-3]}')

if __name__ == '__main__':
    pybot.run((get_setting_json('Token')))

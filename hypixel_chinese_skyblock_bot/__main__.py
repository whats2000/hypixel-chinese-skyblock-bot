import logging
import os

import disnake
from disnake.ext import commands

from CoreFunction.Logger import Logger

intents_setting = disnake.Intents.default()
intents_setting.message_content = True

pybot = commands.Bot(command_prefix="sb?", intents=intents_setting)
pybot.remove_command("help")

bot_logger = Logger(__name__)


@pybot.event
async def on_ready():
    bot_logger.log_message(logging.INFO, "Bot is ready")


for filename in os.listdir("Commands"):
    if not filename.endswith(".py"):
        continue

    bot_logger.log_message(logging.DEBUG, f"Setup > Commands.{filename[:-3]}")

    pybot.load_extension(f"Commands.{filename[:-3]}")

for filename in os.listdir("SlashCommands"):
    if not filename.endswith(".py"):
        continue

    bot_logger.log_message(logging.DEBUG, f"Setup > SlashCommands.{filename[:-3]}")

    pybot.load_extension(f"SlashCommands.{filename[:-3]}")

for filename in os.listdir("UserCommands"):
    if not filename.endswith(".py"):
        continue

    bot_logger.log_message(logging.DEBUG, f"Setup > UserCommands.{filename[:-3]}")

    pybot.load_extension(f"UserCommands.{filename[:-3]}")

for filename in os.listdir("MessageCommand"):
    if not filename.endswith(".py"):
        continue

    bot_logger.log_message(logging.DEBUG, f"Setup > MessageCommand.{filename[:-3]}")

    pybot.load_extension(f"MessageCommand.{filename[:-3]}")

if __name__ == "__main__":
    pybot.run(os.getenv("TOKEN"))

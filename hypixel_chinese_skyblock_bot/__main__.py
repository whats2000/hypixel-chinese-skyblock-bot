import os
from discord.ext import commands
from dislash import InteractionClient
from hypixel_chinese_skyblock_bot.Core.Common import get_setting_json

pybot = commands.Bot(
    command_prefix='sb?',
    help_command=None
)


@pybot.event
async def on_ready():
    print("bot is ready")


for filename in os.listdir(os.getcwd() + '/Commands'):
    if not filename.endswith('.py'):
        continue

    print('Setup > Commands.' + filename[:-3])

    pybot.load_extension('Commands.' + filename[:-3])

for filename in os.listdir(os.getcwd() + '/SlashCommands'):
    if not filename.endswith('.py'):
        continue

    print('Setup > SlashCommands.' + filename[:-3])

    pybot.load_extension('SlashCommands.' + filename[:-3])


inter_client = InteractionClient(pybot)


if __name__ == '__main__':
    pybot.run((get_setting_json('Token')))

import json
import os
from discord.ext import commands
from dislash import InteractionClient

with open(os.getcwd()
          + '/Resources/Setting.json',
          mode='r',
          encoding='utf8'
          ) as settingJson:
    settingJsonData = json.load(settingJson)
settingJson.close()

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

    print('Commands.' + filename[:-3])

    pybot.load_extension('Commands.' + filename[:-3])

for filename in os.listdir(os.getcwd() + '/SlashCommands'):
    if not filename.endswith('.py'):
        continue

    print('SlashCommands.' + filename[:-3])

    pybot.load_extension('SlashCommands.' + filename[:-3])


inter_client = InteractionClient(pybot)


if __name__ == '__main__':
    pybot.run(settingJsonData['Token'])

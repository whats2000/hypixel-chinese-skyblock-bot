import json
import os
from discord.ext import commands

with open(os.getcwd()
          + '/Resources/Setting.json',
          mode='r',
          encoding='utf8'
          ) as settingJson:
    settingJsonData = json.load(settingJson)
settingJson.close()

pybot = commands.Bot(command_prefix='sb?')


@pybot.event
async def on_ready():
    print("bot is ready")

for filename in os.listdir(os.getcwd() + '/Commands'):
    print('Commands.'+filename[:-3])

    if not filename.endswith('.py'):
        continue

    pybot.load_extension('Commands.'+filename[:-3])

if __name__ == '__main__':
    pybot.run(settingJsonData['Token'])

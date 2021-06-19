import json
import os
from discord.ext import commands

with open(os.getcwd() + '/Resources/Setting.json', mode='r',
          encoding='utf8') as Setting_Json:
    Setting_Json_data = json.load(Setting_Json)

pybot = commands.Bot(command_prefix='sb?')


@pybot.event
async def on_ready():
    print("debug code 0")

for filename in os.listdir(os.getcwd() + '/Commands'):
    print('Commands.'+filename[:-3])
    if not filename.endswith('.py'):
        continue
    pybot.load_extension('Commands.'+filename[:-3])

if __name__ == '__main__':
    pybot.run(Setting_Json_data['token'])

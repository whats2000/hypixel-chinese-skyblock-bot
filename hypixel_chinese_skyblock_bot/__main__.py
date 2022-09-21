import os
import disnake
from disnake.ext import commands
from hypixel_chinese_skyblock_bot.Core.Common import get_setting_json

intents_setting = disnake.Intents.default()
intents_setting.message_content = True

pybot = commands.Bot(command_prefix='sb?', intents=intents_setting)
pybot.remove_command('help')


@pybot.event
async def on_ready():
    print('Info > bot is ready')


for filename in os.listdir(f'{os.getcwd()}/Commands'):
    if not filename.endswith('.py'):
        continue

    print(f'Setup > Commands.{filename[:-3]}')

    pybot.load_extension(f'Commands.{filename[:-3]}')

for filename in os.listdir(f'{os.getcwd()}/SlashCommands'):
    if not filename.endswith('.py'):
        continue

    print(f'Setup > SlashCommands.{filename[:-3]}')

    pybot.load_extension(f'SlashCommands.{filename[:-3]}')

if __name__ == '__main__':
    pybot.run((get_setting_json('Token')))

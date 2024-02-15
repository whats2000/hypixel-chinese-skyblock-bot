import json
import logging
import os
import re
from collections import OrderedDict
from typing import Union

import discord
import disnake
import requests
from disnake.ext import commands

from CoreFunction.Logger import Logger

bot_logger = Logger(__name__)

unique_names = set()


class CodExtension(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot


def set_user_id(user: str, name: str):
    with open(f'Resources/VerifyIdList.json',
              mode='r',
              encoding='utf8'
              ) as verify_id_list_json:
        data = json.load(verify_id_list_json)

    verify_id_list_json.close()

    output = data

    output[str(user)] = str(name)

    output = json.dumps(output, ensure_ascii=False, indent=4)

    with open(f'Resources/VerifyIdList.json',
              mode='w',
              encoding='utf8'
              ) as out_json:
        out_json.write(output)

    out_json.close()


def remove_minecraft_color_codes(text):
    # Remove any color codes
    text = re.sub(r'%%.*?%%', '', text)
    # Remove any formatting minecraft color codes
    return re.sub(r'\u00a7[a-fA-F0-9rR]', '', text)


def get_skyblock_name():
    return unique_names


def update_skyblock_name():
    with open('Resources/SkyblockName.json', 'r') as json_file:
        data = json.load(json_file)

        for item_id, item in data.items():
            if isinstance(item, dict):
                unique_names.add(item.get('name', '').lower())

    json_file.close()

    with open('Resources/SkyblockNameExtra.json', 'r') as json_file:
        data = json.load(json_file)

        for item in data['unique_names']:
            unique_names.add(item)

    json_file.close()


def get_setting_json(key: str):
    key = str(key)

    if key in setting_json_data:
        return setting_json_data[key]

    else:
        bot_logger.log_message(logging.ERROR, '無效的 json key 名稱')
        raise NameError('Invalid Key')


def update_setting_json(key: str, value):
    key = str(key)

    # Check if the key already exists in the setting_json_data
    if key in setting_json_data:
        setting_json_data[key] = value
        # Optionally, save the updated JSON data to a file or database here if needed.
        # Save the updated JSON data to the file
        with open('Resources/Setting.json', 'w') as json_file:
            json.dump(setting_json_data, json_file, indent=2)
    else:
        bot_logger.log_message(logging.ERROR, '無效的 json key 名稱')
        raise NameError('Invalid Key')


def get_verify_id_list(key: str):
    with open(f'Resources/VerifyIdList.json',
              mode='r',
              encoding='utf8'
              ) as verify_id_list_json:
        data = json.load(verify_id_list_json)

        verify_id_list_json.close()

    key = str(key)

    if key in data:
        return data[key]

    else:
        bot_logger.log_message(logging.ERROR, 'VerifyIdList.json 找不到該玩家')

        return ''


def get_hypixel_skyblock_items():
    url = "https://api.hypixel.net/resources/skyblock/items"
    response = requests.get(url)
    data = response.json()

    if data["success"]:
        item_list = {}
        for item in data["items"]:
            item_id = item["id"]

            item_name = item["name"]

            item_name = remove_minecraft_color_codes(item_name)

            item_list[item_id] = {"name": item_name}

        sorted_items = OrderedDict(sorted(item_list.items(), key=lambda x: x[0]))

        with open("Resources/SkyblockName.json", "w") as file:
            json.dump(sorted_items, file, indent=4)

        update_skyblock_name()

        return True
    else:
        return False


def get_hypixel_api(name: str):
    if name != '':
        if re.match(r'^[a-zA-Z0-9_]+$', name):
            url = f'{setting_json_data["NameLink"]}?name={name}'
            headers = {
                'API-Key': os.getenv("API_KEY")
            }

            js = requests.get(url, headers=headers)

            return js.json()
        else:
            bot_logger.log_message(logging.ERROR, '無效的玩家 ID')
            return {'success': False}
    else:
        bot_logger.log_message(logging.ERROR, f'缺失玩家 id')

        return {'success': False}


def get_hypixel_skyblock_api(profile: str):
    bot_logger.log_message(logging.INFO, f'嘗試獲取 {profile} 的 hypixel skyblock API')

    url = f'{setting_json_data["SkyblockLink"]}?profile={profile}'
    headers = {
        'API-Key': os.getenv("API_KEY")
    }

    js = requests.get(url, headers=headers)

    return js.json()


def get_senither_weight(profile: str):
    bot_logger.log_message(logging.INFO, f'嘗試獲取 {profile} 的 senither weight API')

    js = requests.get(f'{setting_json_data["SenitherLink"]}{profile}/weight?key={os.getenv("API_KEY")}')

    return js.json()


def get_role_name(ctx: Union[commands.Context, disnake.AppCommandInteraction], role_id: str):
    role = discord.utils.get(ctx.author.guild.roles, id=role_id)
    return role.name


async def add_role(ctx: Union[commands.Context, disnake.AppCommandInteraction, disnake.MessageInteraction],
                   get_role_id: str = None,
                   role_names: str = None,
                   role_id: int = None):
    if get_role_id is not None:
        role = discord.utils.get(ctx.author.guild.roles, id=get_setting_json(get_role_id))
    elif role_names is not None:
        role = discord.utils.get(ctx.author.guild.roles, name=role_names)
    elif role_id is not None:
        role = discord.utils.get(ctx.author.guild.roles, id=role_id)
    else:
        bot_logger.log_message(logging.ERROR, f'缺失 function 變數')
        raise TypeError

    await ctx.author.add_roles(role)


async def remove_role(ctx: Union[commands.Context, disnake.AppCommandInteraction, disnake.MessageInteraction],
                      get_role_id: str = None,
                      get_role_names: str = None,
                      role_id: int = None):
    if get_role_id is not None:
        role = discord.utils.get(ctx.author.guild.roles, id=get_setting_json(get_role_id))
    elif get_role_names is not None:
        role = discord.utils.get(ctx.author.guild.roles, name=get_role_names)
    elif role_id is not None:
        role = discord.utils.get(ctx.author.guild.roles, id=role_id)
    else:
        bot_logger.log_message(logging.ERROR, f'缺失 function 變數')
        raise TypeError

    await ctx.author.remove_roles(role)


def read_json(filename):
    if not os.path.exists(filename):
        return {}
    try:
        with open('Resources/Giveaway.json', 'r') as file:
            content = file.read()
            if not content:
                return {}
            else:
                return json.loads(content)

    except FileNotFoundError:
        bot_logger.log_message(logging.ERROR, f"File not found: {filename}")
        return {}
    except json.JSONDecodeError as e:
        bot_logger.log_message(logging.ERROR, f"JSON decode error: {e}")
        return {}


def write_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


with open(f'Resources/Setting.json',
          mode='r',
          encoding='utf8'
          ) as setting_json:
    setting_json_data = json.load(setting_json)

setting_json.close()

update_skyblock_name()

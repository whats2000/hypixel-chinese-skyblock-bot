import json
import logging
import os

import discord
import requests
from disnake.ext import commands

from hypixel_chinese_skyblock_bot.Core.Logger import Logger


class CodExtension(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


bot_logger = Logger(__name__)


def set_user_id(user, name):
    with open(f'{os.getcwd()}/Resources/VerifyIdList.json',
              mode='r',
              encoding='utf8'
              ) as verify_id_list_json:
        data = json.load(verify_id_list_json)

    verify_id_list_json.close()

    output = data

    output[str(user)] = str(name)

    output = json.dumps(output, ensure_ascii=False, indent=4)

    with open(f'{os.getcwd()}/Resources/VerifyIdList.json',
              mode='w',
              encoding='utf8'
              ) as out_json:
        out_json.write(output)

    out_json.close()


def get_setting_json(key):
    key = str(key)

    if key in setting_json_data:
        return setting_json_data[key]

    else:
        bot_logger.log_message(logging.ERROR, '無效的 json key 名稱')
        raise NameError('Invalid Key')


def get_verify_id_list(key):
    with open(f'{os.getcwd()}/Resources/VerifyIdList.json',
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


def get_hypixel_api(name):
    if name != '':
        bot_logger.log_message(logging.INFO, f'嘗試獲取 {name} 的 hypixel API')

        js = requests.get(f'{setting_json_data["NameLink"]}{setting_json_data["ApiKey"]}&name={name}')

        return js.json()
    else:
        bot_logger.log_message(logging.ERROR, f'缺失玩家 id')

        return {'success': False}


def get_hypixel_skyblock_api(profile):
    bot_logger.log_message(logging.INFO, f'嘗試獲取 {profile} 的 hypixel skyblock API')

    js = requests.get(f'{setting_json_data["SkyblockLink"]}{setting_json_data["ApiKey"]}&profile={profile}')

    return js.json()


def get_senither_weight(profile):
    bot_logger.log_message(logging.INFO, f'嘗試獲取 {profile} 的 senither weight API')

    js = requests.get(f'{setting_json_data["SenitherLink"]}{profile}/weight?key={setting_json_data["ApiKey"]}')

    return js.json()


def get_role_name(ctx, role_id):
    role = discord.utils.get(ctx.author.guild.roles, id=role_id)
    return role.name


async def add_role(ctx, get_role_id=None, get_role_names=None):
    if get_role_id is not None:
        role = discord.utils.get(ctx.author.guild.roles, id=get_setting_json(get_role_id))
    elif get_role_names is not None:
        role = discord.utils.get(ctx.author.guild.roles, name=get_role_names)
    else:
        bot_logger.log_message(logging.ERROR, f'缺失 function 變數')
        raise TypeError

    await ctx.author.add_roles(role)


async def remove_role(ctx, get_role_id=None, get_role_names=None):
    if get_role_id is not None:
        role = discord.utils.get(ctx.author.guild.roles, id=get_setting_json(get_role_id))
    elif get_role_names is not None:
        role = discord.utils.get(ctx.author.guild.roles, name=get_role_names)
    else:
        bot_logger.log_message(logging.ERROR, f'缺失 function 變數')
        raise TypeError

    await ctx.author.remove_roles(role)


with open(f'{os.getcwd()}/Resources/Setting.json',
          mode='r',
          encoding='utf8'
          ) as setting_json:
    setting_json_data = json.load(setting_json)

setting_json.close()

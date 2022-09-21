import json
import os

import discord
import requests
from disnake.ext import commands


class CodExtension(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


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
        print('Error > player no found')

        return ''


def get_hypixel_api(name):
    if name != '':
        print(f'Info > try to get hypixel api of {name}')

        js = requests.get(f'{setting_json_data["NameLink"]}{setting_json_data["ApiKey"]}&name={name}')

        return js.json()
    else:
        print('Error > id is missing')

        return {'success': False}


def get_hypixel_skyblock_api(profile):
    print(f'Info > try to get hypixel skyblock api of {profile}')

    js = requests.get(f'{setting_json_data["SkyblockLink"]}{setting_json_data["ApiKey"]}&profile={profile}')

    return js.json()


def get_senither_weight(profile):
    print(f'Info > try to get senither weight api of {profile}')

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
        raise ValueError

    await ctx.author.add_roles(role)


async def remove_role(ctx, get_role_id=None, get_role_names=None):
    if get_role_id is not None:
        role = discord.utils.get(ctx.author.guild.roles, id=get_setting_json(get_role_id))
    elif get_role_names is not None:
        role = discord.utils.get(ctx.author.guild.roles, name=get_role_names)
    else:
        raise ValueError

    await ctx.author.remove_roles(role)


with open(f'{os.getcwd()}/Resources/Setting.json',
          mode='r',
          encoding='utf8'
          ) as setting_json:
    setting_json_data = json.load(setting_json)

setting_json.close()

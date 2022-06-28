import json
import os

import requests
from discord.ext import commands


class CodExtension(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


def set_user_id(user, name):
    with open(os.getcwd()
              + '/Resources/VerifyIdList.json',
              mode='r',
              encoding='utf8'
              ) as verify_id_list_json:
        data = json.load(verify_id_list_json)

    verify_id_list_json.close()

    output = data

    output[str(user)] = str(name)

    output = json.dumps(output, ensure_ascii=False, indent=4)

    with open(os.getcwd()
              + '/Resources/VerifyIdList.json',
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
        raise NameError("Invalid Key")


def get_verify_id_list(key):
    with open(os.getcwd()
              + '/Resources/VerifyIdList.json',
              mode='r',
              encoding='utf8'
              ) as verify_id_list_json:
        data = json.load(verify_id_list_json)

        verify_id_list_json.close()

    key = str(key)

    if key in data:
        return data[key]

    else:
        print('player no found')

        return ''


def get_hypixel_api(name):
    if name != '':
        print('> try to get hypixel api of ' + name)

        js = requests.get(setting_json_data['NameLink']
                          + setting_json_data['ApiKey']
                          + '&name=' + name
                          )

        return js.json()
    else:
        print('id is missing')

        return {'success': False}


def get_hypixel_skyblock_api(profile):
    print('> try to get hypixel skyblock api of ' + profile)

    js = requests.get(setting_json_data['SkyblockLink']
                      + setting_json_data['ApiKey']
                      + '&profile=' + profile
                      )

    return js.json()


def get_senither_weight(profile):
    print('> try to get senither weight api of ' + profile)

    js = requests.get(setting_json_data['SenitherLink']
                      + profile
                      + '/weight?key='
                      + setting_json_data['ApiKey']
                      )

    return js.json()


with open(os.getcwd()
          + '/Resources/Setting.json',
          mode='r',
          encoding='utf8'
          ) as setting_json:
    setting_json_data = json.load(setting_json)

setting_json.close()

import json
import os

import requests
from discord.ext import commands


class CodExtension(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


def set_user_id(user, id):
    with open(os.getcwd()
              + '/Resources/VerifyIdList.json',
              mode='r',
              encoding='utf8'
              ) as verifyIdListJson:
        verifyIdListJsonData = json.load(verifyIdListJson)

    verifyIdListJson.close()

    outputJson = verifyIdListJsonData

    outputJson[str(user)] = str(id)

    outputJson = json.dumps(outputJson, ensure_ascii=False, indent=4)

    with open(os.getcwd()
              + '/Resources/VerifyIdList.json',
              mode='w',
              encoding='utf8'
              ) as outJson:
        outJson.write(outputJson)

    outJson.close()


def get_setting_json(key):
    key = str(key)

    if key in settingJsonData:
        return settingJsonData[key]

    else:
        raise NameError("Invalid Key")


def get_verify_id_list(key):
    with open(os.getcwd()
              + '/Resources/VerifyIdList.json',
              mode='r',
              encoding='utf8'
              ) as verifyIdListJson:
        verifyIdListJsonData = json.load(verifyIdListJson)

        verifyIdListJson.close()

    key = str(key)

    if key in verifyIdListJsonData:
        return verifyIdListJsonData[key]

    else:
        print('player no found')

        return ''


def get_hypixel_api(name):
    print('> try to get hypixel api of ' + name)

    js = requests.get(settingJsonData['NameLink']
                      + settingJsonData['ApiKey']
                      + '&name=' + name
                      )

    return js.json()


def get_hypixel_skyblock_api(profile):
    print('> try to get hypixel skyblock api of ' + profile)

    js = requests.get(settingJsonData['SkyblockLink']
                      + settingJsonData['ApiKey']
                      + '&profile=' + profile
                      )

    return js.json()


with open(os.getcwd()
          + '/Resources/Setting.json',
          mode='r',
          encoding='utf8'
          ) as settingJson:
    settingJsonData = json.load(settingJson)

settingJson.close()

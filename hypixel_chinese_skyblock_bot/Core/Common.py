import json
import os
import requests
from discord.ext import commands


class Cod_Extension(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


def get_setting_json(key):
    return settingJsonData[key]


def get_hypixel_api(name):
    js = requests.get(settingJsonData['NameLink']
                      + settingJsonData['ApiKey']
                      + '&name=' + name
                      )

    return js.json()


with open(os.getcwd()
          + '/Resources/Setting.json',
          mode='r',
          encoding='utf8'
          ) as settingJson:
    settingJsonData = json.load(settingJson)

settingJson.close()

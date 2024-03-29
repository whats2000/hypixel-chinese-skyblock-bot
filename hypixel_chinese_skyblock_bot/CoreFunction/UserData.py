import json
import logging
import os

from CoreFunction.Common import get_setting_json
from CoreFunction.Logger import Logger

bot_logger = Logger(__name__)


class UserData:
    def __init__(self, user: str):
        self.id = user

        self.discord = ''

        self.uuid = ''

        self.api = {}

        self.profile = {}

        self.skyblock_api = {}

        self.dung_class_level = {
            'healer': 0,
            'mage': 0,
            'berserk': 0,
            'archer': 0,
            'tank': 0
        }

        self.dung_level = {
            'catacombs': 0
        }

        self.slayer_is_max = {
            7: False,
            8: False,
            9: False
        }

        self.skill_is_max = {
            'taming': False,
            'farming': False,
            'mining': False,
            'combat': False,
            'foraging': False,
            'fishing': False,
            'enchanting': False,
            'alchemy': False,
            'carpentry': False,
            'runecrafting': False,
            'social2': False
        }

        self.skill_max_count = 0

        self.senither_weight = 0.0

        self.senither_weight_overflow = 0.0

        self.max_senither_weight = 0.0

        self.senither_weight_pass = False

    def set_dung_class_level(self, dung_class: str, exp: float):
        xp_to_level_list = get_setting_json('dungeon_xp_to_level')

        for i in range(50, 0, -1):
            if exp >= xp_to_level_list[str(i)]:
                self.dung_class_level[dung_class] = i
                break

        else:
            self.dung_class_level[dung_class] = -1

    def get_dung_class_level(self, dung_class: str):
        return self.dung_class_level[dung_class]

    def set_dung_level(self, dung: str, exp: float):
        xp_to_level_list = get_setting_json('dungeon_xp_to_level')

        if exp - 569809640 >= 200000000:
            self.dung_level[dung] = 50 + int((exp - 569809640) // 200000000)

        else:
            for i in range(50, 0, -1):
                if exp >= xp_to_level_list[str(i)]:
                    self.dung_level[dung] = i
                    break

            else:
                self.dung_level[dung] = -1

    def get_dung_level(self, dung: str):
        return self.dung_level[dung]

    def get_dung_class_is_max(self, dung_class: str):
        return self.dung_class_level[dung_class] >= 50

    def set_slayer_level_is_max(self, num: int, boolean: bool):
        if 7 <= num <= 9:
            self.slayer_is_max[num] = boolean

    def get_slayer_level_is_max(self, num: int):
        return self.slayer_is_max[num]

    def set_skill_level_is_max(self, skill: str, boolean: bool):
        if skill in self.skill_is_max:
            self.skill_is_max[skill] = boolean

    def get_skill_level_is_max(self, skill: str):
        return self.skill_is_max[skill]

    def set_skill_max_count(self):
        if self.skill_max_count < sum(self.slayer_is_max.values()) + sum(self.skill_is_max.values()):
            self.skill_max_count = sum(self.slayer_is_max.values()) + sum(self.skill_is_max.values())

    def set_latest_user_api(self):
        if self.api['success']:
            output = self.api

            output = json.dumps(output, ensure_ascii=False, indent=4)

            with open(f'{os.getcwd()}/Resources/LatestUserApi.json',
                      mode='w',
                      encoding='utf8'
                      ) as out_json:
                out_json.write(output)

            out_json.close()

    def try_get_latest_user_api(self):
        with open(f'{os.getcwd()}/Resources/LatestUserApi.json',
                  mode='r',
                  encoding='utf8'
                  ) as verify_id_list_json:
            data = json.load(verify_id_list_json)

            verify_id_list_json.close()

        if data['player'] is not None:
            try:
                if self.id == data['player']['displayname']:
                    self.api = data

            except KeyError:
                bot_logger.log_message(logging.ERROR, f'獲取最新 API 失敗')

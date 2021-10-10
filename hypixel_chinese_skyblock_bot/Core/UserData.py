from hypixel_chinese_skyblock_bot.Core.Common import get_setting_json


class UserData:
    def __init__(self, id):
        self.id = id

        self.dungClassLevel = {
            'healer': 0,
            'mage': 0,
            'berserk': 0,
            'archer': 0,
            'tank': 0
        }

        self.dungLevel = {
            'catacombs': 0
        }

        self.slayerIsMax = {
            7: False,
            8: False,
            9: False
        }

        self.skillIsMax = {
            'taming': False,
            'farming': False,
            'mining': False,
            'combat': False,
            'foraging': False,
            'fishing': False,
            'enchanting': False,
            'alchemy': False,
            'carpentry': False
        }

    def set_dung_class_level(self, dungClass, exp):
        xpToLevelList = get_setting_json('dungeon_xp_to_level')

        for i in range(50, 0, -1):
            if exp >= xpToLevelList[str(i)]:
                self.dungClassLevel[dungClass] = i
                break

        else:
            self.dungClassLevel[dungClass] = -1

    def get_dung_class_level(self, dungClass):
        return self.dungClassLevel[dungClass]

    def set_dung_level(self, dung, exp):
        xpToLevelList = get_setting_json('dungeon_xp_to_level')

        for i in range(50, 0, -1):
            if exp >= xpToLevelList[str(i)]:
                self.dungLevel[dung] = i
                break

        else:
            self.dungLevel[dung] = -1

    def get_dung_level(self, dung):
        return self.dungLevel[dung]

    def get_dung_class_is_max(self, dungClass):
        return self.dungClassLevel[dungClass] >= 50

    def set_slayer_level_is_max(self, num, boolean):
        if 7 <= num <= 9:
            self.slayerIsMax[num] = boolean

    def get_slayer_level_is_max(self, num):
        return self.slayerIsMax[num]

    def set_skill_level_is_max(self, skill, boolean):
        if skill in self.skillIsMax:
            self.skillIsMax[skill] = boolean

    def get_skill_level_is_max(self, skill):
        return self.skillIsMax[skill]
class UserData:
    def __init__(self, id):
        self.id = id
        self.dung = 0  # 未使用中
        self.slayer = {
            7: False,
            8: False,
            9: False}
        self.skill = {
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

    def set_slayer_level(self, num, boolean):
        if 7 <= num <= 9:
            self.slayer[num] = boolean

    def set_skill_level(self, skill, boolean):
        if skill in self.skill:
            self.skill[skill] = boolean

    def get_slayer_level(self, num):
        return self.slayer[num]

    def get_skill_level(self, skill):
        return self.skill[skill]
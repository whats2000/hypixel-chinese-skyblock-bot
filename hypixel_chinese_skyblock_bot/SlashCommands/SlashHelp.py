import discord
from dislash import slash_command

from hypixel_chinese_skyblock_bot.Core.Common import CodExtension, get_setting_json


class SlashHelp(CodExtension):
    @slash_command(
        guild_ids=[int(get_setting_json('ServerId'))],
        name="help",
        description="Open up the commands list"
    )
    async def help(self, inter):
        embed = discord.Embed(
            title='幫助列表',
            description=':scroll: 調適指令'
                        '\n\n :arrow_right: `sb?help` : 打開本列表'
                        '\n\n :arrow_right: `sb?ping` : 察看與bot連線延遲'
                        '\n\n :arrow_right: `sb?translate [語言id] [文字]` : 翻譯語言'
                        '\n\n==============='
                        '\n\n:scroll: 驗證命令'
                        '\n\n :arrow_right: `sb?verifyid [玩家遊戲id]` : 輸入要驗證的id，需與hypixel社群discord綁定一致'
                        '\n\n :arrow_right: `sb?verifyidupdate [玩家遊戲id]` : 輸入要更新的id，需與hypixel社群discord綁定一致'
                        '\n\n :arrow_right: `sb?verifydung` : 驗證地下城職業等級與地下城等級'
                        '\n\n :arrow_right: `sb?verifyprog` : 驗證玩家進度是否滿等'
                        '\n\n================'
                        '\n\n:question: v 如何開啟Api',
            color=0x00ff00
        )

        embed.set_image(url='https://media.giphy.com/media/e2uLbm9lZm1J4QyUvQ/giphy-downsized-large.gif')

        await inter.respond(embed=embed)


def setup(pybot):
    pybot.add_cog(SlashHelp(pybot))
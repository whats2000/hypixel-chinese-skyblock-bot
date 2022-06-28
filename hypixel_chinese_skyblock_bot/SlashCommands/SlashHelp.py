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
                        '\n\n :arrow_right: `sb?help`, `/help` : 打開本列表'
                        '\n\n :arrow_right: `sb?ping`, `/ping` : 察看與bot連線延遲'
                        '\n\n :arrow_right: `sb?translate [語言id] [文字]` : 翻譯語言'
                        '\n\n :arrow_right: `/embed` : 製作對話框'
                        '\n\n==============='
                        '\n\n:scroll: 驗證命令'
                        '\n\n :arrow_right: `sb?verifyid [玩家遊戲id]`, `/verify_id` : 輸入要驗證的id，需與hypixel社群discord綁定一致'
                        '\n\n :arrow_right: `sb?verifyidupdate [玩家遊戲id]`, `/verify_id_update` : '
                        '輸入要更新的id，需與hypixel社群discord綁定一致 '
                        '\n\n :arrow_right: `sb?verifydung`, `/verify_dungeoneer` : 驗證地下城職業等級與地下城等級'
                        '\n\n :arrow_right: `sb?verifyprog`, `/verify_progress` : 驗證玩家進度是否滿等'
                        '\n\n :arrow_right: `sb?verifyweight`, `/verify_weight` : 驗證玩家發展階段，並確認是否符合資深玩家'
                        '\n\n================'
                        '\n\n:question: v 如何開啟Api',
            color=0x00ff00
        )

        embed.set_author(
            name=inter.author.name,
            icon_url=inter.author.avatar_url
        )

        embed.set_image(url='https://media.giphy.com/media/e2uLbm9lZm1J4QyUvQ/giphy-downsized-large.gif')

        await inter.respond(embed=embed)


def setup(pybot):
    pybot.add_cog(SlashHelp(pybot))

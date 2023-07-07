import logging

import disnake
from disnake.ext import commands

from CoreFunction.Common import CodExtension
from CoreFunction.Logger import Logger
from CoreFunction.SendEmbed import set_ctx_embed_author

bot_logger = Logger(__name__)


class Help(CodExtension):
    @commands.command()
    async def help(self, ctx: commands.Context):
        bot_logger.log_message(logging.DEBUG, f'{ctx.message.author.name} 用戶呼叫幫助命令')

        embed = disnake.Embed(
            title='幫助列表',
            description=':scroll: 調適指令'
                        '\n\n :arrow_right: `sb?help`, `/help` : 打開本列表'
                        '\n\n :arrow_right: `sb?ping`, `/ping` : 查看與 bot 連線延遲'
                        '\n\n :arrow_right: `sb?translate` `語言 id` `文字` : 翻譯語言'
                        '\n\n :arrow_right: `/embed` : 製作對話框'
                        '\n\n :arrow_right: `/send_embed` : 發送交互身分組選單'
                        '\n\n :arrow_right: `/verify_title` : 發送切換身分組選單'
                        '\n\n==============='
                        '\n\n:scroll: 驗證命令'
                        '\n\n :arrow_right: `/verify_id` : 輸入要驗證的 id，需與 hypixel 社群 discord 綁定一致'
                        '\n\n :arrow_right: `/verify_id_update` : '
                        '輸入要更新的 id，需與 hypixel 社群 discord 綁定一致 '
                        '\n\n :arrow_right: `/verify_dungeoneer` : 驗證地下城職業等級與地下城等級'
                        '\n\n :arrow_right: `/verify_progress` : 驗證玩家進度是否滿等'
                        '\n\n :arrow_right: `/verify_weight` : 驗證玩家發展階段，並確認是否符合資深玩家'
                        '\n\n :arrow_right: `/verify_title` : 驗證玩家並變更稱號'
                        '\n\n==============='
                        '\n\n:scroll: 其他命令'
                        '\n\n :arrow_right: `/party` : 發送組隊邀請'
                        '\n\n :arrow_right: `/wiki` : 查詢 skyblock wiki'
                        '\n\n================'
                        '\n\n:question: v 如何開啟Api',
            color=0x00ff00
        )

        set_ctx_embed_author(embed, ctx)

        embed.set_image(url='https://cdn.discordapp.com/attachments/1107091685315444817/1119566032365957171/TurnOnAPI.gif')

        await ctx.send(embed=embed)

        await ctx.message.delete()


def setup(pybot):
    pybot.add_cog(Help(pybot))

import logging
import disnake
from disnake.ext import commands

from CoreFunction.Common import get_setting_json, CodExtension
from CoreFunction.Gemini import text_model
from CoreFunction.Logger import Logger
from CoreFunction.SendEmbed import set_inter_embed_author

bot_logger = Logger(__name__)


async def evaluate_message(inter: disnake.ApplicationCommandInteraction, message: disnake.Message):
    member = inter.guild.get_member(message.author.id)
    message_text = message.content
    message_link = f"https://discord.com/channels/" \
                   f"{message.guild.id}/{message.channel.id}/{message.id} "

    if not member:
        try:
            member = await inter.guild.fetch_member(message.author.id)
        except disnake.Forbidden:
            await inter.response.send_message("User not found in this guild.", ephemeral=True)
            return

    if any(role.id == get_setting_json("BotRole") for role in member.roles):
        embed = disnake.Embed(
            title="檢舉評估信息",
            url=message_link,
            description="❌ 錯誤\n你不能檢舉機器人",
            color=0xADD8E6
        )

        set_inter_embed_author(embed, inter)

        await inter.edit_original_message(embed=embed)
        return

    prompt_parts = [
        f"""以下是這個聊天頻道規章
#####
1.尊重、包容、友善
尊重每個人。絕對禁止且不容忍誹謗騷擾、迫害、性別歧視、種族歧視或仇恨言論。
2.禁止不明連結與檔案
若群主未賦予權限，則禁止濫發訊息或個人宣傳（伺服器邀請、廣告、模組等），包含私訊至群組成員。
在分享自己被私訊惡意連結的截圖時，請把惡意連結的部分打碼處理。否則管理員將依當下情節判斷並進行懲處。
3.保持健全環境
保持友善交流，且禁止限制級或猥褻內容。包含文字、圖片或主打裸露、性、肢體暴力，以及其他令人不適的圖像內容等相關連結。
並且為方便頻道管理員管理，請勿使用繁體/簡體中文或英文以外的語言持續聊天。
4.禁止洗頻
請不要傳送大量垃圾信息，會有機器人進行判定，並判定方式會隨時間進行微調。若有誤判情況，請尋找管理員協助。
5.禁止現實金錢交易
請勿公開與其他玩家進行直接的金錢交易者（包括8591寶物交易網、使用 Hypixel Rank 換取他人的道具/服務）。
6.打擊詐騙行為
經被害人告訴並提供證據，管理員審核後認為有確切詐騙行為者（代製物品卻拿走材料、遊戲幣詐騙等），將永久封鎖。
7.遵守官方守則
本群組遵照 Hypixel 官方規則，請勿在此討論官方不允許的事項。如遊戲外掛與複製物品。
#####
任務說明：
你需要評估給定的 Discord 聊天內容，判斷其是否違反上述規章。
如果你認為聊天內容違反了規章，請在第一行回答一個 0 到 100 之間的數字，表示違規可能性的百分比。
如果該可能性小於 85%，則在第二行回答“沒有違規”。
如果該可能性大於或等於 85%，請在第二行指出違反的是哪一條規則。
#####
範例輸入：
"我討厭所有人，你們都很糟糕！"

範例輸出：
95
違反第 1 點規則：尊重、包容、友善
#####
以下是需判斷的 Discord 聊天內容：
#####
"{message_text}"
#####"""
    ]

    try:
        response = text_model.generate_content(prompt_parts)

        # Split the response into a list of lines, first line is the percentage, second line is the rule
        response_content = response.text.splitlines()
        percentage = int(response_content[0])
        rule = response_content[1]

        bot_logger.log_message(logging.INFO, f"違規可能性: {percentage}% {rule}")

        embed = disnake.Embed(
            title="檢舉評估信息",
            url=message_link,
            description=f"違規可能性: {percentage}%\n{rule}",
            color=0x00ff00 if percentage < 85 else 0xff0000
        )
        set_inter_embed_author(embed, inter)

        embed.set_footer(text="該技術使用Google Gemini")

        await inter.edit_original_message(embed=embed)

    except Exception as e:
        await inter.edit_original_message(content=f"❌ 發生錯誤: {str(e)}")
        bot_logger.log_message(logging.ERROR, f'生成回應時發生錯誤: {str(e)}')


class ReportContent(CodExtension):
    @commands.cooldown(1, 60, commands.BucketType.user)
    @commands.message_command(
        guild_ids=[int(get_setting_json('ServerId'))],
        name="檢舉內容"
    )
    async def report_content(self, inter: disnake.ApplicationCommandInteraction, message: disnake.Message):
        await inter.response.defer()
        bot_logger.log_message(logging.INFO, f"{inter.author.name} 檢舉了用戶 {message.author.display_name} 的訊息: \n{message.content}")

        await evaluate_message(inter, message)


def setup(pybot):
    pybot.add_cog(ReportContent(pybot))

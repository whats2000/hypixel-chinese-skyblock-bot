import logging

import disnake
from disnake.ext import commands

from CoreFunction.Common import CodExtension, get_setting_json, remove_role, add_role
from CoreFunction.Logger import Logger
from CoreFunction.SendEmbed import inter_build_embed, set_inter_embed_author

bot_logger = Logger(__name__)


# defines a custom selection containing title options that the user can choose.
class TitleDropdown(disnake.ui.Select):
    def __init__(self):
        # Define the options that will be presented inside the dropdown
        options = [
            disnake.SelectOption(
                label="萬眾矚目", description=f"需取得 內容創作者 Media 身分組", emoji="<:creator:1089956446818545805>"
            ),
            disnake.SelectOption(
                label="金光閃閃", description="需取得 加成者 Booster 身分組", emoji="<:nitrobright:1089956488258261022>"
            ),
            disnake.SelectOption(
                label="好野人", description="需取得 贊助者 Donator 身分組", emoji="<:treasure:1089956529513431190>"
            ),
            disnake.SelectOption(
                label="新人保姆", description="需取得 新手嚮導 Guide 身分組", emoji="<:beacon:1090630689734524978>"
            )
        ]

        super().__init__(
            placeholder="選擇你要的稱號...",
            min_values=1,
            max_values=1,
            options=options,
        )

    # define how to respond to the selection
    async def callback(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer(ephemeral=True)

        bot_logger.log_message(logging.INFO, f'變更稱號 : {inter.author.name}')

        require_roles = get_setting_json('TitleRequireRoleList')

        # check if the use have required role for the tile
        for role in require_roles:
            if self.values[0] == role and require_roles[role] not in [y.id for y in inter.author.roles]:
                bot_logger.log_message(logging.ERROR, f'變更稱號 "{self.values[0]}" 失敗 : 缺失身分組')

                embed = disnake.Embed(
                    title='缺失身分組',
                    description='你缺失必要身分組，無法獲取此稱號',
                    color=0xe74c3c
                )

                set_inter_embed_author(embed, inter)

                await inter.send(embed=embed, ephemeral=True)

                return

        # remove other role as only one role is allow
        title_roles = get_setting_json('TitleRoleList')

        for role in title_roles:
            await remove_role(ctx=inter, role_id=title_roles[role])

        # add the new select role
        await add_role(ctx=inter, role_id=title_roles[self.values[0]])

        bot_logger.log_message(logging.INFO, f'變更稱號 "{self.values[0]}" 成功')

        # get the role name
        role = title_roles[self.values[0]]

        mention_role = disnake.utils.get(inter.guild.roles, id=role)

        # get the icon of the role
        icons = get_setting_json('TitleIconList')

        embed = disnake.Embed(
            title=f'變更稱號完成',
            description=f'成功變更稱號成 {icons[self.values[0]]} {mention_role.mention}',
            color=0x00ff00
        )

        set_inter_embed_author(embed, inter)

        await inter.send(embed=embed, ephemeral=True)


class TitleDropdownView(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        # Add the dropdown to our view object.
        self.add_item(TitleDropdown())


class SlashVerifyTitle(CodExtension):

    @commands.slash_command(
        guild_ids=[int(get_setting_json('ServerId'))],
        name='verify_title',
        description='Verify your title and change it',
    )
    async def verify_title(self, inter: disnake.AppCommandInteraction):
        await inter.response.defer()

        if inter.channel.id != get_setting_json('VerifyTitleChannelId') and \
                inter.channel.id != get_setting_json('DebugChannelId'):
            bot_logger.log_message(logging.ERROR, f'錯誤頻道輸入')

            embed = inter_build_embed('Wrong Channel', inter)

            await inter.send(embed=embed, ephemeral=True)

            return

        view = TitleDropdownView()

        description = f'稱號徽章需有相應的身分組才能進行切換。\n' \
                      f'更多關於身分組的介紹可以前往 <#1018500627380318208> 查看。\n\n' \
                      f'**遊戲進度徽章 : **\n' \
                      f'**Not Coming Soon**\n\n' \
                      f'**須具備身分組〡可切換徽章**\n'

        require_roles = get_setting_json('TitleRequireRoleList')
        title_roles = get_setting_json('TitleRoleList')

        for role in title_roles:
            description += f'<@&{require_roles[role]}>〡<@&{title_roles[role]}>\n'

        embed = disnake.Embed(
            title=f'Skyblock Taiwan — 稱號徽章切換',
            description=description,
            color=16776960
        )

        await inter.send(embed=embed, view=view)


def setup(pybot):
    pybot.add_cog(SlashVerifyTitle(pybot))

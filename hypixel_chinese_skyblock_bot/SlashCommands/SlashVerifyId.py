import logging

import disnake
from disnake.ext import commands

from hypixel_chinese_skyblock_bot.Core.Common import CodExtension, get_hypixel_api, get_setting_json, set_user_id, \
    get_verify_id_list, add_role
from hypixel_chinese_skyblock_bot.Core.Logger import Logger
from hypixel_chinese_skyblock_bot.Core.UserData import UserData


class SlashVerifyId(CodExtension):

    @commands.slash_command(
        guild_ids=[int(get_setting_json('ServerId'))],
        name='verify_id',
        description='Link your discord to your minecraft account'
    )
    async def verify_id(self,
                        inter: disnake.AppCommandInteraction,
                        minecraft_id: str = commands.Param(
                           description='Input your user id here. You have to open up the social media in hypixel'
                        )):
        # check is in the desired channel
        await inter.response.defer(ephemeral=True)

        bot_logger = Logger(__name__)

        if inter.channel.id == get_setting_json('VerifyIdChannelId'):
            embed = disnake.Embed(
                title='正在向 hypixel api 提出訪問請求',
                color=0xf1c40f
            )

            embed.set_author(
                name=inter.author.name,
                icon_url=inter.author.avatar.url
            )

            await inter.edit_original_message(embed=embed)

            # check is user id input correctly
            if minecraft_id is not None:
                # check is player has been verified
                if get_setting_json('VerifyIdRole') not in [y.name.lower() for y in inter.author.roles]:
                    player = get_verify_id_list(inter.author)

                    player_data = UserData(player)

                    player_data.api = get_hypixel_api(minecraft_id)

                    bot_logger.log_message(logging.INFO, f'驗證用戶 : {inter.author.name}')

                    # check get hypixel api is successes
                    if player_data.api['success']:
                        player_data.set_latest_user_api()

                        # try to get player social media discord
                        try:
                            player_data.discord = player_data.api['player']['socialMedia']['links']['DISCORD']

                            # check user name is correct in api
                            if str(inter.author) == player_data.discord:
                                set_user_id(inter.author, player_data.api['player']['displayname'])

                                bot_logger.log_message(logging.INFO, f'驗證 id 成功')

                                embed = disnake.Embed(
                                    title='成功驗證',
                                    description=f'{inter.author} ---> {player_data.api["player"]["displayname"]}',
                                    color=0x00ff00
                                )

                                embed.set_author(
                                    name=inter.author.name,
                                    icon_url=inter.author.avatar.url
                                )

                                await inter.edit_original_message(embed=embed)

                                await add_role(ctx=inter, get_role_names='✔ 已驗證成員')

                            else:
                                bot_logger.log_message(logging.ERROR, f'找不到該名玩家 {minecraft_id}')

                                embed = disnake.Embed(
                                    title='驗證失敗，玩家id不正確',
                                    description=f'{inter.author} -x-> {minecraft_id}',
                                    color=0xe74c3c
                                )

                                embed.set_author(
                                    name=inter.author.name,
                                    icon_url=inter.author.avatar.url
                                )

                                await inter.edit_original_message(embed=embed)
                        except (KeyError, TypeError):
                            bot_logger.log_message(logging.ERROR, f'玩家未開啟 hypixel discord API')

                            embed = disnake.Embed(
                                title='驗證失敗，請先打開discord api',
                                description=f'{inter.author} -x-> {minecraft_id}',
                                color=0xe74c3c
                            )

                            embed.set_author(
                                name=inter.author.name,
                                icon_url=inter.author.avatar.url
                            )

                            await inter.edit_original_message(embed=embed)
                    else:
                        if 'cause' not in player_data.api:
                            player_data.api['cause'] = '玩家 id 綁定丟失，請更新 id (很可能是 nitro 導致編號變更)'

                        bot_logger.log_message(logging.ERROR, f'獲取 hypixel API 失敗  : {player_data.api["cause"]}')

                        embed = disnake.Embed(
                            title='驗證失敗，請稍後重試',
                            description=f'{inter.author} -x-> {minecraft_id}\n\n原因 : {player_data.api["cause"]}',
                            color=0xe74c3c
                        )

                        embed.set_author(
                            name=inter.author.name,
                            icon_url=inter.author.avatar.url
                        )

                        await inter.edit_original_message(embed=embed)

                else:
                    bot_logger.log_message(logging.ERROR, f'玩家已經驗證')

                    embed = disnake.Embed(
                        title='你已經驗證，更新請用 /verifyidupdate',
                        description=f'{inter.author} -x-> {minecraft_id}',
                        color=0xe74c3c
                    )

                    embed.set_author(
                        name=inter.author.name,
                        icon_url=inter.author.avatar.url
                    )

                    await inter.edit_original_message(embed=embed)

            else:
                bot_logger.log_message(logging.ERROR, f'玩家 {minecraft_id} 輸入錯誤')

                embed = disnake.Embed(
                    title='驗證失敗，請稍後重試',
                    description=f'{inter.author} -x-> {minecraft_id}',
                    color=0xe74c3c
                )

                embed.set_author(
                    name=inter.author.name,
                    icon_url=inter.author.avatar.url
                )

                await inter.edit_original_message(embed=embed)

        else:
            bot_logger.log_message(logging.ERROR, f'錯誤頻道輸入')

            embed = disnake.Embed(
                title='請在正確頻道輸入',
                color=0xe74c3c
            )

            embed.set_author(
                name=inter.author.name,
                icon_url=inter.author.avatar.url
            )

            await inter.send(embed=embed, ephemeral=True)


def setup(pybot):
    pybot.add_cog(SlashVerifyId(pybot))

import logging

import disnake
from disnake.ext import commands

from hypixel_chinese_skyblock_bot.Core.Common import CodExtension, get_hypixel_api, get_setting_json, \
    get_verify_id_list, get_senither_weight, add_role
from hypixel_chinese_skyblock_bot.Core.Logger import Logger
from hypixel_chinese_skyblock_bot.Core.UserData import UserData

bot_logger = Logger(__name__)


class SlashVerifyWeight(CodExtension):

    @commands.slash_command(
        guild_ids=[int(get_setting_json('ServerId'))],
        name='verify_weight',
        description='Verify your weight',
    )
    async def verifyweight(self, inter: disnake.AppCommandInteraction):
        await inter.response.defer(ephemeral=True)

        # check is in the desired channel.
        if inter.channel.id == get_setting_json('VerifyWeightChannelId') \
                or inter.channel.id == get_setting_json('DebugChannelId'):
            embed = disnake.Embed(
                title='正在向 hypixel api 提出訪問請求',
                color=0xf1c40f
            )

            embed.set_author(
                name=inter.author.name,
                icon_url=inter.author.avatar.url
            )

            await inter.edit_original_message(embed=embed)

            # check is player has been verified
            if get_setting_json('VerifyIdRole') in [y.name.lower() for y in inter.author.roles]:
                player = get_verify_id_list(inter.author)

                player_data = UserData(player)

                player_data.api = get_hypixel_api(player)

                # try to call the cache in order to skip the api request cool down
                if not player_data.api['success']:
                    player_data.try_get_latest_user_api()

                    bot_logger.log_message(logging.DEBUG, '嘗試呼叫緩存 LatestUserApi.json')

                bot_logger.log_message(logging.INFO, f'驗證用戶 {inter.author.name} 進度')

                # check get hypixel api is successes
                if player_data.api['success']:
                    bot_logger.log_message(logging.INFO, f'獲取 hypixel API 成功')

                    player_data.set_latest_user_api()

                    # try to get profile data
                    try:
                        player_data.uuid = player_data.api['player']['uuid']

                        player_data.profile = player_data.api['player']['stats']['SkyBlock']['profiles']

                        # loop for checking all profile
                        for profile_id in player_data.profile:
                            bot_logger.log_message(logging.INFO, f'正在驗證 '
                                                                 f'{player_data.profile[profile_id]["cute_name"]}')

                            embed = disnake.Embed(
                                title='驗證處理中',
                                description=f'正在驗證 -> {player_data.profile[profile_id]["cute_name"]}',
                                color=0xf1c40f
                            )

                            embed.set_author(
                                name=inter.author.name,
                                icon_url=inter.author.avatar.url
                            )

                            await inter.edit_original_message(embed=embed)

                            # try to get weight api
                            try:
                                weight = get_senither_weight(profile_id)

                                # check is api respond
                                if weight['status'] == 200:
                                    player_data.senither_weight = weight['data']['weight']
                                    player_data.senither_weight_overflow = weight['data']['weight_overflow']

                                    if player_data.senither_weight \
                                            + player_data.senither_weight_overflow \
                                            > player_data.max_senither_weight:
                                        player_data.max_senither_weight \
                                            = player_data.senither_weight + player_data.senither_weight_overflow

                                    desc = f'**Senither :**' \
                                           f'\n\n:man_lifting_weights: Weight : ' \
                                           f'{round(player_data.senither_weight, 2)}' \
                                           f'\n\n:person_lifting_weights: Overflow Weight : ' \
                                           f'{round(player_data.senither_weight_overflow)}' \
                                           f'\n\n:woman_lifting_weights:  Total Weight : ' \
                                           f'{round(player_data.max_senither_weight, 2)}'

                                    embed = disnake.Embed(
                                        title=f'{player_data.profile[profile_id]["cute_name"]} 的 Weight',
                                        description=desc,
                                        color=0x00ff00
                                    )

                                    embed.set_author(
                                        name=inter.author.name,
                                        icon_url=inter.author.avatar.url
                                    )

                                    await inter.send(embed=embed, delete_after=30.0)

                                else:
                                    bot_logger.log_message(logging.ERROR, f'senither weight no respond : '
                                                                          f'{weight["reason"]}')

                                    embed = disnake.Embed(
                                        title='驗證失敗，請稍後重試',
                                        description=f'{inter.author} -x-> Weight\n\n'
                                                    f'原因 : {weight["reason"]}\n\n'
                                                    f'描述 : 請確保 Api 為開啟狀態',
                                        color=0xe74c3c
                                    )

                                    embed.set_author(
                                        name=inter.author.name,
                                        icon_url=inter.author.avatar.url
                                    )

                                    await inter.send(embed=embed, delete_after=20.0)

                            except KeyError:
                                bot_logger.log_message(logging.ERROR,
                                                       f'驗證 hypixel skyblock API '
                                                       f'{player_data.profile[profile_id]["cute_name"]} 失敗')

                        weight_require = get_setting_json('SkillWeightRequire')

                        if player_data.max_senither_weight >= weight_require:
                            print(f' - skill weight > {weight_require}')

                            player_data.senither_weight_pass = True

                            await add_role(ctx=inter, get_role_id='SeniorPlayer')

                            # try to create result output
                            try:
                                desc = f'你的最高 senither weight : ' \
                                       f'{player_data.max_senither_weight} >= {weight_require}, 符合申請資格'

                                embed = disnake.Embed(
                                    title='已成功認證',
                                    description=str(desc),
                                    color=0x00ff00
                                )

                                embed.set_author(
                                    name=inter.author.name,
                                    icon_url=inter.author.avatar.url
                                )

                                await inter.edit_original_message(embed=embed)

                            except TypeError:
                                bot_logger.log_message(logging.ERROR, f'建立 embed 失敗')

                        elif not player_data.senither_weight_pass:
                            bot_logger.log_message(logging.INFO, f'未有進度達標')

                            desc = f'你的最高 senither weight : ' \
                                   f'{player_data.max_senither_weight} < {weight_require} , 不符合申請資格'

                            embed = disnake.Embed(
                                title='你目前Weight未達標，請再接再厲',
                                description=desc,
                                color=0xe74c3c
                            )

                            embed.set_author(
                                name=inter.author.name,
                                icon_url=inter.author.avatar.url
                            )

                            await inter.edit_original_message(embed=embed)

                    except KeyError:
                        bot_logger.log_message(logging.ERROR, f'玩家未開啟 hypixel discord API')

                        embed = disnake.Embed(
                            title='驗證失敗，請先打開 hypixel discord api',
                            description=f'{inter.author} -x-> Weight',
                            color=0xe74c3c
                        )

                        embed.set_author(
                            name=inter.author.name,
                            icon_url=inter.author.avatar.url
                        )

                        await inter.send(embed=embed, delete_after=20.0)
                else:
                    if 'cause' not in player_data.api:
                        player_data.api['cause'] = '玩家 id 綁定丟失，請更新 id (很可能是 nitro 導致編號變更)'

                    bot_logger.log_message(logging.ERROR, f'玩家獲取資料失敗: {player_data.api["cause"]}')

                    embed = disnake.Embed(
                        title='驗證失敗，請稍後重試',
                        description=f'{inter.author} -x-> Weight\n\n原因 : {player_data.api["cause"]}',
                        color=0xe74c3c
                    )

                    embed.set_author(
                        name=inter.author.name,
                        icon_url=inter.author.avatar.url
                    )

                    await inter.send(embed=embed, delete_after=20.0)

            else:
                bot_logger.log_message(logging.ERROR, f'玩家 id 缺失')

                embed = disnake.Embed(
                    title='你未登記id，請先登記id',
                    description=f'{inter.author} -x-> Weight',
                    color=0xe74c3c
                )

                embed.set_author(
                    name=inter.author.name,
                    icon_url=inter.author.avatar.url
                )

                await inter.send(embed=embed, delete_after=20.0)

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
    pybot.add_cog(SlashVerifyWeight(pybot))

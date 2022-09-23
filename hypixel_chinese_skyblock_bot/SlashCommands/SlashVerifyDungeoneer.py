import logging

import disnake
from disnake.ext import commands

from hypixel_chinese_skyblock_bot.Core.Common import CodExtension, get_hypixel_api, get_setting_json, \
    get_verify_id_list, get_hypixel_skyblock_api, add_role, remove_role
from hypixel_chinese_skyblock_bot.Core.Logger import Logger
from hypixel_chinese_skyblock_bot.Core.UserData import UserData

bot_logger = Logger(__name__)


class SlashVerifyDungeoneer(CodExtension):

    @commands.slash_command(
        guild_ids=[int(get_setting_json('ServerId'))],
        name='verify_dungeoneer',
        description='Verify your dungeon class level and dungeon exp level',
    )
    async def verifydung(self, inter: disnake.AppCommandInteraction):
        await inter.response.defer(ephemeral=True)

        # check is in the desired channel.
        if inter.channel.id == get_setting_json('VerifyDungeoneerChannelId'):
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
                await add_role(ctx=inter, get_role_id='DungeoneerRole')

                player = get_verify_id_list(inter.author)

                player_data = UserData(player)

                player_data.api = get_hypixel_api(player)

                # try to call the cache in order to skip the api request cool down
                if not player_data.api['success']:
                    player_data.try_get_latest_user_api()

                    bot_logger.log_message(logging.DEBUG, '嘗試呼叫緩存 LatestUserApi.json')

                bot_logger.log_message(logging.INFO, f'驗證用戶 {inter.author.name} 地下城')

                # check get hypixel api is successes
                if player_data.api['success']:
                    bot_logger.log_message(logging.INFO, f'獲取 hypixel API 成功')

                    player_data.set_latest_user_api()

                    # try to get profile data and max class data
                    try:
                        player_dung_max_level = player_data.api['player']['achievements']['skyblock_dungeoneer']

                        player_data.uuid = player_data.api['player']['uuid']

                        player_data.profile = player_data.api['player']['stats']['SkyBlock']['profiles']

                        # loop for checking all profile
                        for profile_id in player_data.profile:
                            is_class_level_get_success = False

                            is_dung_level_get_success = False

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

                            # try to get skyblock api
                            try:
                                player_data.skyblock_api = get_hypixel_skyblock_api(profile_id)

                                # check get skyblock api is successes
                                if player_data.skyblock_api['success']:
                                    bot_logger.log_message(logging.INFO, f'獲取 hypixel skyblock API 成功')

                                    dung_api = \
                                        player_data.skyblock_api['profile']['members'][player_data.uuid]['dungeons']

                                    # get dungeon classes level
                                    try:
                                        for dung_class in dung_api['player_classes']:
                                            class_exp = dung_api['player_classes'][dung_class]['experience']

                                            print(f' - {dung_class} : {class_exp}')

                                            player_data.set_dung_class_level(dung_class, class_exp)

                                        is_class_level_get_success = True

                                    except KeyError:
                                        bot_logger.log_message(logging.ERROR, f'獲取職業等級失敗')

                                    # get dungeon level
                                    try:
                                        for dung in player_data.dung_level:
                                            dung_exp = dung_api['dungeon_types'][dung]['experience']

                                            print(f' - {dung} : {dung_exp}')

                                            player_data.set_dung_level(dung, dung_exp)

                                            dung_level = player_data.get_dung_level(dung)

                                            if dung_level > player_dung_max_level:
                                                player_dung_max_level = dung_level

                                        is_dung_level_get_success = True

                                    except KeyError:
                                        bot_logger.log_message(logging.ERROR, f'獲取地下城等級失敗')

                                else:
                                    bot_logger.log_message(logging.ERROR, f'獲取 hypixel skyblock API 失敗')

                                    embed = disnake.Embed(
                                        title='驗證失敗，請稍後重試',
                                        description=f'{player_data.profile[profile_id]["cute_name"]} -x-> Dungeoneer',
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

                            # create embed
                            try:
                                if is_class_level_get_success and is_dung_level_get_success:
                                    desc = f':trophy: 最高地下城等級 : ' \
                                           f'{player_dung_max_level}' \
                                           f'\n\n===============\n\n:island: 島嶼職業等級 :\n\n'

                                    for dung_class in player_data.dung_class_level:
                                        print(f' - {dung_class} : {player_data.get_dung_class_level(dung_class)}')

                                        dung_class_list = get_setting_json('dung_class_list')

                                        desc = f'{desc} - {dung_class_list[dung_class]} : ' \
                                               f'{player_data.get_dung_class_level(dung_class)}\n\n'

                                    desc += '===============\n\n:classical_building: 地下城等級 : \n\n'

                                    for dung in player_data.dung_level:
                                        print(f' - {dung} : {player_data.get_dung_level(dung)}')

                                        dung_list = get_setting_json('dung_list')

                                        desc = f'{desc} - {dung_list[dung]} : ' \
                                               f'{player_data.get_dung_level(dung)}\n\n'

                                    embed = disnake.Embed(
                                        title=f'{player_data.profile[profile_id]["cute_name"]} 已更新地下城',
                                        description=str(desc),
                                        color=0x00ff00
                                    )

                                    embed.set_author(
                                        name=inter.author.name,
                                        icon_url=inter.author.avatar.url
                                    )

                                    await inter.send(embed=embed, delete_after=20.0)

                                else:
                                    bot_logger.log_message(logging.ERROR,
                                                           f'驗證 hypixel skyblock API '
                                                           f'{player_data.profile[profile_id]["cute_name"]} 失敗')

                                    embed = disnake.Embed(
                                        title=f'驗證 {player_data.profile[profile_id]["cute_name"]} 失敗，請打開該島api',
                                        description=f'{player_data.profile[profile_id]["cute_name"]} -x-> Dungeoneer',
                                        color=0xe74c3c
                                    )

                                    embed.set_author(
                                        name=inter.author.name,
                                        icon_url=inter.author.avatar.url
                                    )

                                    await inter.send(embed=embed, delete_after=20.0)

                            except TypeError:
                                bot_logger.log_message(logging.ERROR, f'建立 embed 失敗')

                        # give role
                        try:
                            for i in range(10):
                                await remove_role(ctx=inter, get_role_names=f'< {i}')

                                await remove_role(ctx=inter, get_role_names=f'{i} >')

                            for i in range(3, 6):
                                if player_dung_max_level >= 10 * i:
                                    await add_role(ctx=inter, get_role_id=f'cata{i}0')

                            if player_dung_max_level >= 100 or player_dung_max_level < 0:
                                bot_logger.log_message(logging.ERROR, f'無匹配身分組')

                                embed = disnake.Embed(
                                    title='驗證失敗，目前沒有匹配身分組',
                                    description=f'{inter.author} -x-> Dungeoneer',
                                    color=0xe74c3c
                                )

                                embed.set_author(
                                    name=inter.author.name,
                                    icon_url=inter.author.avatar.url
                                )

                                await inter.send(embed=embed, delete_after=20.0)

                            else:
                                await add_role(ctx=inter, get_role_names=f'< {player_dung_max_level // 10}')

                                await add_role(ctx=inter, get_role_names=f'{player_dung_max_level % 10} >')

                        except KeyError:
                            bot_logger.log_message(logging.ERROR, f'給予身分組失敗')

                    except KeyError:
                        bot_logger.log_message(logging.ERROR, f'玩家未開啟 hypixel discord API')

                        embed = disnake.Embed(
                            title='驗證失敗，請先打開 hypixel discord api',
                            description=f'{inter.author} -x-> Dungeoneer',
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
                        description=f'{inter.author} -x-> Dungeoneer\n\n原因 : {player_data.api["cause"]}',
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
                    description=f'{inter.author} -x-> Dungeoneer',
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
    pybot.add_cog(SlashVerifyDungeoneer(pybot))

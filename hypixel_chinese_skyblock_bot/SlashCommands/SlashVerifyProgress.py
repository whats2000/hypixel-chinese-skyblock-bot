import logging

import disnake
from disnake.ext import commands

from CoreFunction.Common import CodExtension, get_hypixel_api, get_setting_json, \
    get_verify_id_list, get_hypixel_skyblock_api, add_role, get_role_name
from CoreFunction.Logger import Logger
from CoreFunction.UserData import UserData

bot_logger = Logger(__name__)


class SlashVerifyProgress(CodExtension):

    @commands.slash_command(
        guild_ids=[int(get_setting_json('ServerId'))],
        name='verify_progress',
        description='Verify your slayer progress and skill level',
    )
    async def verify_progress(self, inter: disnake.AppCommandInteraction):
        await inter.response.defer(ephemeral=True)
        # check is in the desired channel.
        if inter.channel.id == get_setting_json('VerifyProgressChannelId')\
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
                await add_role(ctx=inter, get_role_id='ProgressRole')

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

                            # try to get skyblock api
                            try:
                                player_data.skyblock_api = get_hypixel_skyblock_api(profile_id)

                                # check get skyblock api is successes
                                if player_data.skyblock_api['success']:
                                    bot_logger.log_message(logging.INFO, f'獲取 hypixel skyblock API 成功')

                                    profile_api \
                                        = player_data.skyblock_api['profile']['members'][player_data.uuid]

                                    bot_logger.log_message(logging.INFO, f'獲取 hypixel skyblock profile id 成功')

                                    is_verify_pass = False

                                    # try to get slayer level
                                    try:
                                        # loop for checking all slayers
                                        for i in range(7, 10):
                                            # check if player achieve slayer level
                                            if f'level_{i}' in \
                                                    (profile_api['slayer_bosses']['zombie']['claimed_levels'] and
                                                     profile_api['slayer_bosses']['spider']['claimed_levels'] and
                                                     profile_api['slayer_bosses']['wolf']['claimed_levels'] and
                                                     profile_api['slayer_bosses']['enderman']['claimed_levels'] and
                                                     profile_api['slayer_bosses']['blaze']['claimed_levels']):

                                                await add_role(ctx=inter, get_role_id=f'AllSlayer{i}')

                                                print(f' - slayer {i}')

                                                player_data.set_slayer_level_is_max(i, True)

                                                # check if pass
                                                if not is_verify_pass:
                                                    is_verify_pass = True

                                            else:
                                                print(f' - no slayer archive {i}')
                                    except KeyError:
                                        bot_logger.log_message(logging.ERROR, f'驗證 slayer 等級失敗')

                                        embed = disnake.Embed(
                                            title='驗證slayer失敗，連結API錯誤，請稍後重試',
                                            description=f'請卻保有打開skyblock中slayer訪問api\n\n'
                                                        f'{player_data.profile[profile_id]["cute_name"]}'
                                                        f' -x-> Progress',
                                            color=0xe74c3c
                                        )

                                        embed.set_author(
                                            name=inter.author.name,
                                            icon_url=inter.author.avatar.url
                                        )

                                        await inter.send(embed=embed, delete_after=20.0)

                                    # try to get skill level
                                    try:
                                        skill_list = get_setting_json('skill_list')

                                        # loop for checking all skill
                                        for skill in skill_list:
                                            skill_level = profile_api[f'experience_skill_{skill}']

                                            # check if player achieve max skill level
                                            if skill_level >= skill_list[skill]:
                                                await add_role(ctx=inter, get_role_id=f'skill_{skill}')

                                                print(f' - {skill} : {skill_level} is verified')

                                                player_data.set_skill_level_is_max(skill, True)

                                                # check if pass
                                                if not is_verify_pass:
                                                    is_verify_pass = True

                                            else:
                                                print(f' - {skill} : {skill_level} is not archive')
                                    except KeyError:
                                        bot_logger.log_message(logging.ERROR, f'驗證 skill 等級失敗')

                                        embed = disnake.Embed(
                                            title='驗證skill失敗，連結API錯誤，請稍後重試',
                                            description=f'請卻保有打開skyblock中skill訪問api\n\n'
                                                        f'{player_data.profile[profile_id]["cute_name"]}'
                                                        f' -x-> Progress',
                                            color=0xe74c3c
                                        )

                                        embed.set_author(
                                            name=inter.author.name,
                                            icon_url=inter.author.avatar.url
                                        )

                                        await inter.send(embed=embed, delete_after=20.0)

                                    # check if any slayer or skill achieve
                                    if is_verify_pass:
                                        # try to create index output
                                        try:
                                            desc = ''

                                            # loop for checking all slayers
                                            for i in range(7, 10):
                                                boolean = player_data.get_slayer_level_is_max(i)

                                                # check if pass
                                                if boolean:
                                                    desc += '\u2705 : '

                                                else:
                                                    desc += '\u274c : '

                                                desc = f'{desc}' \
                                                       f'{get_role_name(inter, get_setting_json(f"AllSlayer{i}"))}\n\n'

                                            skill_list = get_setting_json('skill_list')

                                            # loop for checking all skill
                                            for skill in skill_list:
                                                boolean = player_data.get_skill_level_is_max(skill)

                                                # check if pass
                                                if boolean:
                                                    desc += '\u2705 : '

                                                else:
                                                    desc += '\u274c : '

                                                desc = f'{desc}' \
                                                       f'{get_role_name(inter, get_setting_json(f"skill_{skill}"))}\n\n'

                                            embed = disnake.Embed(
                                                title=f'{player_data.profile[profile_id]["cute_name"]} 已更新進度',
                                                description=str(desc),
                                                color=0x00ff00
                                            )

                                            embed.set_author(
                                                name=inter.author.name,
                                                icon_url=inter.author.avatar.url
                                            )

                                            await inter.send(embed=embed, delete_after=20.0)

                                            player_data.set_skill_max_count()

                                        except TypeError:
                                            bot_logger.log_message(logging.ERROR, f'建立 embed 失敗')

                                        # try to create extra index output
                                        try:
                                            # loop for player all skill
                                            for skill in player_data.skill_is_max:
                                                # check player all skill is max
                                                if skill != 'social2' and not player_data.skill_is_max[skill]:
                                                    print(' - all skills arent max')
                                                    break
                                            else:
                                                print(' - all skills are max')

                                                await add_role(ctx=inter, get_role_id='AllSkillMax')

                                                embed = disnake.Embed(
                                                    title=f'{player_data.profile[profile_id]["cute_name"]} 已更新進度',
                                                    description=f'\u2705 : '
                                                    f'{get_role_name(inter, get_setting_json("AllSkillMax"))}',
                                                    color=0x00ff00
                                                )

                                                embed.set_author(
                                                    name=inter.author.name,
                                                    icon_url=inter.author.avatar.url
                                                )

                                                await inter.send(embed=embed, delete_after=20.0)

                                        except TypeError:
                                            bot_logger.log_message(logging.ERROR, f'建立 extra embed 失敗')

                                    if player_data.skill_max_count > 0:
                                        embed = disnake.Embed(
                                            title=f'目前共取得進度數 : {player_data.skill_max_count}',
                                            color=0x00ff00
                                        )

                                        embed.set_author(
                                            name=inter.author.name,
                                            icon_url=inter.author.avatar.url
                                        )

                                        await inter.edit_original_message(embed=embed)

                                    else:
                                        bot_logger.log_message(logging.INFO, f'未有進度達標')

                                        embed = disnake.Embed(
                                            title='你目前未有任何進度達標，請再接再厲',
                                            description=f'{player_data.profile[profile_id]["cute_name"]} -x-> Progress',
                                            color=0xe74c3c
                                        )

                                        embed.set_author(
                                            name=inter.author.name,
                                            icon_url=inter.author.avatar.url
                                        )

                                        await inter.edit_original_message(embed=embed)

                                else:
                                    bot_logger.log_message(logging.ERROR,
                                                           f'驗證 hypixel skyblock API '
                                                           f'{player_data.profile[profile_id]["cute_name"]} 失敗')

                                    embed = disnake.Embed(
                                        title='驗證失敗，請稍後重試',
                                        description=f'{player_data.profile[profile_id]["cute_name"]} -x-> Progress',
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

                    except KeyError:
                        bot_logger.log_message(logging.ERROR, f'玩家未開啟 hypixel discord API')

                        embed = disnake.Embed(
                            title='驗證失敗，請先打開 hypixel discord api',
                            description=f'{inter.author} -x-> Progress',
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
                        description=f'{inter.author} -x-> Progress\n\n原因 : {player_data.api["cause"]}',
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
                    description=f'{inter.author} -x-> Progress',
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
    pybot.add_cog(SlashVerifyProgress(pybot))

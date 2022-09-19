import discord
from dislash import slash_command

from hypixel_chinese_skyblock_bot.Core.Common import CodExtension, get_hypixel_api, get_setting_json, \
    get_verify_id_list, get_hypixel_skyblock_api
from hypixel_chinese_skyblock_bot.Core.UserData import UserData


class SlashVerifyProgress(CodExtension):

    @slash_command(
        guild_ids=[int(get_setting_json('ServerId'))],
        name='verify_progress',
        description='Verify your slayer progress and skill level',
    )
    async def verifyprog(self, inter):
        # check is in the desired channel.
        if inter.channel.id == get_setting_json('VerifyProgressChannelId'):
            embed = discord.Embed(
                title='正在向 hypixel api 提出訪問請求',
                color=0xf1c40f
            )

            embed.set_author(
                name=inter.author.name,
                icon_url=inter.author.avatar_url
            )

            await inter.send(embed=embed, ephemeral=True)

            # check is player has been verified
            if get_setting_json('VerifyIdRole') in [y.name.lower() for y in inter.author.roles]:
                role = discord.utils.get(inter.author.guild.roles, name=get_setting_json('ProgressRole'))

                await inter.author.add_roles(role)

                player = get_verify_id_list(inter.author)

                player_data = UserData(player)

                player_data.api = get_hypixel_api(player)

                # try to call the cache in order to skip the api request cool down
                if not player_data.api['success']:
                    player_data.try_get_latest_user_api()

                    print('Info > 嘗試呼叫緩存')

                print(f'Info > verify player progress : {inter.author}')

                # check get hypixel api is successes
                if player_data.api['success']:
                    print('Info > get hypixel api success')

                    player_data.set_latest_user_api()

                    # try to get profile data
                    try:
                        player_data.uuid = player_data.api['player']['uuid']

                        player_data.profile = player_data.api['player']['stats']['SkyBlock']['profiles']

                        # loop for checking all profile
                        for profile_id in player_data.profile:
                            print(f'Info > - 正在驗證 {player_data.profile[profile_id]["cute_name"]}')

                            embed = discord.Embed(
                                title='驗證處理中',
                                description=f'正在驗證 -> {player_data.profile[profile_id]["cute_name"]}',
                                color=0xf1c40f
                            )

                            embed.set_author(
                                name=inter.author.name,
                                icon_url=inter.author.avatar_url
                            )

                            message = await inter.send(embed=embed)

                            # try to get skyblock api
                            try:
                                player_data.skyblock_api = get_hypixel_skyblock_api(profile_id)

                                print('Info > get api success')

                                # check get skyblock api is successes
                                if player_data.skyblock_api['success']:

                                    profile_api \
                                        = player_data.skyblock_api['profile']['members'][player_data.uuid]

                                    print('Info > get profileId success')

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

                                                role = discord.utils.get(inter.author.guild.roles,
                                                                         name=get_setting_json(f'AllSlayer{i}'))

                                                await inter.author.add_roles(role)

                                                print(f'Info > - slayer {i}')

                                                player_data.set_slayer_level_is_max(i, True)

                                                # check if pass
                                                if not is_verify_pass:
                                                    is_verify_pass = True

                                            else:
                                                print(f'Info > - no slayer archive {i}')
                                    except KeyError:
                                        print('Error > fail in verify slayer')

                                        embed = discord.Embed(
                                            title='驗證slayer失敗，連結API錯誤，請稍後重試',
                                            description=f'請卻保有打開skyblock中slayer訪問api\n\n'
                                                        f'{player_data.profile[profile_id]["cute_name"]}'
                                                        f' -x-> Progress',
                                            color=0xe74c3c
                                        )

                                        embed.set_author(
                                            name=inter.author.name,
                                            icon_url=inter.author.avatar_url
                                        )

                                        await message.edit(embed=embed, delete_after=20.0)

                                    # try to get skill level
                                    try:
                                        skill_list = get_setting_json('skill_list')

                                        # loop for checking all skill
                                        for skill in skill_list:
                                            skill_level = profile_api[f'experience_skill_{skill}']

                                            # check if player achieve max skill level
                                            if skill_level >= skill_list[skill]:
                                                role = discord.utils.get(inter.author.guild.roles,
                                                                         name=get_setting_json(f'skill_{skill}'))

                                                await inter.author.add_roles(role)

                                                print(f'Info > - {skill} : {skill_level} is verified')

                                                player_data.set_skill_level_is_max(skill, True)

                                                # check if pass
                                                if not is_verify_pass:
                                                    is_verify_pass = True

                                            else:
                                                print(f'Info > - {skill} : {skill_level} is not archive')
                                    except KeyError:
                                        print('Error > fail in verify skill')

                                        embed = discord.Embed(
                                            title='驗證skill失敗，連結API錯誤，請稍後重試',
                                            description=f'請卻保有打開skyblock中skill訪問api\n\n'
                                                        f'{player_data.profile[profile_id]["cute_name"]}'
                                                        f' -x-> Progress',
                                            color=0xe74c3c
                                        )

                                        embed.set_author(
                                            name=inter.author.name,
                                            icon_url=inter.author.avatar_url
                                        )

                                        await message.edit(embed=embed, delete_after=20.0)

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

                                                desc = f'{desc}{get_setting_json(f"AllSlayer{i}")}\n\n'

                                            skill_list = get_setting_json('skill_list')

                                            # loop for checking all skill
                                            for skill in skill_list:
                                                boolean = player_data.get_skill_level_is_max(skill)

                                                # check if pass
                                                if boolean:
                                                    desc += '\u2705 : '

                                                else:
                                                    desc += '\u274c : '

                                                desc = f'{desc}{get_setting_json(f"skill_{skill}")}\n\n'

                                            embed = discord.Embed(
                                                title=f'{player_data.profile[profile_id]["cute_name"]} 已更新進度',
                                                description=str(desc),
                                                color=0x00ff00
                                            )

                                            embed.set_author(
                                                name=inter.author.name,
                                                icon_url=inter.author.avatar_url
                                            )

                                            await message.edit(embed=embed, delete_after=20.0)

                                        except TypeError:
                                            print('Error > fail at create index embed')

                                        # try to create extra index output
                                        try:
                                            # loop for player all skill
                                            for skill in player_data.skill_is_max:
                                                # check player all skill is max
                                                if skill != 'carpentry' and not player_data.skill_is_max[skill]:
                                                    print('Info > - all skills arent max')
                                                    break
                                            else:
                                                print('Info > - all skills are max')

                                                role = discord.utils.get(inter.author.guild.roles,
                                                                         name=get_setting_json('AllSkillMax'))

                                                await inter.author.add_roles(role)

                                                embed = discord.Embed(
                                                    title=f'{player_data.profile[profile_id]["cute_name"]} 已更新進度',
                                                    description=f'\u2705 : {get_setting_json("AllSkillMax")}',
                                                    color=0x00ff00
                                                )

                                                embed.set_author(
                                                    name=inter.author.name,
                                                    icon_url=inter.author.avatar_url
                                                )

                                                await message.edit(embed=embed, delete_after=20.0)

                                        except TypeError:
                                            print('Error > fail at create extra embed')
                                    else:
                                        print('Info > nothing is verified')

                                        embed = discord.Embed(
                                            title='你目前未有任何進度達標，請再接再厲',
                                            description=f'{player_data.profile[profile_id]["cute_name"]} -x-> Progress',
                                            color=0xe74c3c
                                        )

                                        embed.set_author(
                                            name=inter.author.name,
                                            icon_url=inter.author.avatar_url
                                        )

                                        await message.edit(embed=embed, delete_after=20.0)

                                else:
                                    print('Error >　Please wait a little bit and try again')

                                    embed = discord.Embed(
                                        title='驗證失敗，請稍後重試',
                                        description=f'{player_data.profile[profile_id]["cute_name"]} -x-> Progress',
                                        color=0xe74c3c
                                    )

                                    embed.set_author(
                                        name=inter.author.name,
                                        icon_url=inter.author.avatar_url
                                    )

                                    await message.edit(embed=embed, delete_after=20.0)

                            except KeyError:
                                print(f'Error > fail to get skyblock api in '
                                      f'{player_data.profile[profile_id]["cute_name"]}')

                    except KeyError:
                        print('Error > The player do not open the social media')

                        embed = discord.Embed(
                            title='驗證失敗，請先打開 hypixel discord api',
                            description=f'{inter.author} -x-> Progress',
                            color=0xe74c3c
                        )

                        embed.set_author(
                            name=inter.author.name,
                            icon_url=inter.author.avatar_url
                        )

                        await inter.send(embed=embed, delete_after=20.0)
                else:
                    print('Error > Please wait a little bit and try again')

                    if 'cause' not in player_data.api:
                        player_data.api['cause'] = '玩家 id 綁定丟失，請更新 id (很可能是 nitro 導致編號變更)'

                    print(f'Error > fail reason : {player_data.api["cause"]}')

                    embed = discord.Embed(
                        title='驗證失敗，請稍後重試',
                        description=f'{inter.author} -x-> Progress\n\n原因 : {player_data.api["cause"]}',
                        color=0xe74c3c
                    )

                    embed.set_author(
                        name=inter.author.name,
                        icon_url=inter.author.avatar_url
                    )

                    await inter.send(embed=embed, delete_after=20.0)

            else:
                print('Error > Require verify id')

                embed = discord.Embed(
                    title='你未登記id，請先登記id',
                    description=f'{inter.author} -x-> Progress',
                    color=0xe74c3c
                )

                embed.set_author(
                    name=inter.author.name,
                    icon_url=inter.author.avatar_url
                )

                await inter.send(embed=embed, delete_after=20.0)

        else:
            print('Error > Wrong channel')

            embed = discord.Embed(
                title='請在正確頻道輸入',
                color=0xe74c3c
            )

            embed.set_author(
                name=inter.author.name,
                icon_url=inter.author.avatar_url
            )

            await inter.send(embed=embed, ephemeral=True)


def setup(pybot):
    pybot.add_cog(SlashVerifyProgress(pybot))

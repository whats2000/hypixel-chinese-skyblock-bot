import discord
from dislash import slash_command

from hypixel_chinese_skyblock_bot.Core.Common import CodExtension, get_hypixel_api, get_setting_json, \
    get_verify_id_list, get_hypixel_skyblock_api
from hypixel_chinese_skyblock_bot.Core.UserData import UserData


class SlashVerifyDungeoneer(CodExtension):

    @slash_command(
        guild_ids=[int(get_setting_json('ServerId'))],
        name='verify_dungeoneer',
        description='Verify your dungeon class level and dungeon exp level',
    )
    async def verifydung(self, inter):
        # check is in the desired channel.
        if inter.channel.id == get_setting_json('VerifyDungeoneerChannelId'):
            # check is player has been verified
            if get_setting_json('VerifyIdRole') in [y.name.lower() for y in inter.author.roles]:
                role = discord.utils.get(inter.author.guild.roles, name=get_setting_json('DungeoneerRole'))

                await inter.author.add_roles(role)

                player = get_verify_id_list(inter.author)

                player_data = UserData(player)

                player_data.api = get_hypixel_api(player)

                # try to call the cache in order to skip the api request cool down
                if not player_data.api['success']:
                    player_data.try_get_latest_user_api()

                    print('Info > 嘗試呼叫緩存')

                print(f'Info > verify player dungeoneer : {inter.author}')

                # check get hypixel api is successes
                if player_data.api['success']:
                    print('Info > get hypixel api success')

                    player_data.set_latest_user_api()

                    # try to get profile data and max class data
                    try:
                        player_dung_max_level = player_data.api['player']['achievements']['skyblock_dungeoneer']

                        print('Info > - {player_dung_max_level}')

                        player_data.uuid = player_data.api['player']['uuid']

                        player_data.profile = player_data.api['player']['stats']['SkyBlock']['profiles']

                        # loop for checking all profile
                        for profile_id in player_data.profile:
                            is_class_level_get_success = False

                            is_dung_level_get_success = False

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

                            await inter.send(embed=embed, delete_after=10.0)

                            # try to get skyblock api
                            try:
                                player_data.skyblock_api = get_hypixel_skyblock_api(profile_id)

                                print('Info > get api success')

                                # check get skyblock api is successes
                                if player_data.skyblock_api['success']:
                                    dung_api = \
                                        player_data.skyblock_api['profile']['members'][player_data.uuid]['dungeons']

                                    # get dungeon classes level
                                    try:
                                        for dung_class in dung_api['player_classes']:
                                            class_exp = dung_api['player_classes'][dung_class]['experience']

                                            print(f'Info > - {dung_class} : {class_exp}')

                                            player_data.set_dung_class_level(dung_class, class_exp)

                                        is_class_level_get_success = True

                                    except KeyError:
                                        print('Error > fail at get class level')

                                    # get dungeon level
                                    try:
                                        for dung in player_data.dung_level:
                                            dung_exp = dung_api['dungeon_types'][dung]['experience']

                                            print(f'Info > - {dung} : {dung_exp}')

                                            player_data.set_dung_level(dung, dung_exp)

                                            dung_level = player_data.get_dung_level(dung)

                                            if dung_level > player_dung_max_level:
                                                player_dung_max_level = dung_level

                                        is_dung_level_get_success = True

                                    except KeyError:
                                        print('Error > fail at get dung level')

                                else:
                                    print('Error >　Please wait a little bit and try again')

                                    embed = discord.Embed(
                                        title='驗證失敗，請稍後重試',
                                        description=f'{player_data.profile[profile_id]["cute_name"]} -x-> Dungeoneer',
                                        color=0xe74c3c
                                    )

                                    embed.set_author(
                                        name=inter.author.name,
                                        icon_url=inter.author.avatar_url
                                    )

                                    await inter.send(embed=embed, delete_after=20.0)

                            except KeyError:
                                print(f'Error > fail to get skyblock api in '
                                      f'{player_data.profile[profile_id]["cute_name"]}')

                            # create embed
                            try:
                                if is_class_level_get_success and is_dung_level_get_success:
                                    desc = f':trophy: 最高地下城等級 : ' \
                                           f'{player_dung_max_level}' \
                                           f'\n\n===============\n\n:island: 島嶼職業等級 :\n\n'

                                    for dung_class in player_data.dung_class_level:
                                        print(f'Info > - {dung_class} : {player_data.get_dung_class_level(dung_class)}')

                                        dung_class_list = get_setting_json('dung_class_list')

                                        desc = f'{desc} - {dung_class_list[dung_class]} : ' \
                                               f'{player_data.get_dung_class_level(dung_class)}\n\n'

                                    desc += '===============\n\n:classical_building: 地下城等級 : \n\n'

                                    for dung in player_data.dung_level:
                                        print(f'Info > - {dung} : {player_data.get_dung_level(dung)}')

                                        dung_list = get_setting_json('dung_list')

                                        desc = f'{desc} - {dung_list[dung]} : ' \
                                               f'{player_data.get_dung_level(dung)}\n\n'

                                    embed = discord.Embed(
                                        title=f'{player_data.profile[profile_id]["cute_name"]} 已更新地下城',
                                        description=str(desc),
                                        color=0x00ff00
                                    )

                                    embed.set_author(
                                        name=inter.author.name,
                                        icon_url=inter.author.avatar_url
                                    )

                                    await inter.send(embed=embed)

                                else:
                                    embed = discord.Embed(
                                        title=f'驗證 {player_data.profile[profile_id]["cute_name"]} 失敗，請打開該島api',
                                        description=f'{player_data.profile[profile_id]["cute_name"]} -x-> Dungeoneer',
                                        color=0xe74c3c
                                    )

                                    embed.set_author(
                                        name=inter.author.name,
                                        icon_url=inter.author.avatar_url
                                    )

                                    await inter.send(embed=embed, delete_after=20.0)

                            except TypeError:
                                print('Error > fail at create index embed')

                        # give role
                        try:
                            for i in range(10):
                                if i < 5:
                                    role = discord.utils.get(inter.author.guild.roles, name=f'< {i}')

                                    await inter.author.remove_roles(role)

                                role = discord.utils.get(inter.author.guild.roles, name=f'{i} >')

                                await inter.author.remove_roles(role)
                            if player_dung_max_level >= 50:
                                role = discord.utils.get(inter.author.guild.roles,
                                                         name=get_setting_json('cata50'))

                                await inter.author.add_roles(role)

                            if player_dung_max_level >= 100 or player_dung_max_level < 0:
                                print('Error > No match role can give')

                                embed = discord.Embed(
                                    title='驗證失敗，目前沒有匹配身分組',
                                    description=f'{inter.author} -x-> Dungeoneer',
                                    color=0xe74c3c
                                )

                                embed.set_author(
                                    name=inter.author.name,
                                    icon_url=inter.author.avatar_url
                                )

                                await inter.send(embed=embed, delete_after=20.0)

                            else:
                                role = discord.utils.get(inter.author.guild.roles,
                                                         name=f'< {player_dung_max_level // 10}')

                                await inter.author.add_roles(role)

                                role = discord.utils.get(inter.author.guild.roles,
                                                         name=f'{player_dung_max_level % 10} >')

                                await inter.author.add_roles(role)

                        except KeyError:
                            print('Error > fail at give role')

                    except KeyError:
                        print('Error > The player do not open the social media')

                        embed = discord.Embed(
                            title='驗證失敗，請先打開 hypixel discord api',
                            description=f'{inter.author} -x-> Dungeoneer',
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
                        player_data.api['cause'] = 'player id is missing, try verify id first'

                    print(f'Error > fail reason : {player_data.api["cause"]}')

                    embed = discord.Embed(
                        title='驗證失敗，請稍後重試',
                        description=f'{inter.author} -x-> Dungeoneer\n\n原因 : {player_data.api["cause"]}',
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
                    description=f'{inter.author} -x-> Dungeoneer',
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

            await inter.send(embed=embed, delete_after=20.0)


def setup(pybot):
    pybot.add_cog(SlashVerifyDungeoneer(pybot))

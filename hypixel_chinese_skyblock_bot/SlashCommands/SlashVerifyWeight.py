import discord
from dislash import slash_command

from hypixel_chinese_skyblock_bot.Core.Common import CodExtension, get_hypixel_api, get_setting_json, \
    get_verify_id_list, get_senither_weight
from hypixel_chinese_skyblock_bot.Core.UserData import UserData


class SlashVerifyWeight(CodExtension):

    @slash_command(
        guild_ids=[int(get_setting_json('ServerId'))],
        name='verify_weight',
        description='Verify your weight',
    )
    async def verifyweight(self, inter):
        # check is in the desired channel.
        if inter.channel.id == get_setting_json('VerifyWeightChannelId'):
            embed = discord.Embed(
                title='正在向 hypixel api 提出訪問請求',
                color=0xf1c40f
            )

            embed.set_author(
                name=inter.author.name,
                icon_url=inter.author.avatar_url
            )

            message = await inter.send(embed=embed, ephemeral=True)

            # check is player has been verified
            if get_setting_json('VerifyIdRole') in [y.name.lower() for y in inter.author.roles]:
                player = get_verify_id_list(inter.author)

                player_data = UserData(player)

                player_data.api = get_hypixel_api(player)

                # try to call the cache in order to skip the api request cool down
                if not player_data.api['success']:
                    player_data.try_get_latest_user_api()

                    print('Info > 嘗試呼叫緩存')

                print(f'Info > verify player weight : {inter.author}')

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

                                    embed = discord.Embed(
                                        title=f'{player_data.profile[profile_id]["cute_name"]} 的 Weight',
                                        description=str(desc),
                                        color=0x00ff00
                                    )

                                    embed.set_author(
                                        name=inter.author.name,
                                        icon_url=inter.author.avatar_url
                                    )

                                    await message.edit(embed=embed)

                                else:
                                    print('Error > senither weight no respond')

                                    print(f'Error > fail reason : {weight["reason"]}')

                                    embed = discord.Embed(
                                        title='驗證失敗，請稍後重試',
                                        description=f'{inter.author} -x-> Weight\n\n'
                                                    f'原因 : {weight["reason"]}\n\n'
                                                    f'描述 : 請確保 Api 為開啟狀態',
                                        color=0xe74c3c
                                    )

                                    embed.set_author(
                                        name=inter.author.name,
                                        icon_url=inter.author.avatar_url
                                    )

                                    await message.edit(embed=embed, delete_after=20.0)

                            except KeyError:
                                print(f'Error > fail to get weight api in '
                                      f'{player_data.profile[profile_id]["cute_name"]}')

                        weight_require = get_setting_json('SkillWeightRequire')

                        if player_data.max_senither_weight >= weight_require:
                            print(f'Info > - skill weight > {weight_require}')

                            role = discord.utils.get(inter.author.guild.roles,
                                                     name=get_setting_json('SeniorPlayer'))

                            await inter.author.add_roles(role)

                            # try to create result output
                            try:
                                desc = f'你的最高 senither weight : ' \
                                       f'{player_data.max_senither_weight} >= {weight_require}, 符合申請資格'

                                embed = discord.Embed(
                                    title='已成功認證',
                                    description=str(desc),
                                    color=0x00ff00
                                )

                                embed.set_author(
                                    name=inter.author.name,
                                    icon_url=inter.author.avatar_url
                                )

                                await inter.send(embed=embed)

                            except TypeError:
                                print('Error > fail at create result embed')

                        else:
                            print('Info > nothing is verified')

                            desc = f'你的最高 senither weight : ' \
                                   f'{player_data.max_senither_weight} < {weight_require} , 不符合申請資格'

                            embed = discord.Embed(
                                title='你目前Weight未達標，請再接再厲',
                                description=desc,
                                color=0xe74c3c
                            )

                            embed.set_author(
                                name=inter.author.name,
                                icon_url=inter.author.avatar_url
                            )

                            await message.edit(embed=embed, delete_after=20.0)

                    except KeyError:
                        print('Error > The player do not open the social media')

                        embed = discord.Embed(
                            title='驗證失敗，請先打開 hypixel discord api',
                            description=f'{inter.author} -x-> Weight',
                            color=0xe74c3c
                        )

                        embed.set_author(
                            name=inter.author.name,
                            icon_url=inter.author.avatar_url
                        )

                        await message.edit(embed=embed, delete_after=20.0)
                else:
                    print('Error > Please wait a little bit and try again')

                    if 'cause' not in player_data.api:
                        player_data.api['cause'] = '玩家 id 綁定丟失，請更新 id (很可能是 nitro 導致編號變更)'

                    print(f'Error > fail reason : {player_data.api["cause"]}')

                    embed = discord.Embed(
                        title='驗證失敗，請稍後重試',
                        description=f'{inter.author} -x-> Weight\n\n原因 : {player_data.api["cause"]}',
                        color=0xe74c3c
                    )

                    embed.set_author(
                        name=inter.author.name,
                        icon_url=inter.author.avatar_url
                    )

                    await message.edit(embed=embed, delete_after=20.0)

            else:
                print('Error > Require verify id')

                embed = discord.Embed(
                    title='你未登記id，請先登記id',
                    description=f'{inter.author} -x-> Weight',
                    color=0xe74c3c
                )

                embed.set_author(
                    name=inter.author.name,
                    icon_url=inter.author.avatar_url
                )

                await message.edit(embed=embed, delete_after=20.0)

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
    pybot.add_cog(SlashVerifyWeight(pybot))

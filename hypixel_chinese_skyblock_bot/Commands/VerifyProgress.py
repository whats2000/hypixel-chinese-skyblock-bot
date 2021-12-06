import discord
from discord.ext import commands
from hypixel_chinese_skyblock_bot.Core.Common import CodExtension, get_hypixel_api, get_setting_json, \
    get_hypixel_skyblock_api, get_verify_id_list
from hypixel_chinese_skyblock_bot.Core.UserData import UserData


class VerifyProgress(CodExtension):

    @commands.command()
    async def verifyprog(self, ctx):
        # check is player has been verified
        if get_setting_json('VerifyIdRole') in [y.name.lower() for y in ctx.message.author.roles]:
            role = discord.utils.get(ctx.message.author.guild.roles, name=get_setting_json('ProgressRole'))

            await ctx.author.add_roles(role)

            player = get_verify_id_list(ctx.message.author)

            player_api = get_hypixel_api(player)

            print('> verify player progress : ' + str(ctx.message.author))

            # check get hypixel api is successes
            if player_api['success']:
                print('> get hypixel api success')

                # try to get profile data
                try:
                    player_uuid = player_api['player']['uuid']

                    player_profile = player_api['player']['stats']['SkyBlock']['profiles']

                    player_data = UserData(player)

                    # loop for checking all profile
                    for profileId in player_profile:
                        print('- 正在驗證'
                              + player_profile[profileId]['cute_name']
                              )

                        embed = discord.Embed(
                            title='驗證處理中',
                            description='正在驗證 -> '
                                        + player_profile[profileId]['cute_name'],
                            color=0xf1c40f
                        )

                        embed.set_author(
                            name=ctx.message.author.name,
                            icon_url=ctx.message.author.avatar_url
                        )

                        await ctx.send(embed=embed, delete_after=10.0)

                        # try to get skyblock api
                        try:
                            skyblock_api = get_hypixel_skyblock_api(profileId)

                            print('> get api success')

                            # check get skyblock api is successes
                            if skyblock_api['success']:

                                player_profile_api = skyblock_api['profile']['members'][player_uuid]

                                print('> get profileId success')

                                is_verify_pass = False

                                # try to get slayer level
                                try:
                                    # loop for checking all slayers
                                    for i in range(7, 10):
                                        # check if player achieve slayer level
                                        if 'level_' + str(i) in \
                                            (player_profile_api['slayer_bosses']['zombie']['claimed_levels'] and
                                             player_profile_api['slayer_bosses']['spider']['claimed_levels'] and
                                             player_profile_api['slayer_bosses']['wolf']['claimed_levels'] and
                                             player_profile_api['slayer_bosses']['enderman']['claimed_levels']):

                                            role = discord.utils.get(ctx.message.author.guild.roles,
                                                                     name=get_setting_json('AllSlayer' + str(i)))

                                            await ctx.author.add_roles(role)

                                            print('- slayer ' + str(i))

                                            player_data.set_slayer_level_is_max(i, True)

                                            # check if pass
                                            if not is_verify_pass:
                                                is_verify_pass = True

                                        else:
                                            print('- no slayer archive' + str(i))
                                except:
                                    print('> fail in verify slayer')

                                    embed = discord.Embed(
                                        title='驗證slayer失敗，連結API錯誤，請稍後重試',
                                        description='請卻保有打開skyblock中slayer訪問api\n\n'
                                                    + player_profile[profileId]['cute_name']
                                                    + ' -x-> Progress',
                                        color=0xe74c3c
                                    )

                                    embed.set_author(
                                        name=ctx.message.author.name,
                                        icon_url=ctx.message.author.avatar_url
                                    )

                                    await ctx.send(embed=embed, delete_after=20.0)

                                # try to get skill level
                                try:
                                    skill_list = get_setting_json('skill_list')

                                    # loop for checking all skill
                                    for skill in skill_list:
                                        skill_level = player_profile_api['experience_skill_' + skill]

                                        # check if player achieve max skill level
                                        if skill_level >= skill_list[skill]:
                                            role = discord.utils.get(ctx.message.author.guild.roles,
                                                                     name=get_setting_json('skill_' + skill))

                                            await ctx.author.add_roles(role)

                                            print('- ' + skill + ' : ' + str(skill_level) + ' is verified')

                                            player_data.set_skill_level_is_max(skill, True)

                                            # check if pass
                                            if not is_verify_pass:
                                                is_verify_pass = True

                                        else:
                                            print('- ' + skill + ' : ' + str(skill_level) + ' is not archive')
                                except:
                                    print('> fail in verify skill')

                                    embed = discord.Embed(
                                        title='驗證skill失敗，連結API錯誤，請稍後重試',
                                        description='請卻保有打開skyblock中skill訪問api\n\n'
                                                    + player_profile[profileId]['cute_name']
                                                    + ' -x-> Progress',
                                        color=0xe74c3c
                                    )

                                    embed.set_author(
                                        name=ctx.message.author.name,
                                        icon_url=ctx.message.author.avatar_url
                                    )

                                    await ctx.send(embed=embed, delete_after=20.0)

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

                                            desc = desc + str(get_setting_json('AllSlayer' + str(i))) + '\n\n'

                                        skill_list = get_setting_json('skill_list')

                                        # loop for checking all skill
                                        for skill in skill_list:
                                            boolean = player_data.get_skill_level_is_max(skill)

                                            # check if pass
                                            if boolean:
                                                desc += '\u2705 : '

                                            else:
                                                desc += '\u274c : '

                                            desc += str(get_setting_json('skill_' + skill)) + '\n\n'

                                        embed = discord.Embed(
                                            title=player_profile[profileId]['cute_name'] + ' 已更新進度',
                                            description=str(desc),
                                            color=0x00ff00
                                        )

                                        embed.set_author(
                                            name=ctx.message.author.name,
                                            icon_url=ctx.message.author.avatar_url
                                        )

                                        await ctx.send(embed=embed)

                                    except:
                                        print('> fail at create index embed')

                                    # try to create extra index output
                                    try:
                                        # loop for player all skill
                                        for skill in player_data.skillIsMax:
                                            # check player all skill is max
                                            if skill != 'carpentry' and not player_data.skillIsMax[skill]:
                                                print('- all skills arent max')
                                                break
                                        else:
                                            print('- all skills are max')

                                            role = discord.utils.get(ctx.message.author.guild.roles,
                                                                     name=get_setting_json('AllSkillMax'))

                                            await ctx.author.add_roles(role)

                                            embed = discord.Embed(
                                                title=player_profile[profileId]['cute_name'] + ' 已更新進度',
                                                description='\u2705 : '
                                                            + get_setting_json('AllSkillMax'),
                                                color=0x00ff00
                                            )

                                            embed.set_author(
                                                name=ctx.message.author.name,
                                                icon_url=ctx.message.author.avatar_url
                                            )

                                            await ctx.send(embed=embed)

                                    except:
                                        print('> fail at create extra embed')
                                else:
                                    print('> nothing is verified')

                                    embed = discord.Embed(
                                        title='你目前未有任何進度達標，請再接再厲',
                                        description=player_profile[profileId]['cute_name'] + ' -x-> Progress',
                                        color=0xe74c3c
                                    )

                                    embed.set_author(
                                        name=ctx.message.author.name,
                                        icon_url=ctx.message.author.avatar_url
                                    )

                                    await ctx.send(embed=embed, delete_after=20.0)

                            else:
                                print('>　Please wait a little bit and try again')

                                embed = discord.Embed(
                                    title='驗證失敗，請稍後重試',
                                    description=player_profile[profileId]['cute_name'] + ' -x-> Progress',
                                    color=0xe74c3c
                                )

                                embed.set_author(
                                    name=ctx.message.author.name,
                                    icon_url=ctx.message.author.avatar_url
                                )

                                await ctx.send(embed=embed, delete_after=20.0)

                        except:
                            print('> fail to get skyblock api in ' + str(player_profile[profileId]['cute_name']))

                except:
                    print('> The player do not open the social media')

                    embed = discord.Embed(
                        title='驗證失敗，請先打開 hypixel discord api',
                        description=str(ctx.message.author) + ' -x-> Progress',
                        color=0xe74c3c
                    )

                    embed.set_author(
                        name=ctx.message.author.name,
                        icon_url=ctx.message.author.avatar_url
                    )

                    await ctx.send(embed=embed, delete_after=20.0)
            else:
                print('> Please wait a little bit and try again')

                print('> fail reason : ' + player_api['cause'])

                embed = discord.Embed(
                    title='驗證失敗，請稍後重試',
                    description=str(ctx.message.author) + ' -x-> Progress\n\n' + '原因 : ' + player_api['cause'],
                    color=0xe74c3c
                )

                embed.set_author(
                    name=ctx.message.author.name,
                    icon_url=ctx.message.author.avatar_url
                )

                await ctx.send(embed=embed, delete_after=20.0)

        else:
            print('> Require verify id')

            embed = discord.Embed(
                title='你未登記id，請先登記id',
                description=str(ctx.message.author) + ' -x-> Progress',
                color=0xe74c3c
            )

            embed.set_author(
                name=ctx.message.author.name,
                icon_url=ctx.message.author.avatar_url
            )

            await ctx.send(embed=embed, delete_after=20.0)

        await ctx.message.delete()


def setup(pybot):
    pybot.add_cog(VerifyProgress(pybot))

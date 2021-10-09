import json
import os

import discord
from discord.ext import commands
from hypixel_chinese_skyblock_bot.Core.Common import CodExtension, get_hypixel_api, get_setting_json, \
    get_hypixel_skyblock_api, get_verify_id_list
from hypixel_chinese_skyblock_bot.Core.UserData import UserData


class VerifyProgress(CodExtension):

    @commands.command()
    async def verifyprog(self, ctx):
        if get_setting_json('VerifyIdRole') in [y.name.lower() for y in ctx.message.author.roles]:
            role = discord.utils.get(ctx.message.author.guild.roles, name=get_setting_json('ProgressRole'))

            await ctx.author.add_roles(role)

            player = get_verify_id_list(ctx.message.author)

            playerApi = get_hypixel_api(player)

            print('> verify player progress : ' + str(ctx.message.author))

            if playerApi['success']:
                try:
                    playerUUID = playerApi['player']['uuid']

                    playerProfile = playerApi['player']['stats']['SkyBlock']['profiles']

                    playerData = UserData(player)

                    for profileId in playerProfile:
                        print('- 正在驗證'
                              + playerProfile[profileId]['cute_name']
                              )

                        embed = discord.Embed(
                            title='驗證處理中',
                            description='正在驗證 -> '
                                        + playerProfile[profileId]['cute_name'],
                            color=0xf1c40f
                        )

                        embed.set_author(
                            name=ctx.message.author.name,
                            icon_url=ctx.message.author.avatar_url
                        )

                        await ctx.send(embed=embed, delete_after=10.0)

                        try:
                            skyblockApi = get_hypixel_skyblock_api(profileId)

                            print('> get api success')

                            if skyblockApi['success']:

                                api = skyblockApi['profile']['members'][playerUUID]

                                print('> get profileId success')

                                isVerifyPass = False

                                try:
                                    for i in range(7, 10):
                                        if 'level_' + str(i) in (api['slayer_bosses']['zombie']['claimed_levels'] and
                                                         api['slayer_bosses']['spider']['claimed_levels'] and
                                                         api['slayer_bosses']['wolf']['claimed_levels'] and
                                                         api['slayer_bosses']['enderman']['claimed_levels']):

                                            role = discord.utils.get(ctx.message.author.guild.roles,
                                                                     name=get_setting_json('AllSlayer' + str(i)))

                                            await ctx.author.add_roles(role)

                                            print('- slayer ' + str(i))

                                            playerData.set_slayer_level(i, True)

                                            if not isVerifyPass:
                                                isVerifyPass = True

                                        else:
                                            print('- no slayer archive' + str(i))
                                except:
                                    print('> fail in verify slayer')

                                    embed = discord.Embed(
                                        title='驗證slayer失敗，連結API錯誤，請稍後重試',
                                        description='請卻保有打開skyblock中slayer訪問api\n\n'
                                                    + playerProfile[profileId]['cute_name']
                                                    + ' -x-> Progress',
                                        color=0xe74c3c
                                    )

                                    embed.set_author(
                                        name=ctx.message.author.name,
                                        icon_url=ctx.message.author.avatar_url
                                    )

                                    await ctx.send(embed=embed, delete_after=20.0)

                                try:
                                    skillList = get_setting_json('skill_list')

                                    for skill in skillList:
                                        skillLevel = api['experience_skill_' + skill]

                                        if skillLevel >= skillList[skill]:
                                            role = discord.utils.get(ctx.message.author.guild.roles,
                                                                     name=get_setting_json('skill_' + skill))

                                            await ctx.author.add_roles(role)

                                            print('- ' + skill + ' : ' + str(skillLevel) + ' is verified')

                                            playerData.set_skill_level(skill, True)

                                            if not isVerifyPass:
                                                isVerifyPass = True

                                        else:
                                            print('- ' + skill + ' : ' + str(skillLevel) + ' is not archive')
                                except :
                                    print('> fail in verify skill')

                                    embed = discord.Embed(
                                        title='驗證skill失敗，連結API錯誤，請稍後重試',
                                        description='請卻保有打開skyblock中skill訪問api\n\n'
                                                    + playerProfile[profileId]['cute_name']
                                                    + ' -x-> Progress',
                                        color=0xe74c3c
                                    )

                                    embed.set_author(
                                        name=ctx.message.author.name,
                                        icon_url=ctx.message.author.avatar_url
                                    )

                                    await ctx.send(embed=embed, delete_after=20.0)

                                if isVerifyPass:
                                    try:
                                        desc = ''

                                        for i in range(7, 10):
                                            boolean = playerData.get_slayer_level(i)

                                            if boolean:
                                                desc += '\u2705 : '

                                            else:
                                                desc += '\u274c : '

                                            desc = desc + str(get_setting_json('AllSlayer' + str(i))) + '\n\n'

                                        skillList = get_setting_json('skill_list')

                                        for skill in skillList:
                                            boolean = playerData.get_skill_level(skill)

                                            if boolean:
                                                desc += '\u2705 : '

                                            else:
                                                desc += '\u274c : '

                                            desc += str(get_setting_json('skill_' + skill)) + '\n\n'

                                        embed = discord.Embed(
                                            title=playerProfile[profileId]['cute_name']
                                                  + ' 已更新進度',
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
                                else:
                                    print('> nothing is verified')

                                    embed = discord.Embed(
                                        title='你目前未有任何進度達標，請再接再厲',
                                        description=playerProfile[profileId]['cute_name']
                                                    + ' -x-> Progress',
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
                                    description=playerProfile[profileId]['cute_name']
                                                + ' -x-> Progress',
                                    color=0xe74c3c
                                )

                                embed.set_author(
                                    name=ctx.message.author.name,
                                    icon_url=ctx.message.author.avatar_url
                                )

                                await ctx.send(embed=embed, delete_after=20.0)

                        except:
                            print('> fail to get skyblock api in ' + str(playerProfile[profileId]['cute_name']))

                except:
                    print('＞　The player do not open the social media')

                    embed = discord.Embed(
                        title='驗證失敗，請先打開discord api',
                        description=str(ctx.message.author)
                                    + ' -x-> Progress',
                        color=0xe74c3c
                    )

                    embed.set_author(
                        name=ctx.message.author.name,
                        icon_url=ctx.message.author.avatar_url
                    )

                    await ctx.send(embed=embed, delete_after=20.0)
            else:
                print('> Please wait a little bit and try again')

                embed = discord.Embed(
                    title='驗證失敗，請稍後重試',
                    description=str(ctx.message.author)
                                + ' -x-> Progress',
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
                description=str(ctx.message.author)
                            + ' -x-> Progress',
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

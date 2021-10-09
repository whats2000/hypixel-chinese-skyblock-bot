import json
import os

import discord
from discord.ext import commands
from hypixel_chinese_skyblock_bot.Core.Common import Cod_Extension, get_hypixel_api, get_setting_json, \
    get_hypixel_skyblock_api


class VerifyProgress(Cod_Extension):

    @commands.command()
    async def verifyprog(self, ctx):
        if get_setting_json('VerifyIdRole') in [y.name.lower() for y in ctx.message.author.roles]:
            role = discord.utils.get(ctx.message.author.guild.roles, name=get_setting_json('ProgressRole'))

            await ctx.author.add_roles(role)

            with open(os.getcwd()
                      + '/Resources/VerifyIdList.json',
                      mode='r',
                      encoding='utf8'
                      ) as VerifyIdListJson:
                VerifyIdListJsonData = json.load(VerifyIdListJson)

            try:
                player = VerifyIdListJsonData[str(ctx.message.author)]

            except:
                print('player not found')
                player = ''

            playerApi = get_hypixel_api(player)

            print('verify player progress : ' + str(ctx.message.author))

            if playerApi['success']:
                try:
                    playerProfile = playerApi['player']['stats']['SkyBlock']['profiles']

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

                        skyblockApi = get_hypixel_skyblock_api(profileId)

                        if skyblockApi['success']:

                            api = skyblockApi['profile']['members'][profileId]

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

                                        embed = discord.Embed(
                                            title='成功驗證進度',
                                            description=str(ctx.message.author)
                                                        + ' ---> slayer'
                                                        + str(i),
                                            color=0x00ff00
                                        )

                                        embed.set_author(
                                            name=ctx.message.author.name,
                                            icon_url=ctx.message.author.avatar_url
                                        )

                                        await ctx.send(embed=embed)

                                    else:
                                        print('-no slayer archive' + str(i))
                            except:
                                print('fail in verify slayer')

                                embed = discord.Embed(
                                    title='驗證失敗，連結API錯誤，請稍後重試',
                                    description=str(ctx.message.author)
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
                                    if api['experience_skill_' + skill] >= skillList[skill]:
                                        role = discord.utils.get(ctx.message.author.guild.roles,
                                                                 name=get_setting_json('skill_' + skill))

                                        await ctx.author.add_roles(role)

                                        print('- ' + skill + 'is verified')

                                        embed = discord.Embed(
                                            title='成功驗證進度',
                                            description=str(ctx.message.author)
                                                        + ' ---> '
                                                        + str(skill),
                                            color=0x00ff00
                                        )

                                        embed.set_author(
                                            name=ctx.message.author.name,
                                            icon_url=ctx.message.author.avatar_url
                                        )

                                        await ctx.send(embed=embed)

                                    else:
                                        print('- ' + skill + ' is not archive')
                            except :
                                print('fail in verify skill')

                                embed = discord.Embed(
                                    title='驗證失敗，連結API錯誤，請稍後重試',
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
                            print('Please wait a little bit and try again')

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

                except:
                    print('The player do not open the social media')

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
                print('Please wait a little bit and try again')

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
            print('Require verify id')

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

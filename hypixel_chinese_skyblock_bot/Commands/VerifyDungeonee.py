import json
import os

import discord
from discord.ext import commands
from hypixel_chinese_skyblock_bot.Core.Common import CodExtension, get_hypixel_api, get_setting_json, \
    get_verify_id_list, get_hypixel_skyblock_api
from hypixel_chinese_skyblock_bot.Core.UserData import UserData


class VerifyDungeoneer(CodExtension):

    @commands.command()
    async def verifydung(self, ctx):
        if get_setting_json('VerifyIdRole') in [y.name.lower() for y in ctx.message.author.roles]:
            role = discord.utils.get(ctx.message.author.guild.roles, name=get_setting_json('DungeoneerRole'))

            await ctx.author.add_roles(role)

            player = get_verify_id_list(ctx.message.author)

            playerApi = get_hypixel_api(player)

            print('> verify player dungeoneer : ' + str(ctx.message.author))

            if playerApi['success']:
                print('> get hypixel api success')

                try:
                    playerDungMaxLevel = playerApi['player']['achievements']['skyblock_dungeoneer']

                    print('- ' + str(playerDungMaxLevel))

                    playerUUID = playerApi['player']['uuid']

                    playerProfile = playerApi['player']['stats']['SkyBlock']['profiles']

                    for profileId in playerProfile:
                        print('- 正在驗證'
                              + playerProfile[profileId]['cute_name']
                              )

                        playerData = UserData(player)

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
                                dungApi = skyblockApi['profile']['members'][playerUUID]['dungeons']

                                try:
                                    for dungClass in dungApi['player_classes']:
                                        classExp = dungApi['player_classes'][dungClass]['experience']

                                        print('- ' + dungClass + ' : ' + str(classExp))

                                        playerData.set_dung_class_level(dungClass, classExp)

                                        classLevel = playerData.get_dung_class_level(dungClass)

                                        if classLevel > playerDungMaxLevel:
                                            playerDungMaxLevel = classLevel

                                except:
                                    print('> fail at get class level')

                                try:
                                    for i in range(10):
                                        if i < 5:
                                            i = str(i)

                                            role = discord.utils.get(ctx.message.author.guild.roles, name='< ' + i)

                                            await ctx.author.remove_roles(role)

                                        i = str(i)

                                        role = discord.utils.get(ctx.message.author.guild.roles, name=i + ' >')

                                        await ctx.author.remove_roles(role)
                                    if playerDungMaxLevel >= 50:
                                        role = discord.utils.get(ctx.message.author.guild.roles,
                                                                 name=get_setting_json('cata50'))

                                        await ctx.author.add_roles(role)

                                    else:
                                        role = discord.utils.get(ctx.message.author.guild.roles,
                                                                 name='< ' + str(playerDungMaxLevel // 10))

                                        await ctx.author.add_roles(role)

                                        role = discord.utils.get(ctx.message.author.guild.roles,
                                                                 name=str(playerDungMaxLevel % 10) + ' >')

                                        await ctx.author.add_roles(role)

                                except:
                                    print('> fail at give role')

                                try:
                                    for dung in playerData.dungLevel:
                                        dungExp = dungApi['dungeon_types'][dung]['experience']

                                        print('- ' + dung + ' : ' + str(dungExp))

                                        playerData.set_dung_level(dung, dungExp)

                                except:
                                    print('> fail at get dung level')

                            else:
                                print('>　Please wait a little bit and try again')

                                embed = discord.Embed(
                                    title='驗證失敗，請稍後重試',
                                    description=playerProfile[profileId]['cute_name']
                                                + ' -x-> Dungeoneer',
                                    color=0xe74c3c
                                )

                                embed.set_author(
                                    name=ctx.message.author.name,
                                    icon_url=ctx.message.author.avatar_url
                                )

                                await ctx.send(embed=embed, delete_after=20.0)

                        except:
                            print('> fail to get skyblock api in ' + str(playerProfile[profileId]['cute_name']))

                        try:
                            desc = ':trophy: 最高職業等級 : ' \
                                   + str(playerDungMaxLevel) \
                                   + '\n\n===============\n\n:island: 島嶼職業等級 :\n\n'

                            for dungClass in playerData.dungClassLevel:
                                print('- '
                                      + dungClass
                                      + ' : '
                                      + str(playerData.get_dung_class_level(dungClass)))

                                dungClassList = get_setting_json('dung_class_list')

                                desc = desc \
                                       + ' - ' \
                                       + dungClassList[dungClass] \
                                       + ' : ' \
                                       + str(playerData.get_dung_class_level(dungClass)) \
                                       + '\n\n'

                            desc += '===============\n\n:classical_building: 地下城等級 : \n\n'

                            for dung in playerData.dungLevel:
                                print(dung
                                      + ' : '
                                      + str(playerData.get_dung_level(dung)))

                                dungList = get_setting_json('dung_list')

                                desc = desc \
                                       + ' - ' \
                                       + dungList[dung] \
                                       + ' : ' \
                                       + str(playerData.get_dung_level(dung)) \
                                       + '\n\n'

                            embed = discord.Embed(
                                title=playerProfile[profileId]['cute_name']
                                      + ' 已更新地下城',
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

                except:
                    print('> The player do not open the social media')

                    embed = discord.Embed(
                        title='驗證失敗，請先打開 hypixel discord api',
                        description=str(ctx.message.author)
                                    + ' -x-> Dungeoneer',
                        color=0xe74c3c
                    )

                    embed.set_author(
                        name=ctx.message.author.name,
                        icon_url=ctx.message.author.avatar_url
                    )

                    await ctx.send(embed=embed, delete_after=20.0)
            else:
                print('> Please wait a little bit and try again')

                print('> fail reason : ' + playerApi['cause'])

                embed = discord.Embed(
                    title='驗證失敗，請稍後重試',
                    description=str(ctx.message.author)
                                + ' -x-> Dungeoneer\n\n'
                                + '原因 : '
                                + playerApi['cause'],
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
                            + ' -x-> Dungeoneer',
                color=0xe74c3c
            )

            embed.set_author(
                name=ctx.message.author.name,
                icon_url=ctx.message.author.avatar_url
            )

            await ctx.send(embed=embed, delete_after=20.0)

        await ctx.message.delete()


def setup(pybot):
    pybot.add_cog(VerifyDungeoneer(pybot))

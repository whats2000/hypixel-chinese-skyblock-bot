import json
import os

import discord
from discord.ext import commands
from hypixel_chinese_skyblock_bot.Core.Common import Cod_Extension, get_hypixel_api, get_setting_json


class VerifyId(Cod_Extension):

    @commands.command()
    async def verifyid(self, ctx, args):
        if get_setting_json('VerifyIdRole') not in [y.name.lower() for y in ctx.message.author.roles]:
            playerApi = get_hypixel_api(args)

            print('verify player user : ' + str(ctx.message.author))

            if playerApi['success']:
                try:
                    playerDisord = playerApi['player']['socialMedia']['links']['DISCORD']

                    if str(ctx.message.author) == playerDisord:
                        print('- Verify Id success')

                        embed = discord.Embed(
                            title='成功驗證',
                            description=str(ctx.message.author)
                                        + ' ---> '
                                        + args,
                            color=0x00ff00
                        )

                        embed.set_author(
                            name=ctx.message.author.name,
                            icon_url=ctx.message.author.avatar_url
                        )

                        await ctx.send(embed=embed)

                        role = discord.utils.get(ctx.message.author.guild.roles, name=get_setting_json('VerifyIdRole'))

                        await ctx.author.add_roles(role)

                        with open(os.getcwd()
                             + '/Resources/VerifyIdList.json',
                             mode='r',
                             encoding='utf8'
                             ) as VerifyIdListJson:
                            VerifyIdListJsonData = json.load(VerifyIdListJson)

                        VerifyIdListJson.close()

                        outputJson = VerifyIdListJsonData

                        outputJson[str(ctx.message.author)] = args

                        outputJson = json.dumps(outputJson, ensure_ascii=False, indent=4)

                        with open(os.getcwd()
                             + '/Resources/VerifyIdList.json',
                             mode='w',
                             encoding='utf8'
                             ) as outJson:
                            outJson.write(outputJson)

                        outJson.close()
                    else:
                        print('Player not found')

                        embed = discord.Embed(
                            title='驗證失敗，玩家id不正確',
                            description=str(ctx.message.author)
                                        + ' -x-> '
                                        + args,
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
                                    + ' -x-> '
                                    + args,
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
                                + ' -x-> '
                                + args,
                    color=0xe74c3c
                )

                embed.set_author(
                    name=ctx.message.author.name,
                    icon_url=ctx.message.author.avatar_url
                )

                await ctx.send(embed=embed, delete_after=20.0)

        else:
            print('Has already verified')

            embed = discord.Embed(
                title='你已經驗證，更新請用sb?verifyidupdate',
                description=str(ctx.message.author)
                            + ' -x-> '
                            + args,
                color=0xe74c3c
            )

            embed.set_author(
                name=ctx.message.author.name,
                icon_url=ctx.message.author.avatar_url
            )

            await ctx.send(embed=embed, delete_after=20.0)

        await ctx.message.delete()

    @commands.command()
    async def verifyidupdate(self, ctx, args):
        playerApi = get_hypixel_api(args)

        print('update player user : ' + str(ctx.message.author))

        if get_setting_json('VerifyIdRole') in [y.name.lower() for y in ctx.message.author.roles]:
            if playerApi['success']:
                try:
                    playerDisord = playerApi['player']['socialMedia']['links']['DISCORD']

                    if str(ctx.message.author) == playerDisord:
                        print('update Id success')

                        embed = discord.Embed(
                            title='成功更新',
                            description=str(ctx.message.author)
                                        + ' ---> '
                                        + args,
                            color=0x00ff00
                        )

                        embed.set_author(
                            name=ctx.message.author.name,
                            icon_url=ctx.message.author.avatar_url
                        )

                        await ctx.send(embed=embed)

                        with open(os.getcwd()
                                  + '/Resources/VerifyIdList.json',
                                  mode='r',
                                  encoding='utf8'
                                  ) as VerifyIdListJson:
                            VerifyIdListJsonData = json.load(VerifyIdListJson)

                        VerifyIdListJson.close()

                        outputJson = VerifyIdListJsonData

                        outputJson[str(ctx.message.author)] = args

                        outputJson = json.dumps(outputJson, ensure_ascii=False, indent=4)

                        with open(os.getcwd()
                                  + '/Resources/VerifyIdList.json',
                                  mode='w',
                                  encoding='utf8'
                                  ) as outJson:
                            outJson.write(outputJson)

                        outJson.close()

                    else:
                        print('Player not found')

                        embed = discord.Embed(
                            title='驗證失敗，玩家id不正確',
                            description=str(ctx.message.author)
                                        + ' -x-> '
                                        + args,
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
                                    + ' -x-> '
                                    + args,
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
                                + ' -x-> '
                                + args,
                    color=0xe74c3c
                )

                embed.set_author(
                    name=ctx.message.author.name,
                    icon_url=ctx.message.author.avatar_url
                )

                await ctx.send(embed=embed, delete_after=20.0)

        await ctx.message.delete()

def setup(pybot):
    pybot.add_cog(VerifyId(pybot))

import json
import os

import discord
from discord.ext import commands
from hypixel_chinese_skyblock_bot.Core.Common import CodExtension, get_hypixel_api, get_setting_json, get_verify_id_list


class VerifyDungeoneer(CodExtension):

    @commands.command()
    async def verifydung(self, ctx):
        if get_setting_json('VerifyIdRole') in [y.name.lower() for y in ctx.message.author.roles]:
            role = discord.utils.get(ctx.message.author.guild.roles, name=get_setting_json('DungeoneerRole'))

            await ctx.author.add_roles(role)

            player = get_verify_id_list(ctx.message.author)

            playerApi = get_hypixel_api(player)

            print('verify player dungeoneer : ' + str(ctx.message.author))

            if playerApi['success']:
                try:
                    playerDung = playerApi['player']['achievements']['skyblock_dungeoneer']

                    print('- ' + playerDung)

                    for i in range(10):
                        if i < 5:
                            i = str(i)

                            role = discord.utils.get(ctx.message.author.guild.roles, name='< ' + i)

                            await ctx.author.remove_roles(role)

                        i = str(i)

                        role = discord.utils.get(ctx.message.author.guild.roles, name=i + ' >')

                        await ctx.author.remove_roles(role)
                    if playerDung >= 50:
                        role = discord.utils.get(ctx.message.author.guild.roles, name=get_setting_json('cata50'))

                        await ctx.author.add_roles(role)

                    else:
                        role = discord.utils.get(ctx.message.author.guild.roles, name='< ' + str(playerDung // 10))

                        await ctx.author.add_roles(role)

                        role = discord.utils.get(ctx.message.author.guild.roles, name=str(playerDung % 10) + ' >')

                        await ctx.author.add_roles(role)

                    embed = discord.Embed(
                        title='成功驗證地下城等級',
                        description=str(ctx.message.author)
                                    + ' ---> '
                                    + str(playerDung),
                        color=0x00ff00
                    )

                    embed.set_author(
                        name=ctx.message.author.name,
                        icon_url=ctx.message.author.avatar_url
                    )

                    await ctx.send(embed=embed)

                except:
                    print('The player do not open the social media')

                    embed = discord.Embed(
                        title='驗證失敗，請先打開discord api',
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
                print('Please wait a little bit and try again')

                embed = discord.Embed(
                    title='驗證失敗，請稍後重試',
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
            print('Require verify id')

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
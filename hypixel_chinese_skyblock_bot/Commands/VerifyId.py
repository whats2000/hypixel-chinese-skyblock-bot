import discord
from discord.ext import commands
from hypixel_chinese_skyblock_bot.Core.Common import CodExtension, get_hypixel_api, get_setting_json, set_user_id, \
    get_verify_id_list
from hypixel_chinese_skyblock_bot.Core.UserData import UserData


class VerifyId(CodExtension):

    @commands.command()
    async def verifyid(self, ctx, args=None):
        # check is in the desired channel.
        if ctx.channel.id == get_setting_json('VerifyIdChannelId'):
            # check is player input its id
            if args is not None:
                # check is player has been verified
                if get_setting_json('VerifyIdRole') not in [y.name.lower() for y in ctx.message.author.roles]:
                    player = get_verify_id_list(ctx.message.author)

                    player_data = UserData(player)

                    player_data.api = get_hypixel_api(args)

                    print(f'Info > verify player user : {ctx.message.author}')

                    # check get hypixel api is successes
                    if player_data.api['success']:
                        print('Info > get hypixel api success')

                        player_data.set_latest_user_api()

                        # try to get player social media discord
                        try:
                            player_data.discord = player_data.api['player']['socialMedia']['links']['DISCORD']

                            # check user name is correct in api
                            if str(ctx.message.author) == player_data.discord:
                                set_user_id(ctx.message.author, player_data.api['player']['displayname'])

                                print('Info > Verify Id success')

                                embed = discord.Embed(
                                    title='成功驗證',
                                    description=f'{ctx.message.author} ---> {player_data.api["player"]["displayname"]}',
                                    color=0x00ff00
                                )

                                embed.set_author(
                                    name=ctx.message.author.name,
                                    icon_url=ctx.message.author.avatar_url
                                )

                                await ctx.send(embed=embed)

                                role = discord.utils.get(ctx.message.author.guild.roles,
                                                         name=get_setting_json('VerifyIdRole'))

                                await ctx.author.add_roles(role)

                            else:
                                print('Error > Player not found')

                                embed = discord.Embed(
                                    title='驗證失敗，玩家id不正確',
                                    description=f'{ctx.message.author} -x-> {args}',
                                    color=0xe74c3c
                                )

                                embed.set_author(
                                    name=ctx.message.author.name,
                                    icon_url=ctx.message.author.avatar_url
                                )

                                await ctx.send(embed=embed, delete_after=20.0)
                        except KeyError:
                            print('Error > The player do not open the social media')

                            embed = discord.Embed(
                                title='驗證失敗，請先打開discord api',
                                description=f'{ctx.message.author} -x-> {args}',
                                color=0xe74c3c
                            )

                            embed.set_author(
                                name=ctx.message.author.name,
                                icon_url=ctx.message.author.avatar_url
                            )

                            await ctx.send(embed=embed, delete_after=20.0)
                    else:
                        print('Error > Please wait a little bit and try again')

                        embed = discord.Embed(
                            title='驗證失敗，請稍後重試',
                            description=f'{ctx.message.author} -x-> {args}',
                            color=0xe74c3c
                        )

                        embed.set_author(
                            name=ctx.message.author.name,
                            icon_url=ctx.message.author.avatar_url
                        )

                        await ctx.send(embed=embed, delete_after=20.0)

                else:
                    print('Error > Has already verified')

                    embed = discord.Embed(
                        title='你已經驗證，更新請用sb?verifyidupdate',
                        description=f'{ctx.message.author} -x-> {args}',
                        color=0xe74c3c
                    )

                    embed.set_author(
                        name=ctx.message.author.name,
                        icon_url=ctx.message.author.avatar_url
                    )

                    await ctx.send(embed=embed, delete_after=20.0)

            else:
                print('Error > Required id')

                embed = discord.Embed(
                    title='你需要在指令後方加上自己的 id',
                    description=f'{ctx.message.author} -x-> ?',
                    color=0xe74c3c
                )

                embed.set_author(
                    name=ctx.message.author.name,
                    icon_url=ctx.message.author.avatar_url
                )

                await ctx.send(embed=embed, delete_after=20.0)
        else:
            print('Error > Wrong channel')

            embed = discord.Embed(
                title='請在正確頻道輸入',
                color=0xe74c3c
            )

            embed.set_author(
                name=ctx.message.author.name,
                icon_url=ctx.message.author.avatar_url
            )

            await ctx.send(embed=embed, delete_after=20.0)

        await ctx.message.delete()

    @commands.command()
    async def verifyidupdate(self, ctx, args=None):
        # check is in the desired channel.
        if ctx.channel.id == get_setting_json('VerifyIdChannelId'):
            # check is player input its id
            if args is not None:
                player = get_verify_id_list(ctx.message.author)

                player_data = UserData(player)

                player_data.api = get_hypixel_api(args)

                print(f'Info > update player user : {ctx.message.author}')

                # check is player has been verified
                if get_setting_json('VerifyIdRole') in [y.name.lower() for y in ctx.message.author.roles]:
                    # check get hypixel api is successes
                    if player_data.api['success']:
                        print('Info > get hypixel api success')

                        player_data.set_latest_user_api()

                        # try to get player social media discord
                        try:
                            player_data.discord = player_data.api['player']['socialMedia']['links']['DISCORD']

                            # check user name is correct in api
                            if str(ctx.message.author) == player_data.discord:
                                set_user_id(ctx.message.author, player_data.api['player']["displayname"])

                                print('Info > update Id success')

                                embed = discord.Embed(
                                    title='成功更新',
                                    description=f'{ctx.message.author} ---> {player_data.api["player"]["displayname"]}',
                                    color=0x00ff00
                                )

                                embed.set_author(
                                    name=ctx.message.author.name,
                                    icon_url=ctx.message.author.avatar_url
                                )

                                await ctx.send(embed=embed)

                            else:
                                print('Error > Player not found')

                                embed = discord.Embed(
                                    title='驗證失敗，玩家id不正確',
                                    description=f'{ctx.message.author} -x-> {args}',
                                    color=0xe74c3c
                                )

                                embed.set_author(
                                    name=ctx.message.author.name,
                                    icon_url=ctx.message.author.avatar_url
                                )

                                await ctx.send(embed=embed, delete_after=20.0)
                        except KeyError:
                            print('Error > The player do not open the social media')

                            embed = discord.Embed(
                                title='驗證失敗，請先打開 hypixel discord api',
                                description=f'{ctx.message.author} -x-> {args}',
                                color=0xe74c3c
                            )

                            embed.set_author(
                                name=ctx.message.author.name,
                                icon_url=ctx.message.author.avatar_url
                            )

                            await ctx.send(embed=embed, delete_after=20.0)
                    else:
                        print('Error >　Please wait a little bit and try again')

                        print(f'Error > fail reason : {player_data.api["cause"]}')

                        embed = discord.Embed(
                            title='驗證失敗，請稍後重試',
                            description=f'{ctx.message.author} -x-> {args}\n\n原因 : {player_data.api["cause"]}',
                            color=0xe74c3c
                        )

                        embed.set_author(
                            name=ctx.message.author.name,
                            icon_url=ctx.message.author.avatar_url
                        )

                        await ctx.send(embed=embed, delete_after=20.0)

            else:
                print('Error > Required id')

                embed = discord.Embed(
                    title='你需要在指令後方加上自己的 id',
                    description=f'{ctx.message.author} -x-> ?',
                    color=0xe74c3c
                )

                embed.set_author(
                    name=ctx.message.author.name,
                    icon_url=ctx.message.author.avatar_url
                )

                await ctx.send(embed=embed, delete_after=20.0)

        else:
            print('Error > Wrong channel')

            embed = discord.Embed(
                title='請在正確頻道輸入',
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

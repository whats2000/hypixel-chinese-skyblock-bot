import discord
from dislash import slash_command, OptionType
from dislash.slash_commands import Option
from hypixel_chinese_skyblock_bot.Core.Common import CodExtension, get_hypixel_api, get_setting_json, set_user_id, \
    get_verify_id_list
from hypixel_chinese_skyblock_bot.Core.UserData import UserData


class SlashVerifyId(CodExtension):

    @slash_command(
        guild_ids=[int(get_setting_json('ServerId'))],
        name="verify_id",
        description="Link your discord to your minecraft account",
        options=[
            Option(
                name='user_id',
                description='Input your user id here. You have to open up the social media in hypixel',
                type=OptionType.STRING,
                required=True
            )
        ]
    )
    async def verifyid(self, inter, user_id=None):
        # check is in the desired channel.
        if inter.channel.id == get_setting_json('VerifyIdChannelId'):
            # check is user id input correctly
            if user_id is not None:
                # check is player has been verified
                if get_setting_json('VerifyIdRole') not in [y.name.lower() for y in inter.author.roles]:
                    player = get_verify_id_list(inter.author)

                    player_data = UserData(player)

                    player_data.api = get_hypixel_api(user_id)

                    print('> verify player user : ' + str(inter.author))

                    # check get hypixel api is successes
                    if player_data.api['success']:
                        player_data.set_latest_user_api()

                        # try to get player social media discord
                        try:
                            player_data.discord = player_data.api['player']['socialMedia']['links']['DISCORD']

                            # check user name is correct in api
                            if str(inter.author) == player_data.discord:
                                set_user_id(inter.author, user_id)

                                print('- Verify Id success')

                                embed = discord.Embed(
                                    title='成功驗證',
                                    description=str(inter.author) + ' ---> ' + user_id,
                                    color=0x00ff00
                                )

                                embed.set_author(
                                    name=inter.author.name,
                                    icon_url=inter.author.avatar_url
                                )

                                await inter.send(embed=embed)

                                role = discord.utils.get(inter.author.guild.roles,
                                                         name=get_setting_json('VerifyIdRole')
                                                         )

                                await inter.author.add_roles(role)

                            else:
                                print('> Player not found')

                                embed = discord.Embed(
                                    title='驗證失敗，玩家id不正確',
                                    description=str(inter.author) + ' -x-> ' + user_id,
                                    color=0xe74c3c
                                )

                                embed.set_author(
                                    name=inter.author.name,
                                    icon_url=inter.author.avatar_url
                                )

                                await inter.send(embed=embed, delete_after=20.0)
                        except KeyError:
                            print('> The player do not open the social media')

                            embed = discord.Embed(
                                title='驗證失敗，請先打開discord api',
                                description=str(inter.author) + ' -x-> ' + user_id,
                                color=0xe74c3c
                            )

                            embed.set_author(
                                name=inter.author.name,
                                icon_url=inter.author.avatar_url
                            )

                            await inter.send(embed=embed, delete_after=20.0)
                    else:
                        print('> Please wait a little bit and try again')

                        embed = discord.Embed(
                            title='驗證失敗，請稍後重試',
                            description=str(inter.author) + ' -x-> ' + user_id,
                            color=0xe74c3c
                        )

                        embed.set_author(
                            name=inter.author.name,
                            icon_url=inter.author.avatar_url
                        )

                        await inter.send(embed=embed, delete_after=20.0)

                else:
                    print('> Has already verified')

                    embed = discord.Embed(
                        title='你已經驗證，更新請用sb?verifyidupdate',
                        description=str(inter.author) + ' -x-> ' + user_id,
                        color=0xe74c3c
                    )

                    embed.set_author(
                        name=inter.author.name,
                        icon_url=inter.author.avatar_url
                    )

                    await inter.send(embed=embed, delete_after=20.0)

            else:
                print('>　Input id is incorrect')

                embed = discord.Embed(
                    title='驗證失敗，請稍後重試',
                    description=str(inter.author) + ' -x-> ' + str(user_id),
                    color=0xe74c3c
                )

                embed.set_author(
                    name=inter.author.name,
                    icon_url=inter.author.avatar_url
                )

                await inter.send(embed=embed, delete_after=20.0)

        else:
            print('> Wrong channel')

            embed = discord.Embed(
                title='請在正確頻道輸入',
                color=0xe74c3c
            )

            embed.set_author(
                name=inter.author.name,
                icon_url=inter.author.avatar_url
            )

            await inter.send(embed=embed, delete_after=20.0)

    @slash_command(
        guild_ids=[int(get_setting_json('ServerId'))],
        name="verify_id_update",
        description="Update your discord to your minecraft account",
        options=[
            Option(
                name='user_id',
                description='Input your user id here. You have to open up the social media in hypixel',
                type=OptionType.STRING,
                required=True
            )
        ]
    )
    async def verifyidupdate(self, inter, user_id=None):
        # check is in the desired channel.
        if inter.channel.id == get_setting_json('VerifyIdChannelId'):
            # check is user id input
            if user_id is not None:
                player = get_verify_id_list(inter.author)

                player_data = UserData(player)

                player_data.api = get_hypixel_api(user_id)

                print('> update player user : ' + str(inter.author))

                # check is player has been verified
                if get_setting_json('VerifyIdRole') in [y.name.lower() for y in inter.author.roles]:
                    # check get hypixel api is successes
                    if player_data.api['success']:
                        player_data.set_latest_user_api()

                        # try to get player social media discord
                        try:
                            player_data.discord = player_data.api['player']['socialMedia']['links']['DISCORD']

                            # check user name is correct in api
                            if str(inter.author) == player_data.discord:
                                set_user_id(inter.author, user_id)

                                print('> update Id success')

                                embed = discord.Embed(
                                    title='成功更新',
                                    description=str(inter.author) + ' ---> ' + user_id,
                                    color=0x00ff00
                                )

                                embed.set_author(
                                    name=inter.author.name,
                                    icon_url=inter.author.avatar_url
                                )

                                await inter.send(embed=embed)

                            else:
                                print('> Player not found')

                                embed = discord.Embed(
                                    title='驗證失敗，玩家id不正確',
                                    description=str(inter.author) + ' -x-> ' + user_id,
                                    color=0xe74c3c
                                )

                                embed.set_author(
                                    name=inter.author.name,
                                    icon_url=inter.author.avatar_url
                                )

                                await inter.send(embed=embed, delete_after=20.0)
                        except KeyError:
                            print('> The player do not open the social media')

                            embed = discord.Embed(
                                title='驗證失敗，請先打開 hypixel discord api',
                                description=str(inter.author) + ' -x-> ' + user_id,
                                color=0xe74c3c
                            )

                            embed.set_author(
                                name=inter.author.name,
                                icon_url=inter.author.avatar_url
                            )

                            await inter.send(embed=embed, delete_after=20.0)
                    else:
                        print('>　Please wait a little bit and try again')

                        print('> fail reason : ' + player_data.api['cause'])

                        embed = discord.Embed(
                            title='驗證失敗，請稍後重試',
                            description=str(inter.author) + ' -x-> ' + user_id + '\n\n' + '原因 : ' + player_data.api[
                                'cause'],
                            color=0xe74c3c
                        )

                        embed.set_author(
                            name=inter.author.name,
                            icon_url=inter.author.avatar_url
                        )

                        await inter.send(embed=embed, delete_after=20.0)

            else:
                print('>　Input id is incorrect')

                embed = discord.Embed(
                    title='驗證失敗，請稍後重試',
                    description=str(inter.author) + ' -x-> ' + str(user_id),
                    color=0xe74c3c
                )

                embed.set_author(
                    name=inter.author.name,
                    icon_url=inter.author.avatar_url
                )

                await inter.send(embed=embed, delete_after=20.0)

        else:
            print('> Wrong channel')

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
    pybot.add_cog(SlashVerifyId(pybot))

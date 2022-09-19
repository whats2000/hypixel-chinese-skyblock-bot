import discord
from dislash import slash_command, OptionType
from dislash.slash_commands import Option
from hypixel_chinese_skyblock_bot.Core.Common import CodExtension, get_hypixel_api, get_setting_json, set_user_id, \
    get_verify_id_list
from hypixel_chinese_skyblock_bot.Core.UserData import UserData


class SlashVerifyId(CodExtension):

    @slash_command(
        guild_ids=[int(get_setting_json('ServerId'))],
        name='verify_id',
        description='Link your discord to your minecraft account',
        options=[
            Option(
                name='minecraft_id',
                description='Input your user id here. You have to open up the social media in hypixel',
                type=OptionType.STRING,
                required=True
            )
        ]
    )
    async def verifyid(self, inter, minecraft_id=None):
        # check is in the desired channel.
        if inter.channel.id == get_setting_json('VerifyIdChannelId'):
            embed = discord.Embed(
                title='正在向 hypixel api 提出訪問請求',
                color=0xf1c40f
            )

            embed.set_author(
                name=inter.author.name,
                icon_url=inter.author.avatar_url
            )

            await inter.send(embed=embed, ephemeral=True)

            # check is user id input correctly
            if minecraft_id is not None:
                # check is player has been verified
                if get_setting_json('VerifyIdRole') not in [y.name.lower() for y in inter.author.roles]:
                    player = get_verify_id_list(inter.author)

                    player_data = UserData(player)

                    player_data.api = get_hypixel_api(minecraft_id)

                    print(f'Info > verify player user : {inter.author}')

                    # check get hypixel api is successes
                    if player_data.api['success']:
                        player_data.set_latest_user_api()

                        # try to get player social media discord
                        try:
                            player_data.discord = player_data.api['player']['socialMedia']['links']['DISCORD']

                            # check user name is correct in api
                            if str(inter.author) == player_data.discord:
                                set_user_id(inter.author, player_data.api['player']['displayname'])

                                print('Info > Verify Id success')

                                embed = discord.Embed(
                                    title='成功驗證',
                                    description=f'{inter.author} ---> {player_data.api["player"]["displayname"]}',
                                    color=0x00ff00
                                )

                                embed.set_author(
                                    name=inter.author.name,
                                    icon_url=inter.author.avatar_url
                                )

                                await inter.send(embed=embed, delete_after=20.0)

                                role = discord.utils.get(inter.author.guild.roles,
                                                         name=get_setting_json('VerifyIdRole')
                                                         )

                                await inter.author.add_roles(role)

                            else:
                                print('Error > Player not found')

                                embed = discord.Embed(
                                    title='驗證失敗，玩家id不正確',
                                    description=f'{inter.author} -x-> {minecraft_id}',
                                    color=0xe74c3c
                                )

                                embed.set_author(
                                    name=inter.author.name,
                                    icon_url=inter.author.avatar_url
                                )

                                await inter.send(embed=embed, delete_after=20.0)
                        except (KeyError, TypeError):
                            print('Error > The player do not open the social media')

                            embed = discord.Embed(
                                title='驗證失敗，請先打開discord api',
                                description=f'{inter.author} -x-> {minecraft_id}',
                                color=0xe74c3c
                            )

                            embed.set_author(
                                name=inter.author.name,
                                icon_url=inter.author.avatar_url
                            )

                            await inter.send(embed=embed, delete_after=20.0)
                    else:
                        print('Error > Please wait a little bit and try again')

                        embed = discord.Embed(
                            title='驗證失敗，請稍後重試',
                            description=f'{inter.author} -x-> {minecraft_id}',
                            color=0xe74c3c
                        )

                        embed.set_author(
                            name=inter.author.name,
                            icon_url=inter.author.avatar_url
                        )

                        await inter.send(embed=embed, delete_after=20.0)

                else:
                    print('Error > Has already verified')

                    embed = discord.Embed(
                        title='你已經驗證，更新請用sb?verifyidupdate',
                        description=f'{inter.author} -x-> {minecraft_id}',
                        color=0xe74c3c
                    )

                    embed.set_author(
                        name=inter.author.name,
                        icon_url=inter.author.avatar_url
                    )

                    await inter.send(embed=embed, delete_after=20.0)

            else:
                print('Error >　Input id is incorrect')

                embed = discord.Embed(
                    title='驗證失敗，請稍後重試',
                    description=f'{inter.author} -x-> {minecraft_id}',
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

            await inter.send(embed=embed, ephemeral=True)


def setup(pybot):
    pybot.add_cog(SlashVerifyId(pybot))

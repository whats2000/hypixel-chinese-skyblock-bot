import disnake
from disnake.ext import commands

from hypixel_chinese_skyblock_bot.Core.Common import CodExtension, get_hypixel_api, get_setting_json, set_user_id, \
    get_verify_id_list, add_role
from hypixel_chinese_skyblock_bot.Core.UserData import UserData


class SlashVerifyId(CodExtension):

    @commands.slash_command(
        guild_ids=[int(get_setting_json('ServerId'))],
        name='verify_id',
        description='Link your discord to your minecraft account'
    )
    async def verify_id(self,
                        inter: disnake.AppCommandInteraction,
                        minecraft_id: str = commands.Param(
                           description='Input your user id here. You have to open up the social media in hypixel'
                        )):
        # check is in the desired channel
        await inter.response.defer(ephemeral=True)

        if inter.channel.id == get_setting_json('VerifyIdChannelId'):
            embed = disnake.Embed(
                title='正在向 hypixel api 提出訪問請求',
                color=0xf1c40f
            )

            embed.set_author(
                name=inter.author.name,
                icon_url=inter.author.avatar.url
            )

            await inter.edit_original_message(embed=embed)

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

                                embed = disnake.Embed(
                                    title='成功驗證',
                                    description=f'{inter.author} ---> {player_data.api["player"]["displayname"]}',
                                    color=0x00ff00
                                )

                                embed.set_author(
                                    name=inter.author.name,
                                    icon_url=inter.author.avatar.url
                                )

                                await inter.send(embed=embed, delete_after=20.0)

                                await add_role(ctx=inter, get_role_names='✔ 已驗證成員')

                            else:
                                print('Error > Player not found')

                                embed = disnake.Embed(
                                    title='驗證失敗，玩家id不正確',
                                    description=f'{inter.author} -x-> {minecraft_id}',
                                    color=0xe74c3c
                                )

                                embed.set_author(
                                    name=inter.author.name,
                                    icon_url=inter.author.avatar.url
                                )

                                await inter.send(embed=embed, delete_after=20.0)
                        except (KeyError, TypeError):
                            print('Error > The player do not open the social media')

                            embed = disnake.Embed(
                                title='驗證失敗，請先打開discord api',
                                description=f'{inter.author} -x-> {minecraft_id}',
                                color=0xe74c3c
                            )

                            embed.set_author(
                                name=inter.author.name,
                                icon_url=inter.author.avatar.url
                            )

                            await inter.send(embed=embed, delete_after=20.0)
                    else:
                        print('Error > Please wait a little bit and try again')

                        embed = disnake.Embed(
                            title='驗證失敗，請稍後重試',
                            description=f'{inter.author} -x-> {minecraft_id}',
                            color=0xe74c3c
                        )

                        embed.set_author(
                            name=inter.author.name,
                            icon_url=inter.author.avatar.url
                        )

                        await inter.send(embed=embed, delete_after=20.0)

                else:
                    print('Error > Has already verified')

                    embed = disnake.Embed(
                        title='你已經驗證，更新請用 /verifyidupdate',
                        description=f'{inter.author} -x-> {minecraft_id}',
                        color=0xe74c3c
                    )

                    embed.set_author(
                        name=inter.author.name,
                        icon_url=inter.author.avatar.url
                    )

                    await inter.send(embed=embed, delete_after=20.0)

            else:
                print('Error >　Input id is incorrect')

                embed = disnake.Embed(
                    title='驗證失敗，請稍後重試',
                    description=f'{inter.author} -x-> {minecraft_id}',
                    color=0xe74c3c
                )

                embed.set_author(
                    name=inter.author.name,
                    icon_url=inter.author.avatar.url
                )

                await inter.send(embed=embed, delete_after=20.0)

        else:
            print('Error > Wrong channel')

            embed = disnake.Embed(
                title='請在正確頻道輸入',
                color=0xe74c3c
            )

            embed.set_author(
                name=inter.author.name,
                icon_url=inter.author.avatar.url
            )

            await inter.send(embed=embed, ephemeral=True)


def setup(pybot):
    pybot.add_cog(SlashVerifyId(pybot))

import disnake
from disnake.ext import commands

from hypixel_chinese_skyblock_bot.Core.Common import CodExtension, get_hypixel_api, get_setting_json, set_user_id, \
    get_verify_id_list
from hypixel_chinese_skyblock_bot.Core.UserData import UserData


class SlashVerifyIdUpdate(CodExtension):

    @commands.slash_command(
        guild_ids=[int(get_setting_json('ServerId'))],
        name='verify_id_update',
        description='Update your discord to your minecraft account'
    )
    async def verify_id_update(self,
                               inter: disnake.AppCommandInteraction,
                               minecraft_id: str = commands.Param(
                                   description='Input your user id here. '
                                               'You have to open up the social media in hypixel'
                               )):
        await inter.response.defer(ephemeral=True)

        # check is in the desired channel.
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

            # check is user id input
            if minecraft_id is not None:
                player = get_verify_id_list(inter.author)

                player_data = UserData(player)

                player_data.api = get_hypixel_api(minecraft_id)

                print(f'Info > update player user : {inter.author}')

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
                                set_user_id(inter.author, player_data.api['player']['displayname'])

                                print('Info > update Id success')

                                embed = disnake.Embed(
                                    title='成功更新',
                                    description=f'{inter.author} ---> {player_data.api["player"]["displayname"]}',
                                    color=0x00ff00
                                )

                                embed.set_author(
                                    name=inter.author.name,
                                    icon_url=inter.author.avatar.url
                                )

                                await inter.send(embed=embed, delete_after=20.0)

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
                                title='驗證失敗，請先打開 hypixel discord api',
                                description=f'{inter.author} -x-> {minecraft_id}',
                                color=0xe74c3c
                            )

                            embed.set_author(
                                name=inter.author.name,
                                icon_url=inter.author.avatar.url
                            )

                            await inter.send(embed=embed, delete_after=20.0)
                    else:
                        print('Error >　Please wait a little bit and try again')

                        print(f'Error > fail reason : {player_data.api["cause"]}')

                        embed = disnake.Embed(
                            title='驗證失敗，請稍後重試',
                            description=f'{inter.author} -x-> {minecraft_id}\n\n原因 : {player_data.api["cause"]}',
                            color=0xe74c3c
                        )

                        embed.set_author(
                            name=inter.author.name,
                            icon_url=inter.author.avatar.url
                        )

                        await inter.send(embed=embed, delete_after=20.0)

                else:
                    print('Error > You have not verified')

                    embed = disnake.Embed(
                        title='你未驗證，更新請用 /verifyid',
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
    pybot.add_cog(SlashVerifyIdUpdate(pybot))

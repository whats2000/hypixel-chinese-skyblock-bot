import logging

import disnake
from disnake.ext import commands

from CoreFunction.Common import CodExtension, get_hypixel_api, get_setting_json, set_user_id, \
    get_verify_id_list
from CoreFunction.Logger import Logger
from CoreFunction.SendEmbed import inter_build_embed, set_inter_embed_author
from CoreFunction.UserData import UserData

bot_logger = Logger(__name__)


class SlashVerifyIdUpdate(CodExtension):

    @commands.slash_command(
        guild_ids=[int(get_setting_json('ServerId'))],
        name='update',
        description='Update your discord to your minecraft account'
    )
    async def verify(self, inter: disnake.AppCommandInteraction,
                     minecraft_id: str = commands.Param(
                         description='Input your user id here. '
                                     'You have to open up the social media in hypixel'
                     )):
        await self.verify_id_update(inter, minecraft_id)

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
        if inter.channel.id == get_setting_json('VerifyIdChannelId') \
                or inter.channel.id == get_setting_json('DebugChannelId'):
            embed = disnake.Embed(
                title='正在向 hypixel api 提出訪問請求',
                color=0xf1c40f
            )

            set_inter_embed_author(embed, inter)

            await inter.edit_original_message(embed=embed)

            # check is user id input
            if minecraft_id is not None:
                player = get_verify_id_list(inter.author)

                player_data = UserData(player)

                player_data.api = get_hypixel_api(minecraft_id)

                bot_logger.log_message(logging.INFO, f'更新用戶 : {inter.author.name}')

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

                                bot_logger.log_message(logging.INFO, f'更新 id 成功')

                                embed = disnake.Embed(
                                    title='成功更新',
                                    description=f'{inter.author} ---> {player_data.api["player"]["displayname"]}',
                                    color=0x00ff00
                                )

                                set_inter_embed_author(embed, inter)

                                await inter.edit_original_message(embed=embed)

                            else:
                                bot_logger.log_message(logging.ERROR, f'找不到該名玩家 {minecraft_id}')

                                embed = disnake.Embed(
                                    title='驗證失敗，玩家id不正確',
                                    description=f'{inter.author} -x-> {minecraft_id}',
                                    color=0xe74c3c
                                )

                                set_inter_embed_author(embed, inter)

                                await inter.edit_original_message(embed=embed)
                        except (KeyError, TypeError):
                            bot_logger.log_message(logging.ERROR, f'玩家未開啟 hypixel discord API')

                            embed = disnake.Embed(
                                title='驗證失敗，請先打開 hypixel discord api',
                                description=f'{inter.author} -x-> {minecraft_id}',
                                color=0xe74c3c
                            )

                            set_inter_embed_author(embed, inter)

                            await inter.edit_original_message(embed=embed)
                    else:
                        if 'cause' not in player_data.api:
                            player_data.api['cause'] = '玩家 id 綁定丟失，請更新 id (很可能是 nitro 導致編號變更)'

                        bot_logger.log_message(logging.ERROR, f'獲取 hypixel API 失敗 : {player_data.api["cause"]}')

                        embed = disnake.Embed(
                            title='驗證失敗，請稍後重試',
                            description=f'{inter.author} -x-> {minecraft_id}\n\n原因 : {player_data.api["cause"]}',
                            color=0xe74c3c
                        )

                        set_inter_embed_author(embed, inter)

                        await inter.edit_original_message(embed=embed)

                else:
                    bot_logger.log_message(logging.ERROR, f'玩家已經驗證')

                    embed = disnake.Embed(
                        title='你未驗證，更新請用 /verifyid',
                        description=f'{inter.author} -x-> {minecraft_id}',
                        color=0xe74c3c
                    )

                    set_inter_embed_author(embed, inter)

                    await inter.edit_original_message(embed=embed)

            else:
                bot_logger.log_message(logging.ERROR, f'玩家 {minecraft_id} 輸入錯誤')

                embed = disnake.Embed(
                    title='驗證失敗，請稍後重試',
                    description=f'{inter.author} -x-> {minecraft_id}',
                    color=0xe74c3c
                )

                set_inter_embed_author(embed, inter)

                await inter.edit_original_message(embed=embed)

        else:
            bot_logger.log_message(logging.ERROR, f'錯誤頻道輸入')

            embed = inter_build_embed('Wrong Channel', inter)

            await inter.send(embed=embed, ephemeral=True)


def setup(pybot):
    pybot.add_cog(SlashVerifyIdUpdate(pybot))

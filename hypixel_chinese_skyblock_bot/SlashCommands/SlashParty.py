import logging

import disnake
from disnake.ext import commands

from CoreFunction.Common import CodExtension, get_setting_json
from CoreFunction.Logger import Logger
from CoreFunction.SendEmbed import inter_build_embed, set_inter_embed_author

bot_logger = Logger(__name__)


class SlashParty(CodExtension):

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.slash_command(
        guild_ids=[int(get_setting_json('ServerId'))],
        name='party',
        description='Start a party'
    )
    async def party(self,
                    inter: disnake.AppCommandInteraction,
                    party: str = commands.Param(choices=['Catacombs',
                                                         'Master Mode Catacombs',
                                                         'Kuudra',
                                                         'Leech',
                                                         'Bacte',
                                                         'Dragon',
                                                         'Vanquisher',
                                                         'Fishing',
                                                         'Diana'],
                                                description='Choose party type'
                                                ),
                    tier: int = commands.Param(ge=1, le=7,
                                               description=f'Dungeon : 1 ~ 7 | '
                                                           f'Kuudra : '
                                                           f'1 ~ {get_setting_json("KuudraMaxTier")} | '
                                                           f'Others : 1'),
                    cata_need: int = commands.Param(name='catacombs_level_need',
                                                    ge=1, le=50,
                                                    description='Input the lowest level require.',
                                                    default=None),

                    class_info: str = commands.Param(name='class_need',
                                                     description='Input the class or weapon required information',
                                                     default=None),

                    about: str = commands.Param(description='Input some extra information about the party',
                                                default=None),

                    voice_channel: str = commands.Param(description='Input the voice channel link',
                                                        default=None)
                    ):
        await inter.response.defer()

        bot_logger.log_message(logging.DEBUG, f'{inter.author.name} 用戶呼叫組隊命令')

        # check is in the desired channel.
        if inter.channel.id == get_setting_json('PartyChannelId') \
                or inter.channel.id == get_setting_json('DebugChannelId'):
            # check is player has been verified
            if get_setting_json('VerifyIdRole') in [y.name.lower() for y in inter.author.roles]:
                # check the kuudra tier is correct
                if party == 'Kuudra' and tier > get_setting_json('KuudraMaxTier'):
                    bot_logger.log_message(logging.ERROR, f'錯誤範圍值')

                    embed = disnake.Embed(
                        title=f'Kuudra 目前沒開放 {tier - 1} 階以上',
                        color=0xe74c3c
                    )

                    set_inter_embed_author(embed, inter)

                    await inter.edit_original_message(embed=embed)
                else:
                    # check display type
                    if party == 'Catacombs' or party == 'Master Mode Catacombs':
                        role_id_list = get_setting_json(party)

                        mention_role = disnake.utils.get(inter.guild.roles, id=role_id_list[str(tier)])

                        desc = f'**尋找 :** {party} Floor {tier}\n' \
                               f'> {mention_role.mention}\n\n'

                        if party == 'Catacombs':
                            thread_name = f'Floor {tier}'
                        else:
                            thread_name = f'MM Floor {tier}'

                        # check if level required is set
                        if cata_need is not None:
                            desc += f'**地下城等級需求 :** {cata_need}\n\n'

                            thread_name = f'{thread_name} ({cata_need}+)'

                        # check if class information required is set
                        if class_info is not None:
                            desc += f'**職業 / 武器需求 :** {class_info}\n\n'

                    elif party == 'Kuudra':
                        role_id_list = get_setting_json(party)

                        mention_role = disnake.utils.get(inter.guild.roles, id=role_id_list[str(tier)])

                        desc = f'**尋找 :** {party} T{tier}\n' \
                               f'> {mention_role.mention}\n\n'

                        # check if class information required is set
                        if class_info is not None:
                            desc += f'**職業 / 武器需求 :** {class_info}\n\n'

                        thread_name = f'{party} T{tier}'
                    else:
                        role = get_setting_json(party)

                        mention_role = disnake.utils.get(inter.guild.roles, id=role)

                        desc = f'**尋找 :** {party} Party\n' \
                               f'> {mention_role.mention}\n\n'

                        thread_name = f'{party} Party'

                    # check if voice chat link is provide
                    if voice_channel is not None:
                        desc += f'**語音連結 :** {voice_channel}\n\n'

                    # check if extra information is set
                    if about is not None:
                        desc += f'**備註 :** \n' \
                                f'> {about}'

                    embed = disnake.Embed(
                        title=f'招募隊友',
                        color=0x00ff00,
                        description=desc
                    )

                    set_inter_embed_author(embed, inter)

                    await inter.edit_original_message(f'**{party} 組隊通知**')

                    message = await inter.followup.send(f'{mention_role.mention}',
                                                        embed=embed,
                                                        allowed_mentions=disnake.AllowedMentions(roles=True))

                    await inter.channel.create_thread(
                        name=thread_name,
                        auto_archive_duration=60,
                        message=message
                    )

            else:
                bot_logger.log_message(logging.ERROR, f'玩家 id 缺失')

                embed = inter_build_embed('Missing Id', inter)

                await inter.edit_original_message(embed=embed)

        else:
            bot_logger.log_message(logging.ERROR, f'錯誤頻道輸入')

            embed = inter_build_embed('Wrong Channel', inter)

            await inter.edit_original_message(embed=embed)


def setup(pybot):
    pybot.add_cog(SlashParty(pybot))

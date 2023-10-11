import logging

import disnake
from disnake.ext import commands

from CoreFunction.Common import CodExtension, get_setting_json, get_hypixel_skyblock_items
from CoreFunction.Logger import Logger

bot_logger = Logger(__name__)


class SlashUpdateSkyblockName(CodExtension):

    @commands.has_any_role(get_setting_json('AdminRole'))
    @commands.slash_command(
        guild_ids=[int(get_setting_json('ServerId'))],
        name='update_item_list',
        description='Fetch the newest skyblock items name and id'
    )
    async def send_embed(self,
                         inter: disnake.AppCommandInteraction
                         ):
        bot_logger.log_message(logging.DEBUG, f'{inter.author.name} 更新物品列表')

        await inter.response.defer(ephemeral=True)

        if get_hypixel_skyblock_items():
            await inter.edit_original_message('Done !')
        else:
            await inter.edit_original_message('Fail to update !')


def setup(pybot):
    pybot.add_cog(SlashUpdateSkyblockName(pybot))

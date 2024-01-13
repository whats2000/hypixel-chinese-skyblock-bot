import disnake
from disnake.ext import commands

from CoreFunction.Common import CodExtension
from CoreFunction.InteractionErrorMessage import handle_interaction_error
from CoreFunction.Logger import Logger

bot_logger = Logger(__name__)


class UserCommandErrorHandle(CodExtension):
    @commands.Cog.listener()
    async def on_user_command_error(self, inter: disnake.AppCommandInteraction, error: commands.CommandError):
        await handle_interaction_error(bot_logger, self.bot, inter, error)


def setup(pybot):
    pybot.add_cog(UserCommandErrorHandle(pybot))

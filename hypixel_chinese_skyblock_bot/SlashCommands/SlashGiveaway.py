import asyncio
import json
import logging
import random
import time
from datetime import datetime

import disnake
from disnake.ext import commands, tasks

from CoreFunction.Common import CodExtension, get_setting_json, read_json, write_json
from CoreFunction.Logger import Logger
from CoreFunction.SendEmbed import inter_build_embed

bot_logger = Logger(__name__)


class GiveawayView(disnake.ui.View):
    def __init__(self, message_id):
        super().__init__(timeout=None)
        self.add_item(EnterGiveawayButton(message_id))


class EnterGiveawayButton(disnake.ui.Button):
    def __init__(self, message_id):
        super().__init__(style=disnake.ButtonStyle.primary, emoji="🎉")
        self.message_id = message_id

    async def callback(self, interaction: disnake.MessageInteraction):
        user_id = str(interaction.user.id)

        # Read the current state of giveaways
        giveaways = read_json('Resources/Giveaway.json')
        required_chat_role_id = giveaways.get(self.message_id, {}).get("ChatLevelRequired", None)

        # Check if already entered
        giveaway_data = giveaways.get(self.message_id, {}).get("Entry", {})
        if user_id in giveaway_data:
            await interaction.response.send_message("You have already entered this giveaway!", ephemeral=True)
            return

        # Check for verification if required
        if giveaways.get(self.message_id, {}).get("RequiredVerify", False):
            verify_role = get_setting_json('VerifyIdRole').lower()
            if verify_role not in [y.name.lower() for y in interaction.user.roles]:
                bot_logger.log_message(logging.ERROR, f'玩家 id 缺失')

                embed = inter_build_embed('Missing Id', interaction)

                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

        # Get role levels from settings
        role_levels = get_setting_json('RoleLevel')

        # Check if user has the required role or a higher-level role
        user_role_ids = [str(role.id) for role in interaction.user.roles]

        if required_chat_role_id and required_chat_role_id not in user_role_ids:
            # Check if the user has a higher-level role
            required_role_level = role_levels.get(str(required_chat_role_id), 0)
            if not any(role_levels.get(role_id, 0) >= required_role_level for role_id in user_role_ids):
                await interaction.response.send_message(
                    "You do not have the required chat level to enter this giveaway!", ephemeral=True)
                return

        # Determine bonus and add entry
        bonus = 2 if any(
            role.id in get_setting_json('TitleRequireRoleList').values() for role in interaction.user.roles) else 1
        giveaway_data[user_id] = bonus

        try:
            # Update the entry in the giveaways dictionary
            giveaways[self.message_id]["Entry"] = giveaway_data
        except KeyError:
            await interaction.response.send_message("The giveaway was ended!", ephemeral=True)
            return

        # Write updated data back to file
        await asyncio.to_thread(write_json, giveaways, 'Resources/Giveaway.json')

        # Update the button label with the number of entries
        total_entries = sum(giveaway_data.values())
        self.label = f"{total_entries}"

        # Create a new view with the updated button
        updated_view = GiveawayView(self.message_id)
        updated_view.clear_items()
        updated_view.add_item(self)

        # Edit the original message to update the view
        await interaction.message.edit(view=updated_view)

        await interaction.response.send_message("You've successfully entered the giveaway!", ephemeral=True)


class SlashGiveaway(CodExtension):

    def __init__(self, bot):
        super().__init__(bot)
        self.has_run_startup = False

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.has_run_startup:
            self.has_run_startup = True
            self.check_giveaways.start()
            await self.reactivate_giveaway_buttons()

    @commands.has_any_role(get_setting_json('AdminRole'))
    @commands.slash_command(
        guild_ids=[int(get_setting_json('ServerId'))],
        name='giveaway',
        description='Start a giveaway event'
    )
    async def giveaway(self,
                       inter: disnake.AppCommandInteraction,
                       title: str = commands.Param(description='Makes the title of the embed'),
                       end_time: str = commands.Param(description='The time, format example "2023/10/10/20:00"'),
                       winner: int = commands.Param(description='The winner for the prize'),
                       prize: str = commands.Param(description='The prize for the winners'),
                       host: disnake.User = commands.Param(description='Host of the giveaway', default=None),
                       chat_level: disnake.Role = commands.Param(description='The min required chat level role',
                                                                 default=None),
                       required_verify: bool = commands.Param(description='If the user need verify',
                                                              default=False),
                       color: str = commands.Param(description='Makes the description', default=None),
                       picture: str = commands.Param(description='The picture url of the embed', default=None),
                       thumbnail: str = commands.Param(description='The thumbnail url for the embed', default=None)):
        await inter.response.defer()

        bot_logger.log_message(logging.INFO, f'建立 Giveaway : {inter.author.name}')

        # Calculate the remaining time and convert to Unix timestamp
        end_time_obj = datetime.strptime(end_time, "%Y/%m/%d/%H:%M")
        unix_timestamp = int(time.mktime(end_time_obj.timetuple()))

        # Fetch the special roles with 2x entry chances
        title_role_list = get_setting_json('TitleRequireRoleList')

        # Construct the role list string
        special_roles = "\n".join([f"<@&{role_id}> - 2x 機率" for role_name, role_id in title_role_list.items()])

        # Embed description with Discord timestamp and special roles
        embed_description = (
            f"### 獎品: {prize}\n"
            f"**點擊下方按鈕加入!**\n\n"
            f"贊助人: {host.mention if host else '匿名'}\n"
            f"得獎人數: {winner}\n"
            f"結束時間: <t:{unix_timestamp}:f>\n\n"
            f"### 加倍機率: \n"
            f"{special_roles}\n"
            f"\n"
            f"最低聊天等級需要 : {chat_level.mention if chat_level else '無'}"
        )

        # Creating embed
        embed = disnake.Embed(title=title, description=embed_description, color=color or disnake.Color.random())
        if picture:
            embed.set_image(url=picture)
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)

        # Sending the embed and getting the message object
        message = await inter.followup.send(embed=embed)

        # Assume 'message' is the message object after sending the embed
        message_id = str(message.id)

        # Read existing giveaways
        giveaways = read_json('Resources/Giveaway.json')

        # Update with new giveaway info
        giveaways[message_id] = {
            "Prize": prize,
            "Host": host.mention if host else '匿名',
            "EndTime": unix_timestamp,
            "Winner": winner,
            "ChatLevelRequired": chat_level.id if chat_level else 0,
            "RequiredVerify": required_verify,
            "ChannelID": inter.channel.id,
            "Entry": {}
        }

        # Write initial data to JSON
        await asyncio.to_thread(write_json, giveaways, 'Resources/Giveaway.json')

        # Check if the task is not running, then start it
        if not self.check_giveaways.is_running():
            bot_logger.log_message(logging.INFO, 'Starting the giveaway check task.')
            self.check_giveaways.start()

        # Creating the view with the button
        view = GiveawayView(message_id)

        # Edit the original message to include the view
        await message.edit(embed=embed, view=view)

    async def reactivate_giveaway_buttons(self):
        bot_logger.log_message(logging.INFO, f'Reactivating giveaway: System')
        try:
            with open('Resources/Giveaway.json', 'r') as file:
                giveaways = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            giveaways = {}

        for message_id, giveaway in giveaways.items():
            # Only add views to giveaways that haven't ended yet
            if int(time.time()) < giveaway['EndTime']:
                channel = self.bot.get_channel(giveaway['ChannelID'])
                if channel:
                    try:
                        # Get the total number of entries
                        total_entries = sum(giveaway['Entry'].values())

                        # Update the button label with the number of entries
                        enter_button = EnterGiveawayButton(message_id)
                        enter_button.label = f'{total_entries}'

                        # Create a new view with the updated button
                        updated_view = GiveawayView(message_id)
                        updated_view.clear_items()
                        updated_view.add_item(enter_button)

                        # Fetch message and edit with the new view
                        message = await channel.fetch_message(int(message_id))
                        await message.edit(view=updated_view)
                    except Exception as e:
                        bot_logger.log_message(logging.ERROR, f'Error reactivating giveaway: {message_id} | {e}')

    def cog_unload(self):
        self.check_giveaways.cancel()

    @tasks.loop(seconds=10)
    async def check_giveaways(self):
        giveaways = read_json('Resources/Giveaway.json')
        if not giveaways:
            bot_logger.log_message(logging.INFO, 'No active giveaways. Stopping the task.')
            self.check_giveaways.cancel()
            return

        current_time = int(time.time())

        ended_giveaways = []  # List to store message IDs of ended giveaways

        for message_id, giveaway in giveaways.items():
            if current_time >= giveaway["EndTime"]:
                bot_logger.log_message(logging.INFO, f'抽選 Giveaway : {giveaway["Prize"]}')
                await self.roll_winner(message_id, giveaway)
                ended_giveaways.append(message_id)  # Add to the list

        # Remove ended giveaways after iterating
        for message_id in ended_giveaways:
            del giveaways[message_id]

        # Update the JSON file after processing
        await asyncio.to_thread(write_json, giveaways, 'Resources/Giveaway.json')

    async def roll_winner(self, message_id, giveaway):
        entries = giveaway["Entry"]

        # Get the channel from stored channel ID
        channel = self.bot.get_channel(giveaway["ChannelID"])

        if not entries:
            if channel:
                try:
                    message = await channel.fetch_message(int(message_id))
                    new_embed = disnake.Embed.from_dict(message.embeds[0].to_dict())  # Clone the original embed
                    new_embed.description = (
                        f"### 獎品: {giveaway['Prize']}\n"
                        f"贊助人: {giveaway.get('Host', '匿名')}\n"
                        f"得獎人: 無\n"
                        f"結束時間: <t:{giveaway['EndTime']}:f>"
                    )
                    await message.edit(embed=new_embed, view=None)

                except disnake.NotFound:
                    bot_logger.log_message(logging.ERROR, f'找不到頻道或信息')
                except Exception as e:
                    bot_logger.log_message(logging.ERROR, f'宣告贏家失敗: {e}')
            return

        # Flatten the entries considering the bonus
        user_ids = [user_id for user_id, bonus in entries.items() for _ in range(bonus)]

        # Shuffle the list to randomize it
        random.shuffle(user_ids)

        # Select unique winners
        winners = []
        for user_id in user_ids:
            if user_id not in winners:
                winners.append(user_id)
            if len(winners) >= giveaway["Winner"]:
                break

        winner_mentions = " ".join([f"<@{winner_id}>" for winner_id in winners])

        if channel:
            try:
                message = await channel.fetch_message(int(message_id))
                new_embed = disnake.Embed.from_dict(message.embeds[0].to_dict())  # Clone the original embed
                new_embed.description = (
                    f"### 獎品: {giveaway['Prize']}\n"
                    f"贊助人: {giveaway.get('Host', '匿名')}\n"
                    f"得獎人: {winner_mentions}\n"
                    f"結束時間: <t:{giveaway['EndTime']}:f>"
                )
                await message.edit(embed=new_embed, view=None)

                # Announcing winners in the chat with a link to the giveaway message
                giveaway_message_link = f"https://discord.com/channels/" \
                                        f"{message.guild.id}/{message.channel.id}/{message.id} "
                announcement_message = f"🎉 恭喜得獎者: {winner_mentions}!\n查看抽獎: [點擊這裡]({giveaway_message_link})"
                await channel.send(announcement_message)

            except disnake.NotFound:
                bot_logger.log_message(logging.ERROR, f'找不到頻道或信息')
            except Exception as e:
                bot_logger.log_message(logging.ERROR, f'宣告贏家失敗: {e}')

    @check_giveaways.before_loop
    async def before_check_giveaways(self):
        await self.bot.wait_until_ready()


def setup(pybot):
    pybot.add_cog(SlashGiveaway(pybot))

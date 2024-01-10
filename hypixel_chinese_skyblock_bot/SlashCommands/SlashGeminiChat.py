import logging
import re

import disnake
import google.generativeai as genai
from disnake.ext import commands

from CoreFunction.Common import CodExtension, get_setting_json
from CoreFunction.Logger import Logger
from CoreFunction.SendEmbed import set_inter_embed_author

bot_logger = Logger(__name__)

# Config for Google AI
GOOGLE_AI_KEY = get_setting_json('GeminiApiKey')
genai.configure(api_key=GOOGLE_AI_KEY)
text_generation_config = genai.GenerationConfig(**{
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 1024,
})

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
]
text_model = genai.GenerativeModel(
    model_name="gemini-pro", generation_config=text_generation_config, safety_settings=safety_settings)


async def generate_response_with_text(inter, message_text):
    # Create a regular expression pattern to match text between < and > then replace it with an empty string
    bracket_pattern = re.compile(r'<[^>]+>')
    message_text = bracket_pattern.sub('', message_text)

    prompt_parts = [f"請簡短回應以下文字: {message_text}"]
    accumulated_response = f"**{inter.author.name}**: \n{message_text}\n\n**Gemini**: \n"

    try:
        response = text_model.generate_content(prompt_parts, stream=True)

        # Iterate over the response stream and print the chunks.
        for chunk in response:
            accumulated_response += chunk.text
            embed = disnake.Embed(
                title="雙子星語言模型回應",
                url="https://deepmind.google/technologies/gemini/#build-with-gemini",
                description=accumulated_response,
                color=0x00ff00
            )
            set_inter_embed_author(embed, inter)

            embed.set_footer(text="該技術使用Google Gemini")

            await inter.edit_original_message(embed=embed)

    except Exception as e:
        await inter.edit_original_message(content=f"❌ 發生錯誤: {str(e)}")
        bot_logger.log_message(logging.ERROR, f'生成回應時發生錯誤: {str(e)}')



class SlashGeminiChatCommand(CodExtension):
    @commands.cooldown(1, 20, commands.BucketType.user)
    @commands.slash_command(
        guild_ids=[int(get_setting_json('ServerId'))],
        name='chat',
        description='Return the response from Gemini Language Model',
    )
    async def gemini_chat(self, inter: disnake.AppCommandInteraction,
                          text: str = commands.Param(
                              description='Input the text you want to chat with Gemini Language Model')
                          ):
        await inter.response.defer()

        bot_logger.log_message(logging.DEBUG, f'{inter.author.name} 用戶呼叫雙子星語言模型命令: {text}')

        await generate_response_with_text(inter, text)


def setup(pybot):
    pybot.add_cog(SlashGeminiChatCommand(pybot))

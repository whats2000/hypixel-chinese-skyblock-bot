import disnake
import requests
from bs4 import BeautifulSoup
from disnake.ext import commands

from CoreFunction.Common import CodExtension, get_setting_json
from CoreFunction.Logger import Logger
from CoreFunction.SendEmbed import set_inter_embed_author

bot_logger = Logger(__name__)


class SlashWiki(CodExtension):
    @commands.slash_command(
        guild_ids=[int(get_setting_json('ServerId'))],
        name='wiki',
        description='Return the wiki result',
    )
    async def wiki(self, inter: disnake.AppCommandInteraction,
                   query: str = commands.Param(
                       description='The search input'
                   )):
        await inter.response.defer()

        url = f'https://wiki.hypixel.net/index.php?search={query}&title=Special%3ASearch'

        response = requests.get(url)

        if response.status_code == 200:
            final_url = response.url

            soup = BeautifulSoup(response.text, 'html.parser')

            result_title = soup.find('div', {'class': 'page-heading'}).text.strip()

            embed = disnake.Embed(
                title=result_title,
                description=f'搜尋 {query} 結果',
                url=final_url,
                color=0x7289DA
            )

            if result_title.endswith('(disambiguation)'):
                listspacing = soup.find('div', {'class': 'listspacing'})
                if listspacing:
                    list_items = listspacing.find_all('li')

                    for item in list_items:
                        name_links = item.find_all('a', {'title': True})
                        if name_links:
                            for name_link in name_links:
                                link_title = name_link.text.strip()
                                link_url = 'https://wiki.hypixel.net' + name_link['href']

                                if link_title:
                                    embed.add_field(name=link_title, value=link_url, inline=False)
                                    break
            elif result_title == 'Search results':
                search_results = soup.find('ul', {'class': 'mw-search-results'})

                if search_results:
                    links = search_results.find_all('a')

                    for link in links:
                        link_title = link.text.strip()
                        link_url = 'https://wiki.hypixel.net' + link['href']
                        embed.add_field(name=link_title, value=link_url, inline=False)
            else:
                info_box = soup.find('table', {'class': 'infobox'})

                # get simple information from info box
                if info_box:

                    image_tag = info_box.find('img')
                    if image_tag and 'src' in image_tag.attrs:
                        image_url = 'https://wiki.hypixel.net' + image_tag['src']

                        embed.set_thumbnail(url=image_url)

                    rows = info_box.find_all('tr')

                    added_types = []

                    for row in rows:
                        cells = row.find_all('td')

                        if len(cells) == 2:
                            field = cells[0].text.strip()
                            value_cell = cells[1]

                            if field == 'Category':
                                value = value_cell.get_text(strip=True)
                                embed.add_field(name='分類: ', value=value, inline=False)

                            elif field == 'Type':
                                value = value_cell.get_text(strip=True)

                                if value not in added_types:
                                    embed.add_field(name='類型: ', value=value, inline=False)

                                    added_types.append(value)

                            elif field == 'Rarity':
                                value = value_cell.get_text(strip=True)
                                embed.add_field(name='稀有度: ', value=value, inline=False)

                            elif field == 'Internal ID':
                                value_div = value_cell.find('div', class_='hp-spoiler-text')

                                if value_div:
                                    value = value_div.decode_contents(formatter="html").replace("<br/>", "\n").replace("<wbr/>", "")
                                else:
                                    value = value_cell.text.strip()

                                embed.add_field(name='物品 id: ', value=value.strip(), inline=False)

                content = soup.find('div', {'class': 'mw-parser-output'})

                if content:
                    headings = content.find_all('h2')

                    for heading in headings:
                        title = heading.text.strip()

                        if title in ['Loot', 'Upgrading']:
                            continue

                        next_element = heading.find_next_sibling()

                        while next_element and next_element.name in ['p', 'ul', 'blockquote']:
                            if next_element.name in ['p', 'ul', 'blockquote']:
                                description_text = next_element.text.strip()

                                if description_text is not None:
                                    embed.add_field(name=title, value=description_text, inline=False)
                                    title = ' '

                            next_element = next_element.find_next_sibling()


            set_inter_embed_author(embed, inter)

            await inter.send(embed=embed)
        else:
            embed = disnake.Embed(
                title='查詢失敗',
                description='訪問 wiki 失敗，請稍後重試',
                color=0xe74c3c
            )

            set_inter_embed_author(embed, inter)

            await inter.send(embed=embed, ephemeral=True)

def setup(pybot):
    pybot.add_cog(SlashWiki(pybot))

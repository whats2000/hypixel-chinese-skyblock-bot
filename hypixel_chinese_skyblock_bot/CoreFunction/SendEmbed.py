import disnake

from CoreFunction.Common import get_setting_json


def inter_build_embed(case: str, inter: disnake.AppCommandInteraction) -> disnake.Embed:
    if case == 'Wrong Channel':
        embed = disnake.Embed(
            title='請在正確頻道輸入',
            color=0xe74c3c
        )

        set_inter_embed_author(embed, inter)

    elif case == 'Missing Id':
        channel_id = get_setting_json('VerifyIdChannelId')

        embed = disnake.Embed(
            title='你未登記id，請先登記id',
            description=f'{inter.author} 你需要先驗證後才可用該命令，請到 <#{channel_id}> 驗證',
            color=0xe74c3c
        )

        set_inter_embed_author(embed, inter)

    elif case == 'Missing Api':
        embed = disnake.Embed(
            title='驗證失敗，請先打開 hypixel discord api',
            description=f'{inter.author} 你需先開啟 Hypixel Api 詳細請用 `/help` 查看如何開啟',
            color=0xe74c3c
        )

        set_inter_embed_author(embed, inter)

    else:
        embed = disnake.Embed(
            title='驗證失敗，未知錯誤類別',
            description=f'{inter.author} 請回報管理員該錯誤',
            color=0xe74c3c
        )

        set_inter_embed_author(embed, inter)

    return embed


def set_inter_embed_author(embed, inter):
    if inter.author.avatar.url is not None:
        embed.set_author(
            name=inter.author.name,
            icon_url=inter.author.avatar.url
        )
    else:
        embed.set_author(
            name=inter.author.name
        )


def set_ctx_embed_author(embed, ctx):
    if ctx.message.author.avatar.url is not None:
        embed.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar.url
        )
    else:
        embed.set_author(
            name=ctx.message.author.name,
        )

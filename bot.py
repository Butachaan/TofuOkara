
import discord

import json
from typing import Union
import logging
import textwrap

import asyncio
import random
import datetime
import DiscordUtils

from discord.ext import commands
Intents = discord.Intents.all()
with open(f"config.json","r",encoding="utf-8") as j:
    f = json.load(j)


bot = commands.Bot(command_prefix=f["prefix"],owner_id=478126443168006164,Intents=Intents)





class Help(commands.HelpCommand):
    def __init__(self):
        super().__init__()
        self.no_category = "カテゴリ未設定"
        self.command_attrs["description"] = "このメッセージを表示します。"
        self.command_attrs["help"] = "このBOTのヘルプコマンドです。"

    async def create_category_tree(self, category, enclosure):
        """
        コマンドの集まり（Group、Cog）から木の枝状のコマンドリスト文字列を生成する。
        生成した文字列は enlosure 引数に渡された文字列で囲われる。
        """
        content = ""
        command_list = category.walk_commands()
        for cmd in await self.filter_commands(command_list, sort=True):
            if cmd.root_parent:
                # cmd.root_parent は「根」なので、根からの距離に応じてインデントを増やす
                index = cmd.parents.index(cmd.root_parent)
                indent = "\t" * (index + 1)
                if indent:
                    content += f"{indent}- {cmd.name} / {cmd.description}\n"
                else:
                    # インデントが入らない、つまり木の中で最も浅く表示されるのでprefixを付加
                    content += f"{self.context.prefix}{cmd.name} / {cmd.description}\n"
            else:
                # 親を持たないコマンドなので、木の中で最も浅く表示する。prefixを付加
                content += f"{self.context.prefix}{cmd.name} / {cmd.description}\n"

        return enclosure + textwrap.dedent(content) + enclosure

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="helpコマンド", color=0x5d00ff)
        if self.context.bot.description:
            # もしBOTに description 属性が定義されているなら、それも埋め込みに追加する
            embed.description = self.context.bot.description
            embed.add_field(name="サポート", value="https://discord.gg/uPbXyFh6")
        for cog in mapping:
            if cog:
                cog_name = cog.qualified_name
            else:
                # mappingのキーはNoneになる可能性もある
                # もしキーがNoneなら、自身のno_category属性を参照する
                cog_name = self.no_category

            command_list = await self.filter_commands(mapping[cog], sort=True)
            content = ""
            for cmd in command_list:
                content += f"`{cmd.name}` "
            embed.add_field(name=cog_name, value=content, inline=False)

        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog):
        embed = discord.Embed(title=cog.quaylified_name, description=cog.description, color=0x00ff00)
        embed.add_field(name="コマンドリスト：", value=await self.create_category_tree(cog, "```"))
        await self.get_destination().send(embed=embed)

    async def send_group_help(self, group):
        embed = discord.Embed(title=f"{self.context.prefix}{group.qualified_name}",
                              description=group.description, color=0x00ff00)
        if group.aliases:
            embed.add_field(name="有効なエイリアス：", value="`" + "`, `".join(group.aliases) + "`", inline=True)
        if group.help:
            embed.add_field(name="必要な権限：", value=group.help, inline=True)
        embed.add_field(name="サブコマンドリスト：", value=await self.create_category_tree(group, "```"), inline=True)
        await self.get_destination().send(embed=embed)

    async def send_command_help(self, command):
        params = " ".join(command.clean_params.keys())
        embed = discord.Embed(title=f"{self.context.prefix}{command.qualified_name} {params}",
                              description=command.description, color=0x00ff00)
        if command.aliases:
            embed.add_field(name="有効なエイリアス：", value="`" + "`, `".join(command.aliases) + "`", inline=True)
        if command.help:
            embed.add_field(name="必要な権限：", value=command.help, inline=True)
        if command.name:
            embed.add_field(name="name", value=command.name, inline=True)

        await self.get_destination().send(embed=embed)

    async def send_error_message(self, error):
        embed = discord.Embed(title="ヘルプ表示のエラー", description=error, color=0xff0000)
        await self.get_destination().send(embed=embed)

    def command_not_found(self, string):
        return f"{string} というコマンドは存在しません。"

    def subcommand_not_found(self, command, string):
        if isinstance(command, commands.Group) and len(command.all_commands) > 0:
            # もし、そのコマンドにサブコマンドが存在しているなら
            return f"{command.qualified_name} に {string} というサブコマンドは登録されていません。"
        return f"{command.qualified_name} にサブコマンドは登録されていません。"


bot = commands.Bot(command_prefix="to:", help_command=Help(), description="```to:helps で調べられます``` ")




bot.load_extension('ext.info')
bot.load_extension('ext.admin')
bot.load_extension('ext.other')
bot.load_extension('ext.moderation')
bot.load_extension('ext.report')
bot.load_extension('ext.fun')



bot.load_extension("jishaku")
@bot.event
async def on_command(ctx):
    e = discord.Embed(title="コマンド実行ログ", description=f"実行分:`{ctx.message.clean_content}`")
    e.set_author(name=f"{ctx.author}({ctx.author.id})", icon_url=ctx.author.avatar_url_as(static_format="png"))
    e.add_field(name="実行サーバー", value=f"{ctx.guild.name}({ctx.guild.id})")
    e.add_field(name="実行チャンネル", value=ctx.channel.name)
    e.set_thumbnail(url=ctx.guild.icon_url)
    e.timestamp = ctx.message.created_at
    ch = bot.get_channel(803558816834650152)

    await ch.send(embed=e)


@bot.event
async def on_ready():
    activity = discord.Game(name="to:helpsで確認", type=3)
    await bot.change_presence(status=discord.Status.idle, activity=activity)
    print("Bot is ready!")


bot.remove_command('help')
@bot.command()
async def help(ctx):
    e1 = discord.Embed(title="Helpメニュー", description="`to:help <コマンド>`で確認できます\n```接頭辞:to:```",
                       color=0x5d00ff).add_field(name="`豆腐ログ`というチャンネルを使うと自動でログチャンネルになります`", value="Page 1")
    e1.set_thumbnail(
        url="https://images-ext-1.discordapp.net/external/AmvDNxw_njYIs1oblYB2zAGerdJXk5qp6QHW0s0Rslo/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/803281008703176706/9327faa387255c25d6cb69d70a839f51.png?width=493&height=493")

    e2 = discord.Embed(title="information", color=0x5d00ff).add_field(name="Example", value="Page 2")
    e2.add_field(name="**userinfo <user>**", value="ユーザーの情報を表示します", inline=False)
    e2.add_field(name="**user <user>**", value="外部ユーザーの情報を表示します", inline=False)
    e2.add_field(name="**serverinfo <server>**", value="サーバーの情報を表示します", inline=False)
    e2.add_field(name="**roleinfo <role>**", value="役職の情報を表示します", inline=False)
    e2.add_field(name="**channelinfo <channel>**", value="チャンネルの情報を表示します", inline=False)
    e2.add_field(name="**messageinfo <message>**", value="メッセージの情報を表示します", inline=False)
    e2.add_field(name="**avatar <user>**", value="ユーザーのアバターの情報を表示します", inline=False)
    e2.add_field(name="**emoji**", value="絵文字を表示します")
    e3 = discord.Embed(title="Moderation", color=0x5d00ff).add_field(name="モデレーション機能です", value="Page 3")
    e3.add_field(name="**kick <user> <reason>**", value="ユーザーをサーバーからkickします", inline=True)
    e3.add_field(name="**ban <user> <reason>**", value="ユーザーをサーバーからbanします", inline=True)
    e3.add_field(name="**unban <user>**", value="BANされたユーザーをban解除します", inline=True)
    e3.add_field(name="**hackban <user> <reason>**", value="ユーザーをhackbanします", inline=True)
    e3.add_field(name="**baninfo <user>**", value="banされたユーザーのban情報を表示します", inline=True)
    e3.add_field(name="**banlist**", value="banされたユーザー一覧を表示します", inline=True)
    e3.add_field(name="**poll <質問内容>**", value="アンケートを取れます", inline=True)
    e3.add_field(name="**addrole <user> <役職>**", value="ユーザーに役職を付与します", inline=True)
    e3.add_field(name="**removerole <user> <役職>**", value="ユーザーの役職を剥奪します", inline=True)
    e3.add_field(name="**mute <user> <秒数>**", value="ユーザーを指定した秒数muteします", inline=True)
    e3.add_field(name="**unmute <muteされたuser>**", value="muteを解除します", inline=True)
    e3.add_field(name="**purge <数字>**", value="指定された文字数分文章を消します")
    e4 = discord.Embed(title="everyone", description="誰でも使えます", colro=0x5d00ff)
    e4.add_field(name="**timer <秒数>**", value="タイマー機能です")
    e4.add_field(name="**invite**", value="招待リンクを表示します")
    e4.add_field(name="**official**", value="サポート鯖のリンクを表示します")
    e4.add_field(name="**ping**", value="ネットの速さを知れます")
    e4.add_field(name="**say <内容>**", value="幽々子に言いたいことを言わせます")
    e5 = discord.Embed(title="admin", description="page4", color=0x5d00ff)
    e5.add_field(name="**load/unload/reload <extension名>**", value="ファイルをロード/アンロード/リロードします",
                 inline=False)
    e5.add_field(name="**eval <コード>**", value="コードをevaluate(評価)します")
    e4.add_field(name="**changestatus <status>**", value="幽々子のステータスを変えます")
    e5.add_field(name="**changenick <名前>**", value="ユーザーのニックネームを変えます")
    e5.add_field(name="**set_playing <game名>**", value="幽々子のplaying statuを変えます")
    e5.add_field(name="**announce <内容>**", value="運営がアナウンスをします")
    e5.add_field(name="**dm <user> <内容>**", value="指定したユーザーにDMを送ります")
    e5.add_field(name="**servers**", value="botが入ってるサーバー一覧を表示します")
    e5.add_field(name="**system_shutdown**", value="botを停止します")
    e5.add_field(name="**log <数>**", value="指定された数分のメッセージを保存します")
    e6 = discord.Embed(title="fun", descriotion="お遊び機能です", color=0x5d00ff)
    e6.add_field(name="**password**", value="DMに暗号文を表示します")
    e6.add_field(name="**slot**", value="スロットをします")
    e7 = discord.Embed(title="report", description="何かあれば", color=0x5d00ff)
    e7.add_field(name="**request <要望> <理由>**", value="リクエスト随時受付中です")
    e7.add_field(name="**feedback <内容>**", value="フィートバックを送ります")

    e2.set_thumbnail(
        url="https://images-ext-1.discordapp.net/external/AmvDNxw_njYIs1oblYB2zAGerdJXk5qp6QHW0s0Rslo/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/803281008703176706/9327faa387255c25d6cb69d70a839f51.png?width=493&height=493")
    e3.set_thumbnail(
        url="https://images-ext-1.discordapp.net/external/AmvDNxw_njYIs1oblYB2zAGerdJXk5qp6QHW0s0Rslo/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/803281008703176706/9327faa387255c25d6cb69d70a839f51.png?width=493&height=493")
    e4.set_thumbnail(
        url="https://images-ext-1.discordapp.net/external/AmvDNxw_njYIs1oblYB2zAGerdJXk5qp6QHW0s0Rslo/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/803281008703176706/9327faa387255c25d6cb69d70a839f51.png?width=493&height=493")
    e5.set_thumbnail(
        url="https://images-ext-1.discordapp.net/external/AmvDNxw_njYIs1oblYB2zAGerdJXk5qp6QHW0s0Rslo/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/803281008703176706/9327faa387255c25d6cb69d70a839f51.png?width=493&height=493")
    e6.set_thumbnail(
        url="https://images-ext-1.discordapp.net/external/AmvDNxw_njYIs1oblYB2zAGerdJXk5qp6QHW0s0Rslo/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/803281008703176706/9327faa387255c25d6cb69d70a839f51.png?width=493&height=493")
    e7.set_thumbnail(
        url="https://images-ext-1.discordapp.net/external/AmvDNxw_njYIs1oblYB2zAGerdJXk5qp6QHW0s0Rslo/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/803281008703176706/9327faa387255c25d6cb69d70a839f51.png?width=493&height=493")

    paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx)
    paginator.add_reaction('⏮️', "first")
    paginator.add_reaction('⏪', "back")
    paginator.add_reaction('🔐', "lock")
    paginator.add_reaction('⏩', "next")
    paginator.add_reaction('⏭️', "last")
    embeds = [e1, e2, e3, e4, e5, e6, e7]
    await paginator.run(embeds)


@bot.event
async def on_user_update(before, after):
    if before.name != after.name:
        e = discord.Embed(title="ニックネームが変わりました", color=0x5d00ff, timestamp=datetime.utcnow())
        fields = [("Before", before.name, False), ("After", after.name, False)]

        for name, value, inline in fields:
            e.add_field(name=name, value=value, inline=inline)

        channel = discord.utils.get(before.get_channels, name="幽々子ログ")
        await channel.send(embed=e)


@bot.event
async def on_guild_channel_create(channel):
    e = discord.Embed(title="チャンネル作成", timestamp=channel.created_at,color=0x5d00ff)
    e.add_field(name="チャンネル名", value=channel.mention)
    channel = discord.utils.get(channel.guild.channels, name="幽々子ログ")
    await channel.send(embed=e)

@bot.event
async def on_member_ban(g, user):
    guild = bot.get_guild(g.id)
    bl = await guild.audit_logs(limit=1, action=discord.AuditLogAction.ban).flatten()
    e = discord.Embed(title="ユーザーのban", color=0x5d00ff)
    e.add_field(name="ユーザー名", value=str(user))
    e.add_field(name="実行者", value=str(bl[0].user))
    channel = discord.utils.get(bot.get.channels, name="幽々子ログ")
    await channel.send(embed=e)

@bot.event
async def on_invite_create(invite):
    e = discord.Embed(title="サーバー招待の作成", color=0x5d00ff)
    e.add_field(name="作成ユーザー", value=str(invite.inviter))
    e.add_field(name="使用可能回数", value=str(invite.max_uses))
    e.add_field(name="使用可能時間", value=str(invite.max_age))
    e.add_field(name="チャンネル", value=str(invite.channel.mention))
    e.add_field(name="コード", value=str(invite.code))
    channel = discord.utils.get(invite.guild.channels, name="幽々子ログ")
    await channel.send(embed=e)




@bot.event
async def on_message_delete(message):
    if not message.author.bot:
        e = discord.Embed(title="メッセージ削除", color=0x5d00ff)
        e.add_field(name="メッセージ", value=f'```{message.content}```',inline=False)
        e.add_field(name="メッセージ送信者", value=message.author.mention)
        e.add_field(name="メッセージチャンネル", value=message.channel.mention)
        e.add_field(name="メッセージのid", value=message.id)

        channel = discord.utils.get(message.guild.channels, name="幽々子ログ")
        await channel.send(embed=e)

@bot.event
async def on_guild_role_update(before, after):
    print("1")
    if before.name != after.name:
        embed = discord.Embed(title="Role " + before.name + " renamed to " + after.name + ".",color=0x5d00ff)

        embed.set_author(name="名前が変りました")
        embed.add_field(name="id",value=after.id)
        embed.add_field(name="名前",value=after.name)
        embed.add_field(name="位置", value=after.position)
        channel = discord.utils.get(before.guild.channels, name="幽々子ログ")
        await channel.send(embed=embed)

    if before.color != after.color:
        e = discord.Embed(title="Role " + before.name + " change to " + after.name + ".",color=0x5d00ff)
        e.set_author(name="色が変りました")
        e.add_field(name="id", value=after.id)
        e.add_field(name="名前", value=after.name)
        e.add_field(name="位置",value=after.position)
        channel = discord.utils.get(before.guild.channels, name="幽々子ログ")
        await channel.send(embed=e)


@bot.event
async def on_message_edit(before, after):

    embed = discord.Embed(
        title="メッセージが編集されました",
        timestamp=after.created_at,
        description = f"<#{before.channel.id}>で<@!{before.author.id}>がメッセージを編集しました",
        colour = discord.Colour(0x5d00ff)
        )
    embed.set_author(name=f'{before.author.name}#{before.author.discriminator}', icon_url=before.author.avatar_url)
    embed.set_footer(text=f"Author ID:{before.author.id} • Message ID: {before.id}")
    embed.add_field(name='Before:', value=before.content, inline=False)
    embed.add_field(name="After:", value=after.content, inline=False)
    embed.add_field(name="メッセージのURL", value=after.jump_url)
    channel = discord.utils.get(after.guild.channels, name="幽々子ログ")
    await channel.send(embed=embed)




@bot.event
async def on_guild_role_create(role):
    e = discord.Embed(title="役職の作成", color=0x5d00ff,timestamp=role.created_at)
    e.add_field(name="役職名", value=role.name)

    e.add_field(name="id", value=role.id)

    ch = discord.utils.get(role.guild.channels, name="幽々子ログ")
    await ch.send(embed=e)

@bot.event
async def on_guild_role_delete(role):
    e = discord.Embed(title="役職の削除", color=0x5d00ff)
    e.add_field(name="役職名", value=role.name)

    ch = discord.utils.get(role.guild.channels, name="幽々子ログ")
    await ch.send(embed=e)


@bot.event
async def on_guild_channel_delete(channel):
    e = discord.Embed(title="チャンネル削除", color=0x5d00ff)
    e.add_field(name="チャンネル名", value=channel.name)
    ch = discord.utils.get(channel.guild.channels, name="幽々子ログ")
    await ch.send(embed=e)




@bot.event
async def on_guild_channel_update(before, after):
    channel = discord.utils.get(before.guild.channels, name="幽々子ログ")
    embed = discord.Embed(title="Channel Name Updated", description="チャンネルがアップデートしました",color=0x5d00ff)
    embed.add_field(name="Old name", value=f"The old name was: {before}.", inline=True)
    embed.add_field(name="New name", value=f"The old name was: {after}.", inline=False)
    await channel.send(embed=embed)

@bot.event
async def on_voice_state_update(before, after):
    if before.voice.voice_channel is None and after.voice.voice_channel is not None:
        for channel in before.server.channels:
            if channel.name == 'あざ':
                await bot.send_message(channel, "Howdy")




@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingPermissions):
        e1 = discord.Embed(title="権限がありません")
        await ctx.send(embed=e1)

    elif isinstance(error,commands.MissingRequiredArgument):
        e2 = discord.Embed(title="必要なすべての引数を入力してください")
        await ctx.send(embed=e2)

    elif isinstance(error, commands.CommandNotFound):
        e3 = discord.Embed(title="コマンドが存在しません")
        await ctx.send(embed=e3)

    elif isinstance(error, commands.ChannelNotFound):
        e4 = discord.Embed(title="チャンネルが存在しません")
        await ctx.send(embed=e4)

    elif isinstance(error, commands.UserNotFound):
        e5 = discord.Embed(title="ユーザーが存在しません")
        await ctx.send(embed=e5)


    elif isinstance(error,commands.RoleNotFound):
        e6 = discord.Embed(title="役職が存在しません")
        await ctx.send(embed=e6)





@bot.event
async def on_member_join(member):
    # On member joins we find a channel called general and if it exists,
    # send an embed welcoming them to our guild
    channel = discord.utils.get(member.guild.text_channels, name="幽々子ログ")
    if channel:
        embed = discord.Embed(
            description="Welcome to our guild!",
            color=0x5d00ff,
        )
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_author(name=member.name, icon_url=member.avatar_url)
        embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
        embed.timestamp = datetime.datetime.utcnow()

        await channel.send(embed=embed)



@bot.event
async def on_member_remove(member):
    # On member remove we find a channel called general and if it exists,
    # send an embed saying goodbye from our guild-
    channel = discord.utils.get(member.guild.text_channels, name="recording")
    if channel:
        embed = discord.Embed(
            description="Goodbye from all of us..",
            color=0x5d00ff,
        )
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_author(name=member.name, icon_url=member.avatar_url)
        embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
        embed.timestamp = datetime.datetime.utcnow()

        await channel.send(embed=embed)



bot.run(f["TOKEN"])




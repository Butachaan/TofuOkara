import textwrap
from discord import Intents
import typing
import aiohttp
from datetime import datetime, timedelta
from typing import Optional

from typing import Union
import time

import platform
from discord.ext import commands
from platform import python_version
from discord import __version__ as discord_version
from asyncio import sleep
import json
from discord.utils import get

from collections import OrderedDict, deque, Counter
import datetime
import os

import asyncio, discord
import random
import secrets
from io import BytesIO
import ast
import psutil
import functools
import inspect
from discord.ext.commands import clean_content
from discord import Embed
from discord.ext.commands import Cog
import sys
import json
import traceback
import wikipedia
import io
from contextlib import redirect_stdout
import re
import DiscordUtils
import tracemalloc


class help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def helps(self, ctx):
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


def setup(bot):
    bot.add_cog(help(bot))
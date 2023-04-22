from time import sleep
from typing import List
from disnake.ext import commands
from lib import Logger, get_commands, get_oauth_url
from var import CC, LL, ROLE_OAUTH_URL, ROLE_OAUTH_SCOPE
from webserver import start_server, web
from flask import request
import disnake
import random as rnd
import threading


webserver = threading.Thread(target=start_server, daemon=True)
logger = Logger()

omikuji_list = ["大凶", "凶", "ゴミ", "おわた", "吉かも",
                "吉の可能性あり", "きt", "いやああ吉かなあ...", "勉強しろ"]


class Others(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_interaction(self, interaction: disnake.ApplicationCommandInteraction):
        if interaction.author.bot:
            return
        logger.log(
            LL.TRACE,
            f"{interaction.author.name} sent {CC.BG_BLUE.value}command{CC.BG_DEFAULT.value} `{interaction.application_command.name}` in `{interaction.guild.name if interaction.guild else 'DM'}`",
        )

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.author.bot:
            return
        logger.log(
            LL.TRACE,
            f"{message.author.name} sent {CC.BG_CYAN.value}message{CC.BG_DEFAULT.value} `{message.content}` in `{message.guild.name if message.guild else 'DM'}`",
        )

    @commands.command()
    async def dummy(self, ctx: commands.Context):
        await ctx.send("dummy")

    @commands.slash_command(description="show help")
    async def help(self, interaction: disnake.ApplicationCommandInteraction):
        bot_commands = await get_commands(self.bot)
        embed = disnake.Embed(
            title="Help",
            description="help about commands",
            color=0xffffff,
        )
        slash_commands_text = ""
        message_commands_text = ""
        for i in bot_commands["slash_commands"]:
            slash_commands_text += f"`/{i.name}`\n"
        for i in bot_commands["message_commands"]:
            message_commands_text += f"`th!{i.name}`\n"
        embed.add_field("Slash Commands", slash_commands_text, inline=False)
        embed.add_field("Message Commands",
                        message_commands_text, inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @commands.slash_command(description="おみくじ")
    async def omikuji(self, interaction: disnake.ApplicationCommandInteraction):
        class OmikujiText:
            self.texts: List[str]
            self.title: str

            def __init__(self, title="**おみくじの結果はこちら**"):
                self.texts = []
                self.title = title

            def add(self, text: str):
                self.texts.append(text)

            def __str__(self) -> str:
                return (
                    self.title
                    + "\n┏━┓\n"
                    + "\n".join(map(lambda text: f"┃{text}┃", self.texts))
                    + "\n┗━┛"
                )

        result = rnd.choice(omikuji_list)
        title = "**おみくじの結果はこちら！**"
        omikuji_text = OmikujiText()
        await interaction.response.send_message(title)
        for i in result:
            sleep(0.3)
            omikuji_text.add(i)
            logger.log(str(omikuji_text.texts), LL.DEBUG)
            await interaction.edit_original_message(str(omikuji_text))


class OnReady(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def first_log_commands(self):
        slash_commands = await self.bot.fetch_global_commands()
        commands = self.bot.commands
        logger.log("slash commands", LL.DEBUG, custom_formats=[CC.BOLD])
        for i in slash_commands:
            logger.log(f"{i.name}", LL.DEBUG)
        logger.log("message commands", LL.DEBUG, custom_formats=[CC.BOLD])
        for i in commands:
            logger.log(f"{i.name}", LL.DEBUG)

    @commands.Cog.listener()
    async def on_ready(self):
        logger.log(f"logged in as {self.bot.user.name}", LL.INFO)
        await self.first_log_commands()
        logger.log("starting web server thread", LL.INFO)
        webserver.start()


class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(description="ping to bot")
    async def ping(self, interaction: disnake.ApplicationCommandInteraction):
        embed = disnake.Embed(
            title="pong!", color=0x00ff00, timestamp=interaction.created_at
        )
        embed.add_field(
            name="Latency", value=f"`{round(self.bot.latency * 1000)}ms`")
        await interaction.response.send_message(embed=embed)

    @commands.slash_command(description="ping to bot silently")
    async def silent_ping(self, interaction: disnake.ApplicationCommandInteraction):
        embed = disnake.Embed(
            title="pong!", color=0x00ff00, timestamp=interaction.created_at
        )
        embed.add_field(
            name="Latency", value=f"`{round(self.bot.latency * 1000)}ms`")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @commands.command(name="ping", aliases=["latency", "latence"])
    async def message_ping(self, ctx: commands.Context):
        embed = disnake.Embed(
            title="pong!", color=0x00ff00, timestamp=ctx.message.created_at
        )
        embed.add_field(
            name="Latency", value=f"`{round(self.bot.latency * 1000)} ms`")

        await ctx.send(embed=embed)


class Verify(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


def setup(bot: commands.Bot):
    bot.add_cog(Ping(bot))
    bot.add_cog(OnReady(bot))
    bot.add_cog(Others(bot))

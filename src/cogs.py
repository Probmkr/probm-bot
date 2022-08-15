from time import sleep
from typing import List
from disnake.ext import commands
from lib import Logger, get_commands, get_oauth_url
from var import CC, LT, ROLE_OAUTH_URL
import disnake
import random as rnd

logger = Logger()

omikuji_list = ["大凶", "凶", "ゴミ", "おわた", "吉かも", "吉の可能性あり", "きt", "いやああ吉かなあ...", "勉強しろ"]


class Others(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_interaction(self, interaction: disnake.ApplicationCommandInteraction):
        logger.log(
            LT.TRACE, f"{interaction.author.name} sent command `{interaction.application_command.name}` in `{interaction.guild.name if interaction.guild else 'DM'}`")

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        logger.log(
            LT.TRACE, f"{message.author.name} sent message `{message.content}` in `{message.guild.name if message.guild else 'DM'}`")

    @commands.command()
    async def dummy(self, ctx: commands.Context):
        await ctx.send("dummy")

    @commands.slash_command(description="show help")
    async def help(self, interaction: disnake.ApplicationCommandInteraction):
        bot_commands = await get_commands(self.bot)
        embed = disnake.Embed(
            title="Help", description="help about commands", color=0x7799+rnd.randrange(0, 0x100))
        slash_commands_text = ""
        message_commands_text = ""
        for i in bot_commands["slash_commands"]:
            slash_commands_text += f"`/{i.name}`\n"
        for i in bot_commands["message_commands"]:
            message_commands_text += f"`th!{i.name}`\n"
        embed.add_field("Slash Commands", slash_commands_text, inline=False)
        embed.add_field("Message Commands",
                        message_commands_text, inline=False)
        await interaction.response.send_message("this feature is not implemented yet", embed=embed)

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
                return self.title + "\n┏━┓\n" + "\n".join(map(lambda text: f"┃{text}┃", self.texts)) + "\n┗━┛"

        result = rnd.choice(omikuji_list)
        title = "**おみくじの結果はこちら！**"
        omikuji_text = OmikujiText()
        await interaction.response.send_message(title)
        for i in result:
            sleep(0.3)
            omikuji_text.add(i)
            logger.log(LT.DEBUG, str(omikuji_text.texts))
            await interaction.edit_original_message(str(omikuji_text))


class OnReady(commands.Cog):
    def __init__(self, bot: disnake.Client):
        self.bot = bot

    async def first_log_commands(self):
        slash_commands = await self.bot.fetch_global_commands()
        commands = self.bot.commands
        logger.log(LT.DEBUG, f"slash commands", custom_formats=[CC.BOLD])
        for i in slash_commands:
            logger.log(LT.DEBUG, f"{i.name}")
        logger.log(LT.DEBUG, f"message commands", custom_formats=[CC.BOLD])
        for i in commands:
            logger.log(LT.DEBUG, f"{i.name}")

    @commands.Cog.listener()
    async def on_ready(self):
        logger.log(LT.INFO, f"Logged in as {self.bot.user.name}")
        await self.first_log_commands()


class Ping(commands.Cog):
    def __init__(self, bot: disnake.Client):
        self.bot = bot

    @commands.slash_command(description="ping to bot")
    async def ping(self, interaction: disnake.ApplicationCommandInteraction):
        embed = disnake.Embed(title="pong!", color=0x00ff00,
                              timestamp=interaction.created_at)
        embed.add_field(
            name="Latency", value=f"`{round(self.bot.latency * 1000)}ms`")
        await interaction.response.send_message(embed=embed)

    @commands.slash_command(description="ping to bot silently")
    async def silent_ping(self, interaction: disnake.ApplicationCommandInteraction):
        embed = disnake.Embed(title="pong!", color=0x00ff00,
                              timestamp=interaction.created_at)
        embed.add_field(
            name="Latency", value=f"`{round(self.bot.latency * 1000)}ms`")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @commands.command(name="ping", aliases=["latency", "latence"])
    async def message_ping(self, ctx: commands.Context):
        embed = disnake.Embed(
            title="pong!", color=0x00ff00, timestamp=ctx.message.created_at)
        embed.add_field(name="Latency",
                        value=f"`{round(self.bot.latency * 1000)} ms`")

        await ctx.send(embed=embed)


class Verify(commands.Cog):
    def __init__(self, bot: disnake.Client):
        self.bot = bot

    async def give_role(self, interaction: disnake.ApplicationCommandInteraction, role: disnake.Role):
        if role in interaction.author.roles:
            await interaction.response.send_message("You already have this role!", ephemeral=True)
            return
        await interaction.author.add_roles(role)
        await interaction.response.send_message(f"You have been given the role `{role.name}`", ephemeral=True)
        logger.log(
            LT.INFO, f"Giving role {role.name} to {interaction.author.name}")

    @commands.slash_command(name="get_role", description="get role", options=[
        disnake.Option(name="role", description="role to get",
                       type=disnake.OptionType.role, required=True)
    ])
    async def get_role(self, interaction: disnake.ApplicationCommandInteraction):
        if interaction.author.guild_permissions.administrator:
            view = disnake.ui.View()
            url = get_oauth_url(
                self.bot.user.id, ROLE_OAUTH_URL, state=interaction.guild.id)
            print(url)
            print("https://discord.com/api/oauth2/authorize?client_id=1004037991871815812&redirect_uri=https%3A%2F%2Fverify.probmkr.com%2Fverify&response_type=code&scope=identify")
            button = disnake.ui.Button(
                label="Get Role", style=disnake.ButtonStyle.primary, url=url)
            # button.callback = lambda inter: self.give_role(
            #     inter, interaction.options["role"])
            view.add_item(button)
            embed = disnake.Embed(
                title="Get Role", description=f"You can click the button below to get the role: <@&{interaction.options['role'].id}>", color=0x5555ee)
            await interaction.response.send_message(embed=embed, view=view)
        else:
            await interaction.response.send_message("You need administrator permissions to use this command!", ephemeral=True)

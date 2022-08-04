from disnake.ext import commands
from lib import Logger, get_oauth_url
from var import LT
import disnake

logger = Logger()


class OnReady(commands.Cog):
    def __init__(self, bot: disnake.Client):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.log(LT.INFO, f"Logged in as {self.bot.user.name}")


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
        await interaction.response.send_message("pong!", ephemeral=True)


class MessagePing(commands.Cog):
    def __init__(self, bot: disnake.Client):
        self.bot = bot

    @commands.command(aliases=["latency", "latence"])
    async def ping(self, ctx: commands.Context):
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
            button = disnake.ui.Button(
                label="Get Role", style=disnake.ButtonStyle.primary, custom_id="get_role", url=get_oauth_url())
            # button.callback = lambda inter: self.give_role(
            #     inter, interaction.options["role"])
            view.add_item(button)
            embed = disnake.Embed(
                title="Get Role", description="You can click the button below to get a role.", color=0x5555ee)
            await interaction.response.send_message(embed=embed, view=view)
        else:
            await interaction.response.send_message("You need administrator permissions to use this command!", ephemeral=True)


class LogCommands(commands.Cog):
    def __init__(self, bot: disnake.Client):
        self.bot = bot

    @commands.Cog.listener()
    async def on_interaction(self, interaction: disnake.ApplicationCommandInteraction):
        logger.log(LT.TRACE, f"{interaction.author.name} sent command `{interaction.application_command.name}`")

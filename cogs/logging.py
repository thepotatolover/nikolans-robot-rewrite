import discord
from discord.ext import commands
from discord_webhook import DiscordEmbed, AsyncDiscordWebhook, DiscordWebhook

class rls(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

        webhook = DiscordWebhook(url=self.bot.logginghook, username=f"{self.bot.logginghookname} - hi")
        whembed = DiscordEmbed(title="Cog Loaded!", description="The logging cog has been loaded successfully!", color="03b2f8")
        whembed.set_timestamp()
        webhook.add_embed(whembed)
        webhook.execute()


    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.respond(
                f"The resource is being ratelimited, try again in {error.retry_after:.2f} seconds :3",
                ephemeral=True)
            rlhook = AsyncDiscordWebhook(url=self.bot.logginghook, username=f"{self.bot.logginghookname} - ratelimited user")
            rlembed = DiscordEmbed(title="Ratelimited user", description=f"User {ctx.author.name} ({ctx.author.id}) got ratelimited while trying to run {ctx.command} :(", color="ff0000")
            rlembed.set_timestamp()
            rlhook.add_embed(rlembed)
            await rlhook.execute()
        else:
            if ctx.selected_options:
                fancyoptions = ', '.join(f"{option['name']}: {option['value']}" for option in ctx.selected_options)
            else:
                fancyoptions = ''
            print(f"Error in command {ctx.command} {fancyoptions}: {error}")
            embed = discord.Embed(title = "Error", description = f"An unknown error has occured. This has been reported to the developers.")
            embed.color = discord.Colour.red()
            await ctx.respond(embed=embed, ephemeral=True)
            rlhook = AsyncDiscordWebhook(url=self.bot.suggestionshook, username=f"{self.bot.logginghookname} - error")
            rlembed = DiscordEmbed(title="Unknown Error", description=f"User {ctx.author.name} ({ctx.author.id}) got an error while trying to run {ctx.command} :(\n```{error}```", color="ff0000")
            rlembed.set_timestamp()
            rlhook.add_embed(rlembed)
            await rlhook.execute()
    
    @commands.Cog.listener()
    async def on_application_command(self, ctx):
        if ctx.selected_options:
            fancyoptions = ', '.join(f"{option['name']}: {option['value']}" for option in ctx.selected_options)
        else:
            fancyoptions = ''
        rlhook = AsyncDiscordWebhook(url=self.bot.logginghook, username=f"{self.bot.logginghookname} - commands")
        if ctx.guild:
            rlembed = DiscordEmbed(title=f"{ctx.user.name} ran a command", description=f"User {ctx.author.name} ({ctx.author.id}) ran `/{ctx.command} {fancyoptions}` in <#{ctx.channel.id}>, `{ctx.guild.name}` (`{ctx.guild.id}`)", color="03b2f8")
        else:
            rlembed = DiscordEmbed(title=f"{ctx.user.name} ran a command", description=f"User {ctx.author.name} ({ctx.author.id}) ran `/{ctx.command} {fancyoptions}` in <#{ctx.channel.id}>, no guild", color="03b2f8")
        rlembed.set_timestamp()
        rlhook.add_embed(rlembed)
        await rlhook.execute()

def setup(bot):
    bot.add_cog(rls(bot))

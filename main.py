import os
import discord
import valo_api
from discord.ext import commands
from matchResults.check_recent_matchs import checkRecentMatches

def main():
    bot = commands.Bot(debug_guilds=[554515721170714634, 433369993346809877])
    valo_api.set_api_key('<YOUR_API_KEY_HERE>')
    
    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user} (ID: {bot.user.id})")
        print("------")
        await bot.change_presence(activity=discord.Game('VALORANT'))
        await checkRecentMatches(bot)

    @bot.slash_command(name='reload')
    async def reload(ctx: discord.commands.context.ApplicationContext, extension):
            await ctx.defer()
            try:
                bot.unload_extension(f'cogs.{extension}')
                bot.load_extension(f'cogs.{extension}')
                await ctx.respond(f'Cog Reloaded: {extension}')
            except:
                await ctx.respond(f'Error reloading Cog: {extension}')
        
    for filename in os.listdir(r"cogs"):
        if filename.endswith('.py'):
                bot.load_extension(f'cogs.{filename[:-3]}')

    bot.run("<YOUR_BOT_TOKEN_HERE>")

if __name__ == '__main__':
    main()
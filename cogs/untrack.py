import os
import json
import asyncio
import discord
import valo_api
from discord.ext import commands

class UntrackCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='untrack', description='Remove a match result alert.')
    @discord.option("name", 
                    type=discord.SlashCommandOptionType.string,
                    description='Riot ID')
    @discord.option("tag", 
                    type=discord.SlashCommandOptionType.string,
                    description='Riot Tag')
    async def match(self, ctx: discord.commands.context.ApplicationContext, name: str, tag: str):
        await ctx.defer()
        try:
            user = valo_api.get_account_details_by_name(version='v1', name=name, tag=tag)

            try:
                with open('alerts.json', 'r') as alerts_file:
                    alerts = json.load(alerts_file)
            except Exception as e:
                await ctx.respond(f'An error has occured:\n`{e}`')
            
            removeIndex = 0 
            canRemove = False

            for index, alert in enumerate(alerts):
                if (alert['puuid'] == user.puuid) and (alert['creator'] == ctx.user.id) and (alert['channel_id'] == ctx.channel_id):
                    removeIndex = index
                    canRemove = True
            
            if canRemove:
                alerts.pop(removeIndex)
                    
                writeComplete = False
                while writeComplete == False:
                    try:
                        with open('alerts.json.lock', 'x') as lock_file:
                            with open('alerts.json', 'w') as alerts_file:
                                json.dump(alerts, alerts_file, indent = 4)
                        os.remove('alerts.json.lock')
                        writeComplete = True
                    
                    except:
                        await asyncio.sleep(15)
                
                await ctx.respond(f'Alert for `{name}#{tag}` removed')

            else:
                await ctx.respond('Alert not Found or You don\'t have permission to remove this account.')
            
        except Exception as e:
            await ctx.respond(f'An error has occured:\n`{e}`')
            

def setup(bot):
    bot.add_cog(UntrackCog(bot))
    print('Cog loaded: Untrack')
                    
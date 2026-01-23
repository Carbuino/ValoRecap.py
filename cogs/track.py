import os
import json
import asyncio
import discord
import valo_api
from discord.ext import commands

class TrackCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='track', description='Have the bot track an accounts match results')
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

                alerts.append({'puuid': user.puuid, 'channel_id': ctx.channel_id, 'creator': ctx.user.id, 'match_id': 'match'})

            except:
                await ctx.respond(f'An error has occured:\n`{e}`')

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
            
            await ctx.respond(f'Alert for `{name}#{tag}` added\nYour most recent match will be sent on the next cycle.')
            
        except Exception as e:
            await ctx.respond(f'An error has occured:\n`{e}`')
            

def setup(bot):
    bot.add_cog(TrackCog(bot))
    print('Cog loaded: Track')
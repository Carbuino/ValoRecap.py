import io
import discord
import valo_api
from discord.ext import commands
from matchResults.match_results import genMessage

class MatchCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='match', description='Get a match breakdown')
    @discord.option("name", 
                    type=discord.SlashCommandOptionType.string,
                    description='Riot ID')
    @discord.option("tag", 
                    type=discord.SlashCommandOptionType.string,
                    description='Riot Tag')
    async def match(self, ctx: discord.commands.context.ApplicationContext, name: str, tag: str):
        await ctx.defer()
        try:
            print(f'Match of {name}#{tag}, Requested by {ctx.author.display_name}')
            user = valo_api.get_account_details_by_name(version='v1', name=name, tag=tag)
            matchId = valo_api.get_match_history_by_puuid_v3(version='v3', region=user.region, puuid=user.puuid, size=1)[0].metadata.matchid
            
            embed, file = genMessage(match_id=matchId, puuid=user.puuid)
            if file:
                with io.BytesIO() as image_binary:
                        file.save(image_binary, 'PNG')
                        image_binary.seek(0)
                        await ctx.respond(file=discord.File(fp=image_binary, filename='match.png'))
            else:
                await ctx.respond(embed=embed)
        except Exception as e:
            await ctx.respond(f'An error has occured:\n`{e}`')
            

def setup(bot):
    bot.add_cog(MatchCog(bot))
    print('Cog loaded: Match')
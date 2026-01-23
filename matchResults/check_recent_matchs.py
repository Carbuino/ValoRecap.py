import io
import os
import discord
import json
import asyncio
import valo_api
import datetime
from discord.ext import commands
from matchResults.match_results import genMessage

async def checkRecentMatches(bot: commands.Bot):
    while True:
        print('---------- Cycle at {0} ----------'.format(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
        try:
            with open('alerts.json', 'r') as alerts_file:
                print('Exisiting alerts.json Loaded')
                alerts = json.load(alerts_file)
        except:
            writeComplete = False
            while writeComplete == False:
                try:
                    with open('alerts.json.lock', 'x') as lock_file:
                        with open('alerts.json', 'w') as alerts_file:
                            json.dump([], alerts_file, indent = 4)
                            print('New alerts.json Loaded')
                    os.remove('alerts.json.lock')
                    writeComplete = True
                
                except:
                    print('alerts.json is locked, trying again in 15 seconds')
                    await asyncio.sleep(15)

        # Loop through the alerts
        processedMatchIDs = []
        for entry in alerts:
            try:
                print(f"Checking match data for {entry['puuid']}", end=' ')
                user = valo_api.get_account_details_by_puuid(version='v1', puuid=entry['puuid'])
                print(f"({user.name}#{user.tag})", end=' ')

                matchID = valo_api.get_match_history_by_puuid_v3(version='v3', region=user.region, puuid=entry['puuid'], size=1)[0].metadata.matchid
                channel = bot.get_channel(entry['channel_id'])

                if processedMatchIDs.count(matchID) > 0:
                    print('- Same', end=' ')
                    entry['match_id'] = matchID

                if entry['match_id'] != matchID:
                    print('- New')
                    embed, file = genMessage(match_id=matchID, puuid=entry['puuid'])
                    entry['match_id'] = matchID
                    processedMatchIDs.append(matchID)
                                
                    if file:
                        with io.BytesIO() as image_binary:
                                file.save(image_binary, 'PNG')
                                image_binary.seek(0)
                                await channel.send(file=discord.File(fp=image_binary, filename='match.png'))
                    else:
                        await channel.send(embed=embed)

                else:
                    print('- Old')
                    processedMatchIDs.append(matchID)

            except Exception as e:
                print()
                print(f"ERROR: {e}")
                await asyncio.sleep(300)
                continue
            
        writeComplete = False
        while writeComplete == False:
            try:
                with open('alerts.json.lock', 'x') as lock_file:
                    with open('alerts.json', 'w') as alerts_file:
                        json.dump(alerts, alerts_file, indent = 4)
                        print('alerts.json updated successfully')
                os.remove('alerts.json.lock')
                writeComplete = True

            except:
                print('alerts.json is locked, trying again in 15 seconds')
                await asyncio.sleep(15)
            
        await asyncio.sleep(300)
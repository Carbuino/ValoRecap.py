from PIL import Image, ImageDraw, ImageFont
import json
import requests
import discord
import datetime
import valo_api
from valo_api.responses.match_history import MatchHistoryPointV3

GREEN = '#66C2A9'
DARK_GREEN = '#274940'
RED = '#F05C57'
DARK_RED = '#562020'
GREY = '#98A29F'
DARK_GREY = '#343837'
YELLOW = '#EAD991'

FALLING_SKY_BLACK = ImageFont.FreeTypeFont('./assets/fonts/FallingSky-JKwK.otf')
FALLING_SKY_BOLD = ImageFont.FreeTypeFont('./assets/fonts/FallingSkyBoldplus-6GZ1.otf')
AIRBORNE_II_PILOT = ImageFont.FreeTypeFont('./assets/fonts/airbrne2.ttf')

try:
    mapPhotos = dict()
    
    mapResponse = requests.get('https://valorant-api.com/v1/maps')
    if mapResponse.status_code != 200:
        raise Exception('maps - Status Code not 200')
    
    mapData = json.loads(mapResponse.content)['data']

    for gameMap in mapData:
        mapPhotos[gameMap['displayName'].upper()] = gameMap['listViewIconTall']
except Exception as e:
    print(e)

def generateStandardImage(matchData: MatchHistoryPointV3, puuid: str):

    def getFixedCoords(objWidth: int, position: int, spaceWidth: int, inverted=False):
        if not inverted: return position
        return spaceWidth - position - objWidth

    def generateMVPBox(playerData: dict, color: str, inverted: bool):
        box = Image.new('RGBA', (792, 323), '#00000074')
        draw = ImageDraw.Draw(box)
        if inverted: 
            anchor1 = 'lt'
            anchor2 = 'rt'
        else: 
            anchor1 = 'rt'
            anchor2 = 'lt'

        # MVP Box
        xB = getFixedCoords(219, 0, 792, inverted)
        draw.rectangle((xB, 56, xB+219, 138), YELLOW)

        # MVP Text
        xT  = getFixedCoords(0, 182, 792, inverted)
        draw.text(xy=(xT, 80),
                anchor=anchor1,
                text='MVP', 
                font=FALLING_SKY_BOLD.font_variant(size=50),
                fill='#000000',
                align='right')
        
        if playerData['name'] == '':
            return box
        
        #------------------------------------------------------------------------------------
        
        # Agent Icon
        agent = Image.open(requests.get(playerData['bust'], stream=True).raw)
        agent.thumbnail((1057, 957), Image.Resampling.BILINEAR)
        xAgent = getFixedCoords(1057, -25, 792, inverted)
        box.alpha_composite(agent, (xAgent, -125))
        
        #------------------------------------------------------------------------------------

        # KDA
        xK  = getFixedCoords(0, 752, 792, inverted)
        kdaStr = f'{playerData["kills"]}/{playerData["deaths"]}/{playerData["assists"]}'
        # Outline
        draw.text(xy=(xK - 2, 82 - 2), anchor=anchor1, text=kdaStr, font=AIRBORNE_II_PILOT.font_variant(size=50), fill='#000000', align='right')
        draw.text(xy=(xK + 2, 82 - 2), anchor=anchor1, text=kdaStr, font=AIRBORNE_II_PILOT.font_variant(size=50), fill='#000000', align='right')
        draw.text(xy=(xK - 2, 82 + 2), anchor=anchor1, text=kdaStr, font=AIRBORNE_II_PILOT.font_variant(size=50), fill='#000000', align='right')
        draw.text(xy=(xK + 2, 82 + 2), anchor=anchor1, text=kdaStr, font=AIRBORNE_II_PILOT.font_variant(size=50), fill='#000000', align='right')
        # Text
        draw.text(xy=(xK, 82), anchor=anchor1, text=kdaStr, font=AIRBORNE_II_PILOT.font_variant(size=50), fill=YELLOW, align='right')

        #------------------------------------------------------------------------------------
        
        # ACS
        xK  = getFixedCoords(0, 752, 792, inverted)
        acsStr = str(playerData['acs'])
        # Outline
        draw.text(xy=(xK - 2, 164 - 2), anchor=anchor1, text=acsStr, font=AIRBORNE_II_PILOT.font_variant(size=50), fill='#000000', align='right')
        draw.text(xy=(xK + 2, 164 - 2), anchor=anchor1, text=acsStr, font=AIRBORNE_II_PILOT.font_variant(size=50), fill='#000000', align='right')
        draw.text(xy=(xK - 2, 164 + 2), anchor=anchor1, text=acsStr, font=AIRBORNE_II_PILOT.font_variant(size=50), fill='#000000', align='right')
        draw.text(xy=(xK + 2, 164 + 2), anchor=anchor1, text=acsStr, font=AIRBORNE_II_PILOT.font_variant(size=50), fill='#000000', align='right')
        # Text
        draw.text(xy=(xK, 164), anchor=anchor1, text=acsStr, font=AIRBORNE_II_PILOT.font_variant(size=50), fill=YELLOW, align='right')

        #------------------------------------------------------------------------------------
        
        # Headshots
        xK  = getFixedCoords(0, 752, 792, inverted)
        hsStr = str(playerData['hs'])
        # Outline
        draw.text(xy=(xK - 2, 246 - 2), anchor=anchor1, text=hsStr, font=AIRBORNE_II_PILOT.font_variant(size=50), fill='#000000', align='right')
        draw.text(xy=(xK + 2, 246 - 2), anchor=anchor1, text=hsStr, font=AIRBORNE_II_PILOT.font_variant(size=50), fill='#000000', align='right')
        draw.text(xy=(xK - 2, 246 + 2), anchor=anchor1, text=hsStr, font=AIRBORNE_II_PILOT.font_variant(size=50), fill='#000000', align='right')
        draw.text(xy=(xK + 2, 246 + 2), anchor=anchor1, text=hsStr, font=AIRBORNE_II_PILOT.font_variant(size=50), fill='#000000', align='right')
        # Text
        draw.text(xy=(xK, 246), anchor=anchor1, text=hsStr, font=AIRBORNE_II_PILOT.font_variant(size=50), fill=YELLOW, align='right')

        #------------------------------------------------------------------------------------

        # Player Agent
        xA  = getFixedCoords(0, 34, 792, inverted)
        agentStr = playerData['agent']
        # Outline
        draw.text(xy=(xA - 2, 223 - 2), anchor=anchor2, text=agentStr, font=FALLING_SKY_BLACK.font_variant(size=20), fill='#000000', align='left')
        draw.text(xy=(xA + 2, 223 - 2), anchor=anchor2, text=agentStr, font=FALLING_SKY_BLACK.font_variant(size=20), fill='#000000', align='left')
        draw.text(xy=(xA - 2, 223 + 2), anchor=anchor2, text=agentStr, font=FALLING_SKY_BLACK.font_variant(size=20), fill='#000000', align='left')
        draw.text(xy=(xA + 2, 223 + 2), anchor=anchor2, text=agentStr, font=FALLING_SKY_BLACK.font_variant(size=20), fill='#000000', align='left')
        # Text
        draw.text(xy=(xA, 223), anchor=anchor2, text=agentStr, font=FALLING_SKY_BLACK.font_variant(size=20), fill='#FFFFFF', align='left')
        
        #------------------------------------------------------------------------------------

        # Player Name
        xN  = getFixedCoords(0, 29, 792, inverted)
        nameStr = playerData['name']
        # Outline
        draw.text(xy=(xN - 2, 250 - 2), anchor=anchor2, text=nameStr, font=FALLING_SKY_BLACK.font_variant(size=40), fill='#000000', align='left')
        draw.text(xy=(xN + 2, 250 - 2), anchor=anchor2, text=nameStr, font=FALLING_SKY_BLACK.font_variant(size=40), fill='#000000', align='left')
        draw.text(xy=(xN - 2, 250 + 2), anchor=anchor2, text=nameStr, font=FALLING_SKY_BLACK.font_variant(size=40), fill='#000000', align='left')
        draw.text(xy=(xN + 2, 250 + 2), anchor=anchor2, text=nameStr, font=FALLING_SKY_BLACK.font_variant(size=40), fill='#000000', align='left')
        # Text
        draw.text(xy=(xN, 250), anchor=anchor2, text=nameStr, font=FALLING_SKY_BLACK.font_variant(size=40), fill=color, align='left')

        return box

    def generateResultBox(roundsWon: int, color: str, inverted: bool):
        box = Image.new('RGBA', (792, 154), color)
        draw = ImageDraw.Draw(box)

        if inverted: 
            anchor1 = 'lt'
            anchor2 = 'rt'
        else: 
            anchor1 = 'rt'
            anchor2 = 'lt'

        if color == GREEN: 
            dark_color = DARK_GREEN
            result = 'WIN'
        elif color == RED: 
            dark_color = DARK_RED
            result = 'LOSS'
        else: 
            dark_color = DARK_GREY
            result = 'DRAW'

        # Rounds Won
        xN = getFixedCoords(0, 770, 792, inverted)
        draw.text(xy=(xN, 30),
            anchor=anchor1,
            text=str(roundsWon), 
            font=AIRBORNE_II_PILOT.font_variant(size=128),
            fill=dark_color,
            align='right')
        
        # Game Result
        xN = getFixedCoords(0, 73, 792, inverted)
        draw.text(xy=(xN, 30),
            anchor=anchor2,
            text=result, 
            font=AIRBORNE_II_PILOT.font_variant(size=128),
            fill=dark_color,
            align='left')
        
        return box

    def generateMapBox(gameMap: str):
        box = Image.new('RGBA', (296, 482), '#000000')
        draw = ImageDraw.Draw(box)

        # Map Photo
        im = Image.open(requests.get(mapPhotos[gameMap], stream=True).raw)
        im.thumbnail((9999, 482), Image.Resampling.BILINEAR)
        
        # Center horizontally
        x_offset = (296 - im.width) // 2
        box.alpha_composite(im, (x_offset, 0))

        # Map Name
        draw.text(xy=(149, 460),
                anchor='mm',
                text=gameMap, 
                font=FALLING_SKY_BOLD.font_variant(size=30),
                fill=YELLOW,
                align='center')

        return box

    def generateInfoBox(gameMode: str):
        box = Image.new('RGBA', (296, 482), '#000000')
        draw = ImageDraw.Draw(box)

        # Valorant Card
        im = Image.open('./assets/valo-card.png')

        w, h = im.size
        im = im.crop((8, 0, w, h))
        im = im.resize((296, 729))

        box.alpha_composite(im, (0, 0))

        # Gamemode
        if len(gameMode) > 15:
            fontSize = int(30 * 15 / len(gameMode))
        else:
            fontSize = 30
            
        draw.multiline_text(xy=(149, 460),
                anchor='mm',
                text=gameMode, 
                font=FALLING_SKY_BOLD.font_variant(size=fontSize),
                fill=YELLOW,
                align='center')

        return box

    def generatePlayerBox(playerData: dict, color: str, inverted: bool):
        box = Image.new('RGBA', (486, 113), '#000000CC')
        draw = ImageDraw.Draw(box)
        if inverted: 
            anchor1 = 'lt'
            anchor2 = 'rt'
        else: 
            anchor1 = 'rt'
            anchor2 = 'lt'

        if color == GREEN: dark_color = DARK_GREEN
        elif color == RED: dark_color = DARK_RED
        else: dark_color = DARK_GREY

        # Player Data Box
        xB = getFixedCoords(373, 113, 486, inverted)
        draw.rectangle((xB, 0, xB+372, 113), color)

        if playerData['name'] == '':
            return box

        # Agent Icon
        agent = Image.open(requests.get(playerData['icon'], stream=True).raw)
        agent.thumbnail((113, 113), Image.Resampling.BILINEAR)
        xAgent = getFixedCoords(113, 0, 486, inverted)
        box.alpha_composite(agent, (xAgent, 0))

        # Player KDA
        xD  = getFixedCoords(0, 470, 486, inverted)
        kdaStr = f'{playerData["kills"]}/{playerData["deaths"]}/{playerData["assists"]}'
        draw.text(xy=(xD, 13),
                anchor=anchor1,
                text=kdaStr, 
                font=AIRBORNE_II_PILOT.font_variant(size=48),
                fill='#000000',
                align='right')
        
        # Player ACS
        draw.text(xy=(xD, 61),
                anchor=anchor1,
                text=str(playerData['acs']), 
                font=AIRBORNE_II_PILOT.font_variant(size=48),
                fill='#000000',
                align='right')
        
        # Player Agent
        xP  = getFixedCoords(0, 124, 486, inverted)
        draw.text(xy=(xP, 63),
                anchor=anchor2,
                text=playerData['agent'], 
                font=FALLING_SKY_BLACK.font_variant(size=16),
                fill=dark_color,
                align='left')
        
        # Player Name
        draw.text(xy=(xP, 80),
                anchor=anchor2,
                text=playerData['name'], 
                font=FALLING_SKY_BLACK.font_variant(size=24),
                fill='#000000',
                align='left')

        return box

    def generateCenterBox():
        box = Image.new('RGBA', (214, 979))
        
        # Top Box
        topBox = Image.new('RGBA', (214, 154), '#000000CC')
        logo = Image.open('./assets/V_Logomark_White.png')
        logo.thumbnail((120, 120), Image.Resampling.BILINEAR)
        topBox.paste(logo, (47, 16), logo)

        # Main Box
        mainBox = Image.new('RGBA', (214, 815), '#000000CC')
        draw = ImageDraw.Draw(mainBox)

        draw.text(xy=(107, 102), anchor='mm', text='KDA', font=FALLING_SKY_BLACK.font_variant(size=20), fill=YELLOW, align='center') # MVP KDA
        draw.text(xy=(107, 185), anchor='mm', text='ACS', font=FALLING_SKY_BLACK.font_variant(size=20), fill=YELLOW, align='center') # MVP ACS
        draw.text(xy=(107, 266), anchor='mm', text='HEADSHOTS', font=FALLING_SKY_BLACK.font_variant(size=20), fill=YELLOW, align='center') # MVP Headshots
        
        draw.text(xy=(107, 366), anchor='mm', text='KDA', font=FALLING_SKY_BLACK.font_variant(size=20), fill=YELLOW, align='center') # P2 KDA
        draw.text(xy=(107, 414), anchor='mm', text='ACS', font=FALLING_SKY_BLACK.font_variant(size=20), fill=YELLOW, align='center') # P2 ACS

        draw.text(xy=(107, 490), anchor='mm', text='KDA', font=FALLING_SKY_BLACK.font_variant(size=20), fill=YELLOW, align='center') # P3 KDA
        draw.text(xy=(107, 538), anchor='mm', text='ACS', font=FALLING_SKY_BLACK.font_variant(size=20), fill=YELLOW, align='center') # P3 ACS

        draw.text(xy=(107, 614), anchor='mm', text='KDA', font=FALLING_SKY_BLACK.font_variant(size=20), fill=YELLOW, align='center') # P3 KDA
        draw.text(xy=(107, 662), anchor='mm', text='ACS', font=FALLING_SKY_BLACK.font_variant(size=20), fill=YELLOW, align='center') # P3 ACS

        draw.text(xy=(107, 738), anchor='mm', text='KDA', font=FALLING_SKY_BLACK.font_variant(size=20), fill=YELLOW, align='center') # P3 KDA
        draw.text(xy=(107, 786), anchor='mm', text='ACS', font=FALLING_SKY_BLACK.font_variant(size=20), fill=YELLOW, align='center') # P3 ACS

        box.alpha_composite(topBox, (0, 0))
        box.alpha_composite(mainBox, (0, 164))
        return box

    def generateTeamBox(matchInfo: dict, team='red' or 'blue', inverted=False):
        box = Image.new('RGBA', (792, 979), '#00000000')

        if not inverted: sideBox = generateMapBox(matchInfo['map'])
        else: sideBox = generateInfoBox(matchInfo['gamemode'])

        if team == 'red':
            otherTeam = 'blue'
        else:
            otherTeam = 'red'

        if matchInfo['winningTeam'] == team:
            color = GREEN
        elif matchInfo['winningTeam'] == otherTeam:
            color = RED
        else:
            color = GREY

        teamPlayerData = matchInfo['playerData'][team]

        results = generateResultBox(roundsWon=matchInfo['roundsWon'][team], color=color, inverted=inverted)
        box.alpha_composite(results)

        xPlayer = getFixedCoords(486, 306, 792, inverted)
        yPlayer = 497
        for i in range(len(teamPlayerData)):
            if i == 0:
                mvp = generateMVPBox(playerData=teamPlayerData[0], color=color, inverted=inverted)
                box.alpha_composite(mvp, (0, 164))

            else:
                player = generatePlayerBox(playerData=teamPlayerData[i], color=color, inverted=inverted)
                box.alpha_composite(player, (xPlayer, yPlayer))
                yPlayer += 123

        xSide = getFixedCoords(296, 0, 792, inverted)
        box.alpha_composite(sideBox, (xSide, 497))
        return box

    def parseStandardMatchData(matchData: MatchHistoryPointV3, puuid: str):
        playerTeam = 'nil'
        otherTeam = 'nil'
        roundsPlayed = matchData.metadata.rounds_played
        roundsResult = {'red': 0, 'blue': 0}
        teamPlayerData = {'red': list(), 'blue': list()}
        gamemode = matchData.metadata.mode.upper()
        gameMap = matchData.metadata.map.upper()

        for i in range(len(matchData.players.red)):
            player = matchData.players.red[i]
            stat = player.stats
            teamPlayerData['red'].append({'name': player.name.upper(),
                                    'acs': (stat.score // roundsPlayed), 
                                    'kills': stat.kills, 
                                    'deaths': stat.deaths, 
                                    'assists': stat.assists, 
                                    'hs': stat.headshots, 
                                    'agent': player.character.upper(),
                                    'icon': player.assets.agent.small, 
                                    'bust': player.assets.agent.bust})
            
            if (player.puuid == puuid) & (playerTeam == 'nil'):
                playerTeam = 'red'
                otherTeam = 'blue'

        if (playerTeam == 'nil'):
                playerTeam = 'blue'
                otherTeam = 'red'

        for i in range(len(matchData.players.blue)):
            player = matchData.players.blue[i]
            stat = player.stats
            teamPlayerData['blue'].append({'name': player.name.upper(),
                                    'acs': (stat.score // roundsPlayed), 
                                    'kills': stat.kills, 
                                    'deaths': stat.deaths, 
                                    'assists': stat.assists, 
                                    'hs': stat.headshots, 
                                    'agent': player.character.upper(),
                                    'icon': player.assets.agent.small, 
                                    'bust': player.assets.agent.bust})

        teamPlayerData['red'] = sorted(teamPlayerData['red'], key=lambda x: (x['acs'], x['kills'], x['deaths']), reverse=True) 
        teamPlayerData['blue'] = sorted(teamPlayerData['blue'], key=lambda x: (x['acs'], x['kills'], x['deaths']), reverse=True)

        roundsResult[playerTeam] = getattr(matchData.teams, playerTeam).rounds_won
        roundsResult[otherTeam] = getattr(matchData.teams, otherTeam).rounds_won

        if getattr(matchData.teams, playerTeam).has_won == True:
            winningTeam = playerTeam
        elif getattr(matchData.teams, otherTeam).has_won == True:
            winningTeam = otherTeam
        else:
            winningTeam = 'draw'

        return {'playerTeam': playerTeam, 'playerData': teamPlayerData, 'roundsWon': {playerTeam: roundsResult[playerTeam], otherTeam: roundsResult[otherTeam]}, 'winningTeam': winningTeam, 'gamemode': gamemode, 'map': gameMap}

    matchInfo = parseStandardMatchData(matchData, puuid)
    canvas = Image.open('./assets/match_results_bg.jpg')
    canvas = canvas.resize((1920, 1080), Image.Resampling.BILINEAR)

    if matchInfo['playerTeam'] == 'red':
        otherTeam = 'blue'
    else:
        otherTeam = 'red'

    team1Box = generateTeamBox(matchInfo=matchInfo, team=matchInfo['playerTeam'])
    team2Box = generateTeamBox(matchInfo=matchInfo, team=otherTeam, inverted=True)
    centerBox = generateCenterBox()
    canvas.paste(team1Box, (51, 51), team1Box)
    canvas.paste(team2Box, (1077, 51), team2Box)
    canvas.paste(centerBox, (853, 51), centerBox)
    return canvas

def generateDeathmatchEmbed(matchData: MatchHistoryPointV3, puuid: str):
    def parseDeathMatchData(matchData: MatchHistoryPointV3, puuid: str):
        # Get ordinal numbers (3 -> 3rd)
        # https://codegolf.stackexchange.com/questions/4707/outputting-ordinal-numbers-1st-2nd-3rd#answer-4712
        # By Gareth on Stack Exchange
        ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])
    
        playerKills = int()
        killList = list()
        placement = str()
        playerStats = dict()

        for player in matchData.players.all_players:
            killList.append(player.stats.kills)
            if player.puuid == puuid:
                playerStats['name'] = player.name
                playerStats['tag'] = player.tag
                playerStats['kills'] = player.stats.kills
                playerStats['deaths'] = player.stats.deaths
                playerStats['assists'] = player.stats.assists
                playerStats['kdr'] = round(player.stats.kills / player.stats.deaths, 2)
                playerStats['agent'] = {'name': player.character, 'icon': player.assets.agent.small}
                playerKills = player.stats.kills

        killList.sort(reverse=True)
        placement = ordinal(killList.index(playerKills) + 1)

        if playerKills == killList[0]: 
            color = GREEN
            killStr = f'{killList[0]} - {killList[1]}'
        else: 
            color = RED
            killStr = f'{playerKills} - {killList[0]}'
        
        if killList.count(playerKills) > 1: gameResult = placement + ' Place (Tied)'
        else: gameResult = placement + ' Place'

        return {'player': playerStats, 'color': color, 'placeStr': gameResult, 'killStr': killStr, 'map': matchData.metadata.map, 'mode': matchData.metadata.mode}
    
    matchInfo = parseDeathMatchData(matchData, puuid)

    embed=discord.Embed(title=f"{matchInfo['player']['name']}#{matchInfo['player']['tag']} finished a Valorant Game!", 
                        description=f"**Gamemode**: {matchInfo['mode']}\n**Result**: {matchInfo['placeStr']} // {matchInfo['killStr']}", 
                        color=int(matchInfo['color'].replace('#', '0x'), 16), 
                        timestamp=datetime.datetime.fromtimestamp(matchData.metadata.game_start), 
                        url=f"https://tracker.gg/valorant/match/{matchData.metadata.matchid}")

    embed.set_thumbnail(url=matchInfo['player']['agent']['icon'])
    embed.add_field(name="Kills", value=matchInfo['player']['kills'], inline=True)
    embed.add_field(name="Deaths", value=matchInfo['player']['deaths'], inline=True)
    embed.add_field(name="Assists", value=matchInfo['player']['assists'], inline=True)
    embed.add_field(name="KDR", value=matchInfo['player']['kdr'], inline=True)
    embed.add_field(name="Agent", value=matchInfo['player']['agent']['name'], inline=True)
    embed.add_field(name="Map", value=matchInfo['map'], inline=True)

    return embed

def genMessage(match_id: str, puuid: str):
    matchData = valo_api.get_match_details_v2(version='v2', match_id=match_id)
    gamemode = matchData.metadata.mode.upper()

    if (gamemode == 'DEATHMATCH'): 
        return generateDeathmatchEmbed(matchData, puuid), None
    elif (gamemode == 'CUSTOM GAME'): 
        if (matchData.metadata.queue.upper() == 'DEATHMATCH'):
            matchData.metadata.mode = 'Deathmatch (Custom)'
            return generateDeathmatchEmbed(matchData, puuid), None
        else:
            return None, generateStandardImage(matchData, puuid)
    else: 
        return None, generateStandardImage(matchData, puuid)

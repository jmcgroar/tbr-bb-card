"""
Definition of views.
"""

import os
import json
import re
from django.conf import settings
from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
import pandas as pd

import app.models as models

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    headshot = None
    teamLogo = None
    playerInfo = None
    playerStatsHtml = None

    headshotFormatString = getattr(settings, "PLAYER_HEADSHOT_FORMAT_STRING", None)
    teamLogoFormatString = getattr(settings, "TEAM_LOGO_FORMAT_STRING", None)

    # Retrieve the players from the config file.
    playerOptions = getattr(settings, "SAMPLE_MLB_PLAYERS", None)

    # Determine which (if any player) has been selected.
    try:
        playerKey = request.POST['player_select']
        playerOptionIndex = next((index for (index, playerOption) in enumerate(playerOptions) if playerOption["PLAYER_KEY"] == playerKey), None)
    except:
        playerKey = '0_'
        playerOptionIndex = 0

    playerKeyComponents = re.match ("^(\d+)_(H|P*)$", playerKey)

    try:
        bamId = playerKeyComponents.group(1)
    except:
        bamId = '0'

    try:
        playerType = '' if playerKeyComponents.group(2) is None else playerKeyComponents.group(2)
    except:
        playerType = ''

    # For debugging purposes
    pd.set_option('display.max_columns', None)

    # Check for a valid BAM ID
    if (bamId != '0'):
        # In a real-world situation, this section should be loaded once at startup.  This is where we retrieve the MLB leagues and teams
        leagueInfo = models.getMlbLeagues()
        dfLeagues = pd.io.json.json_normalize(leagueInfo)
        teamsInfo = models.getMlbTeams()
        dfTeams = pd.io.json.json_normalize(teamsInfo)
        # End of startup code

        # Capture the headshot and team logo images
        headshot = headshotFormatString.format(bamId)
        teamLogo = teamLogoFormatString.format(playerOptions[playerOptionIndex]['TEAM_LOGO'])

        # Issue to the REST API call to MLB Stats to retrieve the player's biographical and statistical information.
        playerInfo = models.getPlayerInformation(bamId, playerType)

        # Separate the Year x Year and Career stats.  We'll handle them a bit differently
        playerYxYStatsInfo = playerInfo['stats'][0]['splits']
        playerCareerStatsInfo = playerInfo['stats'][1]['splits']

        # Generate Pandas DataFrames for the Year x Year and Career stats.
        # Using DataFrames will give us a nice way of manipulating the data.   
        dfPlayerYxYStats = pd.io.json.json_normalize(playerYxYStatsInfo)
        dfPlayerCareerStats = pd.io.json.json_normalize(playerCareerStatsInfo)
        dfPlayerCareerStats['season'] = 'Career'
        dfPlayerCareerStats['team_abbreviation'] = '--'
        dfPlayerCareerStats['league_abbreviation'] = '--'

        # Merge team information in the Year x Year DataFrame.
        dfPlayerYxYStats = pd.merge(dfPlayerYxYStats, dfTeams[['id','abbreviation']], left_on='team.id', right_on='id', left_index=False, right_index=False, how='left', 
                                                    copy=True, indicator=False, validate=None)
        dfPlayerYxYStats.rename(columns={'abbreviation' : 'team_abbreviation'}, inplace=True)

        # Merge league information in the Year x Year DataFrame.
        dfPlayerYxYStats = pd.merge(dfPlayerYxYStats, dfLeagues[['id','abbreviation']], left_on='league.id', right_on='id', left_index=False, right_index=False, how='left', 
                                                    copy=True, indicator=False, validate=None)
        dfPlayerYxYStats.rename(columns={'abbreviation' : 'league_abbreviation'}, inplace=True)

        # Merge the Year x Year and Career DataFrames into a single DataFrame.
        dfPlayerStats = dfPlayerYxYStats.append(dfPlayerCareerStats)

        # 1. Rename DataFrame columns to abbreviations which will be used in the UI. 
        # 2. Export the DataFrame to a HTML Table with an element ID.  We'll use that ID in order to apply styling to the table using CSS classes.
        if (playerInfo['stats'][0]['group']['displayName'] == 'hitting'):
            dfPlayerStats.rename(columns={'season' : 'Season', 'team_abbreviation' : 'Team', 'league_abbreviation' : 'LG', 'stat.gamesPlayed' : 'G', 'stat.atBats' : 'AB', 'stat.runs' : 'R', 'stat.hits' : 'H', 'stat.totalBases' : 'TB', 'stat.doubles' : '2B', 'stat.triples' : '3B', 'stat.homeRuns' : 'HR', 'stat.rbi' : 'RBI', 'stat.baseOnBalls' : 'BB', 'stat.intentionalWalks' : 'IBB', 'stat.strikeOuts' : 'SO', 'stat.stolenBases' : 'SB', 'stat.caughtStealing' : 'CS', 'stat.avg' : 'AVG', 'stat.obp' : 'OBP', 'stat.slg' : 'SLG', 'stat.ops' : 'OPS', 'stat.groundOutsToAirouts' : 'GO/AO'}, inplace=True)
            playerStatsHtml = dfPlayerStats.to_html (border=0, header=True, index=False, index_names=False, justify='center', columns=['Season', 'Team', 'LG', 'G', 'AB', 'R', 'H', 'TB', '2B', '3B', 'HR', 'RBI', 'BB', 'IBB', 'SO', 'SB', 'CS', 'AVG', 'OBP', 'SLG', 'OPS', 'GO/AO'], table_id='player_stats_table')
        elif (playerInfo['stats'][0]['group']['displayName'] == 'pitching'):
            dfPlayerStats.rename(columns={'season' : 'Season', 'team_abbreviation' : 'Team', 'league_abbreviation' : 'LG', 'stat.wins' : 'W', 'stat.losses' : 'L', 'stat.era' : 'ERA', 'stat.gamesPitched' : 'G', 'stat.gamesStarted' : 'GS', 'stat.completeGames' : 'GC', 'stat.shutouts' : 'SHO', 'stat.holds' : 'HLD', 'stat.saves' : 'SV', 'stat.saveOpportunities' : 'SVO', 'stat.inningsPitched' : 'IP', 'stat.hits' : 'H', 'stat.runs' : 'R', 'stat.earnedRuns' : 'ER', 'stat.homeRuns' : 'HR', 'stat.numberOfPitches' : 'NP', 'stat.hitBatsmen' : 'HB', 'stat.baseOnBalls' : 'BB', 'stat.intentionalWalks' : 'IBB', 'stat.strikeOuts' : 'SO', 'stat.avg' : 'AVG', 'stat.whip' : 'WHIP', 'stat.groundOutsToAirouts' : 'GO/AO'}, inplace=True)
            playerStatsHtml = dfPlayerStats.to_html (border=0, header=True, index=False, index_names=False, justify='center', columns=['Season', 'Team', 'LG', 'W', 'L', 'ERA', 'G', 'GS', 'GC', 'SHO', 'HLD', 'SV', 'SVO', 'IP', 'H', 'R', 'ER', 'HR', 'NP', 'HB', 'BB', 'IBB', 'SO', 'AVG', 'WHIP', 'GO/AO'], table_id='player_stats_table')

    # Set/clear the SELECTED state for each player in the list.
    for playerOption in playerOptions:
        playerOption['STATE'] = 'selected' if playerOption['PLAYER_KEY'] == playerKey else ''

    return render(
        request,
        'app/index.html',
            {
            'bam_id' : bamId,
            'title' : 'Home Page',
            'year' : datetime.now().year,
            'player_options' : playerOptions,
            'headshot' : headshot,
            'team_logo' : teamLogo,
            'player_bio_info' : playerInfo,
            'player_stats_info' : playerStatsHtml,
            }
        )
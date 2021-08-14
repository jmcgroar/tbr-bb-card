from django.conf import settings
import requests
from django.db import models

# Gets all MLB Leagues
def getMlbLeagues ():
	response = requests.get(getattr(settings, "MLB_STATS_BASE_URL", None) + getattr(settings, "MLB_LEAGUES_STRING", ''))
	if (response.status_code == 200):
		leagueInfo = response.json()
		leagueInfo = leagueInfo['leagues']
	else:
		leagueInfo = None

	return (leagueInfo)

# Gets all MLB Leagues
def getMlbTeams ():
	response = requests.get(getattr(settings, "MLB_STATS_BASE_URL", None) + getattr(settings, "MLB_TEAMS_STRING", ''))
	if (response.status_code == 200):
		teamsInfo = response.json()
		teamsInfo = teamsInfo['teams']
	else:
		teamsInfo = None

	return (teamsInfo)

# Gets the selected player's biographical and statistical information.  Which type ofstatistical data is retrieved is determined by the playerType (H or P) argument.
# This could be enhanced to use the player's current primary position to determine which statistical data is retrieved.
def getPlayerInformation (bamId, playerType):
	requestUrl = (getattr(settings, "MLB_STATS_BASE_URL", None) + getattr(settings, "PLAYER_INFO_FORMAT_STRING", None)).format(bamId, 'hitting' if playerType == 'H' else 'pitching')

	response = requests.get(requestUrl)
	if (response.status_code == 200):
		playerInfo = response.json()
		playerInfo = playerInfo['people']
		playerInfo = playerInfo[0]
	else:
		playerInfo = None

	return (playerInfo)


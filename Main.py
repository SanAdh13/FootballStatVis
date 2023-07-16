from time import sleep
import requests
from bs4 import BeautifulSoup
from scouting import * 
from visualisation import *
import json
baseURL = "https://fbref.com"
allPlayerURLs = []
players = {}

def scoutingReport(url):
    # https://fbref.com/en/players/d70ce98e/Lionel-Messi
    # becomes https://fbref.com/en/players/d70ce98e/scout/365_m1/d70ce98e-Scouting-Report

    # Extract the player ID from the player URL
    playerID = url.split('/')[-2]

    # Construct the scouting report URL
    scoutingReportURL = f"https://fbref.com/en/players/{playerID}/scout/365_m1/{playerID}-Scouting-Report"

    response = requests.get(scoutingReportURL)
    response.raise_for_status()

    soup = BeautifulSoup(response.content,'html.parser')
    
    

    print("###############################")
    choice = int(input("Would you like  summary scouting (0) or full scouting report (1)? "))
    print("###############################")

    if choice == 0:
        summary = soup.find('div',id='all_scout_summary')
        if summary == None :
            return(f"No Summary scouting Report Available for {url.split('/')[-1]}")
        else:
            values = getTitles(summary)
    else:
        full = soup.find('div',id='all_scout_full')
        if full == None:
            return(f"No Full scouting Report Available for {url.split('/')[-1]}")
        else:
            values = getTitles(full)

    return values
    # return [summaryTable,fullTable]





def searchFBRefPlayerByName(playerName):
    searchURL = f"{baseURL}/en/search/search.fcgi?&search={playerName.replace(' ', '-')}"

    response = requests.get(searchURL)
    response.raise_for_status()

    soup = BeautifulSoup(response.content,'html.parser')

    #Full names redirect to the player page whereas a partial name search returns list of players with that name    
    if response.url.startswith(f"{baseURL}/en/players"):
        print(f'Player url found: {response.url} ... fetching data')
        return response.url
    else:   
        results = soup.find_all('div',class_='search-item-name')
        players = {}
        for i,result in enumerate(results):
            findPlayer = result.find('a')['href']
            playerURL = f"{baseURL}{findPlayer}"
            PlayerName = result.find('a').text.strip()
            players[i] = {'name':PlayerName,'url':playerURL}
        return players


def getPlayersFromUser():
    playerName = input('Search for player: ')
    searchForPlayer = searchFBRefPlayerByName(playerName)
    if type(searchForPlayer) == dict:
        for key,val in searchForPlayer.items():
            print(f"{key}: {val['name']}")
       
        choice = int(input('Enter Number for player you want '))
        while choice < 0 or choice >= len(searchForPlayer.items()):
            print('invalid choice')
            choice = int(input('Enter Number for player you want '))
        
        chosenPlayer = searchForPlayer[int(choice)]
        allPlayerURLs.append(chosenPlayer['url'])
    else:  
        allPlayerURLs.append(searchForPlayer)

    addMorePlayers = input("Add more players to search? Y/N ").upper()

    if addMorePlayers == "Y":
        getPlayersFromUser()
    

def getData():
    for url in allPlayerURLs:
        players[url.split('/')[-1]] = scoutingReport(url)

if __name__ == '__main__':
    # Firstly get the players we have to search for from the user
    getPlayersFromUser()

    # for each player we will fetch the data, either summary or full (userinput)
    getData()
    
    # we will use the returned players dict to create the visualisation 

    # TODO: when using full data instead of summary, create multiple charts for each subcategory
    createChart(players)




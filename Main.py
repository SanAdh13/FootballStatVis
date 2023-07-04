from time import sleep
import requests
from bs4 import BeautifulSoup
baseURL = "https://fbref.com"

def ScoutingReport(url):
    # https://fbref.com/en/players/d70ce98e/Lionel-Messi
    # becomes https://fbref.com/en/players/d70ce98e/scout/365_m1/Lionel-Messi-Scouting-Report

    # Extract the player ID from the player URL
    player_id = url.split('/')[-2]

    # Construct the scouting report URL
    scouting_report_url = f"https://fbref.com/en/players/{player_id}/scout/365_m1/{player_id}-Scouting-Report"

    return scouting_report_url


def searchForPlayerByName(playerName):
    searchURL = f"{baseURL}/en/search/search.fcgi?&search={playerName.replace(' ', '-')}"

    response = requests.get(searchURL)
    response.raise_for_status()

    soup = BeautifulSoup(response.content,'html.parser')


    # depending on the searched name fbref either gives a result of various players or redirect to one player if fullname given
    # eg. searching 'ronaldo' will give a search result of players
    # searching Cristiano Ronaldo will redirect to his player page

    
    if response.url.startswith(f"{baseURL}/en/players"):
        print(f'Player url found: {response.url} ...fetching data')
        # sleep(5)
        return ScoutingReport(response.url)
    else:   
        results = soup.find_all('div',class_='search-item-name')

        players = {}
        for i,result in enumerate(results):
            findPlayer = result.find('a')['href']
            playerURL = f"{baseURL}{findPlayer}"
            PlayerName = result.find('a').text.strip()
            
            players[i] = {'name':PlayerName,'url':playerURL}
        return players
       

if __name__ == '__main__':

    playerName = input('Search for player: ')

    searchForPlayer = searchForPlayerByName(playerName)

    if type(searchForPlayer) == dict:
        for key,val in searchForPlayer.items():
            print(f"{key}: {val['name']}")

        try:
            choice = input('Enter Number for player you want ')
        except ValueError:
            print('invalid')
                
        chosenPlayer = searchForPlayer[int(choice)]
        
        print(ScoutingReport(chosenPlayer['url']))
    
    




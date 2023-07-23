# calculates the average percentile for each category in the complete scouting report 
# def averageStatForFullScouting(STAT):
#     for stat in STAT:
#         total = 0
#         for eachval in stat:
#             total+=int(eachval[-1])
#     return total//len(stat) 

# def breakDownStatsFull(tableData): 
#     StandardStats = [table[:15] for table in tableData]
#     ShootingStats = [table[15:30] for table in tableData]
#     PassingStats = [table[30:52] for table in tableData]
#     PassTypes = [table[52:67] for table in tableData]
#     GoalShotCreation=[table[67:81] for table in tableData]
#     Defense=[table[81:97] for table in tableData]
#     Posession = [table[97:119] for table in tableData]
#     MiscStats = [table[119:]for table in tableData]

#     return StandardStats,ShootingStats,PassingStats,PassTypes,GoalShotCreation,Defense,Posession,MiscStats

# def breakdownStatsSummary(tableData):

#     return 0



from bs4 import BeautifulSoup


def getScoutingTables(table):
    row_data = {}
    tbody = table.find('tbody')

    tbodyRows = tbody.find_all('tr')
    # TODO: Can probably use enum here for the full scouting and just create averages using ideas from breakdownstatsfull() and averageStatForFullScouting() here instead of having the full 100+ stat
    for row in tbodyRows:
        # this will hold the dict for each thing  eg. {'xG:[<td>,<td>]}
        

        #<th> holds the label while <td> holds the value and percentile
        title = row.find('th')
        titleValue = title.get_text(strip=True)
        # row_data[titleValue] 
        
        cellData = []
        cells = row.find_all('td')
        if all(cell.get_text(strip=True) == '' for cell in cells):
            continue  # Skip the empty row
        
        for cell in cells:
            text = cell.get_text(strip=True)
            if text.endswith('%'):
                cellData.append(text[:-1])
            else:
                cellData.append(text) 
        row_data[titleValue]=cellData
        
    return row_data

def getTitles(div:BeautifulSoup):
    titles = div.find('div',class_='filter switcher')
    atags = titles.findAll('a')

    values = {}
    tables = div.find_all('table')
    for index,a in enumerate(atags):
        value= a.get_text(strip=True)
        
        values[value] = getScoutingTables(tables[index])
    
    return values
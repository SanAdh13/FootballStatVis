# calculates the average percentile for each category in the complete scouting report 
def averageStatForFullScouting(STAT):
    for stat in STAT:
        total = 0
        for eachval in stat:
            total+=int(eachval[-1])
    return total//len(stat) 

def breakDownStatsFull(tableData): 
    StandardStats = [table[:15] for table in tableData]
    ShootingStats = [table[15:30] for table in tableData]
    PassingStats = [table[30:52] for table in tableData]
    PassTypes = [table[52:67] for table in tableData]
    GoalShotCreation=[table[67:81] for table in tableData]
    Defense=[table[81:97] for table in tableData]
    Posession = [table[97:119] for table in tableData]
    MiscStats = [table[119:]for table in tableData]

    return StandardStats,ShootingStats,PassingStats,PassTypes,GoalShotCreation,Defense,Posession,MiscStats

def breakdownStatsSummary(tableData):

    return 0


def getScoutingTables(div):
    tables = div.find_all('table')
    tableData = []
    for table in tables:
        tbody = table.find('tbody')

        # Extract the data from tbody and store it in a list
        tbody_data = []
        rows = tbody.find_all('tr')
        for row in rows:
            row_data = []
            title = row.find('th')
            titleValue = title.get_text(strip=True)
            row_data.append(titleValue)


            # Extract the text from each cell in the row and append it to the tbody_data list
            cells = row.find_all('td')

            if all(cell.get_text(strip=True) == '' for cell in cells):
                continue  # Skip the empty row

            
            for cell in cells:
                text = cell.get_text(strip=True)
                if text.endswith('%'):
                    row_data.append(text[:-1])
                else:
                    row_data.append(text) 
            tbody_data.append(row_data)
        
        # Append the tbody_data list to the table_body_data list
        tableData.append(tbody_data)   

    return tableData

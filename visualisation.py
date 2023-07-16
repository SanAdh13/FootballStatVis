import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
 
positions = []
statsNames = []
results = []
playername = []
def getLabelsAndVals(finalDict):
   #first dict key is the player name and the values are the all the information
    for name,stats in finalDict.items():
        playername.append(name)
        for versusPositions,positionStats in stats.items():
            positions.append(versusPositions)
            positionsVal = []
            # print(versusPositions)
            for statname,statisticsArray in positionStats.items():
                if statname not in statsNames:
                    statsNames.append(statname)
                positionsVal.append(int(statisticsArray[-1])) 
            results.append(positionsVal)

def createChart(values):
    getLabelsAndVals(values)

    fig = make_subplots(rows=1,cols=len(results),specs=[[{'type': 'polar'}]*len(results)])
    for k,v in enumerate(results):
        fig.add_trace(
            go.Scatterpolar(r=v,theta=statsNames, fill='toself',name=positions[k]),1,k+1)
    fig.update_layout(
    # title = f"{scoutURL.split('/')[-1]} percentile",
    font_size = 15,
    )
    if not os.path.exists("results"):
        os.mkdir("results")
    fig.write_image("results/fig.png")


import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from datetime import date
 
def getLabelsAndVals(data:dict):
    grouped_data = {}
    for player, positions in data.items():
        for position, stats in positions.items():
            if position not in grouped_data:
                grouped_data[position] = {}
            grouped_data[position][player] = stats
    return grouped_data

def createPolarCharts(player_stats, position):
    categories = list(player_stats.keys())
    values = [int(stat[1]) for stat in player_stats.values()]
    fig = go.Scatterpolar(
        r=[*values,values[0]],
        theta=categories,
        fill='toself',
        name=position
    )

    return fig

def charts(values:dict):
    
    grouped_data = getLabelsAndVals(values)
    today = date.today()
    if not os.path.exists("./results"):
        os.mkdir("./results")

    for positions,players in grouped_data.items():
        print(f"{' '.join(list(grouped_data.keys()))}  {' '.join(list(players.keys()))}")
        fig = make_subplots(rows = 1,
                            cols = 1,
                            x_title=f"{positions} || {' & '.join(list(players.keys()))}"
                            , specs=[[{'type':'polar'}]])
        for player,stats in players.items():
            fig.add_trace(createPolarCharts(stats, player), row=1, col=1)
        fig.update_layout(showlegend=True)
        fig.write_image(f"./results/{today}_{'_&_'.join(list(players.keys()))}.png")





import plotly.graph_objects as go
import os
 

def getLabelsAndVals(tableData):
    labels = []
    result = []
    for table in tableData:
        value = []
        for item in table:
            if item[0] not in labels:
                labels.append(item[0]) 
            value.append(int(item[-1]))
        result.append(value)

    return labels,result
def createChart(tableData):
    labels,result = getLabelsAndVals(tableData)

    fig = go.Figure(
        data=go.Scatterpolar(r=result[0],theta=labels, fill='toself'),
    )

    if not os.path.exists("results"):
        os.mkdir("results")
    fig.write_image("results/fig.png")


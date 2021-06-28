'''
Stacked Bar chart may be a bit difficult to see
Nested Bar chart is better!

'''

import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

# g = df.sort_values("Total Return", axis = 0)
# x = g['Symbol']
# y1 = g['Total Return']
# y2 = g['Percentage']
# y3 = g['Decay/Increase']

# trace1 = go.Bar(x=x,y=y1, marker=dict(color="#FFD700"))
# trace2 = go.Bar(x=x, y=y2, marker = dict(color="#CD7F32"))
# trace3 = go.Bar(x=x,y=y3,marker=dict(color="#9EA0A1"))

# data = [trace1]

# layout = go.Layout(title='Returns', barmode="stack",
#                   xaxis = dict(tickangle = 90,
#                               showticklabels = True,
#                               type = "category",
#                               dtick = 1))

# fig = go.Figure(data=data,layout=layout)
# fig.show()


def bar(x, y, color ="#FFD700", title = "Bar Plot"):
    trace1 = go.Bar(x=x,y=y, marker=dict(color=color))
    data = [trace1]
    layout = go.Layout(title=title, barmode="stack",
                  xaxis = dict(tickangle = 90,
                              showticklabels = True,
                              type = "category",
                              dtick = 1))
    fig = go.Figure(data = data, layout = layout)
    fig.show()


print("Great! Enabled axis to bar function")
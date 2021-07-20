'''
Predictive Problem:

I want to figure out the feature
'''
from etl import IndeedETL
import pandas as pd


class RFAnalysis:
    def __init__(self):
        pass

df = pd.read_csv(IndeedETL().paths['merged'])

print(df)


# title = all_data['Job Title']
# x = title.value_counts().index
# y = title.value_counts().values
# bar(x,y, title = "Job Title Distribution")





#%%
## All my imports
# Data science
import pandas as pd
import numpy as np
# Visualization 
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style="ticks", color_codes=True)
import os
# Text Stuff
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from nltk.corpus import stopwords
import sys
sys.path.insert(1, '../')
import research
import re
plt.style.use("ggplot")

# Creating an object where my NLP EDA functions are located
nlp = research.nlp_eda()

# %%
paths = {'all_data': '../data/merged_df.csv', 
"headings": "../data/merged_headings_df.csv"}

# ingest
all_data = pd.read_csv(paths['all_data'], index_col = 0)
headings_df = pd.read_csv(paths['headings'], index_col = 0)

# applying transformation
all_data['Description'] = all_data['Description'].apply(clean)

# subsets
ds = all_data[all_data['Job Title'] == "data scientist"]
da = all_data[all_data['Job Title'] == "data analyst"]

# getting word counts
ds_words = nlp.to_wcdf(ds['Description']).sum()
da_words = nlp.to_wcdf(da['Description']).sum()
# %%
ds['Description'].iloc[0]
# %%
ds
# %%

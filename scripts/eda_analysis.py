

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
# ML
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
plt.style.use("ggplot")

# Creating an object where my NLP EDA functions are located
nlp = research.nlp_eda()

colors = {"coral": "#FC766AFF", "pacific coast":"#5B84B1FF" , "black": "#101820FF", "orange": "#F2AA4CFF"}

colors2 = {"pacific coast":"#5B84B1", "coral":"#FC766A" , "red": "#DC5757", "blue": "#4547CA",
          "teal": "#8AF3CC"}
# %%
paths = {'all_data': '../data/merged_df.csv', "headings": "../data/merged_headings_df.csv"}

# ingest
all_data = pd.read_csv(paths['all_data'], index_col = 0)
headings_df = pd.read_csv(paths['headings'], index_col = 0)

def clean(seq):
    ''' This is the preprocessing pipeline that I do with the Random Forest in mind '''
    # converting to lowercase
    seq = seq.lower()
    
    # removing \n
    to_remove = {'\n','analyst','scientist', 'science', 'machine', 'learning','scientists', "experience"}

    resultwords  = [word for word in re.split("\W+",seq) if word.lower() not in to_remove]
    resultwords.remove("") # removing empty strings
    
    # converting back to string
    seq = " ".join(resultwords)
    
    return seq

# applying transformation
all_data['Description'] = all_data['Description'].apply(clean)

# subsets
ds = all_data[all_data['Job Title'] == "data scientist"]
da = all_data[all_data['Job Title'] == "data analyst"]

# getting word counts
ds_words = nlp.to_wcdf(ds['Description']).sum()
da_words = nlp.to_wcdf(da['Description']).sum()
# %%

'''
Input: Raw scraped data
Output: Merged DF
'''

# %%
## All my imports
print("Versions")
# Data science
import pandas as pd
print(f"Pandas: {pd.__version__}")
import numpy as np
print(f"Numpy: {np.__version__}")
# Visualization 
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style="ticks", color_codes=True)
import os
# Text Stuff
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from nltk.corpus import stopwords
# nltk.download("stopwords")

#%%
paths = {
    "heading": '../data/headings/heading_counts_clean.csv',
    'scraping': '../data/scraping_results/',
    'merged': '../data/merged_df.csv', # This is where to store the merged dataframe
    'visualizations': "../visualizations" # Path to store visualizations
}

# Ingesting the data from the Indeed scraping


def ingest_indeed(path = paths['scraping']):
    ''' 
    Inputs: 
    ------
    path : string
        Path of the files where the scraped data (results from the indeed.py
    goes to)   
    
    Outputs: 
    --------
    The final indeed dataframe with just "Title", "Description", and "Location"
    '''
    # initialize
    indeed = pd.DataFrame(columns = ['date', 'details', 'location', 'summary', 
                                     'title', 'url', 'rating'])
    
    # get json files into a list
    json_files = [i for i in os.listdir(path) 
    if 'data.json' in i]

    for file in json_files:
        print(file)
        indeed = indeed.append(pd.read_json(path + file))
        print(pd.read_json(path+file))

    # Combining the Details and Summary section from the indeed into - also adding location 
    # ONE column
    def combine(df):
        ''' 
        Combining the details and summary section
        Bonus: Attaching the location info
        '''
        location = []
        full = []

        for i, j, loc in zip(df['details'], df['summary'], df['location']):
            full.append(i + '\n' + j)

            loc = loc.lower()

            if "san francisco" in loc or "sf" in loc:
                location.append("san francisco")
            elif "new york" in loc or "ny" in loc:
                location.append("new york")
            elif "texas" in loc or "tx" in loc:
                location.append("texas")
            else:
                location.append("other")

        return pd.DataFrame({'Title': df['title'], 'Description': full, 
                            'Location': location})

    # Narrowing down to the parts we want and updating the changes into the 
    # indeed object
    indeed = combine(indeed)
    
    return indeed


#%%
indeed = ingest_indeed()


indeed.head()
# %%
indeed.tail()

# %%

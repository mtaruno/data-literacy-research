# All imports

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


def ETL(
    ''' This function is used to do all the extract, transform, load work.
    Inputs: Nothing
    Outputs: Dataframe with both Indeed and LinkedIn data


    
    '''

    # Ingesting the data from the Indeed scraping

    indeed = pd.DataFrame(columns = ['date', 'details', 'location', 'summary', 'title', 'url', 'rating'])

    for file in [i for i in os.listdir('results') if 'data.json' in i]:
        indeed = indeed.append(pd.read_json('results/' + file))
        
    # Combining the Details and Summary section from the indeed into - also adding location 
    # ONE column
    def combine(df):
        ''' 
        Combining the details and summary section
        Bonus: adding the location info
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


    ### Doing the same for linkedin
    

    return indeed


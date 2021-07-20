'''
Input: Raw scraped data
Output: Merged DF

'''

# %%
## All my imports
# Data science
import pandas as pd
import numpy as np
import os
# Text Stuff
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from nltk.corpus import stopwords
# nltk.download("stopwords")
from abc import ABC, abstractmethod


class ETL(ABC):
    def __init__(self):
        self.paths = {
            "heading": '../data/headings/heading_counts_clean.csv',
            'scraping': '/Users/mtaruno/Documents/DevZone/job-research/data/scraping_results/indeed/',
            'merged': '/Users/mtaruno/Documents/DevZone/job-research/data/merged_df.csv', # This is where to store the merged dataframe
            'visualizations': "../visualizations" , # Path to store visualizations
            'merged_with_headings': '/Users/mtaruno/Documents/DevZone/job-research/data/headings/headings_df.csv'
        }

    @abstractmethod
    def ingest(self):
        pass


#%%
class IndeedETL(ETL):

    # Ingesting the data from the Indeed scraping
    def enumerate_scraping_folder(path: str):
        json_files = [i for i in os.listdir(path) if 'data.json' in i]

        # initializing empty df
        indeed = pd.DataFrame(columns = ['date', 'details', 'location', 'summary', 
                                        'title', 'url', 'rating'])

        # appending all json file dataframes into indeed df
        for file in json_files:
            current_df = pd.read_json(path + file)
            assert isinstance(current_df, (pd.DataFrame,pd.Series))
            indeed = indeed.append(current_df)
        
        return indeed

    # Combining the Details and Summary section from the indeed into - also adding location 
    # ONE column
    def indeed_wrangling(df: pd.DataFrame) -> pd.DataFrame:
        ''' 
        - Combining the details and summary section into a description column
        - Attaches the location info
        '''
        assert 'details' in df.columns

        location = []
        desc = []

        for i, j, loc in zip(df['details'], df['summary'], df['location']):
            desc.append(i + '\n' + j)

            loc = loc.lower()

            if "san francisco" in loc or "sf" in loc:
                location.append("san francisco")
            elif "new york" in loc or "ny" in loc:
                location.append("new york")
            elif "texas" in loc or "tx" in loc:
                location.append("texas")
            else:
                location.append("other")

        return pd.DataFrame({'Title': df['title'], 'Description': desc, 
                            'Location': location})

    def ingest(path: str = None) -> pd.DataFrame:
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

        if path is None:
            path = self.paths['scraping']
        # initialize

        indeed = enumerate_scraping_folder(path)


        # Narrowing down to the parts we want and updating the changes into the indeed object
        indeed = indeed_wrangling(indeed)
        
        return indeed
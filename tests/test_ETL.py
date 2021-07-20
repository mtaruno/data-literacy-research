import unittest
import sys
# sys.path.insert(1, '../')
# from etl import ETL
import os
import pandas as pd

class TestETL(unittest.TestCase):
    def test_enumerate_scraping_folder(self):
        # path = ETL().paths['scraping']
        path = '/Users/mtaruno/Documents/DevZone/job-research/data/scraping_results/indeed/'
        json_files = [i for i in os.listdir(path) 
        if 'data.json' in i]


        # initializing empty df
        indeed = pd.DataFrame()

        for file in json_files:
            current_df = pd.read_json(path + file)
            assert isinstance(current_df, (pd.DataFrame,pd.Series))
            indeed = indeed.append(current_df)

        print(indeed.head())

        return indeed

unittest.main()



#%%
import os
os.listdir('../data/scraping_results')


# %%

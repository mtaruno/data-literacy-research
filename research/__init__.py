'''
Utils for NLP
'''


# Tells python that this directory should be treated like a package
import pandas as pd
import numpy as np
# Visualization 
import seaborn as sns
import matplotlib.pyplot as plt
import os
# Text Stuff
from sklearn.feature_extraction.text import CountVectorizer
import nltk
# Wordcloud
from wordcloud import WordCloud
from nltk.corpus import stopwords


class nlp_eda:

    def __init__(self):
        # Making sure to have the proper stopwords
        self.paths = {
            "heading": '../data/headings/heading_counts_clean.csv',
            'scraping': '../data/scraping_results/',
            'merged': '../data/merged_df.csv', # This is where to store the merged dataframe
            'visualizations': "../visualizations" # Path to store visualizations
        }
        
        # NLTK stopwords
        self.stop = stopwords.words("english") + ["data"]
        # Manual stopwords
        my_stop = ["and", "to", "the", "of", "with", "data"]


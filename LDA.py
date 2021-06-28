'''
This is where I want to execute all my LDA cod
'''

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import euclidean_distances, cosine_similarity
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 
import sys
sys.path.insert(1, '../')
import research
from research import nlp_eda
import re
import pickle 
import pyLDAvis
import os
import gensim
from gensim.utils import simple_preprocess
import nltk
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import gensim.corpora as corpora
from pprint import pprint


class LDA:

    def __init__(self):
        self.paths = {'all_data': '/data/merged_df.csv'}
        all_data = pd.read_csv(self.paths['all_data'], index_col = 0)
        # Subsetting into data scientist vs data analyst
        self.ds = all_data[all_data["Job Title"] == 'data scientist']
        self.da = all_data[all_data["Job Title"] == 'data analyst']

    def main():
        
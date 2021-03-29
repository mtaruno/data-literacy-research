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

    def to_wcdf(self, seq, stopwords = None):
        ''' Converts a sequence into a dataframe of counts using CountVectorizer
        Params:
        ------
        data: Pandas series/list of the corpus

        Returns:
        -------
        counts: dataframe with word counts
        '''
        if stopwords is None:
            stopwords = self.stop
        
        # Initializing the Count Vectorizer, exluding words 
        # that appear less than 5 times
        bagofwords = CountVectorizer(min_df = 5, stop_words = stopwords)
        words = bagofwords.fit_transform(seq)
        counts = pd.DataFrame(columns = bagofwords.get_feature_names(), data = words.toarray())

        return counts

    # Combining entire description column into a single string

    def word_cloud(self, seq, output_path = None, stop = None):
        ''' Creates a word cloud visualization
        Params:
        -------
        seq
            List or Pandas series of words
        output_path
            The path to export the visualization to
        '''
        
        if output_path == None:
            output_path = self.paths['visualizations']
        if stop == None:
            stop = self.stop
        
        combined_corpus = ""
        for i in seq:
            combined_corpus += '\n' + i

        # Generate word cloud visualization
        wordcloud = WordCloud(width = 3000, height = 2000, random_state=1, background_color='salmon', colormap='Pastel1', collocations=False, stopwords = stop).generate(combined_corpus)

        # Visualizing with a bar graph
        plt.figure(figsize=(40, 30))
        plt.imshow(wordcloud) 
        plt.axis("off");


    def visualize_counts(self, seq, n = 30, stopwords = None):
        '''
        Inputs:
        -------
        n: the top n words to visualize and include in the plot

        '''
        
        if stopwords == None:
            stopwords = self.stop
        
        counts = self.to_wcdf(seq, stopwords)

        # Getting word frequencies
        frequencies = counts.sum().sort_values(ascending = False)[1:n]

        # Visualizing
        plt.figure(figsize = (16, 5))
        sns.barplot(frequencies.index, frequencies.values, palette = 'inferno')
        plt.xticks(rotation = 90)
        plt.title(f"Top {n} Most Frequent Words in the Corpus Inside")
        plt.show()


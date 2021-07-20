import pandas as pd
import numpy as np
import os
import json

def clean(seq, to_remove = {'\n','analyst','scientist', 'science', 'machine', 'learning','scientists', "experience"}):
    ''' This is the preprocessing 
    pipeline that I do with the 
    Random Forest in mind.

    1. Convert to lowercase
    2. Remove special tokens 
    that is in to_remove set
    '''
    # converting to lowercase
    seq = seq.lower()

    resultwords  = [word for word in re.split("\W+",seq) if word.lower() not in to_remove]
    resultwords.remove("") # removing empty strings
    
    # converting back to string
    seq = " ".join(resultwords)
    
    return seq

def to_wcdf(seq, stopwords = None):
    ''' Converts a sequence into a dataframe of counts using CountVectorizer
    Params:
    ------
    data: Pandas series/list of the corpus

    Returns:
    -------
    counts: dataframe with word counts
    '''

    from nltk.corpus import stopwords
    from sklearn.feature_extraction.text import CountVectorizer

    if stopwords is None:
        print("Using Default Stopwords" )
        stop = stopwords.words("english") + ["data"]
    
    # Initializing the Count Vectorizer, exluding words 
    # that appear less than 5 times
    bagofwords = CountVectorizer(min_df = 5, stop_words = stop)
    words = bagofwords.fit_transform(seq)
    counts = pd.DataFrame(columns = bagofwords.get_feature_names(), data = words.toarray())

    return counts

# Combining entire description column into a single string


def visualize_counts(self, seq, n = 30, stopwords = None, color = "inferno"):
    '''
    Inputs:
    -------
    n: the top n words to visualize and include in the plot

    '''

    from nltk.corpus import stopwords
    
    if stopwords == None:
        print("Using Default Stopwords" )
        stop = stopwords.words("english") + ["data"]
    
    counts = to_wcdf(seq, stop)

    # Getting word frequencies
    frequencies = counts.sum().sort_values(ascending = False)[1:n]

    # Visualizing
    plt.figure(figsize = (16, 5))
    sns.barplot(frequencies.index, frequencies.values, palette = color)
    plt.xticks(rotation = 90)
    plt.title(f"Top {n} Most Frequent Words in the Corpus Inside")
    plt.show()

def visualize_seq_lengths(seq, title = "Distribution of Word Lengths"
                            , color = None):
    '''
    Parameters:
    -----------
    seq: A Pandas Series or simply a list 
    containing sequences of tokens
    '''
    seq = seq.apply(lambda x: x.split())
    seq_lengths = [len(line) for line in seq]
    plt.figure(figsize = (16, 5))
    sns.distplot(seq_lengths, color = color, 
        norm_hist = True)
    plt.xlabel("Sequence Length")
    plt.title(title)
    plt.show()


def word_cloud(seq, output_path = None, stop = None):
    ''' Creates a word cloud visualization
    Params:
    -------
    seq
        List or Pandas series of words
    output_path
        The path to export the visualization to
    '''
    from nltk.corpus import stopwords
    from sklearn.feature_extraction.text import CountVectorizer
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt

    # if output_path is None:
    #     output_path = IndeedETL().paths()
    if stop is None:
        print("Using Default Stopwords")
        stop = stopwords.words("english") + ["data"]

    combined_corpus = "".join('\n' + i for i in seq)
    # Generate word cloud visualization
    wordcloud = WordCloud(width = 3000, height = 2000, random_state=1, background_color='salmon', colormap='Pastel1', collocations=False, stopwords = stop).generate(combined_corpus)
    plt.figure(figsize=(40, 30))
    plt.imshow(wordcloud)
    plt.axis("off")
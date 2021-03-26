
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


# Combining entire description column into a single string

def visualize_counts(data, output_path = "/Users/mtaruno/Documents/Documents - Matthew’s MacBook Air/Work/SPRING2021/Independent/Independent Study/Dev/visualizations"):
    
    # NLTK stopwords
    stop = stopwords.words("english") + ["data"]
    # Manual stopwords
    my_stop = ["and", "to", "the", "of", "with", "data"]
    
    combined_corpus = ""
    for i in data["Description"]:
        combined_corpus += '\n' + i

    # Generate word cloud visualization
    wordcloud = WordCloud(width = 3000, height = 2000, random_state=1, background_color='salmon', colormap='Pastel1', collocations=False, stopwords = stop).generate(combined_corpus)

    # Visualizing with a bar graph
    plt.figure(figsize=(40, 30))
    plt.imshow(wordcloud) 
    plt.axis("off");
 
    n = 30
   
    # Initializing the Count Vectorizer, exluding words that appear less than 5 times
    bagofwords = CountVectorizer(min_df = 5, stop_words = stop)
    words = bagofwords.fit_transform(data['Description'])
    counts = pd.DataFrame(columns = bagofwords.get_feature_names(), data = words.toarray())
    counts.head()

    # Getting word frequencies
    frequencies = counts.sum().sort_values(ascending = False)[1:n]

    # Visualizing
    plt.figure(figsize = (16, 5))
    sns.barplot(frequencies.index, frequencies.values, palette = 'inferno')
    plt.xticks(rotation = 90)
    plt.title(f"Top {n} Most Frequent Words in the Corpus Inside")
    plt.show()
    
    return counts
    
    

import pandas as pd
import numpy as np
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns


def clean(
    seq: list,
    to_remove={
        "\n",
        "analyst",
        "scientist",
        "science",
        "machine",
        "learning",
        "scientists",
        "experience",
    },
) -> list:
    """ This is the preprocessing 
    pipeline that I do with the 
    Random Forest in mind.

    1. Convert to lowercase
    2. Remove special tokens 
    that is in to_remove set
    """
    # converting to lowercase
    seq = seq.lower()

    resultwords = [
        word for word in re.split("\W+", seq) if word.lower() not in to_remove
    ]
    resultwords.remove("")  # removing empty strings

    # converting back to string
    seq = " ".join(resultwords)

    return seq


def validate_data_types(df, str_columns=[], int_columns=[], float_columns=[]) -> None:
    """ Checks that the data types are correct and updates accordingly """
    for col in str_columns:
        df[col] = df[col].astype(str)
    for col in int_columns:
        df[col] = df[col].astype(int)
    for col in float_columns:
        df[col] = df[col].astype(float)

    print("Schema validated...")


def preprocess_heading_text(text):
    """ Takes in the heading text and returns the cleaned text """
    from nltk.corpus import stopwords
    import re

    exclude = [""]
    # Remove any non-alphanumeric characters
    text = re.sub(r"\W+", " ", text)
    # Remove any non-space whitespace
    text = re.sub(r"\s+", " ", text)
    # Remove any leading/trailing whitespace
    text = text.strip()
    # Convert all words to lowercase
    text = text.lower()
    # Remove any remaining stopwords
    text = " ".join(
        [word for word in text.split() if word not in stopwords.words("english")]
    )
    # Remove any remaining punctuation
    text = "".join(ch for ch in text if ch not in exclude)
    # Remove any remaining numbers
    text = "".join([ch for ch in text if not ch.isdigit()])
    # Remove any remaining non-alphanumeric characters
    text = re.sub(r"\W+", " ", text)
    # Remove any leading/trailing whitespace
    text = text.strip()
    # Remove any remaining stopwords
    text = " ".join(
        [word for word in text.split() if word not in stopwords.words("english")]
    )
    # Remove any remaining punctuation
    text = "".join(ch for ch in text if ch not in exclude)
    # Remove any remaining numbers
    text = "".join([ch for ch in text if not ch.isdigit()])
    # Remove any remaining non-alphanumeric characters
    text = re.sub(r"\W+", " ", text)
    # Remove any leading/trailing whitespace
    text = text.strip()
    # Remove any remaining stopwords
    text = " ".join(
        [word for word in text.split() if word not in stopwords.words("english")]
    )
    # Remove any remaining punctuation
    text = "".join(ch for ch in text if ch not in exclude)
    # Remove any remaining numbers
    text = "".join([ch for ch in text if not ch.isdigit()])
    # Remove any remaining non-alphanumeric characters
    text = re.sub(r"\W+", " ", text)

    return text


def remove_stopwords():
    pass


def to_wcdf(seq: pd.Series, ngram_range=(1, 1), stop=None):
    """ Converts a sequence into a dataframe of counts using CountVectorizer
    Params:
    ------
    data: Pandas series/list of the corpus
    ngram_range:  N gram range (1,2) means bigrams and unigrams

    Returns:
    -------
    counts: dataframe with word counts
    """

    from nltk.corpus import stopwords
    from sklearn.feature_extraction.text import CountVectorizer

    if stop is None:
        print("Using Default Stopwords")
        stopwords = stopwords.words("english") + ["data"]

    # Initializing the Count Vectorizer, exluding words
    # that appear less than 5 times
    bagofwords = CountVectorizer(min_df=5, ngram_range=ngram_range, stop_words=stop)
    words = bagofwords.fit_transform(seq)
    counts = pd.DataFrame(columns=bagofwords.get_feature_names(), data=words.toarray())

    return counts


# Combining entire description column into a single string
def visualize_counts(
    counts: pd.DataFrame,
    n=30,
    stop=None,
    color="inferno",
    title=f"Top 30 Most Frequent Words in the Corpus Inside",
):
    """
    Inputs:
    -------
    n: the top n words to visualize and include in the plot

    """

    from nltk.corpus import stopwords
    import matplotlib.pyplot as plt

    # Getting word frequencies
    frequencies = counts.sum().sort_values(ascending=False)[1:n]

    # Visualizing
    plt.figure(figsize=(16, 5))
    sns.barplot(frequencies.index, frequencies.values, palette=color)
    plt.xticks(rotation=90)
    plt.title(title)
    plt.show()


def visualize_seq_lengths(seq, title="Distribution of Word Lengths", color=None):
    """
    Parameters:
    -----------
    seq: A Pandas Series or simply a list 
    containing sequences of tokens
    """
    seq = seq.apply(lambda x: x.split())
    seq_lengths = [len(line) for line in seq]
    plt.figure(figsize=(16, 5))
    sns.distplot(seq_lengths, color=color, norm_hist=True)
    plt.xlabel("Sequence Length")
    plt.title(title)
    plt.show()


def word_cloud(seq, output_path=None, stop=None):
    """ Creates a word cloud visualization
    Params:
    -------
    seq
        List or Pandas series of words
    output_path
        The path to export the visualization to
    """
    from nltk.corpus import stopwords
    from sklearn.feature_extraction.text import CountVectorizer
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt

    # if output_path is None:
    #     output_path = IndeedETL().paths()
    if stop is None:
        print("Using Default Stopwords")
        stop = stopwords.words("english") + ["data"]

    combined_corpus = "".join("\n" + i for i in seq)
    # Generate word cloud visualization
    wordcloud = WordCloud(
        width=3000,
        height=2000,
        random_state=1,
        background_color="salmon",
        colormap="Pastel1",
        collocations=False,
        stopwords=stop,
    ).generate(combined_corpus)
    plt.figure(figsize=(40, 30))
    plt.imshow(wordcloud)
    plt.axis("off")

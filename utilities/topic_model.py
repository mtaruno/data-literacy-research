"""
Topic Modelling Module
"""


import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import euclidean_distances, cosine_similarity
import sys
import re
import pickle
import pyLDAvis
import os
import gensim
from gensim.utils import simple_preprocess
import nltk
from nltk.corpus import stopwords
import gensim.corpora as corpora
from pprint import pprint
from utilities.utils import preprocess_heading_text
import seaborn as sns
import matplotlib.colors as mcolors
import pyLDAvis.gensim_models


class TopicModelling:
    def __init__(self, n_topics=4):
        self.n_topics = n_topics
        self.headings_df = pd.read_csv(
            "/Users/mtaruno/Documents/DevZone/job-research/data/headings/headings_df.csv",
            index_col=0,
        )

    def ingest_and_filter(self, filter_col_name="Job"):
        df = self.headings_df[
            self.headings_df["Person/Job/Org/None"] == filter_col_name
        ]

        # Taking just the Text and applying a preprocessing pipeline to it
        return (
            df["Heading Text"].astype(str).apply(lambda x: preprocess_heading_text(x))
        )

    def lda_preprocess(self, text_series):
        """
        Input:
            text_series: pd.Series of preprocessed heading text
        """
        # Create Dictionary
        id2word = corpora.Dictionary(text_series)

        # Create Corpus
        texts = text_series

        # Term Document Frequency
        corpus = [id2word.doc2bow(text) for text in texts]

        # View
        print(corpus[:1][0][:30])

        return corpus, id2word

    def train_lda(self, corpus, id2word, num_topics=10):
        # Build LDA model
        lda_model = gensim.models.LdaMulticore(
            corpus=corpus, id2word=id2word, num_topics=num_topics
        )

        # Print the Keyword in the 10 topics
        pprint(lda_model.print_topics())
        doc_lda = lda_model[corpus]

        return lda_model, doc_lda

    def get_topics_sentences_keywords(ldamodel=None, corpus=None, texts=None):
        """Analyzing model and returning exploratory dataframe"""
        # Initialize output
        sent_topics_df = pd.DataFrame()

        # Get main topic in each document
        for i, row_list in enumerate(ldamodel[corpus]):
            row = row_list[0] if ldamodel.per_word_topics else row_list
            # print(row)
            row = sorted(row, key=lambda x: (x[1]), reverse=True)
            # Get the Dominant topic, Perc Contribution
            # and Keywords for each document
            for j, (topic_num, prop_topic) in enumerate(row):
                if j == 0:  # => dominant topic
                    wp = ldamodel.show_topic(topic_num)
                    topic_keywords = ", ".join([word for word, prop in wp])
                    sent_topics_df = sent_topics_df.append(
                        pd.Series(
                            [int(topic_num), round(prop_topic, 4), topic_keywords]
                        ),
                        ignore_index=True,
                    )
                else:
                    break
        sent_topics_df.columns = [
            "Dominant_Topic",
            "Perc_Contribution",
            "Topic_Keywords",
        ]

        # Add original text to the end of the output
        contents = pd.Series(texts)
        sent_topics_df = pd.concat([sent_topics_df, contents], axis=1)

        # Formatting
        # Format
        sent_topics_df = sent_topics_df.reset_index()
        sent_topics_df.columns = [
            "Document_No",
            "Dominant_Topic",
            "Topic_Perc_Contrib",
            "Keywords",
            "Text",
        ]

        return sent_topics_df

    def get_tsne(self, lda_model, corpus):
        # Get topic weights and dominant topics ------------
        from sklearn.manifold import TSNE
        from bokeh.plotting import figure, output_file, show
        from bokeh.models import Label
        from bokeh.io import output_notebook

        # Get topic weights
        topic_weights = []
        for i, row_list in enumerate(lda_model[corpus]):
            topic_weights.append([w for i, w in row_list])

        # Array of topic weights
        arr = pd.DataFrame(topic_weights).fillna(0).values

        # Keep the well separated points (optional)
        arr = arr[np.amax(arr, axis=1) > 0.35]

        # Dominant topic number in each doc
        topic_num = np.argmax(arr, axis=1)

        # tSNE Dimension Reduction
        tsne_model = TSNE(
            n_components=2, verbose=1, random_state=0, angle=0.99, init="pca"
        )
        tsne_lda = tsne_model.fit_transform(arr)

        # Plot the Topic Clusters using Bokeh
        output_notebook()
        n_topics = 4
        mycolors = np.array([color for name, color in mcolors.TABLEAU_COLORS.items()])
        plot = figure(
            title="t-SNE Clustering of {} LDA Topics".format(n_topics),
            plot_width=900,
            plot_height=700,
        )
        plot.scatter(x=tsne_lda[:, 0], y=tsne_lda[:, 1], color=mycolors[topic_num])
        show(plot)

    def get_pyLDAvis(self, lda_model, corpus):
        pyLDAvis.enable_notebook()
        vis = pyLDAvis.gensim_models.prepare(lda_model, corpus, dictionary=lda_model.id2word)
        return vis

    def run(self, choice_text="Job"):
        """ Choice text is either Person/Job/Org/None"""
        text = self.ingest_and_filter(choice_text)
        tokenized_text = text.apply(lambda x: x.split(" "))

        print("Ingestion and preprocessing complete...")
        corpus, id2word = self.lda_preprocess(tokenized_text)

        print("LDA preprocessing complete...")
        lda_model, doc_lda = self.train_lda(
            corpus=corpus, id2word=id2word, num_topics=self.n_topics
        )

        print("LDA training complete...")

        self.get_tsne(lda_model=lda_model, corpus=corpus)

        print("TSNE plot complete...")

        fig = self.get_pyLDAvis(lda_model=lda_model, corpus=corpus)

        return fig


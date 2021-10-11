'''
Header level analysis
'''
#%%
import utilities.utils
from utilities.etl import IndeedETL
# import importlib
# importlib.reload(etl)
import pandas as pd
from utilities.utils import to_wcdf

data = pd.read_csv(IndeedETL().paths['merged_with_headings'], index_col=0)
    


# %%
# checking distribution of job vs person
data['Person/Job/Org/None'].value_counts()

# %%
# creating respective dataframes
person = data[data['Person/Job/Org/None'] == 'Person']
job = data[data['Person/Job/Org/None'] == 'Job']

# %%
person
# %%
job

# %%
from utilities.visualize import bar, distplot

# visualizing

# %%
import utilities.utils
# import importlib
# importlib.reload(utils)
from utilities.utils import word_cloud

# distribution of headings in Person sections
word_cloud(person['Heading'])

# distribution of headings in Job sections
word_cloud(job['Heading'])
# %%
# set analysis 
to_wcdf(list(person['Heading']))

# %%
person['Heading']

# %%
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer

def set_diagnostics(df_a, df_b, name_a, name_b):
    '''
    This function compares the tokens from two sequences.

    It does it by taking the "Heading Text" column from 
    two dataframes, df_a and df_b, then it makes comparisons
    between the two.
    
    Input
    -----
    df_a: Dataframe with a column containing
    tokens you want to compare in the 'Heading Text' column

    df_b: Same thing but for the other df you want to compare
    with

    Output
    ------
    3 graphs: A, B, and A n B tokens
    
    '''

    def topn(data, n = data.shape[0]):
        stop = stopwords.words("english") + ["data"]
        # Initializing the Count Vectorizer, exluding words 
        # that appear less than 5 times
        bagofwords = CountVectorizer(min_df = 5, stop_words = stop)
        words = bagofwords.fit_transform(data['Heading Text'].dropna())
        counts = pd.DataFrame(columns = bagofwords.get_feature_names(), data = words.toarray())
        top = counts.sum().sort_values(ascending=False)[:n]
        return top 
    
    #visualizing top words in person and job
    a_words = set(topn(df_a, 50).index)
    b_words = set(topn(df_b,50).index)

    bar(x = topn(df_a, 50).index, y = topn(df_a, 50).values, 
    title = "Top in {}".format(name_a))
    bar(x = topn(df_b, 50).index, y = topn(df_b, 50).values, 
    title = "Top in {}".format(name_b))

    # visualizing intersections
    intersection = a_words.intersection(b_words)

    # visualizing words that appear in both

    import plotly.express as px

    # creating stacked bar chart of top intersection terms

    a_mask = [i in intersection for i in topn(df_a).index]
    b_mask = [i in intersection for i in topn(df_b).index]

    a_counts = topn(df_a)[a_mask].reset_index()
    a_counts["title"] = [name_a] * a_counts.shape[0]
    b_counts = topn(df_b)[b_mask].reset_index()
    b_counts["title"] = [name_b] * b_counts.shape[0]

    combined = pd.concat([b_counts, a_counts], axis=0)
    combined = combined.rename(columns = {"index": "word", 
    0: "counts"}).sort_values("counts", ascending = False)

    fig = px.bar(combined, x = "word", y = "counts", 
    color = "title", title = f"Comparing Tokens That Appear in {name_a} and {name_b}",
    barmode = "group")

    fig.show()

set_diagnostics(person, job, "Person", "Job") 


# %%

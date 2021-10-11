'''
Ensuring that the headings_df contains the correct data preprocessing steps.

'''

#%% 
import pandas as pd
import plotly.express as px
import numpy as np
from utilities.utils import preprocess_heading_text
from utilities.utils import validate_data_types


df = pd.read_csv("data/headings/headings_df.csv", index_col = 0)
validate_data_types(df, str_columns = ['Heading Text', 'Heading Title', 'Person/Job/Org/None'])

def separate_into_groups(df):
    ''' Takes in the dataframe and outputs the relevant job/person filtered groups '''
    job = df[df['Person/Job/Org/None'] == 'Job']
    person = df[df['Person/Job/Org/None'] == 'Person']
    org = df[df['Person/Job/Org/None'] == 'Org']

    return job, person, org


df['Heading Text'] = df['Heading Text'].apply(preprocess_heading_text)

df = df[(df['Person/Job/Org/None'] == 'Job' )|(df['Person/Job/Org/None'] == 'Person')]

#%%
from utilities.rf import RFAnalysis
from utilities.utils import to_wcdf

# Get features
X = to_wcdf(df['Heading Text'])

# Get target
y = df['Person/Job/Org/None']
#%%

rf = RFAnalysis()

# Split the data
X_train, X_test, y_train, y_test = rf.train_test_split(X, y)

# Train the model
print("Training model...")
fitted_grid = rf.rf_pipeline(X_train, y_train)

# Save the model
print("Saving model...")
rf.save_model(fitted_grid, f'/Users/mtaruno/Documents/DevZone/job-research/data/models')

#%%

# Evaluate the model
print("Evaluating model...")
rf.evaluate_model(X_train, y_train, X_test, y_test, fitted_grid)
#%%
# Get the feature importances
print("Getting feature importances...")
importances = rf.get_feature_importances(fitted_grid, feature_names = X.columns.tolist(), save_directory_path = '/Users/mtaruno/Documents/DevZone/job-research/data/artifacts/importances/{}')
# %%
rf.visualize_feature_importances(importances)

# %%

# %%

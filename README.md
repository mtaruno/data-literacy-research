# Data Literacy Research

In this research project, I collaborate with [Professor Sandra Cannon](https://www.sas.rochester.edu/dsc/people/faculty/cannon-sandra/index.html) in measuring data literacy expectations from the ways employers describe jobs and the way they describe the people they are looking for. We find the discriminatory power between how employers describe jobs and what the actual work on the job entails. 

## Current Pipeline

<!-- ![Data Literacy Expectations Pipeline](https://user-images.githubusercontent.com/44710581/127424263-3b247261-b76a-417b-b2c0-dbd38091e8a2.png)
 -->
![Data Literacy Expectations Pipeline Transparant](https://user-images.githubusercontent.com/44710581/127424664-0d90f2c7-e692-44f4-95c8-f70e3ba31d2c.png)



# Files:

```linkedin.py``` This is the file you use to generated the dataframe of linkedin postings - results will be stored in data/scraping_results (tagged with "linkedin")

```indeed.py``` Same as linkedin.py but for indeed postings - results will be stored in data/scraping_results (tagged with "indeed")



# Notes
Data files:
* `merged_headings_df`: Contains both the LinkedIn and Indeed postings in a single DataFrame



# Utility Functions (in `utilities.utils`)
* `to_wcdf`
* `preprocess_heading_text`: Takes the Heading Text, which is initially intended for `merged_headings_df`, and applies a preprocessing pipeline on it
* `visualize_counts`: Takes in a Pandas series of string row entiresand visualizes using Seaborn teh top n words in that corpus
* `visualize_seq_lengths`: Visualizes the distribution of word lengths in a sequence

'''
This is the script where I take the
based on the description.
merged data and add headings to them


Rule:

If the sequence length in between new line separators is less than 6 and is contained in the vocab list, 
then we consider that a heading. We then can create a division for it and expand the dataframe
to contain heading level information.

Example:  \n qualifications \n 

'''


#%%
import pandas as pd
from utilities.etl import IndeedETL
import numpy as np

e = IndeedETL()

# ingesting merged dataframe
merged = pd.read_csv(e.paths['merged'], index_col = 0)
merged['Job Title'].value_counts()


#%%

# headings section
# Unit testing check function

vocab = ["Job", "Location", "Qualifications", 
"Perks", "Impact", "About", "Description", 
"Compensation", "Why", "Summary", "Skills", 
"Preferred", "Who", "Requirements",
"Opportunity"]

vocab = [i.lower() for i in vocab]

def check(sent, vocab):
    ''' Checks if the heading vocab is 
    inside the sentence you feed it in '''
    contains = False
    for word in vocab:
        evaluate = [word in i for i in sent]
        if True in evaluate:
            contains = True
            break
    return contains


# These are a set of words that I want to require in order for the line to be a heading classification
vocab = ["Job", "Location", "Qualifications", "Perks", "Impact", "About", "Description", 
         "Compensation", "Why", "Summary", "Skills", "Preferred", "Who", "Requirements",
        "Opportunity", "Salary", "Impact", "Work", "Join", "Technical", "Required",
        "Overview", "What", "Benefits", "Vision", "Mission", "Responsibilities",
        'Experience', "Need", "Forward", "Love", "Characteristics", "Desired", "Career",
        "Notices", 'Education']
vocab = [i.lower() for i in vocab]

# Example - we are just testing on one of the description rows
test  = "this position can be based \
remotely anywhere in the usa or based in \
tonawanda ny linde is a leading global industrial \
gases and engineering company with 2019 sales of 28 \
billion 25 billion we live our mission of making our \
world more productive every day by providing high quality \
solutions technologies and \n qualifications \n services which are making our \
customers more successful and helping to sustain and \
protect our planet the company serves a variety of end \
markets including aerospace chemicals food and beverage \
electronics energy healthcare manufacturing and primary \
metals linde s industrial gases are used in countless applications from life saving oxygen for hospitals to high purity specialty gases for electronics manufacturing hydrogen for clean fuels and much more linde also delivers state of the art gas processing solutions to support customer expansion efficiency improvements and emissions reductions for more information about the company and its products and services please visit www linde com position summary this is a unique opportunity to collaborate with a diverse team of technical experts to solve a variety of complex problems in a fun and dynamic environment with flexibility to use the latest tools and technology imagination and creativity are the only limitations on your impact the data will be a member of the digital americas organization digital americas is a multi disciplinary technical team comprised of data software engineers and operations research experts the team serves linde s global business units and is tasked with creating analytics and decision support software solutions for complex problems key accountabilities collaborate with business partners to understand product requirements and define appropriate technical solutions lead technical development of cutting edge analytics and decision support tools stay abreast of new technology and actively contribute ideas for new programs balance development of new solutions with replication and support of existing tools desired skills and basic requirements bs degree in industrial engineering chemical engineering computer statistics or operations research with a specialization in data or analytics excellent analytical and problem solving skills passion for technology with a strong emphasis on user and business value ability to succinctly convey complex solutions to business stakeholders and executive leadership willingness to work in an agile and dynamic environment availability to travel up to 30 domestic and international preferred qualifications ms or higher degree in industrial engineering chemical engineering computer statistics or operations research with a specialization in data or analytics 5 years of relevant industry deep knowledge of and or operations research theory with practical development strong programming skills in python or at least one major programming language demonstrated ability to follow software development best practices ability to develop implement and support production level data pipelines with apis and microservices with web application development deploying solutions to cloud providers preferably azure designing and using relational databases nosql data stores and data historians with data visualization with docker and linux environments all qualified applicants will receive consideration for employment without regard to race color religion sex national origin age disability protected veteran status pregnancy sexual orientation gender identity or expression or any other reason prohibited by applicable law"

def check(sent, vocab):
    ''' 
    Input: A list of tokens
    Outputs: Boolean
    
    Checks if the heading vocab is inside the sentence you feed it in '''
    contains = False
    for word in vocab:
        evaluate = [word in i for i in sent]
        if True in evaluate:
            contains = True
            break
    return contains


def header_separation(desc):
    ''' This function constantly flips between list methods and string methods to do 
    the calculations.
    
    Inputs: 
    -------
    Job Description for ONE entry

    Outputs: 
    --------
    A dataframe with Heading as a column, and Heading text mapped to it in another
    '''
    # Separating it BY NEW LINE and making it a list of lists.
    desc = [i.split() for i in desc.split('\n')]
    
    # Removing all empty lists (entries)
    while [] in desc: desc.remove([]) 
        
    # Prepending: Designating the first header to be called 'Entry'
    headers = ["Entry"]
    master_content = []
    current_content = []

    # Code to classify header = If the line has less than 6 tokens, I consider it a header.
    # Then I take everything in between headers as the current header content
    for i in desc:
        # Checking if the heading vocab is inside the line
        lowered_sent = [e.lower() for e in i]
        if len(i) < 6 and check(lowered_sent, vocab):
#             print("============================================================\n")
#             print(current_content)
            master_content.append([" ".join(i) for i in current_content])
            current_content.clear()
            current_header = " ".join(i)
            headers.append(current_header)
        else:
            current_content.append(i)
            
    # Adjusting for the prepend to add the last entry manually
    master_content.append([" ".join(i) for i in current_content])
    
    # Need to convert from list to just a string
    stringed_master_content = []
    
    # Converting the content from a list to just a string
    for i in master_content:
        if len(i) >= 1:
            stringed_master_content.append(i[0])
        else:
            stringed_master_content.append('')
    
    # Using extracted dictionary to create a new dataframe of Heading and its text
    output = pd.DataFrame({"Heading": headers, "Heading Text": stringed_master_content})
        
    return output


output = header_separation(test)

# %%

# unit tests
def check(sent, vocab):
        ''' 
        Input: A list of tokens
        Outputs: Boolean
        
        Checks if the heading vocab is inside the sentence you feed it in '''
        contains = False
        for word in vocab:
            evaluate = [word in i for i in sent]
            if True in evaluate:
                contains = True
                break
        return contains

check("qualifications of this role is".split(), vocab)
# %%


def remove_punctuations(line, punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''):
    ''' This function is used to remove the punctuations from the dataset '''
    # Removing punctuations
    no_punct = ""
    for char in line:
        if char not in punctuations:
            no_punct = no_punct + char

    return no_punct.lower()


def attach_headings(df, path_to_labels = '../data/headings/heading_labels.csv', 
                    save_to_path = "../data/merged_headings_df.csv",
                    save_job_id_path = "../data/job_id_mappings.csv"):
    '''
    Now for each job posting, based on the ID, I will create new 
    dataframe containing the headings and mapping it to the ID
    '''

    def synthesize_headings(df):
        ''' 
        Inputs: 
        -------
        Job descriptions dataframe 
        
        Outputs:
        -------
        Original dataframe with Job ID column, Heading synthesized dataframe
        '''

        # Creating a unique ID for the df
        df['ID'] = np.arange(df.shape[0])

        heading = pd.DataFrame(columns = ["ID", "Heading", "Heading Text"])
        job_id = []

        for i in range(len(df)):
            # Mini header represents the headings dataframe for ONE given row in the Linkedin dataframe
            # The columns it has is Heading and Heading Text
            mini_header = header_separation(df['Description'].iloc[i])
            heading = pd.concat([heading, mini_header])

            # Manually creating the Job ID row based on the number of rows that results in the mini heading df
            job_id += [df['ID'].iloc[i]] * mini_header.shape[0]

        # Adding Job ID Column into the final heading dataframe
        heading['ID'] = job_id

        return df, heading

    # Merged will be the merged dataframe with the ID column attached, 
    merged_with_job_id, headings = synthesize_headings(df)

    # Cleaning the headings column of the merged headings dataframe
    headings['Heading'] = headings['Heading'].apply(remove_punctuations)

    # Now adding a label onto based on Professor Sandra's suggestion
    heading_labels = pd.read_csv(path_to_labels)

    headings_df = pd.merge(headings, heading_labels, left_on = "Heading", right_on = "Heading Title", how = "inner")
    headings_df.drop(['Unnamed: 0', 'Unnamed: 4', "Heading"], axis = 1, inplace = True)
    
    # Exporting to csv
    headings_df.to_csv(save_to_path)
    merged_with_job_id.to_csv(save_job_id_path)
    
    return headings_df


#%%
# converting merged DF to one with the job IDs
headings_df = attach_headings(merged) 
headings_df.head()


# %%
headings_df
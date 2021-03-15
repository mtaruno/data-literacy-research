'''
This scraper is an end-to-end script for scraping LinkedIn with Selenium.


Their [terms and conditions](https://legal.linkedin.com/api-terms-of-use)

LinkedIn doesn't like scrapers, so they don't have a personal API. But we can still do stuff with our scraping packages that I will show here.

We have a lot of functionality that we could do - and these are limited to what I am able to access usually from my LinkedIn account. 

Selenium provides an API that allows you to access web drivers including Firefox, Internet Explorer, and Chrome. I then use BeautifulSoup to parse the webpage information I am interested in.

Source: https://levelup.gitconnected.com/linkedin-scrapper-a3e6790099b5

From my research, there are two types of info people usually want to scrape from LinkedIn. The first is profile scraping (there are tools like PhantomBuster for that). But the one that we are more interested in for this project is the job descriptions. The code below is for this second part!


Requirements:
-------------
A config.txt file containing your username and password (separated with a space)

'''

import requests, time
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import requests
import pandas as pd
import numpy as np
from selenium.common.exceptions import NoSuchElementException

# from selenium.webdriver.support.ui import WebDriverWail
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as ec


# Initializing account info
# My personal login info (I put it into config.txt for privacy reasons)
with open('config.txt') as f:
    file = f.readlines()[0]
    username, password = file.split()
    

def initialize():
    ''' Initializes a Chrome driver, opens linkedin and automatically inputs my username and password. '''
    # Input path to chrome driver executable
    browser = webdriver.Chrome("../data/chromedriver2") # Now we're connected to a browser!

    # This driver allows us to access webpages from a chrome browser
    # Logging in to LinkedIn
    browser.get('https://www.linkedin.com/login')

    # Entering login info
    elementID = browser.find_element_by_id('username')
    elementID.send_keys(username)

    elementID = browser.find_element_by_id('password')
    elementID.send_keys(password)

    elementID.submit()
    
    return browser

browser = initialize()

# Searching "data" in jobs

browser.get('https://www.linkedin.com/jobs/?showJobAlertsModal=false')
jobID = browser.find_element_by_class_name('jobs-search-box__text-input')
jobID.send_keys("data")

# Make sure to close messages first so that the search button is "clickable"
# This code is an automated way of doing that

def popup():
    ''' Uses try loops to recognize when the popup is available and closing it
    down in the event that it is. '''
    try:
        if browser.find_element_by_class_name('msg-overlay-list-bubble--is-minimized') is not None:
            pass
    except NoSuchElementException:
        try:
            if browser.find_element_by_class_name('msg-overlay-bubble-header') is not None:
                browser.find_element_by_class_name('msg-overlay-bubble-header').click()
        except NoSuchElementException:
            pass

popup()

# Actually clicking the search button (we have to find the HTML element, 
# then use click method on that element)
search = browser.find_element_by_class_name('jobs-search-box__submit-button')
search.click()



# Get page source code
time.sleep(5) # While waiting for page to load

src = browser.page_source

# Beautiful Soup object
soup = BeautifulSoup(src, 'lxml') # Using lxml parser
# Make sure to do pip install lxml if you haven't

# Get the search result number
results = soup.find('small', {'class': 'display-flex t-12 t-black--light t-normal'}).get_text().strip().split()[0]
results = f"There are {int(results.replace(',', ''))} results"
print(results)


### Narrowing to the Information we Want!

# Looking for all the job containers
# I found the class from doing a string search for Umbel (which was my first job result in the chrome driver)

job_container = soup.find_all('li', {"class":"jobs-search-results__list-item occludable-update p0 relative ember-view"})

# Filtering down to the links for individual companies
expression = re.compile(r"\/jobs\/view")
l1 = [job.attrs['href'] for job in soup.find_all('a')]
postings = [ "https://linkedin.com" + s for s in l1 if expression.match(s) ]
postings = list(set(postings)) # Getting unique postings

def scrape():
    ''' Goes through postings one by one that was generated with the code before,
    scrapes out all the desired information, and stores it in a dataframe.
    
    Returns the dataframe and saves it with the timestamp labeled on it as a csv file.
    '''
    title = []
    description = []
    company_name = []
    industry = []
    location = []
    job_functions = []
    time_posted = []
    employment_type = []
    applicant_count = []
    
    for post in postings:
    
        browser.get(post)
        popup()
        time.sleep(2)

        # Parsing out the wanted attributes based on company

        # Classnames are unique, so we filter by that
        # The LinkedIn layout is all the same, hence why this works.

        html = browser.page_source
        time.sleep(2)

        page = BeautifulSoup(html, "lxml")

        # Getting the description
        result = page.find_all("div", {"class": "jobs-box--fadein"})
        description.append(result[0].span.text)

        # Getting the title
        result = page.find_all("div", {"class": "p5"})
        title.append(result[0].h1.text)
        
        # Getting the company name
        result = page.find_all("a", {"class": "ember-view t-black t-normal"})
        company_name.append(result[0].text.replace("\n",""))
        try:
            # Getting the industry
            result = page.find_all("li", {"class": "jobs-description-details__list-item t-14"})
            industry.append(result[0].text.replace("\n",""))
        except:
            industry.append(np.nan)
        try:
            # Getting the job functions (it's in the same class)
            job_functions.append(result[1].text.replace("\n", ""))
        except:
            job_functions.append(np.nan)
        
        # Getting the location
        result = page.find_all("span", {"class": "jobs-unified-top-card__bullet"})
        location.append(result[0].text)
        
        try:
            # Getting the employment type
            result = page.find_all("p", {"class": "t-14 mb3"})
            employment_type.append(result[0].text.replace("\n", ""))
        except:
            employment_type.append(np.nan)
        
        # Getting the time posted
        try:
            result = page.find_all("span", {"class": "jobs-unified-top-card__posted-date"})
            time_posted.append(result[0].text.replace("\n", ""))
        except:
            time_posted.append(np.nan)
        
        # Getting the applicant count
        try:
            result = page.find_all("span", {"class": "jobs-unified-top-card__applicant-count"})
            applicant_count.append(result[0].text.replace("\n", ""))
        except:
            applicant_count.append(np.nan)
    
    # Storing in dataframe
    df = pd.DataFrame({"Title": title, "Description": description,
                      "Company Name": company_name, "Location": location,
                      "Industry": industry, "Job Functions": job_functions, 
                      "Time Posted": time_posted, "Employment Type": employment_type,
                      "Applicant Count": applicant_count})
    
    # Saving dataframe into csv, with a timestamp attached to it
    df.to_csv("results/job_scraping" + str(datetime.now())[:19] + ".csv")
    
    return df

df = scrape()

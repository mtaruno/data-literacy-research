'''
This scraper is an end-to-end script for scraping LinkedIn with Selenium.

'''

import requests, time
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import requests
import pandas as pd
import numpy as np

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
    browser = webdriver.Chrome("../data/chromedriver") # Now we're connected to a browser!

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

from selenium.common.exceptions import NoSuchElementException

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
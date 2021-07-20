'''
NOTE: This is not my work.

Source: [Github](https://github.com/jlgamez/indeed-jobs-scraper)
[Article](https://jlgamez.com/how-i-scrape-jobs-data-from-indeed-com-with-python/)

[Article 2](https://www.jobspikr.com/blog/scraping-indeed-job-data-using-python/)

I built on top of the work I found in these links to match my project needs.
'''

#%%
import json
import re
import ssl
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from datetime import datetime

BASE_URL = "https://www.indeed.com/"
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def main():
    name_of_city = input ("Enter name of city: ")
    keywords = input("Enter keywords: ")
    number_of_pages = input("Number of pages: ")
    name_of_city = "+".join(name_of_city.split(' '))
    keywords = "+".join(keywords.split(' '))
    url_to_scrape = BASE_URL + "/jobs?q=" + keywords + "&l=" + name_of_city
    number_of_pages_nos = int(number_of_pages)
    data_collected = scrape_data(url_to_scrape, number_of_pages_nos)
    with open('../data/scraping_results/data.json' + str(datetime.now())[:16], 'w') as fp:
        json.dump(data_collected, fp, sort_keys = True, indent = 4, ensure_ascii = False)
        
def scrape_data(url_to_scrape, number_of_pages_nos):
    data_collected=[]
    for i in range(0, number_of_pages_nos):
        extension = ""
        if i != 0:
            print('in')
            extension = "&start=" + str(i * 10)
            url = url_to_scrape + extension
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            web_page = urlopen(req).read()
            soup = BeautifulSoup(web_page, 'html.parser')
            data_collected = get_data_from_webpage(data_collected, soup)
    return data_collected
    
def extract_data_points(job, div):
    for a in div.findAll('a', attrs = {'class': 'jobtitle turnstileLink'}):
        job['title'] = a['title']
        print(job['title'])
    for a1 in div.findAll('a', attrs = {'class': 'companyName'}):
        job['companyName'] = a1.text.strip()
    for span in div.findAll('span', attrs = {'class': 'ratingsContent'}):
        job['rating'] = span.text.strip()
    for span1 in div.findAll('span', attrs = {'class': 'location accessible-contrast-color-location'}):
        job['location'] = span1.text.strip()
    for div1 in div.findAll('div', attrs = {'class': 'summary'}):
        summary = div1.text.strip()
        job['summary'] = summary
    for span2 in div.findAll('span',attrs = {'class' : 'date'}):
        job['date'] = span2.text.strip()
    return job

def get_data_from_webpage(data_collected, soup):
    job_posts = []
    for div in soup.findAll('div', attrs = {'class': 'jobsearch-SerpJobCard unifiedRow row result'}):
        job = dict()
        job = extract_data_points(job, div)
        job_posts.append(div['data-jk'])
        single_job_post_extension_url = "https://www.indeed.com/viewjob?jk=" + div['data-jk']
        job['url'] = single_job_post_extension_url
        req = Request(single_job_post_extension_url, headers = {'User-Agent' : 'Mozilla/5.0'})
        web_page = urlopen(req).read()
        job_soup = BeautifulSoup(web_page, 'html.parser')
        
        for inside_div in job_soup.findAll('div', attrs={'class': 'jobsearch-jobDescriptionText'}):
            details=inside_div.text.strip()
            job['details'] = details
        data_collected.append(job)
    return data_collected

if __name__ == "__main__":
    main()
    print("Extraction of data complete. check json file")


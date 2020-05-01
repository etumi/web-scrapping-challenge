# Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist

import re
import pandas as pd


def _init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():

    browser = _init_browser()

    ## Get latest news article and paragraph
    #---------------------------------------------

    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    #Scape Page
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    grid = soup.find('ul', class_='item_list')
    article = grid.find('li', class_='slide')

    news_title = article.find('div', class_='content_title').text
    news_p = article.find('div', class_='article_teaser_body').text

    ## Get featured image from Mars website
    #---------------------------------------------

    # URL of page to be scraped
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    #Scrape Page
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    browser.click_link_by_partial_text('FULL IMAGE')

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    image_relative_path = soup.find('img', class_='fancybox-image')
    image_relative_path = image_relative_path['src']
    featured_image_url = 'https://www.jpl.nasa.gov/' + image_relative_path

    ## Get latest weather from Twitter page
    #---------------------------------------------

    # URL of page to be scraped
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)  

    #Scrape Page
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_weather = soup.find('span', text = re.compile('InSight sol')).text
    mars_weather = mars_weather.replace('InSight s', 'S') 

    ## Get Mars fact from planets fact Website
    #---------------------------------------------

    # URL of page to be scraped
    url = 'https://space-facts.com/mars/'
    browser.visit(url)

    #Scrape Page
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_fact_table = soup.find('table', class_="tablepress tablepress-id-p-mars")
    mars_fact_table = pd.read_html(str(mars_fact_table)) #[0]

    ## Get Hemisphere images
    #---------------------------------------------

    ##Put all collected data in a dictionary

    data_entry = {}

    data_entry['news_title'] = news_title
    data_entry['news_p'] = news_p
    data_entry['featured_image'] = featured_image_url
    data_entry['mars_weather'] = mars_weather
    data_entry['mars_fact_table'] = mars_fact_table
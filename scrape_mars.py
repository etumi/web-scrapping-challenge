# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist

import re
import pandas as pd
import time


def _init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape_info():

    browser = _init_browser()

    #---------------------------------------------
    ## Get latest news article and paragraph
    #---------------------------------------------

    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    time.sleep(2)

    #Scape Page
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    grid = soup.find('ul', class_='item_list')
    article = grid.find('li', class_='slide')

    news_title = article.find('div', class_='content_title').text
    news_p = article.find('div', class_='article_teaser_body').text

    #---------------------------------------------
    ## Get featured image from Mars website
    #---------------------------------------------

    # URL of page to be scraped
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(2)

    #Scrape Page
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #open featured image
    browser.click_link_by_partial_text('FULL IMAGE')

    time.sleep(2)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    img_tag = soup.find('img', class_='fancybox-image')
    image_relative_path = img_tag['src']

    #src has relative path only combine with website url
    featured_image_url = 'https://www.jpl.nasa.gov' + image_relative_path
    image_relative_path = soup.find('img', class_='fancybox-image')

    #---------------------------------------------
    ## Get latest weather from Twitter page
    #---------------------------------------------

    # URL of page to be scraped
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)  
    time.sleep(2)

    #Scrape Page
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_weather = soup.find('span', text = re.compile('InSight sol')).text
    mars_weather = mars_weather.replace('InSight s', 'S') 

    #---------------------------------------------
    ## Get Mars fact from planets fact Website
    #---------------------------------------------

    # URL of page to be scraped
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    time.sleep(2)

    #scrape page using pandas
    html = browser.html
    table = pd.read_html(html)
    table_df = pd.DataFrame(table[0])
    mars_fact_table = table_df.to_html()

    #---------------------------------------------
    ## Get Hemisphere images
    #---------------------------------------------

    # URL of page to be scraped
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(2)

    #Scrape Page
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    hemisphere_image_urls = []
    hemispheres = []
    count = 0

    results = soup.find_all('a', class_='itemLink product-item')

    #from main page get the hemisphere names only
    for result in results:
        try:
            hemisphere_name = result.find('h3').text
            hemispheres.append(hemisphere_name)

        except:
            count += 1
            
    #cylcle through each hemisphere page and save image url
    for hemisphere in hemispheres:
        
        hemisphere_info = {}
        
        #go into page of hemisphere
        browser.click_link_by_partial_text(hemisphere)
        time.sleep(2)
        
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        
        #scrape relative path from src
        img_relative_path = soup.find('img', class_="wide-image")['src']
        
        #combine relative path of image to get full url
        img_url = 'https://astrogeology.usgs.gov' + img_relative_path
        
        #add information to dictionary and main list
        hemisphere_info['title'] = hemisphere
        hemisphere_info['img_url'] = img_url
        
        hemisphere_image_urls.append(hemisphere_info)
        
        #go back to main page
        browser.back()

    #---------------------------------------------
    ##Put all collected data in a dictionary
    #---------------------------------------------

    data_entry = {}

    data_entry['news_title'] = news_title
    data_entry['news_p'] = news_p
    data_entry['featured_image'] = featured_image_url
    data_entry['mars_weather'] = mars_weather
    data_entry['mars_fact_table'] = mars_fact_table

    return data_entry
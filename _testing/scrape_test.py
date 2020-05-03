# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist

import re
import pandas as pd
import time

executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)

#----------------------------------------------------------------------------------------------------#
## SECTION 1

# URL of page to be scraped
url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
browser.visit(url)

time.sleep(2)

#Scape Page
html = browser.html
soup = BeautifulSoup(html, 'html.parser')

try:
    grid = soup.find('ul', class_='item_list')
    article = grid.find('li', class_='slide')

    news_title = article.find('div', class_='content_title').text
    news_p = article.find('div', class_='article_teaser_body').text
except:
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    grid = soup.find('ul', class_='item_list')
    article = grid.find('li', class_='slide')

    news_title = article.find('div', class_='content_title').text
    news_p = article.find('div', class_='article_teaser_body').text

print('Section 1 Scrapping Complete!')

#print(news_title)
#print(news_p)

#----------------------------------------------------------------------------------------------------#
#SECTION 2
# URL of page to be scraped
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)

time.sleep(2)

#Scrape Page
html = browser.html
soup = BeautifulSoup(html, 'html.parser')

browser.click_link_by_partial_text('FULL IMAGE')

html = browser.html
soup = BeautifulSoup(html, 'html.parser')

img_tag = soup.find('img', class_='fancybox-image')

try:
    image_relative_path = img_tag['src']
except:
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    img_tag = soup.find('img', class_='fancybox-image')
    image_relative_path = img_tag['src']

featured_image_url = 'https://www.jpl.nasa.gov' + image_relative_path

print('Section 2 Scrapping Complete!')

#image_relative_path
#featured_image_url

#SECTION 3

# URL of page to be scraped
url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(url)

time.sleep(2)

#Scrape Page
html = browser.html
soup = BeautifulSoup(html, 'html.parser')

try:
    mars_weather = soup.find('span', text = re.compile('InSight sol')).text
except:
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    mars_weather = soup.find('span', text = re.compile('InSight sol')).text
    
mars_weather = mars_weather.replace('InSight s', 'S') 

print('Section 3 Scrapping Complete!')
#mars_weather

##SECTION 4

# URL of page to be scraped
url = 'https://space-facts.com/mars/'
browser.visit(url)

time.sleep(2)

#Scrape Page
html = browser.html
soup = BeautifulSoup(html, 'html.parser')

mars_fact_table = soup.find('table', class_="tablepress tablepress-id-p-mars")

mars_fact_table = pd.read_html(str(mars_fact_table)) #[0]

print('Section 4 Scrapping Complete!')

#mars_fact_table

#----------------------------------------------------------------------------------------------------#
#SECTION 5

# URL of page to be scraped
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)

time.sleep(2)

#Scrape Page
html = browser.html
soup = BeautifulSoup(html, 'html.parser')

#soup.find_all('a', class_='itemLink product-item')

hemisphere_image_urls = []
hemispheres = []
count = 0

results = soup.find_all('a', class_='itemLink product-item')

for result in results:
    try:
        hemisphere_name = result.find('h3').text
        hemispheres.append(hemisphere_name)

    except:
        count += 1
        
#hemispheres

for hemisphere in hemispheres:
    
    hemisphere_info = {}
    
    #go into page of hemisphere
    browser.click_link_by_partial_text(hemisphere)
    
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    #scrape relative path from src
    img_ralative_path = soup.find('img', class_="wide-image")['src']
    
    #combine relative path of image to get full url
    img_url = 'https://astrogeology.usgs.gov' + img_ralative_path
    
    #add information to dictionary and main list
    hemisphere_info['title'] = hemisphere
    hemisphere_info['img_url'] = img_url
    
    hemisphere_image_urls.append(hemisphere_info)
    
    #go back to main page
    browser.back()
    
print('Section 5 Scrapping Complete!')
#hemisphere_image_urls

#----------------------------------------------------------------------------------------------------#
#COMBINE EVERYTHING
data_entry = {}

data_entry['news_title'] = news_title
data_entry['news_p'] = news_p
data_entry['featured_image'] = featured_image_url
data_entry['mars_weather'] = mars_weather
data_entry['mars_fact_table'] = mars_fact_table
data_entry['hemisphere_image_urls'] = hemisphere_image_urls

print('Data Entry Completed!')
#data_entry
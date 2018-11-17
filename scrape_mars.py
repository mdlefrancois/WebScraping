# Dependencies
# Beautiful Soup
from bs4 import BeautifulSoup as bs
# Splinter web browser opener
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
#from selenium import webdriver

# Standard dependencies
import os
import pandas as pd
import time
import requests

# Define scrape function
def scrape():
    # Create a dictionary that holds all the Mars Data
    mars_data = {}

    # Splinter for Windows.  Will open and run Google Chrose
    executable_path = {'executable_path': 'C:\BIN\chromedriver.exe'}

    #To use splinter a browser instance needs to be created
    browser = Browser('chrome', **executable_path, headless=False) #headless means no GUI

    # tutorial from splinter
    # https://splinter.readthedocs.io/en/latest/tutorial.html

    #Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. 
    #Assign the text to variables that you can reference later.
    url = "https://mars.nasa.gov/news/"
    browser.visit(url) #uses splinter

    #using beautiful soup to write it into html
    #assign html content
    html = browser.html
    soup = bs(html,"html.parser")

    news_title = soup.find("div", class_="content_title").text
    news_paragraph = soup.find("div", class_="article_teaser_body").text
    #print(f"Title: {news_title}")
    #print(f"Para: {news_paragraph}")
    
    # Add the news title and summary to the dictionary
    mars_data["news_title"] = news_title
    mars_data["news_paragraph"] = news_paragraph

    # Visit Mars Space Images through splinter module
    image_url_featured = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url_featured)# Visit Mars Space Images through splinter module

    # HTML Object 
    html_image = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html_image, 'html.parser')

    # Retrieve background-image url from style tag 
    featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

    # Website Url 
    main_url = 'https://www.jpl.nasa.gov'

    # Concatenate website url with scrapped route
    featured_image_url = main_url + featured_image_url

    # Display full link to featured image
    featured_image_url 

    # Dictionary entry from FEATURED IMAGE
    mars_data['featured_image_url'] = featured_image_url
    

    #Visit the Mars Weather twitter account and scrape the latest Mars weather tweet.
    #Save the tweet text for the weather report as a variable called mars_weather.
    url_weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_weather)

    html_weather = browser.html
    soup = bs(html_weather, "html.parser")
    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    print(mars_weather)
    mars_data["mars_weather"] = mars_weather

    #Visit the Mars Facts webpage and use Pandas to scrape the table containing facts about the planet including 
    #Diameter, Mass, etc. Use Pandas to convert the data to a HTML table string.
    url_facts = "https://space-facts.com/mars/"

    #Read HTML tables into a list of DataFrame objects.
    MarsFacts = pd.read_html(url_facts)

    #pull the first entry in the list
    df_mars_facts = MarsFacts[0]
    df_mars_facts.columns = ["Description", "Values"]
    mars_table = df_mars_facts.set_index(["Description"])

    # Convert the pd df to HTML table and clean up. 
    mars_html_table = mars_table.to_html(classes='marsdata')
    mars_table = mars_html_table.replace('\n', ' ')

    # Add the Mars facts table to the dictionary
    mars_data["mars_table"] = mars_table

    # Visit hemispheres website through splinter module 
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)

    # HTML Object
    html_hemispheres = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html_hemispheres, 'html.parser')

    # Retreive all items that contain mars hemispheres information
    items = soup.find_all('div', class_='item')

    # Create empty list for hemisphere urls 
    hemispheres = []

    # Store the main_ul 
    hemispheres_main_url = 'https://astrogeology.usgs.gov' 

    # Loop through the items previously stored
    for i in items:
        # Store title
        title = i.find('h3').text
            
        # Store link that leads to full image website
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
            
        # Visit the link that contains the full image website 
        browser.visit(hemispheres_main_url + partial_img_url)
            
        # HTML Object of individual hemisphere information website 
        partial_img_html = browser.html
            
        # Parse HTML with Beautiful Soup for every individual hemisphere information website 
        soup = bs(partial_img_html, 'html.parser')
            
        # Retrieve full image source 
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
            
        # Append the retreived information into a list of dictionaries 
        hemispheres.append({"title" : title, "img_url" : img_url})
        
    mars_data["hemispheres"] = hemispheres
    
    # Return Library
    return mars_data

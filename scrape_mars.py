from bs4 import BeautifulSoup as bs
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from splinter import Browser
import time
import pandas as pd

def scrape():


    executable_path = {"executable_path":"chromedriver.exe"}
    browser_news = Browser("chrome",**executable_path,headless = False)

    url_latest_news = "https://mars.nasa.gov/news/"

    browser_news.visit(url_latest_news)


    soup_news = bs(browser_news.html,"html.parser")

    news_title = soup_news.find("div",class_ = "content_title").find("a").text
    news_p = soup_news.find("div",class_= "article_teaser_body" ).text
    

    browser_news.quit()


    browser_featured_image = Browser("chrome",**executable_path,headless = False)

    browser_featured_image.visit("https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars")

    time.sleep(1)

    soup_featured_image = bs(browser_featured_image.html,'html.parser')

    featured_image_url_string = soup_featured_image.find('article',class_="carousel_item")['style']

    featured_image_url = "https://www.jpl.nasa.gov"+featured_image_url_string[23:].replace(");","").replace("'","").strip()

    

    browser_featured_image.quit()

    


    browser_weather = Browser("chrome",**executable_path,headless = False)

    browser_weather.visit("https://twitter.com/marswxreport?lang=en")

    time.sleep(1)

    soup_tweet = bs(browser_weather.html,"html.parser")

    mars_weather=soup_tweet.find('div',class_ = "js-tweet-text-container").find("p").text

    
    browser_weather.quit()



    table = pd.read_html('https://space-facts.com/mars/')
    
    table[1].columns = ['Profile','Value']

    table_html = table[1].to_html(index = False).replace('\n',"")
    


    hemisphere_image_urls = []

    browser1 = Browser("chrome",**executable_path,headless = False)

    browser1.visit("https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced")

    time.sleep(1)

    soup1 = bs(browser1.html,'html.parser')

    title1 = soup1.find("h2",class_="title").text
    img1_url = "https://astrogeology.usgs.gov"+soup1.find('img',class_="wide-image")['src']

    browser1.quit()


    browser2 = Browser("chrome",**executable_path,headless = False)

    browser2.visit("https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced")

    time.sleep(1)

    soup2 = bs(browser2.html,'html.parser')

    title2 = soup2.find("h2",class_="title").text
    img2_url = "https://astrogeology.usgs.gov"+soup2.find('img',class_="wide-image")['src']

    browser2.quit()


    browser3 = Browser("chrome",**executable_path,headless = False)

    browser3.visit("https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced")

    time.sleep(1)

    soup3 = bs(browser3.html,'html.parser')

    title3 = soup3.find("h2",class_="title").text
    img3_url = "https://astrogeology.usgs.gov"+soup3.find('img',class_="wide-image")['src']

    browser3.quit()


    browser4 = Browser("chrome",**executable_path,headless = False)

    browser4.visit("https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced")

    time.sleep(1)

    soup4 = bs(browser4.html,'html.parser')

    title4 = soup4.find("h2",class_="title").text
    img4_url = "https://astrogeology.usgs.gov"+soup4.find('img',class_="wide-image")['src']

    browser4.quit()


    hemisphere_image_urls.append({"title":title1,"img_url":img1_url})
    hemisphere_image_urls.append({"title":title2,"img_url":img2_url})
    hemisphere_image_urls.append({"title":title3,"img_url":img3_url})
    hemisphere_image_urls.append({"title":title4,"img_url":img4_url})


    mars_scraped = {}

    mars_scraped['latest_news_title'] = news_title
    mars_scraped['latest_news_paragraph'] = news_p

    mars_scraped['featured_image_url'] = featured_image_url

    mars_scraped['mars_weather']=mars_weather

    mars_scraped['facts']=table_html

    mars_scraped['hemisphere_image_urls']=hemisphere_image_urls

    return mars_scraped




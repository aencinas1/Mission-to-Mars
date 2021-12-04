#import splinter and bs
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    #initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    #run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemispheres(browser)
    }

    #stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):
    #visit mars nasa news site
    url = 'http://redplanetscience.com'
    browser.visit(url)

    #optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    #convert html to soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')

    #add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        slide_elem.find('div', class_='content_title')
        #use parent element to find the first 'a' tag and save it as 'news_title
        news_title = slide_elem.find('div', class_='content_title').get_text()
        #use the parent element to tfind the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None

    return news_title, news_p

# ## JPL Space Images Featured Images

def featured_image(browser):
    #visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    #find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    #parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    #add try/except for error handling
    try:
        #find the relative image url
        img_url_rel = img_soup.find('img', class_='headerimage fade-in').get('src')
    
    except AttributeError:
        return None

    #use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url

# ## Mars Facts
def mars_facts():
    #add try/except for error handling
    try:
        #use 'read_html' to scrape the facts table into a df
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    return df.to_html()

# ## Mars Hemispheres
def mars_hemispheres(browser):
    # 1. Use browser to visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    #parse
    hemisphere_html = browser.html
    hemisphere_soup = soup(hemisphere_html, 'html.parser')
    #retrieve class=items for the 4 hemis
    items = hemisphere_soup.find_all('div', class_='item')
    for x in items:
        #create dictionary
        hemispheres = {}
        #find titles for list of dictionaries, which is h3, and get it as text
        title = x.find('h3').text
        #find url to access full size image, need anchor and href to hemi page
        url_img = x.find('a', class_='itemLink product-item')['href']
        #get absolute link and visit
        url_hemi = f'https://astrogeology.usgs.gov/{url_img}'
        browser.visit(url_hemi)
        #parse the data again to get jpg doing same thing
        jpg_html = browser.html
        jpg_soup = soup(jpg_html, 'html.parser')
        jpg_image = jpg_soup.find('div', class_='downloads')
        img_url = jpg_image.find('a')['href']
            
        print(title)
        print(img_url)
    
        #add hemispheres to our master hemisphere_image_urls list
        hemispheres = {
            'title': title,
            'img_url': img_url}
        hemisphere_image_urls.append(hemispheres)


    # 4. Print the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls

if __name__ == "__main__":
    #if running as script, print scraped data
    print(scrape_all())
#import splinter and bs
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

#visit mars nasa news site
url = 'http://redplanetscience.com'
browser.visit(url)
#optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')

#use parent element to find the first 'a' tag and save it as 'news_title
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

#use the parent element to tfind the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

#visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

#find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

#parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

#find the relative image url
img_url_rel = img_soup.find('img', class_='headerimage fade-in').get('src')
img_url_rel

#use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

df.to_html()


# D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

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
hemisphere_image_urls


# 5. Quit the browser
browser.quit()
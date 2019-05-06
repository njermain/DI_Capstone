# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 19:28:11 2019

@author: w10007346
"""

################# get zpids of recently sold houses ######################

from bs4 import BeautifulSoup
import requests

req_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

# get list of zpids associated with the sold query
from random import normalvariate
import time


zpid_list = []
links_list = []


for i in range(2,41):
# go through each page 'current page' and get all the html code
    page =str(i)
    
    with requests.Session() as s:
        
        url = 'https://www.zillow.com/homes/?searchQueryState={%22mapBounds%22:{%22west%22:-129.78612228878262,%22east%22:-40.07811447628262,%22south%22:24.5037236218885,%22north%22:49.406187042558564},%22isMapVisible%22:true,%22mapZoom%22:4,%22pagination%22:{%22currentPage%22:'+page+'},%22filterState%22:{%22doz%22:{%22value%22:%227%22},%22isForSaleByAgent%22:{%22value%22:false},%22isForSaleByOwner%22:{%22value%22:false},%22isNewConstruction%22:{%22value%22:false},%22isForSaleForeclosure%22:{%22value%22:false},%22isComingSoon%22:{%22value%22:false},%22isPreMarketForeclosure%22:{%22value%22:false},%22isPreMarketPreForeclosure%22:{%22value%22:false},%22isMakeMeMove%22:{%22value%22:false},%22isRecentlySold%22:{%22value%22:true},%22isCondo%22:{%22value%22:false},%22isMultiFamily%22:{%22value%22:false},%22isManufactured%22:{%22value%22:false},%22isLotLand%22:{%22value%22:false},%22isTownhouse%22:{%22value%22:false}},%22isListVisible%22:true}'
        r = s.get(url, headers=req_headers)
    soup = BeautifulSoup(r.content, 'html.parser')  

# find all the links
    hrefs = []
    a_tags = soup.findAll('a', {'class':"zsg-photo-card-overlay-link routable hdp-link routable mask hdp-link"})
    for i in range(0,len(a_tags)):
        try:
            hrefs.append(a_tags[i]['href'])
        except:
            pass
#    links = []
#    for link in soup.findAll('a'), {'class': 'list-card-link'}):
#        if link['aria-label'].split(',',2)[0]=='Sold':
#           links.append(link.get('href',""))
#            
# store links
    links_list = links_list+hrefs
 
# split links to get the zpid
    parts = [j.split('/',4)[-2] for j in hrefs]
    zpid = [y.split('_',2)[0] for y in parts]
    zpid_list = zpid_list+zpid
    time.sleep(normalvariate(3,.8))


# write zpids to a csv
import pandas as pd
import os
os.chdir('C:/Users/Nathaniel/Dropbox/DI Capstone')

len(links_list)
len(zpid_list)
df = pd.DataFrame(links_list, columns = ["detes_link"])
df['zpid'] = zpid_list
df.to_csv('zpi_detes_37.csv',index=False)
len(df['zpid'].unique())
links_list[0]
len(df)
############## Get sold prices and zestimates from recently sold #################

# combine all data frames of links 
import os
import numpy as np
os.chdir('C:/Users/Nathaniel/Dropbox/DI Capstone')

uniquelinks=[]
# read saved links and zpids
for i in range(27,38):
    string = str(i)
    links_dat = pd.read_csv('zpi_detes_'+string+'.csv')

# concatonate multiple zpid_dete files to one list

    uniquelinks.append(links_dat['detes_link'].unique())

# convert to data frame and filter for unique links
   
link_array_list = np.concatenate(uniquelinks).ravel().tolist()
link_df = pd.DataFrame(link_array_list, columns = ['links'])
unique_links = pd.DataFrame(link_df['links'].unique(), columns = ['detes_link'])

# get zpid from links
parts = [j.split('/',7)[-2] for j in link_array_list]
zpid = [y.split('_',2)[0] for y in parts]

# unique lists function
def f4(seq): 
   # order preserving
   noDupes = []
   [noDupes.append(i) for i in seq if not noDupes.count(i)]
   return noDupes
# add zpids to dataframe
unique_links['zpid'] = f4(zpid)
    


# add zillow.com tag to hrefs
unique_links['detes_link'] = 'https://www.zillow.com'+unique_links['detes_link']

    # save dataframe
unique_links.to_csv('unique_links_list_3.csv', index=False)


# webscrape pages associated with web details page from unique_lists_link
from bs4 import BeautifulSoup
import requests

req_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

import pandas as pd

import time
from random import normalvariate


# input zpid and home details link, get zpid, zest, and sold price
# empty data frame for output
prices_df= pd.DataFrame(columns = ['zpid','Price', 'Zest', 'img'])

# read in dataframe with links and zpids
api_dat = pd.read_csv('unique_links_list_3.csv')
api_dat.columns.values

for i in range(791,len(api_dat['detes_link'])):
# get html code for each selected house
    with requests.Session() as s:
        url = api_dat['detes_link'][i]
        r = s.get(url, headers=req_headers)
        soup = BeautifulSoup(r.content, 'html.parser')  
# get sold price
    if soup.findAll('div', {'class': 'status'})!=[]:
        if soup.find('div', {'class': 'status'}).text[:6] == ' Sold:':
            sold_text = soup.find('div', {'class': 'status'}).text
            price = sold_text.split(': $',2)[1]
        else: price = 0
    else: 
        price = 0 

# get zestimate
    if soup.findAll('div', {'class': 'zestimate primary-quote'})!=[]:
        zestimate_text = soup.find('div', {'class': 'zestimate primary-quote'}).text
        zest = zestimate_text.split(': $',2)[1]
        zpid = str(api_dat['zpid'][i])
    else: 
        zest = 0
        zpid = 0
        
    
# get photo link
    if soup.findAll('img', {'class': 'photo-tile-image'})!=[]:
        img = soup.findAll('img', {'class': 'photo-tile-image'})[0]['src']
    else:
        img = 0
    
# info scraped to a row and add to data frame
    df_row = pd.Series([zpid,price,zest,img], index =['zpid','Price', 'Zest', 'img'], name=zpid)
    prices_df=pd.concat([prices_df,df_row.to_frame().T])
# sleep so I dont get locked up
    time.sleep(normalvariate(3,.8))



# save output
prices_df.to_csv('Scraped_Prices_10.csv')


##### clean output 
comp_cases = prices_df.replace(0, np.nan).dropna()
comp_cases.to_csv('comp_cases_10.csv')
len(comp_cases)
############### Download Images ############## 


# take link from API R csv, save image to folder labeled by zpid
import urllib.request

API_df = pd.read_csv('comp_cases_10.csv')

os.chdir('C:/Users/Nathaniel/Dropbox/DI Capstone/House_Images')



for i in range(0,len(API_df['zpid'])):
    urllib.request.urlretrieve(API_df['img'][i], str(API_df['zpid'][i])+'.jpg')
    time.sleep(normalvariate(3,.8))


















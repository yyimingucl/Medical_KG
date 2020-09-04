# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 03:08:22 2020

@author: yyimi

acquire navigation bar from "www.jiankangle.com"
"""


import requests
from bs4 import BeautifulSoup
import re

#%% 
#acquire the html content
def downloadPage(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }
    data = requests.get(url, headers=headers).content
    return data
#%%

#parse html content
def parse_html(html):
    
    # chinese pattern
    pattern=u"[^\u4e00-\u9fff]" 
    regex = re.compile(pattern)
    
    # convert html content into tree layout
    soup = BeautifulSoup(html,"html.parser") 
    item_attribute = {}
    
    # parent-level navigation 
    detail_parents = soup.find('div', attrs = {'class' : 'fl first_type'})
    
    #store the navigation information
    if detail_parents != None:
        for bar in detail_parents.find_all('a'):  
            # obtain the corresponding ID between parent dict and sub dict
            ids = int(bar.get_attribute_list('data-tid')[0])     
            # obtain text information
            name = bar.getText()          
            # sub-level navigation
            detail = soup.find('div', attrs = {'id' : 'type_{num}'.format(num=ids)})
            sublevel_detail = detail.findChildren('div',
                                                  attrs = {'class':'clearfix'})
            
            for info in sublevel_detail:
                title = info.find_all('span')[0]
                title = regex.sub('',title.getText())
                
                
                for item in info.find_all('a'):
                    item = item.getText()    
                    item_attribute[item] = [name,title]
                    
                    
    return item_attribute
    
#%%
def Navigation(url):
    handle = parse_html(downloadPage(url))
    return handle
    
            

    

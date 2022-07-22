#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 20:52:18 2022

@author: xietianci
"""

from selenium import webdriver
import pandas as pd

driver_path = "/Users/xietianci/Downloads/chromedriver-2"
browser = webdriver.Chrome(executable_path=driver_path)
browser.get('https://webb-site.com/dbpub/SFClicount.asp')
browser.maximize_window()

table = browser.find_element_by_xpath('/html/body/div[4]/table/tbody')
text = table.text
text = text.split('\n')
num = int(text[-1].split(' Average ')[0])

links = []
name_of_firms = []
for i in range(2,num+2):
        item = browser.find_element_by_xpath('/html/body/div[4]/table/tbody/tr[{}]/td[2]/a'
                                             .format(i))
        lk = item.get_property('href')
        nm = item.text
        links.append(lk)
        name_of_firms.append(nm)

individual_links = []
for link in links:
    browser.get(link)
    clc = browser.find_element_by_xpath('/html/body/div[4]/ul[3]/li[2]/a')
    clc.click()
    table = browser.find_element_by_xpath('/html/body/div[4]/table/tbody')
    text = table.text
    text = text.split('\n')[2:]
    num = len(text)
    for i in range(2,num+2):
        try:
            item = browser.find_element_by_xpath('/html/body/div[4]/table/tbody/tr[{}]/td[2]/a'
                                                 .format(i))
            lk = item.get_property('href')
            individual_links.append(lk)
        except:
            pass

il = set(individual_links)
iil = [i for i in il]
data = []
for link in iil:
    browser.get(link)
    orgnization = 0
    try:
        table = browser.find_element_by_xpath('/html/body/div[4]/table/tbody').text
    except:
        continue
    text = table.split('\n')[1:]
    num = len(text)
    name = browser.find_element_by_xpath('/html/body/div[4]/h2').text
    for i in range (2,num+2):
        fm = 0
        un = 0
        try:
            orgnization = browser.find_element_by_xpath('/html/body/div[4]/table/tbody/tr[{}]/td[2]/a'.format(i)).text
        except:
            pass
        try:
            role = browser.find_element_by_xpath('/html/body/div[4]/table/tbody/tr[{}]/td[3]'.format(i)).text
        except:
            pass
        try:   
            activity = browser.find_element_by_xpath('/html/body/div[4]/table/tbody/tr[{}]/td[4]'.format(i)).text
        except:
            pass
        try:
            fm = browser.find_element_by_xpath('/html/body/div[4]/table/tbody/tr[{}]/td[5]'.format(i)).text
        except:
            pass
        try:
            un = browser.find_element_by_xpath('/html/body/div[4]/table/tbody/tr[{}]/td[6]'.format(i)).text
        except:
            pass
        data.append([name,orgnization,role,activity,fm,un])
            
        
df1 = pd.DataFrame(data,columns=['name','orgnization','role','activity','from','until'])
df1.to_csv('/Users/xietianci/Downloads/webb.csv')

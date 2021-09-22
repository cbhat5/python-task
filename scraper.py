from bs4 import BeautifulSoup
#import urllib.request #, urllib.parse, urllib.error
import requests
import os
from urllib.request import urlretrieve


baseurl = "https://www.eia.gov/dnav/pet"
sideurl = "/pet_pnp_inpt_a_epc0_yir_mbbl_m.htm"
headers = {"User-Agent" : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}
page = requests.get(baseurl+sideurl)
soup = BeautifulSoup(page.content, 'lxml')
title = soup.find_all('div')
for item in title:
    for link in item.find_all('a', href = True):
        if any(link['href'].endswith(x) for x in ['.csv','.xls','.xlsx']):
            href = baseurl + link['href'][1:]
            
            filename = os.path.join(".", href.rsplit('/', 1)[-1])
            href = href.replace('http://','https://')
            urlretrieve(href, filename)
            

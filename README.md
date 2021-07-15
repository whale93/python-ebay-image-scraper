# Ebay Image Scraper
![](https://img.shields.io/badge/Python-3.8.1-blue) ![](https://img.shields.io/badge/ebaysdk%20python-2.2.0-green)


A simple implementation of the [python ebaysdk](https://github.com/timotheus/ebaysdk-python) to scrape product images from Ebay.

## Prerequisites

[python ebaysdk](https://github.com/timotheus/ebaysdk-python)
```sh
pip install ebaysdk
```


## Usage 

Replace with your own [Ebay developer](https://developer.ebay.com/) keys.
```sh
CLIENT_ID = 'ENTER_YOUR_APPID_HERE'
CLIENT_SECRET = 'ENTER_YOUR_CERTID_HERE'
DEV_ID = 'ENTER_YOUR_DEVID_HERE'
EBAY_AUTHNAUTH = 'ENTER_YOUR_AUTH_N_AUTH_TOKEN_HERE'
```
<br />

Replace with search terms.
```sh
KEYWORDS_LIST = ['iphone 4', 'samsung galaxy s4', 'thisdoesnotexist']
```
<br />


Change the *entriesPerPage* to the maximum number of products you want to retrieve.
```sh
def scrape_productIDs(keywords):
    request = {
        'keywords': keywords,
        'paginationInput': {
           'entriesPerPage': 20 #Maximum number of results to fetch
        },
    }
```

This program utilises the following functions for a total of **7500** API calls per day:
- [*getItem*](https://developer.ebay.com/api-docs/buy/browse/resources/item/methods/getItem?mkevt=1&mkcid=1&mkrid=711-53200-19255-0&campid=5337590774&customid=&toolid=10001) function from **Browse** API (5,000 calls per day)
- [*GetSingleItem*](https://developer.ebay.com/devzone/shopping/docs/CallRef/GetSingleItem.html?mkevt=1&mkcid=1&mkrid=711-53200-19255-0&campid=5337590774&customid=&toolid=10001) function from **Shopping** API (2,500 calls per day)

If you are scraping many images, set `PACE = True`.
This will space out the API calls by 11.53 seconds, resulting in about 7493 API calls every 24hrs

```sh
#Pace api calls?
PACE = False
```



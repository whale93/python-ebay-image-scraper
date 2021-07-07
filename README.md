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
client_id = 'ENTER_YOUR_APPID_HERE'
client_secret = 'ENTER_YOUR_CERTID_HERE'
```
<br />

Replace with search terms.
```sh
keywords_list = ['iphone 4', 'samsung galaxy s4', '734tyrhufe79t4uahgr']
```
<br />


Change the *entriesPerPage* to the maximum number of products you want to retrieve.
```sh
request = {
    'keywords': keywords,
    'paginationInput': {
       'entriesPerPage': 20
    },
}
```

If you are downloading many images and may exceed Ebays 5000 calls a day limit, uncomment the following code in *find_products()*. This forces the program to make 1 browsing API call every 17 seconds. Consider implementing a rotating proxy as well or Ebay may temporarily block you IP.
```sh
#start_time = perf_counter()
.
.
.
'''
end_time = perf_counter()
if end_time - start_time < 17:
	sleep(17-(end_time - start_time)) 
'''
```



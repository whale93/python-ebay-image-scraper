#Imports
import os, requests
from ebaysdk.finding import Connection as Finding
from ebaysdk.trading import Connection as Trading
from ebaysdk.shopping import Connection as Shopping
from time import sleep
from datetime import datetime
from time import perf_counter


#Keywords
KEYWORDS_LIST = ['iphone 4', 'samsung galaxy s4', 'thisdoesnotexist']


#Paths
WRITE_PATH = os.path.join(os.getcwd(), "EIS_downloads")

#Pace api calls?
PACE = False

#Configs
 #Ebay developer keys
CLIENT_ID = 'ENTER_YOUR_APPID_HERE'
CLIENT_SECRET = 'ENTER_YOUR_CERTID_HERE'
DEV_ID = 'ENTER_YOUR_DEVID_HERE'
EBAY_AUTHNAUTH = 'ENTER_YOUR_AUTH_N_AUTH_TOKEN_HERE'


 #Ebay API
ebaysdkapi_finding = Finding(config_file=None, appid=CLIENT_ID,certid=CLIENT_SECRET,debug=False, siteid="EBAY-US")
ebaysdkapi_trading = Trading(config_file=None, appid=CLIENT_ID, certid=CLIENT_SECRET, devid=DEV_ID, token=EBAY_AUTHNAUTH, debug=False)
ebaysdkapi_shopping = Shopping(config_file=None, appid=CLIENT_ID,certid=CLIENT_SECRET,debug=False)


#Global variables
keyword_errors_list =[]


#Error codes
 #No internet
connection_error = "<class 'requests.exceptions.ConnectionError'>"
 #No results
keyword_error = "<class 'AttributeError'>"
 #No such product id
productID_error = "<class 'ebaysdk.exception.ConnectionError'>"
 #No picture url
pictureURL_error = "<class 'KeyError'>"
 #Hit maximum api usage for trading api
apilimit_error = "'GetItem: Class: RequestError, Severity: Error, Code: 518, Call usage limit has been reached. Your application has exceeded usage limit on this call, please make call to GetAPIAccessRules to check your call usage.'"



#Definitions
 #Get current date time
def currentdatetime():
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M:%S")

def download_images(url, num, WRITE_PATH):
    while True:
        try:
            r = requests.get(url)
            with open(os.path.join(WRITE_PATH, os.path.basename(WRITE_PATH)+"("+str(num)+")"+".jpg"), "wb") as f:
                f.write(r.content)
            break

        except Exception as e:
            #Retry if connection error
            if str(type(e)) == connection_error:
                print(currentdatetime(), "ConnectionError...Retrying in 5 minutes...")
                sleep(300)

            #Unexpected error
            else :
                print(f'({currentdatetime()}) FatalError...Stopping Script...\n')
                raise

def find_products(productIDs, keywords, WRITE_PATH):
    imageNo = 0
    try:
        for productID in productIDs:
            print(f'\tPID: {productID.itemId}')

            while True:
                try:
                    start_time = perf_counter()
                    response = ebaysdkapi_trading.execute('GetItem', {'ItemID': productID.itemId, 'DetailLevel': 'ReturnAll'})

                    try:
                        #If only one image
                        if response.dict()['Item']['PictureDetails']['PictureURL'][0] == 'h':
                            download_images(response.dict()['Item']['PictureDetails']['PictureURL'], imageNo, os.path.join(WRITE_PATH, keywords))
                            imageNo+=1
                        elif response.dict()['Item']['PictureDetails']['PictureURL'][0].startswith('https'):
                            for imageurl in response.dict()['Item']['PictureDetails']['PictureURL']:
                                download_images(imageurl, imageNo, os.path.join(WRITE_PATH, keywords))
                                imageNo+=1
                        
                    except Exception as e:
                        #If not pictures found
                        if str(type(e)) == pictureURL_error:
                            print(f'\tNo images found for: {productID.itemId}')


                    if PACE:
                        end_time = perf_counter()
                        if end_time - start_time < 11.53:
                            sleep(11.53-(end_time - start_time)) 
                    
                    break

                except Exception as e:
                    #Retry if lose connection
                    if str(type(e)) == connection_error:
                        print(currentdatetime(), "ConnectionError...Retrying in 5 minutes...")
                        sleep(300)

                    elif str(e) == apilimit_error:
                        response = ebaysdkapi_shopping.execute('GetSingleItem',{'ItemID':productID.itemId})

                        try:
                            #If only one image
                            if response.dict()['Item']['PictureURL'][0] == 'h':
                                download_images(response.dict()['Item']['PictureURL'], imageNo, os.path.join(WRITE_PATH, keywords))
                                imageNo+=1
                            elif response.dict()['Item']['PictureURL'][0].startswith('https'):
                                for imageurl in response.dict()['Item']['PictureURL']:
                                    download_images(imageurl, imageNo, os.path.join(WRITE_PATH, keywords))
                                    imageNo+=1

                        except Exception as e:
                            #If not pictures found
                            if str(type(e)) == pictureURL_error:
                                print(f'\tNo images found for: {productID.itemId}')

                        if PACE:
                            end_time = perf_counter()
                            if end_time - start_time < 11.53:
                                sleep(11.53-(end_time - start_time)) 

                        break

                    #If product id not found
                    elif str(type(e)) == productID_error:
                        print(f'\tCould not find PID: {productID.itemId}')
                        break

                    else :
                        print(f'({currentdatetime()}) FatalError...Stopping Script...\n')
                        raise

    except Exception as e:
        print(f'({currentdatetime()}) FatalError...Stopping Script...\n')
        raise

#Search ebay and return the results
def scrape_productIDs(keywords):
    request = {
        'keywords': keywords,
        'paginationInput': {
           'entriesPerPage': 20 #Maximum number of results to fetch
        },
    }

    
    while True:
        try:
            response = ebaysdkapi_finding.execute('findItemsByKeywords', request)
            return response.reply.searchResult.item

        except Exception as e:
            #Retry if connection error
            if str(type(e)) == connection_error:
                print(f'({currentdatetime()}) ConnectionError...Retrying in 5 minutes...')
                sleep(300)

            #No results found
            elif str(type(e)) == keyword_error:
                print(f'\tNo results found for "{keywords}"')
                global keyword_errors_list
                keyword_errors_list.append(keywords)
                return False

            #Unexpected error
            else :
                print(f'({currentdatetime()}) FatalError...Stopping Script...\n')
                raise


#Main function
def main():
    #Create folder to stored downloaded images
    if os.path.exists(WRITE_PATH) == False:
        os.mkdir(WRITE_PATH)

    #Loop through keywords
    for keywords in KEYWORDS_LIST:
        print(f'({currentdatetime()}) Keywords: "{keywords}"')
        productIDs = scrape_productIDs(keywords)
        #Check if there were valid product ids found
        if productIDs != False:
            #Create folder for each individual keyword
            if os.path.exists(os.path.join(WRITE_PATH, keywords)) == False:
                os.mkdir(os.path.join(WRITE_PATH, keywords))
            find_products(productIDs, keywords, WRITE_PATH)


#Run main function
if __name__ == "__main__":
    main()
    #Save keywords with no results
    if len(keyword_errors_list) > 0:
        with open('keyword_errors_list.txt', 'w') as f:
            for keyword in keyword_errors_list:
                f.write(keyword)
                f.write('\n')
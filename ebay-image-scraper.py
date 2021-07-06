#Imports
import os, requests
from ebaysdk.finding import Connection as Finding
from ebaysdk.shopping import Connection as Shopping
from time import sleep
from datetime import datetime


#Keywords
keywords_list = ['iphone 4', 'samsung galaxy s4', '734tyrhufe79t4uahgr']


#Paths
writepath = os.path.join(os.getcwd(), "EIS_downloads")


#Configs
 #Ebay developer keys
client_id = 'ENTER_YOUR_APPID_HERE'
client_secret = 'ENTER_YOUR_CERTID_HERE'


 #Ebay API
ebaysdkapi_finding = Finding(config_file=None, appid=client_id,certid=client_secret,debug=False, siteid="EBAY-US")
ebaysdkapi_browsing = Shopping(config_file=None, appid=client_id,certid=client_secret,debug=False)


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


#Definitions
 #Get current date time
def currentdatetime():
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M:%S")

def download_images(url, num, writepath):
    while True:
        try:
            r = requests.get(url)
            with open(os.path.join(writepath, os.path.basename(writepath)+"("+str(num)+")"+".jpg"), "wb") as f:
                f.write(r.content)
            break

        except Exception as e:
            #Retry if connection error
            if str(type(e)) == connection_error:
                print(currentdatetime(), "ConnectionError...Retry in 5 minutes...")
                sleep(300)

            #Unexpected error
            else :
                print(f'({currentdatetime()}) FatalError...Stopping Script...\n')
                raise

def find_products(productIDs, keywords, writepath):
    imageNo = 0
    try:
        for productID in productIDs:
            print(f'\tPID: {productID.itemId}')

            while True:
                try:
                    #start_time = perf_counter()
                    response = ebaysdkapi_browsing.execute('GetSingleItem',{'ItemID':productID.itemId})

                    try:
                        for imageurl in response.dict()['Item']['PictureURL']:
                            download_images(imageurl, imageNo, os.path.join(writepath, keywords))
                            imageNo+=1

                        '''
                        end_time = perf_counter()
                        if end_time - start_time < 17:
                            sleep(17-(end_time - start_time)) 
                        '''
                    except Exception as e:
                        #If not pictures found
                        if str(type(e)) == pictureURL_error:
                            print(f'\tNo images found for: {productID.itemId}')
                    
                    break

                except Exception as e:
                    #Retry if lose connection
                    if str(type(e)) == connection_error:
                        print(currentdatetime(), "ConnectionError...Retry in 5 minutes...")
                        sleep(300)

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
           'entriesPerPage': 20
        },
    }

    
    while True:
        try:
            response = ebaysdkapi_finding.execute('findItemsByKeywords', request)
            return response.reply.searchResult.item

        except Exception as e:
            #Retry if connection error
            if str(type(e)) == connection_error:
                print(f'({currentdatetime()}) ConnectionError...Retry in 5 minutes...')
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
    if os.path.exists(writepath) == False:
        os.mkdir(writepath)

    for keywords in keywords_list:
        print(f'({currentdatetime()}) Keywords: "{keywords}"')
        productIDs = scrape_productIDs(keywords)
        if productIDs != False:
            if os.path.exists(os.path.join(writepath, keywords)) == False:
                os.mkdir(os.path.join(writepath, keywords))
            find_products(productIDs, keywords, writepath)


#Run main function
if __name__ == "__main__":
    main()
    #Save keywords with no results
    if len(keyword_errors_list) > 0:
        with open('keyword_errors_list.txt', 'w') as f:
            for keyword in keyword_errors_list:
                f.write(keyword)
                f.write('\n')
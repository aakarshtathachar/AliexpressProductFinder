import requests
import re
from bs4 import BeautifulSoup
import ebayScrape



#searchItems = ['biodegradable+dog+poop+bags']
searchItemsvar = input("List of catagories you are interested in selling ex(dog toys)")
searchItems = searchItemsvar.split(',')
numOfItems = int(input("give a number of starting itms you want to check"))
print(searchItems)
goodProducts = []
for i in searchItems:
    i = i.replace(' ', '+')
    url = "https://www.aliexpress.com/wholesale?SearchText="+i
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    bestsellers = soup.find_all("html")
    codes = str(bestsellers)

    codes = codes.split('{"itemType":"productV3","productType":"natural",')
    count = 0
    count2 =0

    for code in codes:       
        result = ''
        result2 = ''
        starRating = ''
        sales = ''
        
        if('seoTitle' in code):

            priceNum = ''
            salesNum = ''
            starRatingNum = ''
            idNum = ''
            #finds the title
            start = code.find('seoTitle') + len('seoTitle":"')
            end = code.find('","displayTitle"')
            result = code[start:end]
            #print(result)
            #gives the actual price
            if('minPriceType":1,"formattedPrice":"US $' in code):
                result2 = code[code.index('"formattedPrice":"US $')+21:code.index('"formattedPrice":"US $')+27]
                #print(result2)       
            elif('minPriceType":2,"formattedPrice":"US $' in code):
                result2 = code[code.index('"formattedPrice":"US $')+21:code.index('"formattedPrice":"US $')+27]
            #starRating
            if 'starRating' in code:
                newCode = code
                starRating = newCode[newCode.index('"starRating":')+13:newCode.index('"starRating":')+16]
                #print(starRating)
            #number of reviews
            if 'tradeDesc' in code:
                newCode2 = code
                sales = newCode2[newCode2.index('"tradeDesc":')+12:newCode2.index('"tradeDesc":')+20]
                #print(sales)
            #ID
            if('productId' in code):
                ID = code[code.index('"productId":')+12:code.index('"productId":')+37]
                #print(ID)
            #free shipping
        

            
            #if the product page has super deals, then find the mionprice2: formatted price instead
            
            #convert all values to pure numbers
            
            for chr1 in result2:
                if(chr1.isnumeric() or chr1=='.'):
                    priceNum += chr1
            for chr2 in starRating:
                if(chr2.isnumeric() or chr2 =='.'):
                    starRatingNum+=chr2
            for chr3 in sales:
                if(chr3.isnumeric() or chr3 ==','):
                    if(chr3 == ','):
                        chr3 = ''
                    salesNum+=chr3
            for chr4 in ID:
                if(chr4.isnumeric()):
                    idNum += chr4
                    
                    
            if(priceNum == ''):
                priceNum = 0
            if(starRatingNum == ''):
                starRatingNum = 0
            if(salesNum == ''):
                salesNum = 0
            
            
            #print(result)
            
            count2+=1
            if((0< float(priceNum) <80) and (3.9<=float(starRatingNum)) and (599<= int(salesNum))):
               
                print('second works')
                ebayResult = ebayScrape.ebayTest(result)
                if(ebayResult == True):
                    print('third works')
                    goodProducts.append(result)
                    goodProducts.append(idNum)
                    
            else:
                print(result)
                print(idNum)
                if(0<float(priceNum)<80):
                    print('price is good')
                else:
                    print('price is wrong', priceNum)         
                if(0<float(float(starRatingNum)>3.9)):
                    print('starRatingNum is good')
                else:
                    print('starRatingNum is wrong', starRatingNum)     
                if(float(salesNum)>599):
                    print('salesNum is good')
                else:
                    print('salesNum is wrong', salesNum)     
            count+=1

        if(count==numOfItems):
            print()
            print(goodProducts)
            print(count2)
            break

#url = 'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw='+search+'&_sacat=0'
import difflib
from difflib import SequenceMatcher
# Define the eBay search URL
import requests
from bs4 import BeautifulSoup
def ebayTest(string):
    #string  = 'Natural Catnip Cat Wall Stick-on Ball Toy Treats Healthy Natural Removes Hair Balls to Promote Digestion Cat Grass Snack Pet'
    search = string.replace(' ', '+')
    # Define the eBay search URL
    url = 'https://www.ebay.com/sch/i.html?_nkw='+search

    # Send a GET request to the URL and store the response
    response = requests.get(url)

    # Parse the HTML content of the response using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the top 5 item listings on the page
    listings = soup.find_all('div', class_='s-item__wrapper')
    count = 0
    count2 = 0
    # Loop through each item listing and extract the seller's reputation
    for listing in listings:
        # Extract the URL of the item's page
        item_url = listing.find('a', class_='s-item__link').get('href')
    
        # Send a GET request to the item's page and store the response
        item_response = requests.get(item_url)
    
        # Parse the HTML content of the response using BeautifulSoup
        noStrSoup = BeautifulSoup(item_response.content, 'html.parser')
        item_soup = str(noStrSoup)
    
    
        # Find the seller's reputation on the page
        #seller_reputation = item_soup.find('span', class_='mbg-l').find('a').text
        seller_reputation = ''
        title = ''
        #print(item_url)
        if('["PSEUDOLINK"],"accessibilityText":"' in item_soup)and('(feedback score)' in item_soup)and('name="referrer"/><meta content='in item_soup):
            try:
                seller_reputation = item_soup[item_soup.index('["PSEUDOLINK"],"accessibilityText":"')+36:item_soup.index('(feedback score)')]
                title = item_soup[item_soup.index('name="referrer"/><meta content=')+31:item_soup.index('  | eBay')]
                count += 1
            except:
                seller_reputation = ''
                title = ''
                print('')
        # Print the seller's reputation for the item
        str2 = title
        seq = SequenceMatcher(a=search, b=str2)
        strseq = seq.ratio()
        print(seq.ratio())
    
        print('Seller reputation for {}: {}'.format(item_url, seller_reputation)) 
        print(title)
        print(string)
        print()
        if(title != '') and (int(seller_reputation)>=100) and (float(strseq)>=0.29):
            count2 +=1
        if(count>7):
            break
    if(count2>1):
        return True
    else:
        return False

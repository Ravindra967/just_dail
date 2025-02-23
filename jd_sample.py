import requests
from bs4 import BeautifulSoup
import pandas as pd
cols = ['CATEGORY','NAME', 'CONTACT','ADDRESS']

outputfile_path='c://temp//JD_data.xlsx'

def get_dealer_details(city):
    df = pd.DataFrame(columns = cols) #Temporary empty dataframe
    categories = ['PG/Hostels']#'Car-Dealers-Maruti-Suzuki', 'Restaurant', 'Hospital', 'Travel-Agents',
    for category in categories:
       page = 1
       while True:
           url = f"https://www.justdial.com/{city}/{category}/page-{page}"
           headers = {
               "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"
           }
           response = requests.get(url, headers=headers,verify=False)

           if response.status_code == 200:
               soup = BeautifulSoup(response.content, 'html.parser')               
               dealers = soup.find_all('div', {'class': 'resultbox_info'})
               
               if len(dealers) == 0:
                   break

               for dealer in dealers:
                   #print(dealer)
                   name = dealer.find('div', {'class': 'resultbox_imagebox complist_img'})
                   name=name.get("title") if name else 'no'
                   contact = (dealer.find('span', {'class': 'callcontent callNowAnchor'}).text if dealer.find('span', {'class': 'callcontent callNowAnchor'}) else 'Contact not found')
                   address = (dealer.find('div', {'class': 'resultbox_address mt-6'}).text if dealer.find('div', {'class': 'resultbox_address mt-6'}) else 'Address not found')

                   print("Category:", category)
                   print("Name:", name)
                   print("Contact:", contact.strip())
                   print("Address:", address.strip())
                   print("--------")
                   df = df._append({'CATEGORY': category,'NAME':name,'CONTACT':contact,'ADDRESS':address},ignore_index=True)
                   df = df[(~df.NAME.str.match('no')) | (~df.ADDRESS.str.match('Address not found')) | (~df.CONTACT.str.match('Contact not found'))]
                   page += 1
           else:
               print(f"Failed to retrieve data from category {category} and page {page}.")
               break
    df.to_excel(outputfile_path)
# Usage Example:
city = 'Hyderabad'

get_dealer_details(city)
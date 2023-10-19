from bs4 import BeautifulSoup
import requests
import pandas as pd
from country_dict import countries
from demonyms import demonyms
import re


c_list = list(countries.keys())

for ctry in c_list:

    n_ctry = re.sub(' ','_',ctry)
    dm = demonyms[ctry]

    if ctry == 'Luxembourg':
        resp = requests.get(f"https://en.wikipedia.org/wiki/Visa_requirements_for_citizens_of_Luxembourg")
    else:
        resp = requests.get(f"https://en.wikipedia.org/wiki/Visa_requirements_for_{dm}_citizens")

    shitty_countries = ["Azerbaijan","Belarus","Canada","China","Cuba","Estonia","Eswatini","Ethiopia","Gambia","Iran","North Korea","Lithuania","Mongolia","Nepal","Qatar","Serbia","Syria","Turkmenistan","Tajikistan","Yemen"]
    super_shitty_countries = ["Domnican Republic","Venezuela","Croatia","Singapore"]
    
    bs = BeautifulSoup(resp.content)

    a  = bs.find_all('table')
    if "Parts of this article" in a[0].text:
        table = a[1]
    elif ctry in shitty_countries:
        table = a[1]
    elif ctry in super_shitty_countries:
        table = a[2]
    elif "Wikipedia does not have an article with this exact name" in a[0].text:
        print(ctry)
        continue
    else:
        table = a[0]

    rows = table.find_all('tr')
    for row in rows:
        try:
            table_row = row.find_all('td')

            if not table_row:
                continue
            else:
                country_row = table_row[0]
                destination = country_row.find_all('a')[0].contents[0]

                if re.findall("(Visa required)|(Travel restricted)|(Admission refused)|(Special permit required)|(Particular visit regime)",table_row[1].text):
                    visa_status = 0
                else:
                    visa_status = 1

                countries[ctry].update({destination:visa_status})
        except:
            print(f"{ctry} to {destination} info not found")
            continue

## Make the results into a dataframe and clean it.        
df = pd.DataFrame(countries)

#Deal with one-offs
drop_rows = ['East Timor','Hong Kong','Kosovo', 'Macau','Montserrat','Macao','Cook Islands','Niue','Cayman Islands','South Ossetia']

#df.to_csv('blimp.csv')

import requests
from bs4 import BeautifulSoup
import os
import json
import pandas as pd

url = 'https://www.jobstreet.co.id/id/job-search/laravel-developer-jobs-in-bogor/'

headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.62'
}


res = requests.get(url, headers=headers)

def Get_Sallary():

    res = requests.get(url, headers=headers)

    try:
        os.mkdir('temp')
    except FileExistsError:
        pass

    with open('temp/res.html', 'w+') as outfile:
        outfile.write(res.text)
        outfile.close()

    #scraping Data Jobstreet
    soup = BeautifulSoup(res.text, 'html.parser')
    result = soup.find_all('div', class_='sx2jih0 zcydq8n lmSnC_0')

    job_list = []
    for item in result:
        title = item.find_all('div', class_='sx2jih0')[0].text
        location = item.find_all('span', class_='sx2jih0')[2].text
        company = item.find_all('span', class_='sx2jih0')[1].text
        try :
            sallary = item.find_all('span', class_='sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc3 _18qlyvc7')[1].text
        except IndexError:
            sallary = 'no sallary information'

        #Sorting Data
        data_dict = {
            'title': title,
            'company name': company,
            'location': location,
            'sallary': sallary
        }

        job_list.append(data_dict)

        # Write Json File
    try:
        os.mkdir('json_result')
    except:
        pass

    with open('json_result/jobstreet_list.json', 'w+') as json_data:
        json.dump(job_list, json_data)
        print('json created')

    # Create file CSV
    df = pd.DataFrame(job_list)
    df.to_csv('Jobstreet_Data.csv', index=False)
    df.to_excel('Jobstreet_Data.xlsx', index=False)

    # File CSV and Xlsx Has Been Created
    print('File CSV and Xlsx Created Success')


if __name__ == '__main__':
    Get_Sallary()

# item to scrape is : Title, Sallary, Company, Location
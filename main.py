import requests
from bs4 import BeautifulSoup
import os
import json
import pandas as pd
from lxml import etree

params = {
    'query': 'query',
    'location': 'location',
    'page': 'page'
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.62 '
}

def Get_Total_Page(query, location):
    url = (f'https://www.jobstreet.co.id/id/job-search/{query}-jobs-in-{location}/')

    params = {
        'query': query,
        'location': location,
    }
    res = requests.get(url, params=params, headers=headers)

    try:
        os.mkdir('temp')
    except FileExistsError:
        pass

    with open('temp/res.html', 'w+') as outfile:
        outfile.write(res.text)
        outfile.close()

    # Scraping Step
    list_page = []
    soup = BeautifulSoup(res.text, 'html.parser')
    pages = soup.find('select', id="pagination")
    pagess = soup.find_all('option')

    for page in pagess:
        list_page.append(page.text)
    try:
        total_pages = (list_page)[-1]
    except IndexError:
        total_pages = 1

    return total_pages


def Get_All_Item(query, location, counter):

    url = (f'https://www.jobstreet.co.id/id/job-search/{query}-jobs-in-{location}/{counter}/')
    # url = (f'https://www.jobstreet.co.id/id/job-search/laravel-jobs-in-bandung/1/')

    params = {
        'query': query,
        'location': location,
        'counter': counter
    }
    res = requests.get(url, params=params, headers=headers)

    with open('temp/res.html', 'w+', encoding="utf-8") as outfile:
        outfile.write(res.text)
        outfile.close()

    # scraping Data Jobstreet
    soup = BeautifulSoup(res.text, 'html.parser')
    result = soup.find_all('div', class_='sx2jih0 zcydq8n lmSnC_0')

    job_list = []
    for item in result:
        title = item.find_all('div', class_='sx2jih0')[0].text
        location = item.find_all('span', class_='sx2jih0')[2].text
        company = item.find_all('span', class_='sx2jih0')[1].text
        try:
            sallary = item.find_all('span', class_='sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc3 _18qlyvc7')[1].text
        except IndexError:
            sallary = 'no sallary information'


    # Sorting Data
        data_dict = {
            'title': title,
            'company name': company,
            'location': location,
            'sallary': sallary
        }
        #
        job_list.append(data_dict)

    # Write Json File
    try:
        os.mkdir('json_result')
    except FileExistsError:
        pass

        with open(f'json_result/{query}_in_{location}_page_{counter}.json', 'w+') as json_data:
            json.dump(job_list, json_data)
    print(f'json page {counter} created')

    return job_list

    # Create file CSV
def Creating_Document(dataFrame, filename):
    try:
        os.mkdir('data_result')
    except:
        pass

    df = pd.DataFrame(dataFrame)
    df.to_csv(f'data_result/{filename}.csv', index=False)
    df.to_excel(f'data_results{filename}.xlsx', index=False)

    print(f'File {filename}.csv and {filename}.xlsx succesfully created')

    # File CSV and Xlsx Has Been Created
    print('File CSV and Xlsx Created Success')


def Run():
    query = input('What is Your Query : ')
    location = input('What Is Your Location : ')

    final_result = []
    total = int(Get_Total_Page(query, location))
    counter = 0
    for counter in range(total):
        counter += 1
        try:
            dynamic_url = (f'https://www.jobstreet.co.id/id/job-search/{query}-jobs-in-{location}/{counter}/')
            Get_All_Item(query, location, counter)
        except ValueError :
            pass
        final_result += Get_All_Item(query, location, counter)

    # Formating Data
    try:
        os.mkdir('reports')
    except FileExistsError:
        pass

    with open(f'reports/.json.format{query}', 'w+') as final_data:
        json.dump(final_result, final_data)

    print('Data Json Created')
    # create docement
    Creating_Document(final_result, query)

if __name__ == '__main__':
    Run()

# item to scrape is : Title, Sallary, Company, Location

import requests
from bs4 import BeautifulSoup
import json
import numpy as np
import pandas as pd
import wget
import tarfile
import shutil
import gzip
import os


def parseHtml(html_url):
    
    r = requests.get(html_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    parsed_html = soup
    amount_of_files = len(parsed_html.find_all('a'))
    data_names = []
    url_list = []
    for i in range(amount_of_files):
        data_files = parsed_html.find_all('a')[i]['href'].split('/')[-1].split('.')[0]
        file_urls = parsed_html.find_all('a')[i]['href']
        
        data_names.append(data_files)
        url_list.append(file_urls)
    
    return data_names, url_list
    

def createFiles(data_files, file_urls):
    
    for dfnames,dfurls in zip(data_files,file_urls):
            
            # download the json.gz file
            filename = wget.download(dfurls)
            names = dfnames
            # unzip the gz file and write a new file as json
            with gzip.open(filename) as g:
                with open(f'{names}.json', 'wb') as f_out:
                    shutil.copyfileobj(g, f_out)

            # if the gz file exists delete (save space) - or log for upload
            if os.path.exists(f"{filename}"):
                os.remove(f"{filename}")
                print("old file removed ;)")
            else:
                print("The file does not exist")

            # if the file exist already we will rewrite over to json file
            #  or we can log as new file if there is new date

            json_path = 'json_files_practice/'
            if not os.path.exists(json_path):
                os.makedirs(json_path)

            if os.path.exists(f"json_files_practice/{names}.json"):
                shutil.copy(f'{names}.json', 'json_files_practice/')
                print('File rewritten')
            else:
            # else the file does not exists we will move the file to the proper folder
                shutil.move(f'{names}.json', 'json_files_practice/')
                print('File moved')


            df = pd.read_json(f'json_files_practice/{names}.json', lines = True)

            # create folder for csv_files
            csv_path = 'csv_files/'
            if not os.path.exists(csv_path):
                os.makedirs(csv_path)

            df.to_csv(f'{csv_path}{names}.csv')

            # remove any extra files lingering
            if os.path.exists(f"{names}.json"):
                os.remove(f"{names}.json")

    print("All files are uploaded")
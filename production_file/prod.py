import requests
from bs4 import BeautifulSoup
import json
import numpy as np
import pandas as pd
import re
import shutil
import gzip
import os
import wget
import tarfile
import time
from time_converter import Time
from pandasql import sqldf
import datetime as dt
from s3upload import *
from user_data_cleaning import *
from receiptItem_data_cleaning import *
from receipt_data_cleaning import *


# Upload data from S3
dataNames, urlList = parseHtml(html_url)
createFiles(dataNames, urlList)

# Clean User data
users_df = cleanUserData()

# Clean Receipt data
receipt_df = receiptDf()

# Clean Receipt Items Data
# receiptItem_df = dataCleaning(receiptItemsDataset(receiptIds()))

# Clean Brands Receipt
brands_df = brandsCleningDF()

pysqldf = lambda q: sqldf(q, globals())

# Query the questions

receiptItem_df = pd.read_pickle('clean_data/receiptitems_dataset.zip')
users_df['createdDate'] = pd.to_datetime(users_df['createdDate'])
date_col = ['createDate','dateScanned','finishedDate','purchaseDate','purchaseDate']

for col in date_col:
    receipt_df[f'{col}'] = pd.to_datetime(receipt_df[f'{col}'])


print('querying your dataset')
queryOne()
queryThree()
queryFour()
queryFive()
print('saved in query data set folder')

import re
import numpy as np
import pandas as pd
import json
import shutil
import gzip
import os
import wget
import tarfile
import time
from time_converter import Time


def BrandIdCpg(id_data, column=None):
    id_list = list(id_data[f'{column}'].to_dict().values())
    cleanedList = []

    for i in range(len(id_list)):

        parsed_name = id_list[i]
        parsed_names = re.findall("'([^']*)'", id_list[i])
        remove_list = ['$ref', 'Cogs','$id', '$oid']
        res = [i for i in parsed_names if i not in remove_list]
        cleanedList.append(res[0])
        
    return cleanedList

def brandsCleningDF():

    brand_df = pd.read_csv('csv_files/brands.csv', index_col = 0)
    brands_df = brand_df.copy()
    brands_df['_id'] = BrandIdCpg(brands_df, column = '_id')
    brands_df['cpg'] = BrandIdCpg(brands_df, column = 'cpg')
    brands_df = brands_df.rename(columns = {'_id':'brand_id'}, inplace = False)
    brands_df = brands_df.rename(columns = {'brandCode':'brandCode_id'}, inplace = False)
    brands_df = brands_df[(brands_df['name'].str.contains("test") == False)]
    brands_df['topBrand'] = brands_df['topBrand'].replace(np.nan, 0)
    brands_df['categoryCode'] = brands_df['category'].str.upper()
    brands_df['barcode'] = brands_df['barcode'].astype('object')
    
    brands_df.to_csv('clean_data_prod/brands_dataset.csv')

    return brands_df
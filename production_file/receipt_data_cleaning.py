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

# Receipt Item Data Model Cleaning

def convertDates(df):
    new_df = df.copy()
    col_list = list(new_df.columns)
    dates_col = col_list[3:10]
    dates_col.remove(col_list[8])
    for dates in dates_col:
        df[f'{dates}'] = cleanDateLog(id_data=df, column=f"{dates}")
        
    return df

def cleanReceipt():
    
    receipt_df = pd.read_csv('csv_files/receipts.csv', index_col = 0)
    receipts_df = convertDates(receipt_df)
    receipts_df['_id'] = cleanIdCpg(receipts_df, column = '_id')
    receipts_df = receipts_df.drop('rewardsReceiptItemList', axis = 1)
    
    return receipts_df

def receiptDf():
    receipt_df = pd.read_csv('csv_files/receipts.csv', index_col = 0)
    receipts_df = convertDates(receipt_df)
    receipts_df['_id'] = cleanIdCpg(receipts_df, column = '_id')
    receipts_df = receipts_df.rename(columns = {'_id':'receipt_id'}, inplace = False)
    date_col = ['createDate','dateScanned','finishedDate','purchaseDate','purchaseDate']
    for col in date_col:
        receipts_df[f'{col}'] = pd.to_datetime(receipts_df[f'{col}'])

    print(receipt_df)
    receipts_df.to_csv('clean_data_prod/receipts_dataset.csv')
    
    return receipts_df
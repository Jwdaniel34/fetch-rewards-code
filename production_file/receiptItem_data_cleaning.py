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



def receiptIds():  
    # creating receipt Item to json file
    df = pd.read_json('json_files/receipts.json', lines = True)
    Items_df = df
    reference_data = receiptDf()[['receipt_id', 'rewardsReceiptItemList', 'purchasedItemCount']]
    # how many items are in this dataset
    
    total  = len(Items_df)
    # Receipt Items nested per receipt_id
    
    sample_lst = []
    receipt_labels = []
    missing_data = []
    missing_labels = []
    
        
    # matched to the amount of data that we have currently
    for i in range(total):
        try:
            # create a variable to iterate through the dataframe
            print(i)
            receiptItem_df = pd.DataFrame(Items_df['rewardsReceiptItemList'][i])

            receiptItem_df['receipt_id'] = reference_data['receipt_id'][i]
    #         somedataframe = somedataframe.append(receiptItem_df[i], ignore_index=True)

            # incase we have keyerrors that could mean its only one 
                # each receipt had several subsets of items
            total_items = len(receiptItem_df)

                # each receipt had several items in so we may have multiple indexes 
            for j in range(total_items):
                if j > 1:
                    receipt_labels.append(reference_data['receipt_id'][i])
                    sample_lst.append(receiptItem_df)
                else:
                    receipt_labels.append(reference_data['receipt_id'][i])
                    sample_lst.append(receiptItem_df)

        # incase we have only one we can count it as missing data 
        # that we can look at later
        except:
            print(i, 'missing data/nan')
            missing_labels.append(reference_data['receipt_id'][i])
            missing_data.append(receiptItem_df)

    # Normalize the json data frames by the subsets and stack(concat) them 
    print(f"Missing Data: {len(missing_data)}")
    print(f"Amount of Data: {len(sample_lst)}")
    
    return sample_lst


def receiptItemsDataset(df):  
    # creating receipt Item to json file
    print('appending all datasets')
    Items_df = df
#     reference_data = receiptDf()[['receipt_id', 'rewardsReceiptItemList', 'purchasedItemCount']]

    # how many items are in this dataset
    total  = len(Items_df)
    # Receipt Items nested per receipt_id
    
    sample_lst = pd.DataFrame()
    missing_data = []
    missing_labels = []
    
    receiptItem_col = ['receipt_id','barcode', 'description', 'finalPrice', 'itemPrice', 'needsFetchReview',
       'partnerItemId', 'preventTargetGapPoints', 'quantityPurchased',
       'userFlaggedBarcode', 'userFlaggedNewItem', 'userFlaggedPrice',
       'userFlaggedQuantity', 'needsFetchReviewReason',
       'pointsNotAwardedReason', 'pointsPayerId', 'rewardsGroup',
       'rewardsProductPartnerId', 'userFlaggedDescription',
       'originalMetaBriteBarcode', 'originalMetaBriteDescription', 'brandCode',
       'competitorRewardsGroup', 'discountedItemPrice',
       'originalReceiptItemText']
    
    print(total)
    # matched to the amount of data that we have currently
    for i in range(total):
        receiptItem_df = Items_df[i]
        
        if sample_lst.empty:
            print('start', i)
            sample_lst = sample_lst.append(receiptItem_df)
            
        else:
            print('continuing: ',i)
            sample_lst = sample_lst.append(receiptItem_df, ignore_index=True)

        # incase we have only one we can count it as missing data 
        # that we can look at later

    print('End: ', i)
    print(f"Missing Data: {len(missing_data)}")
    print(f"Amount of Data: {len(sample_lst)}")
    
    return sample_lst[receiptItem_col]


def dataCleaning(df)   

    datacleaning = df.copy()
    datacleaning['barcode'] = datacleaning['barcode'].replace(np.nan, '4011')
    datacleaning['description'] = datacleaning['description'].replace(np.nan, 'ITEM NOT FOUND')
    datacleaning['needsFetchReview'] = datacleaning['needsFetchReview'].replace(np.nan, False)
    datacleaning['finalPrice'] = datacleaning['finalPrice'].replace(np.nan, 0)
    datacleaning['itemPrice'] = datacleaning['itemPrice'].replace(np.nan, 0)
    datacleaning['quantityPurchased'] = datacleaning['quantityPurchased'].replace(np.nan, 0)
    datacleaning = datacleaning[(datacleaning['finalPrice'] != '1') & (test_1['barcode'] != '4011')]
    
    datacleaning['finalPrice'] = datacleaning['finalPrice'].astype('float64')
    datacleaning['itemPrice'] = datacleaning['itemPrice'].astype('float64')
    datacleaning['quantityPurchased'] = datacleaning['quantityPurchased'].astype('int64')
    
    datacleaning['brandCode'] = datacleaning['brandCode'].replace(np.nan, 'NO BRAND CODE')
    datacleaning['userFlaggedBarcode'] = datacleaning['userFlaggedBarcode'].replace(np.nan,'4011')
    datacleaning['userFlaggedQuantity'] = datacleaning['userFlaggedQuantity'].replace(np.nan, 0)
    datacleaning['userFlaggedDescription'] = datacleaning['userFlaggedDescription'].replace(np.nan, 'ITEM NOT FOUND')
    datacleaning['userFlaggedPrice'] = datacleaning['userFlaggedPrice'].replace(np.nan, 0)
    dataCleaning = dataCleaning.drop(columns=['userFlaggedBarcode', 'userFlaggedDescription'])
    receipts_itemdf = dataCleaning.copy()
    
    receipts_itemdf.to_pickle('clean_data_prod/receiptitems_dataset.zip')
    
    return datacleaning
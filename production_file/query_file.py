from pandasql import sqldf
import datetime as dt
import pandas as pd
import numpy as np
from s3upload import *
from user_data_cleaning import *
from receiptItem_data_cleaning import *
from receipt_data_cleaning import *
from brands_data_cleaning import *
from query_file import *


def fullQuery():
    pysqldf = lambda q: sqldf(q, locals())
    
    # Upload data from S3
    dataNames, urlList = parseHtml()
    createFiles(dataNames, urlList)

    # Clean User data
    users_df = cleanUserData()
    print('user data cleaned')
    
    receipt_df = receiptDf()

    print('receipt data cleaned')

    # Clean Receipt Items Data
    # do not uncomment below it will take a minute
    # receiptItem_df = dataCleaning(receiptItemsDataset(receiptIds()))

    # Clean Brands Receipt
    brands_df = brandsCleaningDF()
    print('brands data cleaned')


    print('Query Setup')
    pysqldf = lambda q: sqldf(q, globals())

    # Query the questions

    receiptItem_df = pd.read_pickle('clean_data_prod/receiptitems_dataset.zip')

    users_df['createdDate'] = pd.to_datetime(users_df['createdDate'])
    date_col = ['createDate','dateScanned','finishedDate','purchaseDate','purchaseDate']

    for col in date_col:
        receipt_df[col] = pd.to_datetime(receipt_df[col])


    q1 = """SELECT receipt_df.receipt_id, count(receiptItem_df.receipt_id) as receipt_count,
            receiptItem_df.brandCode, receipt_df.dateScanned as ds
            FROM receiptItem_df INNER JOIN receipt_df
            ON receiptItem_df.receipt_id = receipt_df.receipt_id WHERE brandCode <> "NO BRAND CODE"
            GROUP BY brandCode ORDER BY receipt_count DESC;"""
    
    recent_month_top_5_brands = pysqldf(q1)

    recent_month_top_5_brands = recent_month_top_5_brands.sort_values(by="ds", ascending = False)

    recent_month_top_5_brands = recent_month_top_5_brands.sort_values(by="receipt_count", ascending = False)

    recent_month_top_5_brands.to_csv('query_datasets/top_5_brands.csv')
    

    q3 = """SELECT receipt_df.rewardsReceiptStatus as reward_status, 
        
        avg(receipt_df.totalSpent) as avg_spend

        FROM receiptItem_df INNER JOIN receipt_df
        
        ON receiptItem_df.receipt_id = receipt_df.receipt_id GROUP BY reward_status;"""
        
    accepted_rejected_spend = pysqldf(q3)
    accepted_rejected_spend = accepted_rejected_spend['reward_status'].replace('FINISHED', 'ACCEPTED')
    accepted_rejected_spend.to_csv('query_datasets/accepted_rejected_spend.csv')

    q4 = """SELECT receipt_df.rewardsReceiptStatus as reward_status, 
        count(receipt_df.purchasedItemCount) as items_purchased
        FROM receiptItem_df INNER JOIN receipt_df ON receiptItem_df.receipt_id = receipt_df.receipt_id GROUP BY reward_status;"""


    accepted_rejected_items = pysqldf(q4)
    accepted_rejected_items.to_csv('query_datasets/accepted_rejected_items.csv')


    start_date = datetime(2021, 2, 2)
    end_date = datetime(2020, 7, 2)

    q5 = """
            SELECT receipt_df.receipt_id, users_df.user_id , users_df.createdDate, receipt_df.totalSpent
            FROM receipt_df INNER JOIN users_df
            ON users_df.user_id = receipt_df.userId;
            """

    users_spent_df = pysqldf(q5)

    q5v2 = """
            SELECT users_spent_df.receipt_id, users_spent_df.createdDate, users_spent_df.totalSpent, 
            receiptItem_df.brandCode
            FROM users_spent_df INNER JOIN receiptItem_df
            ON users_spent_df.receipt_id = receiptItem_df.receipt_id WHERE brandCode <> "NO BRAND CODE"
                
                """

    users_spent_dfv2 = pysqldf(q5v2)

    users_spent_dfv2['createdDate'] = pd.to_datetime(users_spent_dfv2['createdDate'])
    users_spent_dfv2 = users_spent_dfv2.sort_values(by='createdDate',ascending=False).set_index('createdDate')

    users_spent_dfv2.to_csv('query_datasets/users_spent_dfv2s.csv')
 
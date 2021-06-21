from pandasql import sqldf
import datetime as dt
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style="whitegrid")


def queryOne():

    q1 = """SELECT receipt_df.receipt_id, count(receiptItem_df.receipt_id) as receipt_count,

            receiptItem_df.brandCode, receipt_df.dateScanned as ds
            
            FROM receiptItem_df INNER JOIN receipt_df
            
            ON receiptItem_df.receipt_id = receipt_df.receipt_id WHERE brandCode <> "NO BRAND CODE"
            
            GROUP BY brandCode ORDER BY receipt_count DESC;"""


    recent_month_top_5_brands = pysqldf(q1)
    recent_month_top_5_brands = recent_month_top_5_brands.sort_values(by="ds", ascending = False)
    recent_month_top_5_brands = recent_month_top_5_brands.sort_values(by="receipt_count", ascending = False)
    recent_month_top_5_brands.to_csv('query_datasets/top_5_brands.csv')
    
    return recent_month_top_5_brands


def queryThree():

    q3 = """SELECT receipt_df.rewardsReceiptStatus as reward_status, 
        
        avg(receipt_df.totalSpent) as avg_spend

        FROM receiptItem_df INNER JOIN receipt_df
        
        ON receiptItem_df.receipt_id = receipt_df.receipt_id GROUP BY reward_status;"""
        
    accepted_rejected_spend = pysqldf(q3)
    accepted_rejected_spend = accepted_rejected_spend['reward_status'].replace('FINISHED', 'ACCEPTED')
    accepted_rejected_spend.to_csv('query_datasets/accepted_rejected_spend.csv')

    return accept_rejected_spend

def queryFour():

    q4 = """SELECT receipt_df.rewardsReceiptStatus as reward_status, 
        
        count(receipt_df.purchasedItemCount) as items_purchased

        FROM receiptItem_df INNER JOIN receipt_df
        
        ON receiptItem_df.receipt_id = receipt_df.receipt_id GROUP BY reward_status;"""


    accepted_rejected_items = pysqldf(q4)
    accepted_rejected_items.to_csv('query_datasets/accepted_rejected_items.csv')

    return accept_rejected_items


def queryFive():
    
    q5 = """
            SELECT receipt_df.receipt_id, users_df.user_id , users_df.createdDate, receipt_df.totalSpent
            FROM receipt_df INNER JOIN users_df
            ON users_df.user_id = receipt_df.userId;
            """

    q5v2 = """
            SELECT users_spent_df.receipt_id, users_spent_df.createdDate, users_spent_df.totalSpent, 
            receiptItem_df.brandCode
            FROM users_spent_df INNER JOIN receiptItem_df
            ON users_spent_df.receipt_id = receiptItem_df.receipt_id WHERE brandCode <> "NO BRAND CODE"
                
                """

    users_spent_df = pysqldf(q5)
    users_spent_dfv2 = pysqldf(q5v2)

    users_spent_dfv2['createdDate'] = pd.to_datetime(users_spent_dfv2['createdDate'])
    users_spent_dfv2 = users_spent_dfv2.sort_values(by='createdDate',ascending=False).set_index('createdDate')
    user_x_spent = users_spent_dfv2[(users_spent_dfv2.index <= start_date)
                 & (users_spent_dfv2.index >= end_date)]
    
    user_x_spent = pd.DataFrame(user_x_spent.groupby(by='brandCode')['totalSpent'].sum().head(5)
    user_x_spent.to_csv('query_datasets/user_x_spent.csv')

    return user_x_spent
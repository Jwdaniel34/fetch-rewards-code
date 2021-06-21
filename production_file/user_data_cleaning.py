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

# User Data Model cleaning
def cleanDateLog(id_data, column=None):
    id_list = list(id_data[f'{column}'].to_dict().values())
    times_list = []
    dates_list = []
    for i in range(len(id_list)):
        try: 
            
            date_parsed = id_list[i].replace('}', "").split(':')[1].replace(" ", "")
            date_converted = Time(int(date_parsed[:10]), 'posix').to('dt')
            format_date = "%m/%d/%Y"
            format_time = "%H:%M:%S"
            formated_date = date_converted.strftime(format_date)
            formated_time = date_converted.strftime(format_time)
            times_list.append(formated_time)
            dates_list.append(formated_date)
        except AttributeError:
            
            date_parsed = str(id_list[i])
            dates_list.append(date_parsed)
            
    return dates_list

def cleanIdCpg(id_data, column=None):
#     print(id_data[f'{column}'])
    # create the dictionary into a list to only get the values
    id_list = list(id_data[f'{column}'].to_dict().values())
    cleanedList = []
    for i in range(len(id_list)):
        parsed_name = id_list[i]
        # remove commas colons and split at quotations
        parsed_names = re.findall("'([^']*)'", id_list[i])
        # these were reoccuring strings that i saw
        cleanedList.append(parsed_names[-1])

    return cleanedList

def cleanUserData():    
    user_df = pd.read_csv('csv_files/users.csv', index_col = 0)
    users_df = user_df.copy()

    users_df['_id'] = cleanIdCpg(id_data=users_df, column="_id")
    users_df['createdDate'] = cleanDateLog(id_data=users_df, column="createdDate")
    users_df["lastLogin"] = cleanDateLog(id_data=users_df, column="lastLogin")

    # convert to pandas datetime 
    users_df['createdDate'] = pd.to_datetime(users_df['createdDate'])
    users_df["lastLogin"] = pd.to_datetime(users_df['lastLogin'])
    users_df = users_df.rename(columns = {'_id':'user_id'}, inplace = False)
    users_df.to_csv('clean_data_prod/users_dataset.csv')
    
    return users_df


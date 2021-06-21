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
from brands_data_cleaning import *
from query_file import *

def prodReady():
    print('querying your dataset')
    fullQuery()
    print('saved in query data set folder')


prodReady()

# note seems pandasql does not work in main files to run but works in the notebook.
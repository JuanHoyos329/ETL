import glob 
import pandas as pd 
import xml.etree.ElementTree as ET 
from datetime import datetime

import warnings
warnings.filterwarnings('ignore')  # Suppress all warnings

def extract(): 
    extracted_data = pd.DataFrame(columns=['car_model','year_of_manufacture','price','fuel'])  # create an empty data frame to hold extracted data


    return extracted_data


def transform(data): 

        
    return data

def load_to_csv(df, csv_path):
    ''' This function saves the final dataframe as a `CSV` file 
    in the provided path. Function returns nothing.'''
    df.to_csv(csv_path)

def load_to_db(df, sql_connection, table_name):
    ''' This function saves the final dataframe as a database table
    with the provided name. Function returns nothing.'''
    df.to_sql(table_name, sql_connection, if_exists='replace', index=False)
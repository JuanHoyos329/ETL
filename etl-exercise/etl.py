import glob 
import pandas as pd 
import xml.etree.ElementTree as ET 
from datetime import datetime

import warnings
warnings.filterwarnings('ignore')  # Suppress all warnings


def extract_from_csv(file_to_process):
        dataframe = pd.read_csv(file_to_process)
        dataframe = dataframe.fillna("N/A")
        return dataframe

    # Load json files
def extract_from_json(file_to_process):
        dataframe = pd.read_json(file_to_process, lines=True)
        dataframe = dataframe.fillna("N/A")
        return dataframe


    # Load xml files
def extract_from_xml(file_to_process):
        tree = ET.parse(file_to_process)
        root = tree.getroot()

        data = []
        for car in root:
            car_data = {}
            for element in car:
                car_data[element.tag] = element.text
            data.append(car_data)

        extracted_data = pd.DataFrame(data, columns=['car_model','year_of_manufacture','price','fuel'])
        extracted_data = extracted_data.fillna("N/A")
        return extracted_data


def transform(data):
    # Convertimos price a numérico (por si acaso) y redondeamos a 2 decimales
    data["price"] = pd.to_numeric(data["price"], errors="coerce").round(2)
    return data


def load_to_csv(df, csv_path):
    ''' This function saves the final dataframe as a `CSV` file 
    in the provided path. Function returns nothing.'''
    df.to_csv(csv_path)

def load_to_db(df, sql_connection, table_name):
    ''' This function saves the final dataframe as a database table
    with the provided name. Function returns nothing.'''
    df.to_sql(table_name, sql_connection, if_exists='replace', index=False)
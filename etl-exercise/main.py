import sqlite3
import glob
import pandas as pd
from log import log_progress
from etl import extract, transform, load_to_csv, load_to_db

def main():
    log_file = "log_file.txt" 
    target_file = "transformed_data.csv"
    db_name = "Used_Cars.db"
    table_name = "used_cars"
    table_attribs = ['car_model','year_of_manufacture','price','fuel']

    # Log the initialization of the ETL process 
    log_progress("ETL Job Started") 
    
    # Log the beginning of the Extraction process 
    log_progress("Extract phase Started") 

    # Obtener funciones de extracción
    extract_from_csv, extract_from_json, extract_from_xml = extract()

    # Archivos a procesar
    data_folder = "data/"
    all_files = (
        glob.glob(f"{data_folder}*.csv") +
        glob.glob(f"{data_folder}*.json") +
        glob.glob(f"{data_folder}*.xml")
    )

    # Lista para guardar todos los DataFrames
    extracted_dataframes = []

    for file in all_files:
        if file.endswith('.csv'):
            df = extract_from_csv(file)
        elif file.endswith('.json'):
            df = extract_from_json(file)
        elif file.endswith('.xml'):
            df = extract_from_xml(file)
        else:
            continue
        extracted_dataframes.append(df)

    # Concatenar todos los DataFrames extraídos
    extracted_data = pd.concat(extracted_dataframes, ignore_index=True)

    log_progress("Data extraction complete.")

    # Log the beginning of the Transformation process 
    log_progress("Transform phase Started") 

    # Transform (puedes personalizar más si quieres)
    transformed_data = transform(extracted_data)

    log_progress("Data transformation complete.")

    # Load to CSV
    load_to_csv(transformed_data, target_file)
    log_progress("Data loading to CSV complete.")

    # Load to DB
    sql_connection = sqlite3.connect(db_name)
    load_to_db(transformed_data, sql_connection, table_name)
    log_progress("Data loaded to Database as table.")

    # Cerrar conexión a DB
    sql_connection.close()

if __name__ == "__main__":
    main()
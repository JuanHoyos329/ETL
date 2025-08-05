import pytest
import pandas as pd
import tempfile
import os
import json
import xml.etree.ElementTree as ET

# Importamos tus funciones de extracción
from etl import extract_from_csv, extract_from_json, extract_from_xml

# ---------------------------
# Fixtures para archivos de prueba
# ---------------------------

@pytest.fixture
def csv_file():
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.csv', delete=False) as f:
        f.write("car_model,year_of_manufacture,price,fuel\n")
        f.write("Toyota,2020,20000,Petrol\n")
        f.write("Honda,2018,18000,Diesel\n")
        return f.name

@pytest.fixture
def json_file():
    data = [
        {"car_model": "Ford", "year_of_manufacture": 2019, "price": 22000, "fuel": "Petrol"},
        {"car_model": "BMW", "year_of_manufacture": 2021, "price": 35000, "fuel": "Electric"}
    ]
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as f:
        for item in data:
            f.write(json.dumps(item) + "\n")
        return f.name

@pytest.fixture
def xml_file():
    root = ET.Element("cars")
    car1 = ET.SubElement(root, "car")
    ET.SubElement(car1, "car_model").text = "Mazda"
    ET.SubElement(car1, "year_of_manufacture").text = "2017"
    ET.SubElement(car1, "price").text = "15000"
    ET.SubElement(car1, "fuel").text = "Gasoline"

    car2 = ET.SubElement(root, "car")
    ET.SubElement(car2, "car_model").text = "Nissan"
    ET.SubElement(car2, "year_of_manufacture").text = "2016"
    ET.SubElement(car2, "price").text = "14000"
    ET.SubElement(car2, "fuel").text = "Diesel"

    temp_file = tempfile.NamedTemporaryFile(mode='w+', suffix='.xml', delete=False)
    tree = ET.ElementTree(root)
    tree.write(temp_file.name)
    return temp_file.name

# ---------------------------
# Pruebas para CSV
# ---------------------------

def test_extract_from_csv(csv_file):
    df = extract_from_csv(csv_file)
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (2, 4)
    assert list(df.columns) == ['car_model', 'year_of_manufacture', 'price', 'fuel']

def test_extract_from_empty_csv():
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.csv', delete=False) as f:
        empty_csv = f.name
    with pytest.raises(pd.errors.EmptyDataError):
        extract_from_csv(empty_csv)

def test_extract_from_malformed_csv():
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.csv', delete=False) as f:
        f.write("wrong_header\n1,2,3\n")
        malformed_csv = f.name
    df = extract_from_csv(malformed_csv)
    assert 'wrong_header' in df.columns

# ---------------------------
# Pruebas para JSON
# ---------------------------

def test_extract_from_json(json_file):
    df = extract_from_json(json_file)
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (2, 4)
    assert 'car_model' in df.columns

def test_extract_from_invalid_json():
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as f:
        f.write("{invalid json]")
        bad_json = f.name
    with pytest.raises(ValueError):
        extract_from_json(bad_json)

def test_extract_json_missing_fields():
    data = [{"car_model": "Kia"}]  # Falta year_of_manufacture, price, fuel
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as f:
        for item in data:
            f.write(json.dumps(item) + "\n")
        path = f.name
    df = extract_from_json(path)
    assert 'car_model' in df.columns
    assert df.shape == (1, 1)

# ---------------------------
# Pruebas para XML
# ---------------------------

def test_extract_from_xml(xml_file):
    df = extract_from_xml(xml_file)
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (2, 4)
    assert 'car_model' in df.columns

def test_extract_xml_invalid_structure():
    bad_xml_content = "<cars><car><wrong_tag>test</wrong_tag></car></cars>"
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.xml', delete=False) as f:
        f.write(bad_xml_content)
        path = f.name
    df = extract_from_xml(path)
    # Las columnas estarán vacías pero el DataFrame existirá
    assert df.shape == (1, 4)

def test_extract_xml_missing_elements():
    incomplete_xml = "<cars><car><car_model>Opel</car_model></car></cars>"
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.xml', delete=False) as f:
        f.write(incomplete_xml)
        path = f.name
    df = extract_from_xml(path)
    assert 'car_model' in df.columns
    assert df.shape == (1, 4)




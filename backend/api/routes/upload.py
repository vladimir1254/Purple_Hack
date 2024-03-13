from enum import Enum
from typing import Any
from http import HTTPStatus
import os
import csv
import logging
import aiofiles
from zipfile import ZipFile

from fastapi import APIRouter, status, HTTPException, File, UploadFile,Form
from fastapi.responses import StreamingResponse, FileResponse
from models import PriceRequest, PriceResponse
from typing import Optional,Any

from api.exceptions import bad_data
from repositories import BaseRepository, BasePrices, DiscountPrices, DiscountPriceRepository, BasePriceRepository
from models import OkResponse
from services import find_all_parent, category_tree, location_tree, SQLToCSVConverter
import re
from datetime import datetime
import shutil


router = APIRouter()
logger = logging.getLogger()
UPLOAD_FOLDER = "/root/purplehack/backend/upload"
#UPLOAD_FOLDER = "D:/projects/HAKATON_5/upload"


def convert(file_path):
    table_name = "unknown_table"
    base_dir = file_path.rsplit('/', 1)[0]+'/'
    # Открываем файл и читаем все строки
    file_string = ''

    print('file_path=',file_path)
    with open(file_path, 'r', encoding='utf-8') as file:
        file_string = file.read()
    for line in file_string.split('\n'):
        if 'create table' in line:
            table_name_match = re.search(r"create table (\w+)", line)
            if table_name_match:
                table_name = table_name_match.group(1)
                break

    csv_filename = table_name + '_converted.csv'
    csv_file_path = os.path.join(base_dir, csv_filename)

    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        for line in file_string.split('\n'):
            values_match = re.findall(r"\((\d+,\s*\d+,\s*\d+)\)", line.strip())
            for values_str in values_match:
                values = values_str.split(',')
                values = [value.strip() for value in values]
                values.append(str(datetime.utcnow()))
                writer.writerow(values)

    return csv_file_path, table_name



@router.post("/")
async def upload_file(matrix: str = Form(...), file: UploadFile = File(...)):
    extension = file.filename.split('.')[-1]
    print('ext=',file,matrix)
    if extension == "zip":
        file_location = f"{UPLOAD_FOLDER}/{file.filename}"
        with open(file_location, 'wb+') as buffer:
            buffer.write(await file.read())
        with ZipFile(file_location, 'r') as ref:
             for file_z in ref.namelist():
                print('FILE IN ZIP=',file_z,'EXTENS=',file_z.split('.')[-1])
                if file_z.split('.')[-1]=='sql' or file_z.split('.')[-1]=='csv':
                    ref.extractall(f"{UPLOAD_FOLDER}/temp")
                    print('FILE = ',f"{UPLOAD_FOLDER}/temp/{file_z}")
                    with open(f"{UPLOAD_FOLDER}/temp/{file_z}", 'r') as f:
                        file_string = f.read()
                    converter = SQLToCSVConverter(file_string)
                    csv_file_path, table_name = converter.convert(f"{UPLOAD_FOLDER}/temp/",file_z.split('.')[0])
                    print(csv_file_path,table_name)
                    if str(matrix) == "baseline":
                        print('Загрузка baseline таблицы')
                        BasePriceRepository().copy_from_csv(csv_file_path=csv_file_path, table="base_prices")
                    else:
                        BasePriceRepository().copy_from_csv(csv_file_path=csv_file_path, table="discount_prices")
        #os.remove(f"{UPLOAD_FOLDER}/temp/{expected_filename}")
        os.remove(file_location)
    '''
    else:
        file_string = (await file.read()).decode("utf-8")
    if extension == "sql":
        converter = SQLToCSVConverter(file_string)
        csv_file_path, table_name = converter.convert()
    elif extension == "csv":
        table_name = "base_prices"
        if file.filename[:len("baseline_matrix")] != "baseline_matrix":
            table_name = "discount_prices"
        csv_file_path = f"{UPLOAD_FOLDER}/{file.filename}"
        with open(csv_file_path, 'w', newline='') as buffer:
            buffer.write(file_string)
    else:
        return OkResponse(result="error")
    
    if str(matrix) == "baseline":
        print('Загрузка baseline таблицы')
        BasePriceRepository().copy_from_csv(csv_file_path=csv_file_path, table="base_prices")
    #else:
       # BasePriceRepository().copy_from_csv(csv_file_path=csv_file_path, table="discount_prices")
    return OkResponse(result="ok")
    '''
'''

    # ваша логика обработки данных
    print('???',matrix)
    return {"filename": file.filename, "matrix": matrix}    
    if 'file' not in request.files:
        return 'No file part', 400
    
    file = request.files['file']
    matrix =  request.form['matrix']
    print(matrix)
    if file.filename == '':
        return 'No selected file', 400

    if file:

        # Распаковываем архив
        with zipfile.ZipFile(file, 'r') as z:
            z.extractall(UPLOAD_FOLDER)

        # Получаем список файлов в UPLOAD_FOLDER
        file_names = os.listdir(UPLOAD_FOLDER+'/files/')
        for file in file_names:
            convert(UPLOAD_FOLDER+'/files/'+file)
        # Теперь file_names содержит список имен всех файлов в UPLOAD_FOLDER
        print('file_names = ',file_names)
       # filename = file.filename
       # file.save(os.path.join(UPLOAD_FOLDER, filename))
        return 'File uploaded successfully', 200
'''
import uuid
import re
import csv
import os
import logging
from datetime import datetime

logger = logging.getLogger()


class SQLToCSVConverter:
    def __init__(self, file_string):
        self.file_string = file_string

    def convert(self,base_dir,table_name):

        for line in self.file_string.split('\n'):
            if 'create table' in line:
                table_name_match = re.search(r"create table (\w+)", line)
                #if table_name_match:
                   # table_name = table_name_match.group(1)
                #    break

        csv_filename = table_name + '_converted.csv'
        csv_file_path = os.path.join(base_dir, csv_filename)

        with open(csv_file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            for line in self.file_string.split('\n'):
                values_match = re.findall(r"\((\d+,\s*\d+,\s*\d+)\)", line.strip())
                for values_str in values_match:
                    values = values_str.split(',')
                    values = [value.strip() for value in values]
                    values.append(str(datetime.utcnow()))
                    if 'discount' in table_name:
                        values.append(table_name.split('_')[-1])
                    writer.writerow(values)

        return csv_file_path, table_name

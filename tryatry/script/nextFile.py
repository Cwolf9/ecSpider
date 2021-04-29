# -*- coding: UTF-8 -*-

"""
@author: Cwolf9
@file: nextFile
@date: 2021-04-29 17:29
@desc:
"""
import os, shutil
from datetime import datetime, timedelta


DATA_PATH = r'D:\a-university-study\ecnu\周报\\'
if __name__ == '__main__' or True:
    dir_list = os.listdir(DATA_PATH)
    dir_list.sort()
    last_file = dir_list[-1]
    if last_file.split('.')[-1] != 'docx':
        last_file = dir_list[-2]
    print(last_file)
    next_date = datetime.strptime(last_file[:8], '%Y%m%d') + timedelta(days=7)
    next_file_name = next_date.strftime('%Y%m%d') + last_file[8:]
    print(next_file_name)
    shutil.copy(DATA_PATH + last_file, DATA_PATH + next_file_name)
    # with open(DATA_PATH + next_file_name, 'w', encoding='utf-8') as f:
    #     f.write('')
    #

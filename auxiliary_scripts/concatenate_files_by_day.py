from argparse import ArgumentParser
from datetime import datetime
import pandas as pd
import numpy as np
import os
import time

parser = ArgumentParser()
parser.add_argument('--folder', type=str,
        help='Folder where the files are to be organized')
parser.add_argument('--output_folder', type=str,
        help='Location where corrected files will be created')
parser.add_argument('--timestamp_column_name', type=str,
        help='column with the collection timestamp (timestamp or StartTime)')
parser.add_argument('--frequency', type=str,
        help='Frequency in minutes that collections are performed (15 or 60)')

args = parser.parse_args()

folder = args.folder
output_folder = args.output_folder
column_name = args.timestamp_column_name
saveBreak = args.frequency

if (saveBreak == '15'):
    saveBreak = 35
else:
    saveBreak = 8

ls_files = os.popen('ls {folder} | egrep "\.csv"'.format(folder = folder)).read()
files = ls_files.split("\n")
files.pop()

data_frame = {}
data_frame_column = []

ant = files[0]

count = 0

for f in files:
    print(f)
    df = pd.read_csv(folder + '/' + f, index_col=0)
    data_frame_column = df.columns.values
    print(df.shape)
    for (i,row) in df.iterrows():
        date_row = row[column_name]
        date_row = time.strftime('%d-%m-%Y', time.localtime(date_row))
        if (not (date_row in data_frame.keys())):
            data_frame[date_row] = []
        data_frame[date_row].append(row)
    for h in data_frame: 
        print("----->> ",h, len(data_frame[h]))
    a =  ant.split('-')
    dia = a[1]
    mes = a[0]
    d = f.split('-')[1]
    m = f.split('-')[0]
    if(d != dia or m != mes):
        count += 1
    if(count == saveBreak): #teste: 8, asg: 35
        count = 0
        key =  a[1] + '-' + a[0] + '-' + a[2]
        print("escrevendo", key)
        new_df = pd.DataFrame(data_frame[key], columns=data_frame_column)
        print(new_df.shape)
        new_df.reset_index(inplace=True, drop=True)
        new_df.to_csv(output_folder + '/' + key + '.csv')
        data_frame[key] = []
        ant = f

for key_df in data_frame:
    print(key_df, len(data_frame[key_df]))
    if(len(data_frame[key_df]) > 0):
        print('entrou')
        print(data_frame_column)
        new_df = pd.DataFrame(data_frame[key_df], columns=data_frame_column)
        new_df.reset_index(inplace=True, drop=True)
        new_df.to_csv(output_folder + '/' + key_df + '.csv')
        print(output_folder + '/' + key_df + '.csv')

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

args = parser.parse_args()

folder = args.folder
output_folder = args.output_folder
column_name = args.timestamp_column_name

ls_files = os.popen('ls {folder} | egrep "\.csv"'.format(folder = folder)).read()
files = ls_files.split("\n")
files.pop()

data_frame = {}
data_frame_column = []

for f in files:
    print(f)
    df = pd.read_csv(folder + '/' + f, index_col=0)
    data_frame_column = df.columns.values
    for (i,row) in df.iterrows():
        date_row = row[column_name]
        date_row = time.strftime('%d-%m-%Y', time.localtime(date_row))
        if (not (date_row in data_frame.keys())):
            data_frame[date_row] = []
        data_frame[date_row].append(row)

for key in data_frame:
    new_df = pd.DataFrame(data_frame[key], columns=data_frame_column)
    new_df.reset_index(inplace=True, drop=True)
    new_df.to_csv(output_folder + '/' + key + '.csv')

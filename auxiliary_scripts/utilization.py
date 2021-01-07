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

args = parser.parse_args()

folder = args.folder
output_folder = args.output_folder

ls_files = os.popen('ls {folder} | egrep "\.csv"'.format(folder = folder)).read()
files = ls_files.split("\n")
files.pop()

data_frame_day = {}

head = []

for f in files:
    print(f)
    df = pd.read_csv(folder + '/' + f, index_col=0)
    head = df.columns.values
    index = list(df.index.values)
    df = df[~df.index.duplicated(keep='first')]
    for i in index:
        metrics_ok = True
        if 'Average' in head:
            metrics_ok = (metrics_ok and df.loc[i,'Average'] <= 100)
        if 'Maximum' in head:
            metrics_ok = (metrics_ok and df.loc[i,'Maximum'] <= 100)
        if 'Minimum' in head:
            metrics_ok = (metrics_ok and df.loc[i,'Minimum'] <= 100)
        if 'Sum' in head:
            metrics_ok = (metrics_ok and df.loc[i,'Sum'] <= 100)
        
        if metrics_ok:
            timestamp = df.loc[i,'timestamp']
            date = time.strftime('%Y-%m-%d', time.localtime(timestamp))
            row = df.loc[i]
            if (not (date in data_frame_day.keys())):
                data_frame_day[date] = []
            data_frame_day[date].append(row)

for key in data_frame_day:
    print(key)
    new_df = pd.DataFrame(data_frame_day[key], columns = head)
    new_df.to_csv(output_folder + '/' + key + '.csv', index = False)

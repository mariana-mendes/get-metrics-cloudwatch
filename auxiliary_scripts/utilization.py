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

for f in files:
    print(f)
    head = []
    data = []
    df = pd.read_csv(folder + '/' + f, index_col=0)
    head = df.columns.values
    index = list(df.index.values)
    df = df.drop_duplicates(subset=['timestamp','InstanceId','metricName'])
    for (i,row) in df.iterrows():
        metrics_ok = True
        if 'Average' in head:
            metrics_ok = (metrics_ok and row['Average'] <= 100)
        if 'Maximum' in head:
            metrics_ok = (metrics_ok and row['Maximum'] <= 100)
        if 'Minimum' in head:
            metrics_ok = (metrics_ok and row['Minimum'] <= 100)
        if 'Sum' in head:
            metrics_ok = (metrics_ok and row['Sum'] <= 100)
        
        if metrics_ok:
            data.append(row)
    print("Salvando...")
    new_df = pd.DataFrame(data, columns = head)
    new_df.to_csv(output_folder + '/' + f)

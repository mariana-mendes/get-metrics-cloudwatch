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
    df = pd.read_csv(folder + '/' + f, index_col=0)
    qnt_before = 0
    qnt_after = 0
    idx = 0
    data = []
    while len(df.index) > 0:
        idx = idx + (qnt_before - qnt_after)
        auto_scaling_group = df.loc[idx,'AutoscalingGroup']
        timestamp = df.loc[idx,'timestamp']
        qnt_before = len(df.index)
        df = df.drop(df[(df.timestamp == timestamp) & (df.AutoscalingGroup == auto_scaling_group)].index)
        qnt_after = len(df.index)
        data.append([timestamp, auto_scaling_group, (qnt_before - qnt_after)])
    new_df = pd.DataFrame(data, columns=['timestamp','AutoscalingGroup','Cont'])
    new_df.to_csv(output_folder + '/' + f)

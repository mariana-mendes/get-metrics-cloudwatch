from argparse import ArgumentParser
from datetime import datetime
import pandas as pd
import numpy as np
import os
import time

parser = ArgumentParser()
parser.add_argument('--folder', type=str)
parser.add_argument('--output_folder', type=str)

args = parser.parse_args()

folder = args.folder
output_folder = args.output_folder

ls_files = os.popen('ls {folder} | egrep "\.csv"'.format(folder = folder)).read()
files = ls_files.split("\n")
files.pop()

for f in files:
    df = pd.read_csv(folder + '/' + f)
    new_data = []
    for i in range(0,len(df.index)):
        description = df.loc[i,'Description']
        row = df.loc[i]
        arr = row.array
        if 'Detaching' in description or 'Attaching' in description:
            new_arr = np.array([*arr, 'User'])
        elif 'Terminating' in description or 'Launching' in description:
            new_arr = np.array([*arr, 'Automatic'])
        new_data.append(new_arr)
    new_df = pd.DataFrame(new_data, columns=['ActivityId','AutoScalingGroupName','Description','Cause','StartTime','EndTime','StatusCode','ActionActor'])
    new_df.to_csv(output_folder + '/' + f, index=False)
        
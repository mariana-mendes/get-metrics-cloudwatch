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
    data = []
    for i in range(0,len(df.index)):
        description = df.loc[i,'Description']
        row = df.loc[i]
        arr = row.array
        
        if 'Detaching' in description or 'Attaching' in description:
            new_arr = np.array([*arr, 'User'])
        else:  #elif 'Terminating' in description or 'Launching' in description:
            new_arr = np.array([*arr, 'Automatic'])
        
        if 'Detaching' in description or 'Terminating' in description:
            new_arr = np.array([*new_arr, 'Scale-in'])
        elif 'Attaching' in description or 'Launching' in description:
            new_arr = np.array([*new_arr, 'Scale-out'])
        else:
            new_arr = np.array([*new_arr, 'Update'])

        data.append(new_arr)
    new_df = pd.DataFrame(data, columns=['ActivityId','AutoScalingGroupName','Description','Cause','StartTime','EndTime','StatusCode','ActionActor','Scaling'])
    new_df = new_df.drop_duplicates(subset=['ActivityId'])
    new_df.to_csv(output_folder + '/' + f)

from argparse import ArgumentParser
from datetime import datetime
import pandas as pd
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

for f in files:
    df = pd.read_csv(folder + '/' + f)
    for i in range(0,len(df.index)):
        start_time = df.loc[i,'StartTime']
        start_date = time.strftime('%Y-%m-%d', time.localtime(start_time))
        if (not (start_date in data_frame_day.keys())):
            data_frame_day[start_date] = []
        data_frame_day[start_date].append(df.loc[i])
    
for key in data_frame_day:
    newDf = pd.DataFrame(data_frame_day[key], columns=['ActivityId','AutoScalingGroupName','Description','Cause','StartTime','EndTime','StatusCode'])
    newDf.to_csv(output_folder + '/' + key + '.csv', index=False)
    

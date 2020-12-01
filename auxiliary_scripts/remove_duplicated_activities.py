from argparse import ArgumentParser
from datetime import datetime
import pandas as pd
import os
import time

parser = ArgumentParser()
parser.add_argument('--folder', type=str,
        help='Folder where the duplicate files are')
parser.add_argument('--output_folder' type=str,
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
    df = df.drop_duplicates(subset=['ActivityId'])
    df.to_csv(output_folder + '/' + f, index=False)
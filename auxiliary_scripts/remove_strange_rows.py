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
    print(f, '-------------------------------------------------------------')
    fin = open(folder + f).read().splitlines()
    print(len(fin))
    if(len(fin) > 0):
        fout = open(output_folder + f, "wt")
        col = len(fin[0].split(','))
        for line in fin:
            data = line.split(',')
            if(len(data) != col):
                print(line + '\n')
            else:
                if line.split(',')[1] != '':
                    fout.write(line + '\n')
                else:
                    print(line + '\n')
                    
    else:
        print('O ARQUIVO ESTA VAZIO')
    print('\n\n')
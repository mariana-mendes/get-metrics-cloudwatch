from argparse import ArgumentParser
from pathlib import Path
import shutil
import os

parser = ArgumentParser()
parser.add_argument('--folder', type=str,
        help='Folder to be deleted')

args = parser.parse_args()

folder = args.folder

if(folder[len(folder)-1] == '/'):
    folder = folder[:-1] 
folderName = folder.split("/")[-1] + '.zip'

dirpath = Path(os.getcwd(), folder)
if dirpath.exists() and dirpath.is_dir():
    shutil.rmtree(dirpath)

if os.path.exists(folderName):
  os.remove(folderName)
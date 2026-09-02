import os 
import logging 
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="[%(asctime)s]: %(messsage)s: ")

list_of_files = [

    "src/__init__.py",
    "src/helper.py",
    "src/prompt.py",
    ".env",
    ".setup.py",
    "app.py",
    "test.py",
    "research/trails.ipynb",
    "store_index.py"    
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir,filename = os.path.split(filepath)
    if filedir !="":
        os.makedirs(filedir,exist_ok=True)
        logging.info(f" Creating Dir {filedir} for the file {filename}")
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath)==0):
        with open(filepath,'w') as f:
            pass
        logging.info(f"Creating Empty File : {filename}")
    else:
        logging.info(f"{filename} already exists and is not empty .Skipping ")

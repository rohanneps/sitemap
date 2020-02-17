import threading
import os
import pandas as pd

from http_parser.master_parser import MasterParser
from tools.general import *


INPUT_DIR = os.path.join('..','prod_count_below_100')
OUTPUT_DIR = 'output'
NUMBER_OF_THREADS = 8



def donwloadJson(folder_loc,url):

    print(url)
    output_file_name = url.split('/')[-1]
    OUTPUT_DIR = folder_loc
    try:
        MasterParser.parse(url, OUTPUT_DIR, output_file_name)
    except:
        pass


if __name__=='__main__':
# for roots, dirs, files in os.walk(INPUT_DIR):
    for __dir__ in ['3lab']:
        print(__dir__)
        dir_path = os.path.join(INPUT_DIR, __dir__)
        for sroots, sdirs, sfiles in os.walk(dir_path):
            for file in sfiles:
                print(file)
                file_path = os.path.join(dir_path, file)
                df = pd.read_csv(file_path, sep='\t')
                url_list = df['url'].tolist()
                
                folder_loc = os.path.join('output',__dir__)
                if not os.path.exists(folder_loc):
                    os.makedirs(folder_loc)

                for url in url_list:
                    donwloadJson(folder_loc, url)

        print('###########################')




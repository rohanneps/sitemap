import threading
from queue import Queue
from http_parser.master_parser import MasterParser
from tools.general import *
import pandas as pd
import os

# INPUT_FILE = 'sitemap.tsv'
INPUT_FILE = '/media/rohan/media/September/17th_cvdirectomexico/1.sitemap_parser/output/Step4/sitemap/sitemap_products_1.tsv'
# OUTPUT_DIR = 'output/entirelypets'
OUTPUT_DIR = 'output'
NUMBER_OF_THREADS = 10

queue = Queue()
create_dir(OUTPUT_DIR)
crawl_count = 0

df = pd.DataFrame()

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


def work():
    global crawl_count
    while True:
        url = queue.get()
        crawl_count += 1
        # print(url)
        # output_file_name = str(df[df['url']==url].iloc[0]['filename'])
        output_file_name = str(df[df['url']==url].iloc[0]['filename'])
        MasterParser.parse(url, OUTPUT_DIR, output_file_name)
        queue.task_done()


def create_jobs():
    for url in df['url'].tolist():
    # for url in df['url'].tolist():
        queue.put(url)
    queue.join()

if __name__ =='__main__':
    df = pd.read_csv(INPUT_FILE, sep='\t')
    # df = df.iloc[8000:]
    # df = df.iloc[100:300]
    if not 'filename' in df.columns.tolist():
        df['filename'] = range(1, len(df)+1)
        df.to_csv(INPUT_FILE, sep='\t', index=False)
    df = df.iloc[::-1]
    create_workers()
    create_jobs()

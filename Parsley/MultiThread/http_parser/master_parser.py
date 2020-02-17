from urllib.request import Request, urlopen
from http_parser.response_parser import ResponseParser
from http_parser.page_parser import PageParser
from tools.general import *
import os
import requests

# class MasterParser:

#     @staticmethod
#     def parse(url, output_dir, output_file):
#         if not os.path.exists(os.path.join(output_dir,'{}.json'.format(output_file))):
#             print('Crawling ' + url)
#             # resp = urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'}))
#             try:
#                 resp = urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'}))
#             except:
#                 return
#             resp_bytes = resp.read()
#             resp_parser = ResponseParser(resp)

#             page_parser = PageParser(resp_bytes.decode('latin1'))
#             # try:
#             #     page_parser = PageParser(resp_bytes.decode('utf-8'))
#             # except UnicodeDecodeError:
#             #     return
#             json_results = {
#                 'url': url,
#                 'status': resp.getcode(),
#                 'headers': resp_parser.headers,
#                 'tags': page_parser.all_tags
#             }
#             write_json(output_dir + '/' + output_file + '.json', json_results)
#         else:
#             print('Skipping done url '+url)

class MasterParser:
    @staticmethod
    def parse(url, output_dir, output_file):
        if not os.path.exists(os.path.join(output_dir,'{}.json'.format(output_file))):
            try:
                print('Crawling ' + url)
                resp = requests.get(url, headers = {'User-Agent': 'Mozilla/5.0'})
            except:
                print('Timeout for {}'.format(url))    
                return 
            resp_bytes = resp.content
            resp_parser = ResponseParser(resp)

            page_parser = PageParser(resp_bytes.decode('latin1'))
            
            json_results = {
                'url': url,
                'status': resp.status_code,
                'headers': resp_parser.headers,
                'tags': page_parser.all_tags
            }
            write_json(output_dir + '/' + output_file + '.json', json_results)
        else:
            print('Skipping done url '+url)
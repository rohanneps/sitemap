from urllib.request import Request, urlopen
from http_parser.response_parser import ResponseParser
from http_parser.page_parser import PageParser
from tools.general import *
import os

class MasterParser:

    @staticmethod
    def parse(url, output_dir, output_file):
        if not os.path.exists(os.path.join(output_dir,'{}.json'.format(output_file))):
            print('Crawling ' + url)
            try:
                resp = urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'}))
            except:
                return
            resp_bytes = resp.read()
            resp_parser = ResponseParser(resp)
            try:
                page_parser = PageParser(resp_bytes.decode('utf-8'))
            except UnicodeDecodeError:
                return
            json_results = {
                'url': url,
                'status': resp.getcode(),
                'headers': resp_parser.headers,
                'tags': page_parser.all_tags
            }
            write_json(output_dir + '/' + output_file + '.json', json_results)
        else:
            print('Skipping done url '+url)

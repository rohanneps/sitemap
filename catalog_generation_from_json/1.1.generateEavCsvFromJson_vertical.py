import os
import json
import pandas as pd
from collections import OrderedDict

JSON_DIR = ''	#Parsley Output DIR
OUTPUT_DIR = '1.eav_format_output'
CLIENT = 'alliedelec'

OUTPUT_CLIENT_DIR = os.path.join(OUTPUT_DIR, CLIENT)
if not os.path.exists(OUTPUT_CLIENT_DIR):
	os.makedirs(OUTPUT_CLIENT_DIR)

max_count = 0
min_count = 5000
file_tag_dict = {}

def parse_json(filepath, output_file_name):
	json_file = open(filepath)
	data = json.load(json_file)

	p_indx = 0
	global max_count, min_count
	df = pd.DataFrame(columns=['url','p_indx','tag','tag_value','s_indx','attr_name','attr_value'])

	url = data['url']

	URL_LIST = []
	P_INDEX_LIST = []
	TAG_LIST = []
	TAG_VALUE_LIST = []
	S_INDEX_LIST = []
	ATTR_LIST = []
	ATTR_VALUE_LIST = []




	for tag in data['tags']:
		if tag['name'] not in ['noscript','style','input','link','br','hr']:

			tag_name = tag['name']
			content = tag['content']

			if tag_name =='div' and not content:
				continue

			# if 'attributes' in tag.keys() and content is None:
			if 'attributes' in tag.keys():
				if tag['attributes']:
					s_index = 1
					for key in tag['attributes']:
						
						if key not in ['rel','data-image-id','target','data-index','data-src-retina','data-id','data-pin-do']:
							
							attr = key
							attr_content = tag['attributes'][key]

							# for attribute wiht more attribute value
							if ',' in attr_content and ':' in attr_content:
								# print(attr_content)
								sub_attr_list = attr_content.split(';')
								# print(sub_attr_list)
								sub_attr_list = list(filter(lambda x:x!='', sub_attr_list))
								TAG_LIST.append(tag_name)
								TAG_VALUE_LIST.append(content)
								URL_LIST.append(url)
								P_INDEX_LIST.append(p_indx)
								S_INDEX_LIST.append(s_index)
								ATTR_LIST.append(attr)
								ATTR_VALUE_LIST.append('-')

								for key_value_pair in sub_attr_list:
									# print(key_value_pair)

									if len(key_value_pair.split(':'))==2:
										sub_attr = (key_value_pair.split(':')[0]).strip()
										sub_attr_content = (key_value_pair.split(':')[1]).strip().replace("'",'')
									else:
										sub_attr = (key_value_pair.split(':')[0]).strip()
										sub_attr_content = (':'.join(key_value_pair.split(':')[1:])).strip()

									TAG_LIST.append(tag_name)
									TAG_VALUE_LIST.append(content)
									URL_LIST.append(url)
									P_INDEX_LIST.append(p_indx)
									S_INDEX_LIST.append(s_index)
									ATTR_LIST.append(sub_attr)
									ATTR_VALUE_LIST.append(sub_attr_content)

							else:
								TAG_LIST.append(tag_name)
								TAG_VALUE_LIST.append(content)
								URL_LIST.append(url)
								P_INDEX_LIST.append(p_indx)
								S_INDEX_LIST.append(s_index)
								ATTR_LIST.append(attr)
								ATTR_VALUE_LIST.append(attr_content)



							s_index += 1
				else:
					TAG_LIST.append(tag_name)
					TAG_VALUE_LIST.append(content)
					URL_LIST.append(url)
					P_INDEX_LIST.append(p_indx)
					S_INDEX_LIST.append('-')
					ATTR_LIST.append('-')
					ATTR_VALUE_LIST.append('-')
			else:
				TAG_LIST.append(tag_name)
				TAG_VALUE_LIST.append(content)
				URL_LIST.append(url)
				P_INDEX_LIST.append(p_indx)
				S_INDEX_LIST.append('-')
				ATTR_LIST.append('-')
				ATTR_VALUE_LIST.append('-')
			
			# print('---')
			# print(tag_name)
			# print(content)
			# print('-------------------')
			
		p_indx += 1

	df['url'] = URL_LIST
	df['p_indx'] =P_INDEX_LIST
	df['tag'] =TAG_LIST
	df['tag_value'] = TAG_VALUE_LIST
	df['s_indx'] =S_INDEX_LIST
	df['attr_name'] = ATTR_LIST
	df['attr_value'] = ATTR_VALUE_LIST

	df.to_csv(os.path.join(OUTPUT_CLIENT_DIR,output_file_name),sep='\t',index=False, encoding='utf-8')

if __name__=='__main__':
	for roots, dirs, files in os.walk(JSON_DIR):
		for file in files:
			print(file)
			if file !='.json' and '.py' not in file:
				df_file_name = '{}.tsv'.format(file.split('.')[0])
				filepath = os.path.join(JSON_DIR, file)
				print(filepath)
				
				try:
					parse_json(filepath, df_file_name)
				except:
					pass

				print('##############################')
			# exit(1)

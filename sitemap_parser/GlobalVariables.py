import os
import urllib.request
import requests
import gzip
import shutil
import xml.etree.ElementTree as ET
import pandas as pd

OUTPUT_DIR = 'output'

STEP1_DIR = os.path.join(OUTPUT_DIR, 'Step1')
STEP1_OUTPUT = os.path.join(STEP1_DIR, 'robots.txt')

STEP2_DIR = os.path.join(OUTPUT_DIR, 'Step2')

STEP3_DIR = os.path.join(OUTPUT_DIR, 'Step3')
STEP3_COMPRESSED_DIR = os.path.join(STEP3_DIR,'compressed')
STEP3_TEMPUNCOMP_DIR = os.path.join(STEP3_DIR,'temp_uncompressed')

STEP4_DIR = os.path.join(OUTPUT_DIR, 'Step4')
STEP5_DIR = os.path.join(OUTPUT_DIR, 'Step5')

def downloadSourceCodeFromUrl(url,file_location):
	req = urllib.request.Request(
			url, 
			data=None, 
			headers={
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
			}
		)

	site=urllib.request.urlopen(req)
	data=site.read().decode('utf-8')
	# print(data)
	# print(type(data))
	with open(file_location,'w') as file:
		file.writelines(data)
		file.close()

def downloadSitemapFile(sitemap, output_dir):
	if ' ' in sitemap:
		url = sitemap.split(' ')[1]
	else:
		url = sitemap
	# print(url)
	filename_ext = url.split('/')[-1]
	# ext = filename_ext.split('.')[1]
	file_name = os.path.join(output_dir, filename_ext)
	downloadSourceCodeFromUrl(url, file_name)
	return filename_ext

def downloadCompressedFile(url,file_location):
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
	with open(os.path.join(file_location), "wb") as f:
		# r = requests.get(url, headers=headers)
		r = requests.get(url, headers=headers)
		f.write(r.content)

def copyUnzipCompressedFile(src, dest):
	# print(src)
	# print(dest)
	with gzip.open(src, 'rb') as f_in:
		with open(dest, 'wb') as f_out:
			try:
				shutil.copyfileobj(f_in, f_out)
			except Exception as e:
				print(str(e))
				# For cases where the file is not compressed but saved as .gz
				if src.split('/')[-1].endswith('gz'):
					shutil.copy(src, dest)

				
def parseCompleteXml(xml_file_path):
	URL_LIST = []
	tree = ET.parse(xml_file_path)  
	root = tree.getroot()
	# print(root.tag)
	for elem in root:     # sitemap element
		for child in elem:
			if '}' in child.tag:
				child_tag = child.tag.split('}')[1]
			else:
				child_tag = child.tag
			# print(child_tag)			
			
			if child_tag == 'loc':					# xml element with nested sitemap or url
				child_tag_text = child.text
				# print(child_tag_text)
				URL_LIST.append(child_tag_text)
		# print('----------------------------------------------------')
	return URL_LIST


def parseIncompleteXml(xml_file_path):
	URL_LIST = []
	try:
		for event, elem in ET.iterparse(xml_file_path, events=('end', )):
			# print(elem.tag)
			print(elem)
			if '}' in elem.tag:
				child_tag = elem.tag.split('}')[1]
			else:
				child_tag = elem.tag
			if child_tag =='loc':
				URL_LIST.append(elem.text)
			print('---------------')
	except:
		pass
	return URL_LIST

# For each xml file
def parseXML(output_folder_location, xml_file_path, output_filename):
	df = pd.DataFrame(columns=['url'])
	print(xml_file_path)
	URL_LIST = parseCompleteXml(xml_file_path)
	# try:
	# 	URL_LIST = parseCompleteXml(xml_file_path)
	# 	print('Complete XML schema')
	# except:
	# 	URL_LIST = parseIncompleteXml(xml_file_path)
	# 	print('Incomplete XML schema')
	
	df['url'] = URL_LIST
	# df['short_text'] = df['url'].apply(lambda x: x.split('/')[-1]).str.replace('-',' ')
	df.to_csv(os.path.join(output_folder_location,'{}.tsv'.format(output_filename)), index=False, sep='\t')
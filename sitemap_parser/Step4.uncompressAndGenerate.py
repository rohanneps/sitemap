import os
import pandas as pd
import xml.etree.ElementTree as ET
from GlobalVariables import STEP3_COMPRESSED_DIR,STEP3_TEMPUNCOMP_DIR, STEP4_DIR, copyUnzipCompressedFile


'''
For compressed files from Step3.
To be used when we don't want the uncompressed sitemap file to persist
'''
def parseCompleteXml(xml_file_path):
	URL_LIST = []
	tree = ET.parse(xml_file_path)  
	root = tree.getroot()
	# print(root.tag)
	for elem in root:     # sitemap element
		for child in elem:
			if '}' in child.tag:
				child_tag = child.tag.split('}')[1]
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
			if '}' in elem.tag:
				child_tag = elem.tag.split('}')[1]
				if child_tag =='loc':
					# print(child_tag)
					# print(elem.text)
					URL_LIST.append(elem.text)
	except:
		pass
	# print(len(URL_LIST))
	return URL_LIST

# For each xml file
def parseXML(output_folder_location, xml_file_path, output_filename):
	df = pd.DataFrame(columns=['url','short_text'])
	try:
		URL_LIST = parseCompleteXml(xml_file_path)
		print('Complete XML schema')
	except:
		URL_LIST = parseIncompleteXml(xml_file_path)
		print('Incomplete XML schema')
	df['url'] = URL_LIST
	df['short_text'] = df['url'].apply(lambda x: x.split('/')[-1]).str.replace('-',' ')
	df.to_csv(os.path.join(output_folder_location,'{}.tsv'.format(output_filename)), index=False, sep='\t')
	


def uncompressAndGenerateFile(folder_location,compfile):
	src = os.path.join(folder_location, compfile)
	step3_folder_location = os.path.join(STEP3_TEMPUNCOMP_DIR)
	filename = compfile.replace('.gz','')
	dest = os.path.join(step3_folder_location,filename)
	print(src)
	print(dest)

	if not os.path.exists(dest):
		copyUnzipCompressedFile(src, dest)
	uncomp_filename = filename.split('.')[0]
	file_ext = filename.split('.')[-1]
	if not (os.path.exists(os.path.join(STEP4_DIR,'{}.tsv'.format(uncomp_filename)))):
		if file_ext.lower() == 'xml':
			parseXML(STEP4_DIR, dest, uncomp_filename)
		os.remove(dest)
	else:
		print('TSV file already present')

if __name__ == '__main__':
	value= 'sitemap_slideshare{}.xml'

	for roots, dirs, files in os.walk(STEP3_COMPRESSED_DIR):
		for compfile in files: 
			# if file == 'sitemap_topic.xml' or file=='sitemap.xml':
			print('###################')
			print(compfile)
			uncompressAndGenerateFile(STEP3_COMPRESSED_DIR,compfile)
			
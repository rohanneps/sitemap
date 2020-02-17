import os
from GlobalVariables import STEP2_DIR, STEP3_DIR, downloadSitemapFile, STEP3_COMPRESSED_DIR, downloadCompressedFile, copyUnzipCompressedFile
import xml.etree.ElementTree as ET
import re


def parseXML(folder_location, sitemap_file):
	xml_file_location = os.path.join(folder_location,sitemap_file)

	# create directory if it doesn't exist
	step3_folder_location = os.path.join(STEP3_DIR, sitemap_file.split('.')[0])
	if not os.path.exists(step3_folder_location):
		os.makedirs(step3_folder_location)

	tree = ET.parse(xml_file_location)  
	root = tree.getroot()
	# print(root.tag)
	for elem in root:     # sitemap element
		for child in elem:
			if '}' in child.tag:
				child_tag = child.tag.split('}')[1]
			print(child_tag)
			child_tag_text = child.text
			print(child_tag_text)
			
			if child_tag == 'loc':					# xml element with nested sitemap or url

				sitemap_ext = child_tag_text.split('.')[-1]
				#clean up newline characters from extension
				sitemap_ext = re.sub('(\n$)|(\r$)|(\r\n$)','',sitemap_ext)
				if sitemap_ext.lower() == 'xml' or '.xml?' in child_tag_text:
					try:
						downloadSitemapFile(child_tag_text, step3_folder_location)
					except Exception as e:
						print(str(e))
				elif sitemap_ext.lower() == 'gz':
					
					filename = child_tag_text.split("/")[-1]
					src = os.path.join(STEP3_COMPRESSED_DIR,filename)
					dest = os.path.join(step3_folder_location,filename.replace('.gz',''))
					print(dest)
					if not os.path.exists(src):
						print('downloading compressed file')
						downloadCompressedFile(child_tag_text, src)
						# copyUnzipCompressedFile(src, dest)
			print('----------------')
			# exit(1)

		print('---####-----------###-------------##')
		# exit(1)

if __name__ == '__main__':
	value= 'sitemap_slideshare{}.xml'

	for roots, dirs, files in os.walk(STEP2_DIR):
		for file in files:
			# if file == 'sitemap_topic.xml' or file=='sitemap.xml':
			print('###################')
			print(file)
			parseXML(STEP2_DIR,file)


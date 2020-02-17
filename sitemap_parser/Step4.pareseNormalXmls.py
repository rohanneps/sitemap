import os
import xml.etree.ElementTree as ET
from GlobalVariables import STEP3_DIR, STEP4_DIR, parseXML
import pandas as pd

'''
For uncompressed files from step3.
'''


# For all xml files in a folder
def generateUrlFile(folder_loc):
	step4_output_dir = os.path.join(STEP4_DIR, folder_loc)
	if not os.path.exists(step4_output_dir):
		os.makedirs(step4_output_dir)

	step3_output_dir = os.path.join(STEP3_DIR, folder_loc)

	value= 'sitemap_slideshare{}.xml'
	for roots, dirs, files in os.walk(step3_output_dir):
		# files=['sitemap_slideshare7.xml','sitemap_slideshare6.xml','sitemap_slideshare1.xml']
		for file in files:
			print(file)
			filename = file.split('.')[0]
			file_ext = file.split('.')[-1]
			if file_ext.lower() == 'xml' or 'xml?from' in file_ext.lower() or '?target=sitemap' in file :
				parseXML(step4_output_dir, os.path.join(step3_output_dir, file), filename)
				print('##########################-')
			# exit(1)

if __name__ == '__main__':
	# for roots, dirs, files in os.walk(STEP3_DIR):
	for sdir in ["sitemap"]:
		if sdir != 'compressed' and sdir != 'temp_uncompressed':
			print(sdir)
			generateUrlFile(sdir)
			print('##############----------####################------------#############')




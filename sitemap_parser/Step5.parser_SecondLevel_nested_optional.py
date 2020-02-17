## Optional, for cases where the 4th step yields flat file of sitemaps

from GlobalVariables import STEP5_DIR, STEP4_DIR, downloadSitemapFile, parseXML
import pandas as pd
import os

if not os.path.exists(STEP5_DIR):
	os.makedirs(STEP5_DIR)


def generateXMLFile(file_path, output_dir):
	df = pd.read_csv(file_path, sep='\t')

	if not os.path.exists(OUTPUT_DIR):
		os.mkdir(OUTPUT_DIR)


	def generateSitemapFile(row):
		nonlocal output_dir
		sitemap_url = row['url']
		file = downloadSitemapFile(sitemap_url, output_dir)
		filename = '_'.join(file.split('.')[:-1])
		file_ext = file.split('.')[-1]
		if file_ext.lower() == 'xml' or 'xml?from' in file_ext.lower() or '?target=sitemap' in file :
			parseXML(output_dir, os.path.join(output_dir,file), filename)
			os.remove(os.path.join(output_dir,file))
			print('##########################-')
			

	df.apply(generateSitemapFile, axis=1)



if __name__ == '__main__':

	for sdir in ["sitemap"]:
		INPUT_DIR = os.path.join(STEP4_DIR, sdir)
		OUTPUT_DIR = os.path.join(STEP5_DIR, sdir)
		for roots, dirs, files in os.walk(INPUT_DIR):
			for file in files:
				print(file)
				file_path = os.path.join(INPUT_DIR, file)
				generateXMLFile(file_path, OUTPUT_DIR)
				print('------------------------------------')


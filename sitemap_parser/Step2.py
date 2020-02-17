import os
from GlobalVariables import STEP1_OUTPUT, STEP2_DIR, downloadSitemapFile



if __name__ == '__main__':

	with open(STEP1_OUTPUT, 'r') as robot_file:
		lines = robot_file.read()
		lines = lines.split('\n')
		lines =list(filter(lambda x:x!='', lines)) # removing empty strings
		sitemap_lines =list(filter(lambda x: 'sitemap:' in x.lower(), lines)) # filtering only sitemaps
		print(sitemap_lines)

		for sitemap in sitemap_lines:
			print('#############################')
			print(sitemap)
			downloadSitemapFile(sitemap, STEP2_DIR)
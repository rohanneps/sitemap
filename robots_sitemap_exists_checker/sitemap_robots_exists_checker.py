import os
import requests
import argparse

def getProperUrlFormat(sitename):
	if 'http://' not in sitename and 'https://' not in sitename:
		url = 'https://{}'.format(sitename)
	else:
		url = sitename
	url = url.replace('http://','https://')
	return url


def check_if_robots_sitemap_exists(url):
	robots_url = '{}/robots.txt'.format(url)
	robots_exists = False
	sitemap_exists = False

	# First Check for Robots
	try:
		res = requests.get(robots_url, timeout=10)
	except:
		# insecure url check
		try:
			robots_url = robots_url.replace('https://','http://')
			res = requests.get(robots_url, timeout=10)
		except:
			return 'Site Not accessible', 'Site Not accessible'

	if res.status_code != 200 and 'http://' not in robots_url:
		res = requests.get(robots_url.replace('https://','http://'), timeout=10)

	# robots exists check
	if res.status_code == 200:
			robots_exists = True
			lines = res.content.decode('latin-1')
			lines = lines.split('\n')
			lines =list(filter(lambda x:x!='', lines)) # removing empty strings
			sitemap_lines =list(filter(lambda x: 'sitemap:' in x.lower(), lines)) # filtering only sitemaps
			if len(sitemap_lines)>0:
				sitemap_exists = True

	# Direct Site sitemap check
	if not sitemap_exists:
		sitemap_url = '{}/sitemap.xml'.format(url)
		try:
			res = requests.get(sitemap_url, timeout=10)
		except:
			# insecure check
			try:
				res = requests.get(sitemap_url.replace('https://','http://'), timeout=10)
			except:
				pass
		# ensuring that the response is xml
		if res.status_code ==  200 and 'xml' in res.headers['Content-Type']:
			sitemap_exists = True
	return robots_exists, sitemap_exists



def check_robots_sitemap(url):
	url = getProperUrlFormat(url)
	print(url)
	robots_exists, sitemap_exists = check_if_robots_sitemap_exists(url)
	print('robots_exists, sitemap_exists:{},{}'.format(robots_exists, sitemap_exists))


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("--url", help="Url of which sitemap and robots is to be checked", type=str)
	args = parser.parse_args()
	url = args.url
	check_robots_sitemap(url)
	
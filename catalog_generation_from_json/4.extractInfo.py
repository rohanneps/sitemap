import os
import pandas as pd
from Product import Product

INPUT_DIR = '3.filtered_output'
OUTPUT_DIR = '4.extract_info'

def get_product_title(product_df):
	return ''


def get_product_information(url, product_df):
	product_detail = {'url': url}

	product = Product(product_df, url)
	product.extract_info()
	return product.get_product_details()
	

if __name__=='__main__':
	input_file = 'alliedelec_filtered.tsv'
	df = pd.read_csv(os.path.join(INPUT_DIR,input_file), sep='\t')
	# df = df.iloc[:2]
	# product_catalog_df = pd.DataFrame(columns=['url','page_title','name','price','image','sku'])
	product_catalog_df = pd.DataFrame(columns=['url','name','price','image','sku'])
	# df = df[df['url']=='https://www.accentclothing.com/women-c5/womens-footwear-c187/shoes-c6/ugg-australia-m158']

	# df = df[df['url']=='https://www.accentclothing.com/women-c5/womens-clothing-c186/trousers-c67/religion-prime-snake-skin-p1272#attribute[3]=11:attribute_2_=22']
	Product.get_product_name_tagindex_from_title(df)

	for prod_url in df['url'].unique().tolist():
		print(prod_url)
		product_df = df[df['url']==prod_url]
		product_detail = get_product_information(prod_url, product_df)
		product_catalog_df = product_catalog_df.append(product_detail, ignore_index=True)

	product_catalog_df = product_catalog_df.rename(columns={'name':'item_name','image':'image_url','url':'product_url'})
	product_catalog_df.to_csv(os.path.join(OUTPUT_DIR,input_file.replace('filtered','catalog')), sep='\t', index=False)
import os
import pandas as pd

INPUT_DIR = os.path.join('1.eav_format_output','tackle')
# INPUT_DIR = os.path.join('2.merged_output')
OUTPUT_DIR = os.path.join('4.tagindexToCol','output')
UPPER_LOWER_LIMIT = 400

CPI_PRICE_LIST = []

col_df = pd.read_csv(os.path.join('4.tagindexToCol','input','{}.csv'.format('tackle')), sep=',')
col_df = col_df.fillna(value='')


catalog_output_df = pd.DataFrame(columns=['url'])

def getTagValue(prod_url_df, tag, tag_index, col_name, upper_lower_limit=0):

	if upper_lower_limit< UPPER_LOWER_LIMIT:
		try:
			# print(tag)
			if tag =='img':
				# print(upper_lower_limit)
				tag_value = prod_url_df[(prod_url_df['p_indx']>=(tag_index-upper_lower_limit)) &(prod_url_df['p_indx']<=(tag_index+upper_lower_limit)) & (prod_url_df['attr_name']=='src')].iloc[0]['attr_value']
				# print(tag_value)
			# elif col_name =='price':
			# 	tag_value = prod_url_df[(prod_url_df['p_indx']>=(tag_index-upper_lower_limit)) &(prod_url_df['p_indx']<=(tag_index+upper_lower_limit)) & (prod_url_df['tag_value'].str.contains("$",regex=False))].iloc[0]['tag_value']
			else:
				tag_value = prod_url_df[(prod_url_df['p_indx']>=(tag_index-upper_lower_limit)) &(prod_url_df['p_indx']<=(tag_index+upper_lower_limit))].iloc[0]['tag_value']

		except:
			tag_value = None
		# print(tag_value)
		if tag_value:
			return tag_value
		else:
			return getTagValue(prod_url_df,tag, tag_index, col_name, upper_lower_limit+1)
	else:
		return 'No value'


def getPriceDetails(product_detail, price_df):
	cnt = 1
	for price_val in price_df.tag_value:
		# print(price_val)
		if len(price_val) <50 and cnt <=5:
			product_detail['Price_{}'.format(cnt)] = price_val
			cnt += 1

	return product_detail


def getCategoryFromBreadcrumb(df, breadcrumb_pos):
	cat_breadcrumb = ''
	counter = breadcrumb_pos + 1
	
	while True:
		tag_value = df[df['p_indx']==counter].iloc[0]['tag_value']
		counter += 1
		if tag_value !='':
			cat_breadcrumb = '{}/{}'.format(cat_breadcrumb, tag_value)
		else:
			return cat_breadcrumb


def getTagIndexToAttribute(df, url):
	product_detail = {}
	product_detail['url'] = url
	global col_df
	# print(col_df.columns)
	for index, row in col_df.iterrows():
		tag = row['tag']
		tag_index = row['index']
		col_name = row['col_name']
		attr_name = row['attr_name']
		attr_val = row['attr_value']

		# print(col_name)
		# print(attr_val)
		if tag=='' and attr_name=='' :
			product_detail[col_name] = ''
		else:

			if attr_name =='':
				prod_url_df = df[(df['url']==url) &(df['tag']==tag)]

				if col_name != 'Price':
					tag_value = getTagValue(prod_url_df,tag, tag_index, col_name)
					product_detail[col_name] = tag_value
				else:
					# print('price')
					price_df = prod_url_df[prod_url_df['tag_value'].str.contains("$",regex=False)]
					price_df = price_df.sort_values(['p_indx'], ascending=True)
					product_detail = getPriceDetails(product_detail, price_df)
			else:

				if tag!='':
					prod_url_df = df[(df['tag']==tag)&(df['attr_name']==attr_name)&(df['attr_value']==attr_val)]
				else:
					prod_url_df = df[(df['attr_name']==attr_name)&(df['attr_value']==attr_val)]
				
				if col_name != 'Category':

					need_to_process = True
					try:
						value_tag = prod_url_df.iloc[0]['tag']
					except:
						need_to_process = False

					if need_to_process:
						# if value_tag =='meta':
						value_p_index = prod_url_df.iloc[0]['p_indx']
						try:
							product_detail[col_name] = df[(df['p_indx']==value_p_index) & (df['attr_name']=='content')].iloc[0]['attr_value']
						except:
							product_detail[col_name] = prod_url_df.iloc[0]['tag_value']
						# else:
						# 	product_detail[col_name] = prod_url_df.iloc[0]['tag_value']
					else:
						product_detail[col_name] = 'Value Not Found'
				else:

					if tag =='':
						try:
							breadcrumb_pos = prod_url_df.iloc[0]['p_indx']
							product_detail[col_name] = getCategoryFromBreadcrumb(df, breadcrumb_pos)
						except:
							product_detail[col_name] = ''
					else:
						breadcrumb = []
						for value in prod_url_df['tag_value'].tolist():
							if value != '':
								breadcrumb.append(value)
						product_detail[col_name] = '>'.join(breadcrumb)

	return product_detail
	print('------------------------')

	
	


def getAttributeData(row):
	# link = row['resolved link']
	link = row['url']
	filename = row['filename']
	print(link)
	print('---------')
	print(filename)

	vertical_file_path = os.path.join(INPUT_DIR, '{}.tsv'.format(filename))

	if  not os.path.exists(vertical_file_path):
		product_detail= {}
		product_detail['url'] = link
		for index, row in col_df.iterrows():
			col_name = row['col_name']
			product_detail[col_name] = 'Request ISSUE'

	else:
		prod_df = pd.read_csv(vertical_file_path, sep='\t')
		prod_df = prod_df.fillna(value='')
		product_detail = getTagIndexToAttribute(prod_df,link)
	

	global catalog_output_df
	catalog_output_df = catalog_output_df.append(product_detail, ignore_index=True)

	print('#############################################')
	# CPI_PRICE_LIST.append(cpi_link_price)


if __name__ == '__main__':
	cpi_file = 'target.tsv'
	# filaneme = '{}.tsv'.format(file)
	cpi_df = pd.read_csv(os.path.join(cpi_file), sep=',')
	# cpi_df = cpi_df.iloc[:3]

	# cpi_df = cpi_df[cpi_df['filename']==26]
	# print(len(cpi_df))
	cpi_df = cpi_df.fillna(value='')

	cpi_df.apply(getAttributeData, axis=1)

	global catalog_output_df
	# catalog_output_df.to_csv('test.csv',index=False, sep=',')
	output_df =  pd.merge(cpi_df, catalog_output_df, how='left', left_on='url', right_on='url')
	# cpi_df['CPI_Price'] = CPI_PRICE_LIST

	output_df.to_csv(os.path.join(OUTPUT_DIR,cpi_file), index=False, sep=',')


	


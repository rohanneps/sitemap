import os
import pandas as pd

INPUT_DIR = os.path.join('2.merged_output')
# INPUT_DIR = os.path.join('2.merged_output')
OUTPUT_DIR = os.path.join('4.tagindexToCol','output')
UPPER_LOWER_LIMIT = 40



def getTagValueFromIndex(prod_url_df, tag, tag_index, col_name, upper_lower_limit=0):

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
			return getTagValueFromIndex(prod_url_df,tag, tag_index, col_name, upper_lower_limit+1)
	else:
		return 'No value'

def getImgValueFromAttribute(prod_url_df,tag, attr_name, attr_val, col_name):
	# try:
	img_index = prod_url_df[(prod_url_df['attr_name']==attr_name) & (prod_url_df['attr_value']==attr_val)].iloc[0]['p_indx']
	img_src = prod_url_df[(prod_url_df['attr_name']=='src') & (prod_url_df['p_indx']==img_index)].iloc[0]['attr_value']
	return img_src
	# except:
		# return ''


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
	counter = breadcrumb_pos
	
	last_index = df.iloc[-1]['p_indx']

	while counter<last_index:
		try:
			tag_value = df[df['p_indx']==counter].iloc[0]['tag_value']
			counter += 1
		except:
			counter += 1
			continue
		counter += 1
		if tag_value !='':
			cat_breadcrumb = '{}/{}'.format(cat_breadcrumb, tag_value)
		# else:
			# return cat_breadcrumb

	return cat_breadcrumb

def get_subset_df_with_text(text_like_df, text_to_search):
	text_like_df = text_like_df.fillna(value='')
	text_like_df = text_like_df[text_like_df['tag_value'].str.lower().str.contains(text_to_search.lower())]
	return text_like_df


def getTagIndexToAttribute(indivial_eav_location, col_df,filaneme4):
	
	catalog_output_df = pd.DataFrame(columns=['Product URL'])
	
	for roots, dirs, files in os.walk(indivial_eav_location):
		for file in files:
			file_path = os.path.join(indivial_eav_location, file)
			df = pd.read_csv(file_path, sep='\t')
			url = df.url.unique().tolist()[0]
			print(url)
			product_detail = {}
			product_detail['Product URL'] = url

			for index, row in col_df.iterrows():
				tag = row['tag']
				tag_index = row['index']
				col_name = row['col_name']
				attr_name = row['attr_name']
				attr_val = row['attr_value']
				text_like = row['text_like']

				print(col_name)
				# print(tag)
				# print(attr_name)
				# print(attr_val)
				if tag=='':
					product_detail[col_name] = ''

				elif tag=='meta':
					prod_meta_df = df[(df['url']==url) &(df['tag']==tag)]
					# print(len(prod_meta_df))
					p_index = prod_meta_df[(prod_meta_df['attr_name']==attr_name) & (prod_meta_df['attr_value']==attr_val)].iloc[0]['p_indx']

					product_detail[col_name] = prod_meta_df[(prod_meta_df['p_indx']==p_index) & (prod_meta_df['attr_name']=='content')].iloc[0]['attr_value']

				else:

					if attr_name =='':
						prod_url_df = df[(df['url']==url) &(df['tag']==tag)]

						if col_name != 'Price':

							# For cases where text like field is provided
							if text_like !='':
								prod_url_df = get_subset_df_with_text(prod_url_df, text_like)

							if tag_index!='':
								tag_value = getTagValueFromIndex(prod_url_df,tag, tag_index, col_name)
								product_detail[col_name] = tag_value
							else:
								# For cases where text like field is provided
								try:
									product_detail[col_name] = prod_url_df.iloc[0]['tag_value']
								except:
									product_detail[col_name] = ''
						else:
							# print('price')
							price_df = prod_url_df[prod_url_df['tag_value'].str.contains("$",regex=False)]
							price_df = price_df.sort_values(['p_indx'], ascending=True)
							product_detail = getPriceDetails(product_detail, price_df)
					else:
						prod_tag_url_df = df[(df['url']==url) &(df['tag']==tag)&(df['attr_name']==attr_name)&(df['attr_value']==attr_val)]
						
						if attr_name == 'class':
							prod_tag_url_df = df[(df['url']==url) &(df['tag']==tag)&(df['attr_name']==attr_name)&(df['attr_value'].str.contains(attr_val))]	
						
						# For cases where text like field is provided
						if text_like !='':
								prod_tag_url_df = get_subset_df_with_text(prod_tag_url_df, text_like)

						if col_name != 'Category':
							try:
								if tag =='img':
									prod_url_df = df[(df['url']==url) &(df['tag']==tag)]
									product_detail[col_name] = getImgValueFromAttribute(prod_url_df,tag, attr_name, attr_val, col_name)
								else:
									product_detail[col_name] = prod_tag_url_df.iloc[0]['tag_value']
							except Exception as e:
								print(str(e))
								product_detail[col_name] = ''
						else:
							prod_df = df[(df['url']==url)]
							breadcrumb_pos = prod_tag_url_df.iloc[0]['p_indx']
							product_detail[col_name] = getCategoryFromBreadcrumb(prod_tag_url_df, breadcrumb_pos)
				print('-----')
			print('------------------------')
			

			catalog_output_df = catalog_output_df.append(product_detail, ignore_index=True)
	catalog_output_df.to_csv(os.path.join(OUTPUT_DIR, filaneme), index=False, sep='\t')


if __name__ == '__main__':

	file = 'nike'
	filaneme = '{}.tsv'.format(file)

	col_df = pd.read_csv(os.path.join('4.tagindexToCol','input','{}.csv'.format('nike_scheme')), sep=',')
	col_df = col_df.fillna(value='')
	print(col_df.columns)
	indivial_eav_location = os.path.join('1.eav_format_output','nike')
	# indivial_eav_location = os.path.join('1.eav_format_output','test')
	getTagIndexToAttribute(indivial_eav_location,col_df, filaneme)


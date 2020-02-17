import re
# from textblob import TextBlob
# from nltk.corpus import stopwords


class Product():

	# static_variable
	has_product_tagindex_match = False
	product_tag = ''
	product_tag_index = 0
	upper_lower_limit = 100
	price_regex_pattern = '(\$)?( )?((\d)+,)*(\d)+(.(\d)*)?'
	# STOPWORDS = set(stopwords.words("english"))

	# WordsToRemove = ['the', 'an', 'a', 'up', 'there', 'are', 'at', 'by', 'This','to', 'of', 'that', 'you', 
 #                'your', 'is', 'are', 'or', 'It', 'will', 'as', 'with', 'on', 'from', 'can', 'be','and',
 #                's', 'whatever', 'EL','for', 'in', 'up', 'out', 'this', 'just', 'go', 'us', 'not', 'it']

	def __init__(self, product_df, url):
		self.url = url
		self.product_df = product_df.fillna(value='')
		self.product_details = {'url':self.url}
		self.page_title_len = None

	@staticmethod
	def get_product_name_tagindex_from_title(input_df):
		for prod_url in input_df['url'].unique().tolist():
			product_df = input_df[input_df['url']==prod_url]
			try:
				title = product_df[product_df['tag']=='title'].iloc[0]['tag_value']
				if ' | ' in title:
					title = title.split('|')[0].strip()

				

				product_name_df = product_df[(product_df['tag_value']==title) & (product_df['tag']!='title')]
				if len(product_name_df)>0:
					Product.has_product_tagindex_match = True
					if 'h1' in product_name_df['tag'].unique().tolist():
						product_name_df = product_df[(product_df['tag_value']==title) & (product_df['tag']=='h1')]
						if 'category' in product_name_df['attr_value'].iloc[0]:
							product_name_df = product_df[(product_df['tag_value']==title) & (product_df['tag']!='h1')]

					if len(product_name_df)>0:
						Product.product_tag = product_name_df.iloc[0]['tag']
						Product.product_tag_index = product_name_df.iloc[0]['p_indx']
					# print(Product.product_tag, Product.product_tag_index)
					# print(prod_url)
					break
					return		# Existing once match is found
			except:
				continue

	def get_product_page_title(self):
		try:
			title = self.product_df[self.product_df['tag']=='title'].iloc[0]['tag_value']
		except:
			title = ''

		self.page_title_len = len(title)
		self.product_page_title = title

	def get_product_image(self):
		img_df = self.product_df[(self.product_df['tag']=='img') & (self.product_df['attr_name']=='src')]
		img_df = img_df[~(img_df['attr_value'].str.contains('gif'))]
		# self.product_details['image'] = ','.join(img_df.attr_value.unique().tolist())
		img_list = img_df.attr_value.unique().tolist()
		if len(img_list)> 0:
			self.product_details['image'] = img_list[0]
		else:
			self.product_details['image'] = ''

	def get_product_name(self):
		# get product name from title tag and index match
		# print(Product.has_product_tagindex_match)
		product_name = None
		if Product.has_product_tagindex_match:
			# print('From title tag value')
			try:
				product_name = self.product_df[(self.product_df['p_indx']>=(Product.product_tag_index-Product.upper_lower_limit)) &(self.product_df['p_indx']<=(Product.product_tag_index+Product.upper_lower_limit)) & (self.product_df['tag']==Product.product_tag)].iloc[0]['tag_value']
			except:
				product_name = ''
		else:

			# checking presence of h1 tag for Product Title
			if 'h1' in self.product_df['tag'].unique().tolist():
				product_name = self.product_df[self.product_df['tag']=='h1'].iloc[0]['tag_value']
			if not product_name:
				product_name = self.product_page_title.split('|')[0].strip()
				# self.product_df['tag_value_length'] = self.product_df['tag_value'].apply(len)

				# if self.page_title_len and self.page_title_len> 0:
				# 	prod_name_df = self.product_df[(self.product_df['tag_value_length']>=self.page_title_len -2) & (self.product_df['tag_value_length']<=self.page_title_len +2) & (self.product_df['tag']!='title')]
				# 	if len(prod_name_df) > 0:
				# 		product_name = prod_name_df['tag_value'].iloc[0]
				# 	else:
				# 		# getting longest string
				# 		product_name = self.product_df.sort_values(by=['tag_value_length'], ascending=False).iloc[0]['tag_value']
				# else:
				# 	product_name = self.product_df.sort_values(by=['tag_value_length'],ascending=False).iloc[0]['tag_value']
		# print(product_name)
		self.product_details['name'] = product_name



	def get_product_price(self):
		
		self.price_list = []
		
		# checking for price attribute value
		potential_price_value_list = self.product_df[self.product_df['attr_value'].isin(['price'])]['tag_value'].str.strip().tolist()
		if len(potential_price_value_list)>0:
			for value in potential_price_value_list:
				if '$' in value and len(value)<15:
					self.price_list.append(value)
				elif value =='':
					continue	
				else:
					try:
						float(value)
						self.price_list.append(value)
					except:
						pass

				if len(self.price_list)>=2:
						break

		if len(self.price_list) <2:
			# checking for dollar sign
			potential_price_value_list = self.product_df[~(self.product_df['tag'].isin(['title','li','h1','h2','h3','h4','img']))]['tag_value'].str.strip().tolist()
			for value in potential_price_value_list:
				match_obj = re.search(Product.price_regex_pattern,value)
				if match_obj:
					if '$' in match_obj.group():
						self.price_list.append(match_obj.group())
						if len(self.price_list)>=2:
							break
		# print(self.price_list)
		self.price_list = list(set(self.price_list))
		self.product_details['price'] = ','.join(self.price_list)


	def get_tag_value_from_index(self,p_idx):
		try:
			return self.product_df[(self.product_df['p_indx']==p_idx)].iloc[0]['tag_value']
		except:
			return ''

	def check_for_sku(self, value):
		value_is_sku = False

		if not ' ' in value and value !='' and len(value)>2 and len(value)<27 and value not in self.price_list and '$' not in value:
			value_is_sku = True	

		if '#' in value:
			value_is_sku = True

		return value_is_sku


	def get_product_sku(self):
		# potential_sku_value_listing = self.product_df[~(self.product_df['tag'].isin(['img','meta','title','h1']))][~(self.product_df['tag_value'].str.contains(' '))]['tag_value'].unique().tolist()
		# sku_list = []
		# for value in potential_sku_value_listing:
		# 	text_blob = TextBlob(value)
		# 	WordsFromBlobs = text_blob.words
		# 	for Words in WordsFromBlobs:
		# 		DictionaryValue = Words.definitions[:1]
		# 		if len(DictionaryValue) == 0:
		# 			sku_list.append(value)

		# self.product_details['sku'] = ','.join(sku_list)

		# 2nd loginc for sku extraction, assuming sku is near price

		sku_list =[]

		potential_sku_value_list = self.product_df[self.product_df['attr_value'].isin(['sku'])]['tag_value'].str.strip().tolist()
		if len(potential_sku_value_list)>0:
			for tag_value in potential_sku_value_list:
				if self.check_for_sku(tag_value):
					# print('a')
					sku_list.append(tag_value)
					break

		# print(sku_list)
		for price in self.price_list:
			
			# print(price)
			price_pindx_list = self.product_df[self.product_df['tag_value'].str.contains(price.replace('$','\$'))]['p_indx'].unique().tolist()
			for price_indx in price_pindx_list:
				# print(price_indx)
				cnt = 1
				while cnt <= 20:
					sku_indx = price_indx - cnt
					rev_sku_indx = price_indx + cnt
					# print(sku_indx)
					tag_value = self.get_tag_value_from_index(sku_indx)
					rev_tag_value = self.get_tag_value_from_index(rev_sku_indx)
					# print(tag_value)
					# print(rev_tag_value)
					if self.check_for_sku(tag_value):
						# print('a')
						sku_list.append(tag_value)
						break
					elif self.check_for_sku(rev_tag_value):
						# print('b')
						sku_list.append(rev_tag_value)
						break
					cnt += 1
					
		self.product_details['sku'] = ', '.join(list(set(sku_list)))

	def extract_info(self):
		self.get_product_page_title()
		self.get_product_image()
		self.get_product_name()
		self.get_product_price()
		self.get_product_sku()

	def get_product_details(self):
		return self.product_details


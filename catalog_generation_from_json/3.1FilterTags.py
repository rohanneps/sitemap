import os
import pandas as pd

FILTER_DF = pd.read_csv('WordsToFilter.tsv', sep='\t')
IMAGE_RECURRING_LIMIT = 20

INPUT_DIR = '2.merged_output'
CLIENT = 'alliedelec'
OUTPUT_DIR = '3.filtered_output'

def remove_recurring_images(df):
	img_df = df[df['tag']=='img']
	image_src_group = img_df[['url','attr_value']].groupby('attr_value',as_index=False).count()
	# image_src_group = image_src_group.sort_values(by=['url'],ascending=False)
	image_src_group = image_src_group[image_src_group['url']> IMAGE_RECURRING_LIMIT]
	df = df[~(df['attr_value'].isin(image_src_group['attr_value'].tolist())) | (df['tag']=='title')]
	return df

if __name__=='__main__':
	df = pd.read_csv(os.path.join(INPUT_DIR,'{}.tsv'.format(CLIENT)), sep='\t')
	df = df[(df['tag_value'].notnull()) | ((df['tag']=='img') &(df['attr_name']=='src'))]
	df = df[(df['tag_value']!='') | ((df['tag']=='img') &(df['attr_name']=='src'))]
	df = df.fillna(value='')
	df['tag_value_len']=df['tag_value'].apply(len)
	df = df[(df['tag_value_len']<=150) | ((df['tag']=='img') &(df['attr_name']=='src'))]
	
	df = df[df['tag'].isin(['title','h1','h2','h3','span','strong','p','div','img'])]

	groupby_tag_value = df[['url','tag_value']].groupby('tag_value',as_index=False).count()
	# groupby_tag_value = groupby_tag_value.sort_values(by=['url'],ascending=False)
	groupby_tag_value = groupby_tag_value[groupby_tag_value['tag_value']!='']
	upper_threshold = len(df.url.unique().tolist())*3	# count number of unique urls

	groupby_tag_value = groupby_tag_value[groupby_tag_value['url']<=upper_threshold]
	df = df[(df['tag_value'].isin(groupby_tag_value['tag_value'].tolist())) | (df['tag_value']=='')]
	
	del df['tag_value_len']
	df = remove_recurring_images(df)

	df = df[~(df['tag_value'].str.lower().str.strip().isin(FILTER_DF['words_to_filter'].str.lower().str.strip().tolist()))]


	df.to_csv(os.path.join(OUTPUT_DIR,'{}_filtered.tsv'.format(CLIENT)), sep='\t', index=False)
import os
import pandas as pd

INPUT_DIR = '1.eav_format_output'
CLIENT = 'alliedelec'
INPUT_CLIENT_DIR = os.path.join(INPUT_DIR,CLIENT)
OUTPUT_DIR = '2.merged_output'

if __name__=='__main__':
	output_df = pd.DataFrame(columns=['url','p_indx','tag','tag_value','s_indx','attr_name','attr_value'])
	for roots, dirs, files in os.walk(os.path.join(INPUT_DIR,CLIENT)):
		for file in files:
			print(file)
			try:
				df = pd.read_csv(os.path.join(INPUT_DIR, CLIENT,file), sep='\t')
			except:
				continue
			print(df.columns.tolist())
			output_df = output_df.append(df, ignore_index=True)


			print('###################################')

	# output_df = output_df[(output_df['tag_value']!='') & (output_df['tag_value'].notnull()) & (output_df['tag_value']!='▾')]
	output_df.to_csv(os.path.join(OUTPUT_DIR,'{}.tsv'.format(CLIENT)),index=False, sep='\t')
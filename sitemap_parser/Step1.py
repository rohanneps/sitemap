
import os
from GlobalVariables import OUTPUT_DIR, STEP1_DIR, STEP1_OUTPUT,STEP2_DIR,STEP3_DIR,STEP3_TEMPUNCOMP_DIR, STEP3_COMPRESSED_DIR,downloadSourceCodeFromUrl, STEP4_DIR


URL = "https://www.slideshare.net/robots.txt"

def makedirs():
	if not os.path.exists(OUTPUT_DIR):
		os.makedirs(OUTPUT_DIR)

	if not os.path.exists(STEP1_DIR):
		os.makedirs(STEP1_DIR)
	
	if not os.path.exists(STEP2_DIR):
		os.makedirs(STEP2_DIR)

	if not os.path.exists(STEP3_DIR):
		os.makedirs(STEP3_DIR)

	if not os.path.exists(STEP3_COMPRESSED_DIR):
		os.makedirs(STEP3_COMPRESSED_DIR)

	if not os.path.exists(STEP3_TEMPUNCOMP_DIR):
		os.makedirs(STEP3_TEMPUNCOMP_DIR)
		
	if not os.path.exists(STEP4_DIR):
		os.makedirs(STEP4_DIR)

if __name__=='__main__':
	makedirs()
	downloadSourceCodeFromUrl(URL, STEP1_OUTPUT)



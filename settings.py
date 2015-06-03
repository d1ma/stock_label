import os
import random
import logging

PERCENT_TRAINING = .75
SEED = 0

##### [ FILEPATH SETTINGS ] #####
home = os.path.expanduser("~")
vc_dir = "Dropbox/Data Scrape of VC/"
training_dir = "NLP Training Set"
full_input_dir = os.path.join(home, vc_dir, training_dir)

def set_up():
	random.seed(SEED)
	logging.basicConfig(level=logging.DEBUG)
	
	## [ Insert other set up required ] ##

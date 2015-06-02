import os
from os.path import expanduser

import re
home = expanduser("~")
vc_dir = "Dropbox/Data Scrape of VC/"
training_dir = "NLP Training Set"
full_input_dir = os.path.join(home, vc_dir, training_dir)
from tagged_file import *
from util import *

class Main():
	def __init__(self):
		self.tfiles = read_directory(full_input_dir)

	def id_to_tfile(self, id):
		return TFile.id_to_tfile.get(id)


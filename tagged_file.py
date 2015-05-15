""" 

tagged_file.py

represents a file with tags. You feed in a file that contains tags after useful phrases
that are labelled like this "fragment"[[Tag: value]]

"""

import re
import string
import os

from sentence import *
from util import *




class TFile(object):
	def __init__(self, filename):
		with open(filename) as f:
			self.raw = filter_ascii(f.read())
			self.name = filename
			self.raw_clean = re.sub(regex, "", self.raw)
			self.tags = []
			self.tag_pos = []
			self.sentences = []

			for s in parser.tokenize(self.raw):
				self.sentences += [Sentence(s)]


			running_length = 0
			for m in re.finditer(regex, self.raw):
				self.tags += [m]
				sp = m.span()
				adjusted_pos = sp[0] - running_length
				self.tag_pos += [adjusted_pos]
				adjusted_pos += sp[1] - sp[0]

	@property
	def num_tags(self):
		return len(self.tags)

	def find_numbers(self):
		comma_int = r'\d+(?:,\d+)+'
		matches = re.findall(comma_int, self.raw_clean)
		return matches


def read_directory(path):
	tagged_files = []
	for f in os.listdir(path):
		name = os.path.join(path,f)
		if os.path.isfile(name):
			tagged_files += [TFile(name)]

	return tagged_files

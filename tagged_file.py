""" 

tagged_file.py

represents a file with tags. You feed in a file that contains tags after useful phrases
that are labelled like this "fragment"[[Tag: value]]

"""

import re
import string
import os
import json
import numpy as np

from sentence import *
from util import *
CB = 200
CF = 100

labels = {'Total Shares': "TS", 'Series FV Preferred Shares': 'PS', 'Series C2 Preferred Shares': 'PS', 'Series D Preferred Shares': 'PS', 'Series 1 Preferred Shares': 'PS', 'Series Seed1 Preferred Shares': 'PS', 'Series Seed Preferred Shares': 'PS', 'Common Shares': 'CS', 'Series E1 Preferred Shares': 'PS', 'Series A1 Preferred Shares': 'PS', 'Class A Common Shares': 'CS', 'Series 5B2 Preferred Shares': 'PS', 'Series AA Preferred Shares': 'PS', 'Series B2 Preferred Shares': 'PS', 'Series A Preferred Shares': 'PS', 'Series E Preferred Shares': 'PS', 'Series A2 Preferred Shares': 'PS', 'Series B1 Preferred Shares': 'PS', 'Series C Preferred Shares': 'PS', 'Series F1 Preferred Shares': 'PS', 'Series 5 Preferred Shares': 'PS', 'Series 4 Preferred Shares': 'PS', 'Series B Preferred Shares': 'PS', 'Series A3 Preferred Shares': 'PS', 'Series 5A Preferred Shares': 'PS', 'Series 3 Preferred Shares': 'PS', 'Series Z Preferred Shares': 'PS', 'Total Shares': 'TS', 'Series 2 Preferred Shares': 'PS', 'Series D1 Preferred Shares': 'PS', 'Series BB Preferred Shares': 'PS', 'Series 5B1 Preferred Shares': 'PS', 'Series Junior Preferred Shares': 'PS', 'Preferred Shares': 'PS', 'Series C1 Preferred Shares': 'PS', 'Class B Common Shares': 'CS', 'Series FT Preferred Shares': 'PS'}
labels_min = {'Total Shares': "TS", 'Common Shares': "CS", 'Preferred Shares': "PS"}
# output_vals = {"n/a": 0, "TS": 1, "PS": 2, "CS": 3}
output_vals =  {"n/a": "n/a", "TS": "TS", "PS": "PS", "CS": "CS"}

class Number(object):
	def __init__(self, numstr, pos, label, context, original_file):
		self.match = numstr
		try: 
			self.num = int(numstr.replace(',', ''))
		except:
			print "Not able to process number %s" % numstr
			self.num = None
		self.pos = pos
		self.label = label
		self.context = context
		self.feature_vector = None
		self.tfile = original_file

	def __repr__(self):
		tagged = "not tagged" if self.label == None else "tagged"
		return "%s at %i (%s)" % (self.match, self.pos, tagged)

	def set_feature_vector(self, vector):
		self.feature_vector = vector

	@property
	def output_value(self):
		if self.label:
			short = labels_min.get(self.label.tag_key, "n/a")
			val = output_vals.get(short, 0)
			return val
		else:
			return output_vals.get("n/a", 0)


class Tag(object):
	def __init__(self, tag, pos, context):
		self.tag_raw = tag
		self.tag_clean = tag[2:-2]
		split = self.tag_clean.split(":")
		self.tag_key = split[0] ## descriptive phrase
		self.tag_val = split[1] ## the number
		self.pos = pos
		self.context = context # tuple (chunk, sentences)

	@property
	def is_number_tag(self):
		match_key = re.search(comma_int, self.tag_key)
		match_val = re.search(comma_int, self.tag_val)
		if match_key or match_val:
			return True
		else:
			return False

	def __repr__(self):
		return "%s -> %s @ %i" % (self.tag_key, self.tag_val, self.pos)



class TFile(object):
	featurizer = None
	id_to_tfile = {}

	def __init__(self, filename, index_id):
		with open(filename) as f:
			""" 
			Already implemented: 
			--------------------
			raw: as read in from file
			name: filename
			raw_clean: without the labels
			tags: the tags, in order of appearance
			numbers: Number elements
			"""
			self.id = index_id
			TFile.id_to_tfile[index_id] = self
			self.raw = filter_ascii(f.read())
			self.filename = filename
			directory, self.basename = os.path.split(filename)
			self.raw_clean = re.sub(regex, "", self.raw)
			self.tags = []
			self.pos_to_tag = {}
			self.numbers = []

			# self.sentences = []

			# for s in parser.tokenize(self.raw):
			# 	self.sentences += [Sentence(s)]

			running_length = 0
			for m in re.finditer(regex, self.raw):
				sp = m.span()
				adjusted_pos = sp[0] - running_length

				chunk_before = self.raw_clean[max(0, adjusted_pos - CB): adjusted_pos]
				chunk_after = self.raw_clean[adjusted_pos: adjusted_pos + CF]
				tag_obj = Tag(m.group(), adjusted_pos, get_context(chunk_before, chunk_after))
				self.tags += [tag_obj]
				self.pos_to_tag[tag_obj.pos] = tag_obj
				running_length += sp[1] - sp[0]

			for num_match in re.finditer(comma_int, self.raw_clean):
				num = num_match.group()
				label = self.closest_label(num_match.end())
				num_position = num_match.end()
				chunk_before = self.raw_clean[max(0, num_position - CB): num_position]
				chunk_after = self.raw_clean[num_position: num_position + CF]
				context = get_context(chunk_before, chunk_after)
				if label and abs(label.pos - num_match.end()) < 50 :
					if label.tag_key == num or label.tag_val == num:
						self.numbers += [Number(num, num_match.end(), label, context, self)]
				else:
					self.numbers += [Number(num, num_match.end(), None, context, self)]


	@classmethod
	def assignFeatures(cls, FeaturizerClass, training_corpus):
		""" 
		Creates the featurizer class that is responsible for handling all 
		of the mappings for the passed in corpus
		"""
		cls.featurizer = FeaturizerClass(training_corpus)

	def tagged_numbers(self):
		return filter(lambda x: x.label != None, self.numbers)


	def tagged_numbers_str(self):
		nums = self.tagged_numbers()
		num_with_tag = [(n.output_value, n.match) for n in nums]
		r = {}
		for (description, val) in num_with_tag:
			if (description == "n/a"):
				continue
			current = r.get(description, [])
			current += [val]
			r[description] = current

		return str(r)


	def to_json(self):
		d = {'filename': self.name, 'numbers': [ob.__dict__ for ob in self.numbers],
		 	'tags': [ob.__dict__ for ob in self.tags]}
		return json.dumps(d)


	def closest_label(self, number_loc):
		try: 
			return min(self.tags, key=lambda x:abs(x.pos-number_loc))
		except ValueError:
			return None

	@property
	def num_tags(self):
		return len(self.tags)


	def describe(self):
		r = "### [ Numbers ] ###\n"
		r += "\n".join([str(n) for n in self.numbers]) + "\n"
		r += "### [ Tags ] ###\n"
		r += "\n".join([str(t) for t in self.tags]) + "\n"
		r += "### [ Raw ] ###\n"
		r += self.raw_clean
		return r

	def __repr__(self):
		return "(%i numbers, %i tags, %i tagged numbers)" % (len(self.numbers), len(self.tags), len(self.tagged_numbers()))


def read_directory(path):
	tagged_files = []
	i = 0
	for f in os.listdir(path):
		name = os.path.join(path,f)
		if os.path.isfile(name):
			tagged_files += [TFile(name, i)]
			i += 1

	return tagged_files




def get_context(chunk_before, chunk_after):
	""" try to get sentence perhaps? """
	before_start = chunk_before.find(" ")
	after_end = chunk_after.rfind(" ")
	before_stripped = chunk_before[before_start:]
	after_stripped = chunk_after[0:after_end]
	

	return before_stripped, after_stripped

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
comma_int = r'\d+(?:,\d+)+'


class Number(object):
	def __init__(self, numstr, pos, label):
		self.match = numstr
		try: 
			self.num = int(numstr.replace(',', ''))
		except:
			print "Not able to process number %s" % numstr
			self.num = None
		self.pos = pos
		self.label = label

	def __repr__(self):
		tagged = "not tagged" if self.label == None else "tagged"
		return "%s at %i (%s)" % (self.match, self.pos, tagged)


class Tag(object):
	def __init__(self, tag, pos):
		self.tag_raw = tag
		self.tag_clean = tag[2:-2]
		split = self.tag_clean.split(":")
		self.tag_key = split[0]
		self.tag_val = split[1]
		self.pos = pos

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
	def __init__(self, filename):
		with open(filename) as f:
			""" 
			Already implemented: 
			--------------------
			raw: as read in from file
			name: filename
			raw_clean: without the labels
			tags: the tags, in order of appearance
			sentences: a list of sentence objects

			To implement:
			------------
			numbers: Number elements
			"""
			self.raw = filter_ascii(f.read())
			self.name = filename
			self.raw_clean = re.sub(regex, "", self.raw)
			self.tags = []
			self.pos_to_tag = {}
			
			self.sentences = []

			for s in parser.tokenize(self.raw):
				self.sentences += [Sentence(s)]

			running_length = 0
			for m in re.finditer(regex, self.raw):
				sp = m.span()
				adjusted_pos = sp[0] - running_length
				tag_obj = Tag(m.group(), adjusted_pos)
				self.tags += [tag_obj]
				self.pos_to_tag[tag_obj.pos] = tag_obj
				running_length += sp[1] - sp[0]

			self.numbers = []
			for num_match in re.finditer(comma_int, self.raw_clean):
				num = num_match.group()
				label = self.closest_label(num_match.end())
				if label and abs(label.pos - num_match.end()) < 20:
					self.numbers += [Number(num, num_match.end(), label)]
				else:
					self.numbers += [Number(num, num_match.end(), None)]


	def tagged_numbers(self):
		return filter(lambda x: x.label != None, self.numbers)




	def closest_label(self, number_loc):
		try: 
			return min(self.tags, key=lambda x:abs(x.pos-number_loc))
		except ValueError:
			return None

	@property
	def num_tags(self):
		return len(self.tags)

	def find_numbers(self):
		matches = re.findall(comma_int, self.raw_clean)
		return matches

	def __repr__(self):
		return "(%i numbers, %i tags, %i tagged numbers)" % (len(self.numbers), len(self.tags), len(self.tagged_numbers()))


def read_directory(path):
	tagged_files = []
	for f in os.listdir(path):
		name = os.path.join(path,f)
		if os.path.isfile(name):
			tagged_files += [TFile(name)]

	return tagged_files

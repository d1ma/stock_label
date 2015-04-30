import nltk
import string
import re
import numpy as np

parser = nltk.data.load('tokenizers/punkt/english.pickle')
filter_ascii = lambda s: filter(lambda x: x in string.printable, s)
regex = "\[\[(.*?)\]\]"

class SentenceFeature(object):
	""" Given a Sentence object, should return a vector of properties """

	def __init__(self, sentence):
		self.sentence = sentence
					

	def vectorize(self):
		raise NotImplementedError( "Should implement this by subclassing")

	def outputDimension(self):
		sh = self.vectorize().reshape(-1).shape
		return sh[0]

class ContainsCommaNumber(SentenceFeature):
	def __init__(self, sentence):
		self.sentence = sentence

	def vectorize(self):
		""" returns np vector (one dimension) with number of matches for comma sep value """
		comma_int = r'\d+(?:,\d+)+'
		num_matches = len(re.findall(comma_int, self.sentence.raw_clean))
		return np.array([num_matches])

class SentenceLength(SentenceFeature):
	def __init__(self, sentence):
		self.sentence = sentence

	def vectorize(self):
		""" returns np vector """
		return np.array([len(self.sentence.raw_clean.split(" "))])

class ContainsStockOrShare(SentenceFeature):
	def __init__(self, sentence):
		self.sentence = sentence

	def vectorize(self):
		synonyms = ["share", "stock"]
		matches = [self.sentence.raw_clean.find(x) for x in synonyms]
		contains = len([x for x in matches if x > 0]) > 0
		return np.array([contains])


class Sentence(object):
	def __init__(self, sentence):
		self.raw = sentence
		self.raw_clean = re.sub(regex, "", self.raw)
		self.tags = []
		self.tag_pos = []
		running_length = 0
		for m in re.finditer(regex, sentence):
			self.tags += [m]
			sp = m.span()
			adjusted_pos = sp[0] - running_length
			self.tag_pos += [adjusted_pos]
			adjusted_pos += sp[1] - sp[0]

	def __repr__(self):
		return self.show_tag_location()

	def show_tag_location(self):
		if self.is_interesting():
			tags_temp = [0] + self.tag_pos + [len(self.tag_pos)]
			return "^".join([self.raw_clean[tags_temp[r]: tags_temp[r+1]] for r in range(len(tags_temp)-1)])
		else:
			return self.raw_clean

	def to_vector(self, features):
		feature_vectors = [f(self).vectorize() for f in features]
		return np.concatenate(feature_vectors)

	def is_interesting(self):
		return len(self.tags) > 0

	def is_interesting_as_int(self):
		return 1 if self.is_interesting() else 0

	
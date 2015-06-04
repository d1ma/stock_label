import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

class SumsToOther(object):
	
	def __init__(self, tfiles, vectorizer=None):
		pass

	def get_feature_vector(self, tfile_numbers):
		"""
			0. n/a
			1. sums to one of the other numbers
		"""
		int_repr = [tn.num for tn in tfile_numbers]
		result = []
		for i in int_repr:
			int_greater = [n for n in int_repr if n > i]
			found = False

			for greater_candidate in int_greater:

				remainder = greater_candidate - i

				if remainder in int_repr:
					found = True
					break

			if found:
				result += [1]
			else:
				result += [0]
		return np.array(result).reshape(-1,1)

class ContainsOthers(object):
	""" 
		0. n/a
		1. sum of a subset of numbers
	"""
	def __init__(self, tfiles, vectorizer=None):
		pass

	def get_feature_vector(self, tfile_numbers):
		int_repr = [tn.num for tn in tfile_numbers]
		sums = set([])
		for i in int_repr:
			int_greater = [n for n in int_repr if n > i]
			found = False

			for greater_candidate in int_greater:
				remainder = greater_candidate - i
				if remainder in int_repr:
					sums.add(greater_candidate)
					break

		result = []
		for i in int_repr:
			if i in sums:
				result += [1]
			else:
				result += [0]
		return np.array(result).reshape(-1,1)



class NumberOrder(object):
	""" 
	feature representing how big this number is related to other numbers in this
	file
	"""
	def __init__(self, tfiles, vectorizer=None):
		pass

	def get_feature_vector(self, tfile_numbers):
		""" Returns a column """

		as_ints = [num.num for num in tfile_numbers]
		as_ints_sorted = sorted(as_ints, reverse=True)
		return np.array([as_ints_sorted.index(num) for num in as_ints]).reshape(-1,1)


	def get_feature_names(self):
		return [u"Number Order"]


class BagOfWords(object):
	vocab = [u'common',
			u'common shares',
			u'common stock',
			u'number',
			u'number of',
			u'of',
			u'of shares',
			u'preferred',
			u'preferred shares',
			u'preferred stock',
			u'shares',
			u'stock',
			u'stock preferred']

	@classmethod
	def get_vectorizer(cls):
		''' features are assigned to each number in tfiles '''
		vectorizer = CountVectorizer(min_df = 1, binary=True, ngram_range=(1,2), vocabulary=BagOfWords.vocab)
		return vectorizer

	
class BagOfWordsBefore(object):
	def __init__(self, tfiles, vectorizer=None):
		self.tfiles = tfiles
		self.vectorizer = vectorizer

	def get_feature_vector(self, tfile_numbers):
		corpus_before = [n.context[0] for n in tfile_numbers]

		return self.vectorizer.fit_transform(corpus_before).toarray()

	def get_feature_names(self):
		return ['B: ' + word for word in self.vectorizer.get_feature_names()]

class BagOfWordsAfter(object):
	def __init__(self, tfiles, vectorizer=None):
		self.tfiles = tfiles
		self.vectorizer = vectorizer

	def get_feature_vector(self, tfile_numbers):
		corpus_after = [n.context[1] for n in tfile_numbers]
		return self.vectorizer.fit_transform(corpus_after).toarray()

	def get_feature_names(self):
		return ['A: ' + word for word in self.vectorizer.get_feature_names()]


class FeatureConstructor(object):
	tfile_feature_classes = [BagOfWordsBefore, BagOfWordsAfter, NumberOrder, ContainsOthers, SumsToOther]


	def __init__(self, tfiles):
		self.tfiles = tfiles
		self.v = BagOfWords.get_vectorizer()
		self.features = [f(tfiles, self.v) for f in FeatureConstructor.tfile_feature_classes]


	def get_feature_matrix(self, tfile):
		running = None
		if len(self.features) > 0:
			running = self.features[0].get_feature_vector(tfile.numbers)
		for f in self.features[1:]:
			running = np.append(running, f.get_feature_vector(tfile.numbers), axis=1)

		return running

	def get_feature_matrix_and_numbers(self, tfile):
		matrix = self.get_feature_matrix(tfile)
		numbers = tfile.numbers
		return (matrix, numbers)

	def get_feature_matrix_and_output_vector(self, tfile):
		matrix = self.get_feature_matrix(tfile)
		outputs = np.array([num.output_value for num in tfile.numbers])
		return (matrix, outputs)

	def get_feature_names(self):
		names_per_feature = [feat.get_feature_names() for feat in self.features]
		return [name for names in names_per_feature for name in names]


	def assign_feature_vectors(self, tfile):
		feature_array = self.get_feature_matrix(tfile)
		for row, number in zip(feature_array, tfile.numbers):
			number.set_feature_vector(row)

	def __repr__(self):
		return "<FeatureConstructor> with %i files, %i features, %i total columns" % (len(self.tfiles), 
			len(self.features), len(self.get_feature_names()))








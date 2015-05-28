import numpy as np
from sklearn.feature_extraction.text import CountVectorizer


class NumberOrder(object):
	""" 
	feature representing how big this number is related to other numbers in this
	file
	"""
	def __init__(self, tfiles, other=none):
		pass

	def get_feature_vector(self, tfile_numbers):
		as_ints = [num.num for num in tfile_numbers]
		as_ints_sorted = sorted(as_ints)
		return np.column_stack(np.array([as_ints_sorted.index(num) for num in as_ints]))


	def get_feature_names(self, tfile_numbers):
		return ["Number Order"]


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
		vectorizer = CountVectorizer(min_df = 1, binary=True, ngram_range=(1,2), vocabulary=vocab)
		return vectorizer

	
class BagOfWordsBefore(object):
	def __init__(self, tfiles, other=None):
		self.tfiles = tfiles
		self.vectorizer = other

	def get_feature_vector(self, tfile_numbers):
		corpus_before = [n.context[0] for n in tfile_numbers]

		return vectorizer.fit_transform(corpus_before).toarray()

	def get_feature_names(self, tfile_numbers):
		return ['B: ' + word for word in vectorizer.get_feature_names()]

class BagOfWordsAfter(object):
	def __init__(self, tfiles, other=None):
		self.tfiles = tfiles
		self.vectorizer = other

	def get_feature_vector(self, tfile_numbers):
		corpus_after = [n.context[1] for n in tfile_numbers]
		return vectorizer.fit_transform(corpus_after).toarray()

	def get_feature_names(self, tfile_numbers):
		return ['A: ' + word for word in vectorizer.get_feature_names()]


class FeatureConstructor(object):

	tfile_feature_classes = [BagOfWordsBefore, BagOfWordsAfter, NumberOrder]

	def __init__(self, tfiles):
		self.tfiles = tfiles
		self.features = [f(tfiles) for f in tfile_feature_classes]
		self.v = BagOfWords.get_vectorizer()

	def get_vector_matrix(self, tfile):
		''' 
		returns an np matrix, where each row is a feature vector
		corresponding to each number in the tfile 
		'''
		running = None
		if len(self.features) > 0:
			running = self.features[0].get_feature_vector(tfile.numbers)

		for f in self.features[1:]:
			np.append(running, f.get_feature_vector(tfile.numbers))

		return runnin

	def get_feature_names(self, tfile):
		names_per_feature = [feat.get_feature_names() for feat in self.features]
		return [name for names in names_per_feature for name in names]


	def assign_feature_vectors(self, tfile):
		'''
		calls set_feature_vector on each of the numbers in the tfile
		'''
		feature_array = self.get_feature_matrix(tfile)
		for row, number in zip(feature_array, tfile.numbers):
			number.set_feature_vector(row)










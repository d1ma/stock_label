import os
from os.path import expanduser

import re
from tagged_file import read_directory, TFile
from featurize import FeatureConstructor
from classifier import MainClassifier
from settings import full_input_dir
from dependency import StanfordParser
import logging
# import click


class Main():
	def __init__(self):
		# logging.info('Main. Connecting to the Stanford-parser server (running locally)')
		# self.dep = StanfordParser()
		self.dep = None
		logging.info('Main. Reading directory')
		self.tfiles = read_directory(full_input_dir)
		logging.info('Main. Constructing Featurizer')
		self.featurizer = FeatureConstructor(self.tfiles, self.dep)
		logging.info('Main. Constructing Classifier')
		self.cl = MainClassifier(self.tfiles, self.featurizer)
		self.last_result = None

	def id_to_tfile(self, id):
		return TFile.id_to_tfile.get(id)

	def equals(self, other):
		return self.tfiles == other.tfiles and self.featurizer == other.featurizer and self.cl == other.cl

	def get_predictions_per_file(self):
		"""
		Returns a list of tuples: tfile and predictions made by each classifier
		"""
		exclude = ["n/a"]
		return zip(self.tfiles, [self.cl.predict_for_file(t, exclude) for t in self.tfiles])

	def get_models(self):
		return [str(m) for m in self.cl.trained_clf]

	def predict_class_for_each_number(self, tfile):
		pred = self.cl.predict_class_for_each_number(tfile)
		output = zip(tfile.numbers, pred)
		return output

	def get_probabilities_for_each_classifier_and_number(self, tfile):
		class_probabilities = self.cl.class_probabilities_by_classifier(tfile)
		output = []
		for o in class_probabilities:
			cl, p = o
			p_with_num = zip(tfile.numbers, p)
			output += [(cl, p_with_num)]

		logging.debug(output)		
		return output

	def get_cl_report(self):
		return self.cl.get_report()

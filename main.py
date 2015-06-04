import os
from os.path import expanduser

import re
from tagged_file import read_directory, TFile
from featurize import FeatureConstructor
from classifier import MainClassifier
from settings import full_input_dir
import logging



class Main():
	def __init__(self):
		logging.debug('Main. Reading directory')
		self.tfiles = read_directory(full_input_dir)
		logging.debug('Main. Constructing Featurizer')
		self.featurizer = FeatureConstructor(self.tfiles)
		logging.debug('Main. Constructing Classifier')
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
		logging.debug(str(tfile.numbers))
		pred = self.cl.predict_class_for_each_number(tfile)
		logging.debug("Predicted values for this file %s" % str(pred))
		output = zip(tfile.numbers, pred)
		logging.debug("Outputting %s" % str(output))
		return output
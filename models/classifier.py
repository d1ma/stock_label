from settings import *
from sklearn.metrics import confusion_matrix, classification_report
from sklearn import metrics, cross_validation
import numpy as np

class GeneralModel(object):
	def class_probabilities(self, X):
		return self.clf.predict_proba(X)

	def predict(self, X):
		if X.size == 0:
			return None
		return self.clf.predict(X)

	def predict_cv(self, X, y):
		if X.size == 0:
			return None
		return cross_validation.cross_val_predict(self.clf, X, y)

	def get_report(self, X_all, y_all, cv=5):
		if X_all.size == 0:
			return None
		predict = cross_validation.cross_val_predict(self.clf, X_all, y_all, cv=5 )
		return classification_report(y_all, predict)

	def predict_for_file(self, X, raw_nums=None):
		""" If raw_nums are given, will use those instead of the featurization when
		reversing the dictionary """
		if X.size == 0:
			return {}

		# import pdb; pdb.set_trace()
		predictions = self.predict(X)
		chosen_repr = raw_nums if (raw_nums != None) else X
		return_dict = {}
		for num, p in zip(chosen_repr, predictions):
			current_val = return_dict.get(p, [])
			current_val += [num]
			return_dict[p] = current_val
		return return_dict



class SVM(GeneralModel):
	def __init__(self, X, y):
		# create and train the SVM model
		from sklearn import svm
		self.model = svm.SVC(probability=True)
		self.clf = self.model.fit(X, y)

	def __repr__(self):
		return "SVM"



class DecisionTree(GeneralModel):
	def __init__(self, X, y):
		from sklearn import tree
		self.model = tree.DecisionTreeClassifier()
		self.clf = self.model.fit(X, y)

	def __repr__(self):
		return "Decision Tree"

	def class_probabilities(self, X):
		return self.clf.predict_proba(X)

class RandomForest(GeneralModel):
	def __init__(self, X, y):
		from sklearn.ensemble import RandomForestClassifier
		self.model = RandomForestClassifier(n_estimators=300)
		self.clf = self.model.fit(X, y)

	def __repr__(self):
		return "Random Forest"

	def class_probabilities(self, X):
		return self.clf.predict_proba(X)


used_classifiers = [SVM, RandomForest, DecisionTree]

class MainClassifier():

	def class_probabilities_by_classifier(self, tfile):
		X, y = self.featurizer.get_feature_matrix_and_output_vector(tfile)
		r = []
		for c in self.trained_clf:
			r += [c.class_probabilities(X)]
		return zip(self.trained_clf, r)







	def predict_class_for_each_number(self, tfile):
		X = self.featurizer.get_feature_matrix(tfile)
		r = []
		for c in self.trained_clf:
			d = c.predict(X)
			r += [d]
		return zip(*r)









	def predict_for_file(self, tfile, exclude=[]):
		"""
		Returns a dictionary with keys being the classifier names.
		Each  value is a dictionary containing classes as keys, mapping to values
		"""
		X, y = self.featurizer.get_feature_matrix_and_output_vector(tfile)
		r = {}
		for c in self.trained_clf:
			d = c.predict_for_file(X, [n.match for n in tfile.numbers])
			for i in exclude:
				if i in d:
					del d[i]
			r[str(c)] = d
		return r



	def get_report(self):
		return [(cl, cl.get_report(self.all_features, self.all_labels)) for cl in self.trained_clf]



	def __init__(self, tfiles, featurizer):
		"""
		Transforms the input tfiles into vectors using featurizer
		"""
		### [ Featurize the classifier ] ###
		# random.shuffle(tfiles)
		self.featurizer = featurizer
		self.tfiles = tfiles

		# Now build a model based on these vectors
		num_files = len(tfiles)
		num_training_files = int(PERCENT_TRAINING * num_files)
		num_test_files = num_files - num_training_files

		self.train_files = self.tfiles[:num_training_files]
		self.test_files = self.tfiles[num_training_files:]

		self.all_data = [featurizer.get_feature_matrix_and_output_vector(f) for f in self.tfiles]
		all_data_vectors = [d[0] for d in self.all_data]
		print([v.shape for v in all_data_vectors])
		self.all_features = np.vstack(d[0] for d in self.all_data)
		self.all_labels = np.hstack(d[1] for d in self.all_data)

		self.train_data = [featurizer.get_feature_matrix_and_output_vector(f) for f in self.train_files]
		self.train_features = np.vstack([d[0] for d in self.train_data])
		self.train_labels = np.hstack([d[1] for d in self.train_data])

		self.test_data = [featurizer.get_feature_matrix_and_output_vector(f) for f in self.test_files]
		self.test_features = np.vstack([d[0] for d in self.test_data])
		self.test_labels = np.hstack(d[1] for d in self.test_data)

		self.trained_clf = []
		for cl in used_classifiers:
			self.trained_clf += [cl(self.train_features, self.train_labels)]

from settings import *


used_classifiers = [SVM, DecisionTree, RandomForest]



class SVM():
	def __init__(self, X, y):
		pass

	def class_probabilities(self, X):
		pass

	def predict(self, X):
		pass

	def predict_for_file(self, X):
		pass


class DecisionTree():
	def __init__(self, X, y):
		pass

	def class_probabilities(self, X):
		pass

	def predict(self, X):
		pass

	def predict_for_file(self, X):
		pass


class RandomForest():
	def __init__(self, X, y):
		pass

	def class_probabilities(self, X):
		pass

	def predict(self, X):
		pass

	def predict_for_file(self, X):
		pass


class MainClassifier():

	def __init__(self, tfiles, featurizer):
		### [ Featurize the classifier ] ###
		self.featurizer = featurizer
		self.tfiles = tfiles

		# Now build a model based on these vectors
		num_files = len(tfiles)
		num_training_files = int(PERCENT_TRAINING * num_files)
		num_test_files = num_files - num_training_files


		random.shuffle(tfiles)
		self.all_data = [constr.get_feature_matrix_and_output_vector(f) for f in tfiles]
		self.all_features = np.vstack(d[0] for d in all_data)
		self.all_labels = np.hstack(d[1] for d in all_data)

		self.train_data = [constr.get_feature_matrix_and_output_vector(f) for f in train_files]
		self.train_features = np.vstack([d[0] for d in train_data])
		self.train_label = np.hstack([d[1] for d in train_data])

		self.test_data = [constr.get_feature_matrix_and_output_vector(f) for f in test_files]
		self.test_features = np.vstack([d[0] for d in test_data])
		self.test_label = np.hstack(d[1] for d in test_data)

		for cl in used_classifiers:
			cl(self.train_features, self.label)


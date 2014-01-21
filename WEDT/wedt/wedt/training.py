from tparser import parse
import os
import pickle
import re
import nltk.classify

train_path = os.path.join("wedt","training")
classifier_path = os.path.join("wedt","classifiers")

def gather_topics(addresslist, site):
	"""Downloads, parses and pickles all the topics from a list of addresses.
	
	addresslist	- a list of web addresses
	site		- site name (for bundling topics)
	"""
	for address in addresslist:
		parsed = parse(address, True)
		with open(os.path.join(train_path,site,re.findall('[^/]*$',address)[0]), 'w') as file:
			pickle.dump(parsed, file)
			
def train_classifier(classifier, directory, feature, name=None):
	"""Creates and trains a NLTK classifier from nltk.classify package.
	
	classifier	- a classifier class that supports training
	directory	- directory containing the training set (inside wedt/training)
	feature		- feature set function (features.py)
	"""
	featuresets = []
	for filename in os.listdir(os.path.join(train_path,directory)):
		with open(os.path.join(train_path, directory, filename), 'r') as file:
			topic, scores, classes = pickle.load(file)
			featuresets.extend( nltk.classify.util.apply_features(feature, zip(((topic, t) for t in topic), classes)) )
	c = classifier.train(featuresets)
	if name:
		with open(os.path.join(classifier_path, name), 'w') as file:
			pickle.dump((c,feature), file)
	return c

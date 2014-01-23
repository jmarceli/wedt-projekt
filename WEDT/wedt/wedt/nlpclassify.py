import os
import pickle

classifier_path = os.path.join("wedt","classifiers")

def choose_answers(classifier_name, topic):
	"""Performs the classification of posts in the topic using given classifier"""
	classifier,features = load_classifier(classifier_name)
	classes = classifier.batch_classify(map(features, ((topic, t) for t in topic[1:])))
	return [post[0] for post in zip(topic[1:], classes) if post[1]=="acc"]
	
def choose_answer(classifier_name, topic):
	"""Chooses the answer with the highest probability of being acceptable
	Only works for classifiers with prob_classify() method"""
	classifier,features = load_classifier(classifier_name)
	distributions = classifier.batch_prob_classify(map(features, ((topic, t) for t in topic[1:])))
	probs = [dist.prob('acc') for dist in distributions]
	return next(post[0] for post in zip(topic[1:], probs) if post[1]==max(probs))

def load_classifier(name):
	"""Loads a classifier with a given name from the "classifiers" folder"""
	with open(os.path.join(classifier_path, name), 'r') as file:
		classifier, features = pickle.load(file)
	return classifier, features
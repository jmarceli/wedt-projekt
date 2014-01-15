import os, pickle, nltk, re

classifier_path = os.path.join("wedt","classifiers")

def choose_answers(classifier_name, topic):
	classifier,features = load_classifier(classifier_name)
	classes = classifier.batch_classify(map(features, ((topic, t) for t in topic)))
	return [post[0] for post in zip(topic, classes) if post[1]=="acc"]

def load_classifier(name):
	with open(os.path.join(classifier_path, name), 'r') as file:
		classifier, features = pickle.load(file)
	return classifier, features
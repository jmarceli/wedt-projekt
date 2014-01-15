import nltk, re

def simple_features((topic, post)):
	features = {}
	features['longer-than-op'] = len(post.text) > len(topic.op.text)
	return features
	
def word_features((topic, post)):
	features = {}
	for word in post.text.split():
		features[word] = True
	return features



import nltk, re

def featureset_sample(posts):
	features = {}
	features.update(longer_than_op(posts))
	features.update(author_mentioned(posts))
	features.update(author_thanked(posts))
	return features

def longer_than_op((topic, post)):
	features = {}
	features['longer-than-op'] = len(post.text) > len(topic.op.text)
	return features
	
def word_features((topic, post)):
	features = {}
	for word in post.text.split():
		features[word] = True
	return features

def author_mentioned((topic, post)):
	features = {"author-mentioned":False}
	for p in topic:
		if re.search(re.escape(post.author), p.text):
			features["author-mentioned"] = True
	return features
	
def author_thanked((topic, post)):
	features = {"author-thanked":False}
	for p in topic:
		if re.search("[Tt]hanks? (you)? "+post.author, p.text):
			features["author-thanked"] = True
	return features

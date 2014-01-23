import nltk
import re
from itertools import chain

def featureset_sample(posts):
	features = {}
	features.update(longer_than_op(posts))
	features.update(author_mentioned(posts))
	features.update(author_thanked(posts))
	features.update(keywords_from_op(posts))
	return features
	
def featureset2(posts):
	features = {}
	features.update(longer_than_op(posts))
	features.update(author_mentioned(posts))
	features.update(author_thanked(posts))
	features.update(keywords_from_op(posts))
	features.update(written_by_op(posts))
	return features

	
def features_simple(posts):
	features = {}
	features.update(longer_than_op(posts))
	features.update(author_mentioned(posts))
	features.update(author_thanked(posts))
	return features

def features_full(posts):
	features = {}
	features.update(longer_than_op(posts))
	features.update(author_mentioned(posts))
	features.update(author_thanked(posts))
	features.update(keywords_from_op(posts))
	features.update(word_features(posts))
	return features

def longer_than_op((topic, post)):
	features = {}
	features['longer-than-op'] = len(post.text) > len(topic.op.text)
	return features
	
def word_features((topic, post)): #ineffective, training with that takes hours...
	features = {}
	for word in post.text.split():
		features['contains-'+word] = True
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
		if re.search("[Tt][Hh](x|anks?),? (you)? "+re.escape(post.author), p.text):
			features["author-thanked"] = True
	return features
	
def written_by_op((topic, post)):
	return {"written-by-op":post.author==topic.op.author}

def keywords_from_op((topic, post)):
	features = {}
	if not hasattr(keywords_from_op, "last_topic"): #static variable hack
		keywords_from_op.last_topic = None
	if not topic is keywords_from_op.last_topic:
		keywords_from_op.last_topic = topic
		keywords_from_op.op_keywords = keywords(tokenize(topic.op.text))
	post_keywords = keywords(tokenize(post.text))
	keyword_count = len(keywords_from_op.op_keywords & post_keywords)
	for i in range(min(keyword_count,10)):
		features['keyword-count-'+str(i+1)] = True
	return features
	
def tokenize(text):
	sentences = nltk.sent_tokenize(text)
	sentences = [nltk.word_tokenize(sent) for sent in sentences]
	sentences = [nltk.pos_tag(sent) for sent in sentences]
	return sentences

def keywords(sentences):
	return set(word[0] for word in chain(*sentences) if word[1]=='NNP')
	
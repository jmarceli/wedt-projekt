from nlpclassify import load_classifier
import os
import pickle

train_path = os.path.join("wedt","training")
classifier_path = os.path.join("wedt","classifiers")

class Report:
	def __init__(self, classifier_name, directory):
		self.classifier, self.features = load_classifier(classifier_name)
		self.directory = directory
		
	def report(self):
		self.train_classes = [] # classifications from test set
		self.train_answers = [] # correct answers from test set
		
		self.classes = [] # classifications from classifier
		self.answers = [] # best answers from classifier
	
		for filename in os.listdir(os.path.join(train_path,self.directory)):
			with open(os.path.join(train_path, self.directory, filename), 'r') as file:
				topic, train_scores, train_classes = pickle.load(file)
				chosen_answer = next(post[0] for post in zip(topic, train_classes) if post[1]=='acc')
				distributions = self.classifier.batch_prob_classify(
					map(self.features, ((topic, t) for t in topic[1:])))
				probs = [dist.prob('acc') for dist in distributions]
				classification = [dist.max() for dist in distributions]
				best_answer = next(post[0] for post in zip(topic[1:], probs) if post[1]==max(probs))
				
				self.train_classes.append(train_classes[1:])
				self.train_answers.append(chosen_answer)
				self.classes.append(classification[:len(train_classes)]) # cuts some garbage
				self.answers.append(best_answer)

	def breakdown(self):
		i=0
		self.best_hits = [] # True for correct best answers
		self.c_hits = [] # Number of correctly classified posts
		self.c_accuracy = [] # Accuracy of classification
		self.c_recall = [] # Correctly accepted posts
		
		for t_class, t_answer, c_class, c_answer in zip(self.train_classes, self.train_answers, self.classes, self.answers):
			correct = [t==c for t,c in zip(t_class, c_class) ]
			accepted = [t=='acc' and c in zip(c_class, correct)]
			self.c_hits.append(sum(correct))
			self.c_recall.append(sum(accepted))
			self.c_accuracy.append(float(sum(correct))/len(correct))
			self.best_hits.append(t_answer == c_answer)
		
		# Total accuracy for best answers
		self.best_accuracy = float(sum(self.best_hits))/len(self.best_hits)
		# Total accuracy for classification
		self.total_accuracy = float(sum(self.c_hits))/sum([len(c) for c in self.classes])
		# Total recall (correctly accepted answers ratio) for classification
		self.total_recall = float(sum(self.c_recall))/len(self.c_recall)
		
	@staticmethod
	def generate(classifier_name, directory):
		rep = Report(classifier_name, directory)
		rep.report()
		rep.breakdown()
		return rep
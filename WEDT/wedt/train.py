import os
import sys

def main(argv):
	import wedt.training
	import wedt.features

	if argv[1] == "gather":
		if len(argv) < 4:
			print_help()
			return
		for filename in argv[3:]:
			if not os.path.exists(os.path.join(wedt.training.train_path,argv[2])):
				os.makedirs(os.path.join(wedt.training.train_path,argv[2]))
			with open(os.path.join('wedt','site_lists',filename), 'r') as file:
				addresslist = file.read().splitlines()
				wedt.training.gather_topics(addresslist, argv[2])
				
	elif argv[1] == "train":
		if len(argv) < 6:
			print_help()
			return
		try:
			feature = getattr(wedt.features, argv[4])
			wedt.training.train_classifier(argv[3], argv[5], feature, argv[2])
		except AttributeError:
			print "Wrong feature function name - see wedt/features.py"
	
	elif argv[1] == "check":
		if len(argv) < 4:
			print_help()
			return
		from wedt.tparser import parse
		from wedt.nlpclassify import choose_answers
		answers = choose_answers(argv[2], parse(argv[3]))
		for answer in answers:
			print answer
	else:
		print_help()
		
		
def print_help():
	print """Training module of wedt-projekt.
Usage:

train.py gather directory [filenames...]
	Gathers the topics listed in the files in the specified directory

train.py train name type feature trainset
	Trains a new classifier.
	name		name for the new classifier
	type		classifier type: MaxEnt, NaiveBayes or PositiveNaiveBayes
	feature		featureset name (as in wedt/features.py)
	trainset	name of the directory containing the training topics

train.py check classifier address
	Chooses an answer based on given classifier
	classifier	classifier name
	address		topic address
"""

if __name__ == "__main__":
	if len(sys.argv) == 1:
		print_help()
	else:
		main(sys.argv)


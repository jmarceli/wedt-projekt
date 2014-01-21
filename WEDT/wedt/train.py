import os
import sys

def main(argv):
	import wedt.training
	import wedt.features

	if argv[1] == "gather":
		if len(argv) < 4:
			print_help()
			return
		for filename in argv[2:]:
			with open(os.path.join(wedt.training.train_path,filename), 'r') as file:
				addresslist = file.read().splitlines()
				wedt.training.gather_topics(addresslist, argv[1])
				
	if argv[1] == "train":
		if len(argv) < 6:
			print_help()
			return
		try:
			feature = getattr(wedt.features, argv[4])
			wedt.training.train_classifier(argv[3], argv[5], feature, argv[2])
		except AttributeError:
			print "Wrong feature function name - see wedt/features.py"
		
		
		
def print_help():
	print """Training module of wedt-projekt.
Usage:

train.py gather directory [filenames...]
	Gathers the topics listed in the files in the specified directory

train.py train name type feature trainset
	Trains a new classifier.
	name - name for the new classifier
	type - classifier type: MaxEnt, NaiveBayes or PositiveNaiveBayes
	feature - featureset name (as in wedt/features.py)
	trainset - name of the directory containing the training topics"""

if __name__ == "__main__":
	if len(sys.argv) == 1:
		print_help()
	else:
		main(sys.argv)


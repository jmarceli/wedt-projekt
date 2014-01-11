from tparser import parse
import pickle
import re

def gather_topics(addresslist, site):
	for address in addresslist:
		parsed = parse(address, site, True)
		with open("wedt/training/"+site+'/'+re.findall('[^/]*$',address)[0], 'w') as file:
			pickle.dump(parsed, file)
import urllib
from sets import Set
from itertools import izip_longest
from bs4 import BeautifulSoup
from topic import Topic, Post
import re
import json

def parse(address, learnmode=False):
	pages = Set([address])
	addr_site = re.findall('^.+/',address)[0]
	addr_topic = re.findall('[^/]*$',address)[0]
	site = get_site(address)
	with open("wedt/forumstrings/"+site, 'r') as f:
		strings = json.loads(f.read())
	topic = Topic()
	scores = []
	classes = []
	p = 0
	while p < len(pages):
		page = get_page(sorted(pages)[p])
		soup = BeautifulSoup(page)

		# find links to other pages
		if strings['pagination']: # for forums without pagination
			for pagination in soup(True, attrs={"class": strings['pagination']}):
				for link in pagination("a", href=re.compile(re.escape(addr_topic))):
					t = re.search('[^/]*('+strings['page']+')[0-9]+', link['href'])
					if t:
						pages.add(addr_site+t.group(0))

		# extract posts container if possible
		postlist = (soup.find("div", id=strings['postlist']) if strings['postlist'] else soup)

		author = []
		title = []
		text = []
		for postbody in postlist(True, attrs={"class": strings['postbody']}):
			text.append('\n'.join(postbody.stripped_strings))
		if strings['username']:
			for username in postlist(True, attrs={"class": strings['username']}):
				author.append(str(username.string))
		if strings['posttitle']:
			for posttitle in postlist(True, attrs={"class": strings['posttitle']}):
				title.append(str(posttitle.string))
		if learnmode:		
			for postscore in postlist(True, attrs={"class": strings['postscore']}):
				scores.append(str(postscore.span.string))
				classes.append("acc" if strings['postaccepted'] in postscore.get_text() else "nope")

		for (u,t,b) in izip_longest(author, title, text, fillvalue=""):
			topic.append(Post(u,t,b,''))

		# go to the next page
		p=p+1
	return (topic, scores, classes) if learnmode else topic

def get_site(address):
	if re.match(r"(http://)?(www\.)?ubuntuforums(\.com|\.org)", address)
		return "ubuntuforums"
	if re.match(r"(http://)?(www\.)?stack[^\.]*(\.com|\.org)", address)
		return "stackexchange"
	else:
		return "default"
	
def get_page(address):
	file = urllib.urlopen(address)
	page = file.read()
	file.close()
	return page

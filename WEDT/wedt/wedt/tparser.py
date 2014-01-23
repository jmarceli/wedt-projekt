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
		if strings.get('pagination',''): # for forums without pagination
			for pagination in soup(True, attrs={"class": strings['pagination']}):
				for link in pagination("a", href=re.compile(re.escape(addr_topic))):
					t = re.search('[^/]*('+strings['page']+')[0-9]+', link['href'])
					if t:
						pages.add(addr_site+t.group(0))

		# extract posts container if possible
		postlist = (soup.find("div", id=strings['postlist']) if strings.get('postlist','') else soup)

		author = []
		title = []
		text = []
		source = []
		link = []
		for postbody in postlist(True, attrs={"class": strings['postbody']}):
			text.append('\n'.join(postbody.stripped_strings))
			source.append(''.join(map(unicode,postbody.contents)))
		if strings.get('username',''):
			for username in postlist(True, attrs={"class": strings['username']}):
				if username.string:
					author.append(unicode(username.string))
				else:
					author.append(unicode(username.a.string))
		if strings.get('optitle',""):
			optitle = postlist.find(True, id=strings['optitle'])
			title.append(unicode(optitle.string))
		if strings.get('posttitle',""):
			for posttitle in postlist(True, attrs={"class": strings['posttitle']}):
				title.append(unicode(posttitle.string))
		if strings.get('postlink',""):
			for postlink in postlist('a', attrs={"class": strings['postlink']}):
				link.append(addr_site+re.search('[^/]*$', postlink['href']).group(0))
		if learnmode:		
			for postscore in postlist(True, attrs={"class": strings['postscore']}):
				scores.append(unicode(postscore.span.string))
				classes.append("acc" if strings['postaccepted'] in postscore.get_text() else "nope")
		
		if len(text)-len(link)==1: #OP isn't permalinked
			link = [address] + link

		for (u,t,b,l,s) in izip_longest(author, title, text, link, source, fillvalue=""):
			topic.append(Post(u,t,b,l,s))

		# go to the next page
		p=p+1
	return (topic, scores, classes) if learnmode else topic

def get_site(address):
	if re.match(r"(http://)?(www\.)?ubuntuforums(\.com|\.org)", address):
		return "ubuntuforums"
	if re.match(r"(https?://)?(www\.)?drupal\.org", address):
		return "drupal"
	if re.match(r"(http://)?(www\.)?([^/]*.)?stack[^\.]*(\.com|\.org)", address):
		return "stackexchange"
	if re.match(r"(http://)?(www\.)?askubuntu\.com", address):
		return "stackexchange"
	else:
		return "default"
	
def get_page(address):
	file = urllib.urlopen(address)
	page = file.read()
	file.close()
	return page

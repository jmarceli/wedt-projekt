import urllib
from sets import Set
from bs4 import BeautifulSoup
from topic import Topic, Post
import re
import json

def parse(address, site):
	pages = Set([address])
	addr_site = re.findall('^.+/',address)[0]
	addr_topic = re.findall('[^/]*$',address)[0]
	with open("wedt/forumstrings/"+site, 'r') as f:
		strings = json.loads(f.read())
	topic = Topic()
	p = 0
	while p < len(pages):
		page = get_page(sorted(pages)[p])
		soup = BeautifulSoup(page)

		# find links to other pages
		for pagination in soup(True, attrs={"class": strings['pagination']}):
			for link in pagination("a", href=re.compile(re.escape(addr_topic))):
				t = re.search('[^/]*('+strings['page']+')[0-9]+', link['href'])
				if t:
					pages.add(addr_site+t.group(0))

		# extract posts
		postlist = soup.find("div", id=strings['postlist'])

		author = []
		title = []
		text = []
		for username in postlist(True, attrs={"class": strings['username']}):
			author.append(username.string)
		for posttitle in postlist(True, attrs={"class": strings['posttitle']}):
			title.append(posttitle.string)
		for postbody in postlist(True, attrs={"class": strings['postbody']}):
			text.append('\n'.join(postbody.stripped_strings))

		for (u,t,b) in zip(author, title, text):
			topic.append(Post(u,t,b,''))

		# go to the next page
		p=p+1
	return topic

def get_page(address):
	file = urllib.urlopen(address)
	page = file.read()
	file.close()
	return page

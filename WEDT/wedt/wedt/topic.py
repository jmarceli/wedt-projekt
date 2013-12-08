class Post(object):
    """Representation of a single post in a topic."""
    def __init__(self):
        self._author=""
        self._date=""
        self._title=""
        self._text=""
        self._source=""
        
    def __init__(self, author, title, text):
        self._author=author
        self._date=""
        self._title=title
        self._text=text
        self._source=""

    def __init__(self, author, title, text, source):
        self._author=author
        self._date=""
        self._title=title
        self._text=text
        self._source=source

    @property
    def author(self):
        """Username of the post's author."""
        return self._author
        
    @author.setter
    def author(self, value):
        self._author = value

    @property
    def date(self):
        """Time where post was written (if available)."""
        return self._date
        
    @date.setter
    def date(self, value):
        self._date = value

    @property
    def title(self):
        """Title of the post."""
        return self._title
        
    @title.setter
    def title(self, value):
        self._title = value

    @property
    def source(self):
        """Source (formatted) content of the post."""
        return self._source
        
    @source.setter
    def source(self, value):
        self._source = value

    @property
    def text(self):
        """Unformatted content of the post."""
        return self._text
        
    @text.setter
    def text(self, value):
        self._text = value
        
    def __repr__(self):
        """String representation (for debugging)."""
        s = ""
        if len(self._date):
            s += '[{0}] '.format(self._date)
        return s + '{0}: {1}\n{2}'.format(self._author, self._title, self._text)

        
class Topic(object):
    """Representation of a forum topic.
    
    Posts can be accessed with the index operator:
        topic[index]
    or with a method:
        topic.post(index)
        
    Posts can also be iterated over:
        for post in topic:
            print post.text
    
    The original post (OP) can be accessed as a property:
        topic.op
        
    The number of posts is accessed with a build-in function len():
        len(topic)
    """
    def __init__(self):
        self._posts = []
        self._title = ""
    
    @property
    def op(self):
        """Access the original post (OP) as a property."""
        return self._posts[0]
                    
    def __len__(self):
        """Operator overload for getting number of posts with len(topic) syntax."""
        return len(_posts)
    
    def __getitem__(self, index):
        """Operator overload for accessing posts with topic[index] syntax."""
        return self._posts[index]
        
    def post(self, index):
        """Returns the post with given index."""
        return self._posts[index]
        
    def add(self, post):
        """Add a post to the topic."""
        self._posts.append(post)
        
    def append(self, post):
        """Add a post to the topic."""
        self._posts.append(post)
        
    def __repr__(self):
        """String representation (for debugging)."""
        s = self._title
        for p in self._posts:
            s += '\n{0}'.format(p.__repr__())
        return s
'''
simplest function without any real NLP processing
'''


def magic(posts):
    """ Return last reply in topic as an answer """
    return [posts.post(posts.__len__() - 1).text]

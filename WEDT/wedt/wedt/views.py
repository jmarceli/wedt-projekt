'''
Created on 01-12-2013

@author: michal
'''
from django.http import HttpResponse
from django.template import RequestContext, loader
#import vimpdb
import urllib
import tparser
import nlpsort


def main(request):
    template = loader.get_template('main.html')
    context = RequestContext(request, {'title':
                                       'Natural language search engine'})
    return HttpResponse(template.render(context))


def search(request):
    #vimpdb.set_trace()
    requestDict = request.POST
    template = loader.get_template('search.html')

    if 'question' not in requestDict:
        return HttpResponse(template.render(
            RequestContext(request,
                           {'title': 'No question',
                            'question': 'Please write the question first'})))
    question = requestDict['question']

    posts = tparser.parse('http://ubuntuforums.org/showthread.php?t=2198197',
                          'ubuntuforums_org')
    #Do some NLP magic here...
    posts = nlpsort.magic(posts)
    #response = ['good response', 'not so good response']
    #response = test.post(0)

    context = RequestContext(request,
                             {'title': 'Natural language search engine',
                              'question': question, 'response': posts})
    return HttpResponse(template.render(context))

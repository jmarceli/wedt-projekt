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
    requestDict = request.POST
    template = loader.get_template('search.html')

    if 'question' not in requestDict:
        return HttpResponse(template.render(
            RequestContext(request,
                           {'title': 'No question',
                            'question': 'Please write the question URL first'})))
    questionURL = requestDict['question']

    posts = tparser.parse(questionURL, 'ubuntuforums_org')
    #Do some NLP magic here...
    #vimpdb.set_trace()
    posts = nlpsort.magic(posts)
    #response = ['good response', 'not so good response']
    #response = test.post(0)

    context = RequestContext(request,
                             {'title': 'Natural language search engine',
                              'question': questionURL, 'response': posts})
    return HttpResponse(template.render(context))

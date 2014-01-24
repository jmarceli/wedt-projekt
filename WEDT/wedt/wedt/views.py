'''
Created on 01-12-2013

@author: michal
'''
from django.http import HttpResponse
from django.template import RequestContext, loader
from wedt.tparser import parse
from wedt.nlpclassify import choose_answers, choose_answer
#import pdb
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
                            'question': 'Please write the question URL first'
                            })))
    questionURL = requestDict['question']

    parsed = tparser.parse(questionURL)

    if 'drupal' in questionURL:
        posts = choose_answers('bay-sam-drupal', parsed)
        bestpost = choose_answer('bay-sam-drupal', parsed)
    elif 'ubuntu' in questionURL:
        posts = choose_answers('bay-sam-ubu', parsed)
        bestpost = choose_answer('bay-sam-ubu', parsed)
    else:
        posts = choose_answers('bay-sam-mix', parsed)
        bestpost = choose_answer('bay-sam-mix', parsed)
    #pdb.set_trace()

    #Do some NLP magic here...
    #vimpdb.set_trace()
    #posts = nlpsort.magic(posts)
    #response = ['good response', 'not so good response']
    #response = test.post(0)

    context = RequestContext(request,
                             {'title': 'Natural language search engine',
                              'question': questionURL,
                              'response': bestpost,
                              'others': posts})
    return HttpResponse(template.render(context))

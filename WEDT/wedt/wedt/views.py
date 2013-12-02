'''
Created on 01-12-2013

@author: michal
'''
from django.http import HttpResponse
from django.template import RequestContext, loader

def main(request):
    template = loader.get_template('main.html')
    context = RequestContext(request, {'title' : 'Natural language search engine'})
    return HttpResponse(template.render(context))

def search(request):
    requestDict = request.POST
    if 'question' not in requestDict:
        return 
    question = requestDict['question']
    
    #Do some NLP magic here...
    response = ['good response', 'not so good response']
    
    template = loader.get_template('search.html')
    
    context = RequestContext(request, {'title' : 'Natural language search engine', 'question': question, 'response' : response})
    return HttpResponse(template.render(context))
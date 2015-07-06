from django.shortcuts import render, render_to_response
from django.template import RequestContext

# Create your views here.
def index(request):
    context = RequestContext(request)
    template_name = 'umpire/index.html'
    context_dict = {}
    return render_to_response(template_name, context_dict, context)

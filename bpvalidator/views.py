'''
Author: Moon Kwon Kim <mkdmkk@gmail.com>
'''
from django.shortcuts import render_to_response
from django.template.context import Context, RequestContext
from django.core.context_processors import csrf
from bpvalidator.forms import DocumentForm


def render(request, page):
    context = Context()
    context.update(csrf(request))

    context['page'] = page
    template = "index.html"
    form = DocumentForm()

    return render_to_response(
        template,
        {'form': form},
        context_instance=RequestContext(request)
    )

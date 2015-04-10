from time import strftime
from time import gmtime
from bpvalidator.forms import DocumentForm
from bpvalidator.models import BusinessProcess
from bpvalidator.validator import LinkGraphValidator, EssentialElementValidator

__author__ = 'Moon Kwon Kim <mkdmkk@gmail.com>'


from django.shortcuts import render_to_response
from django.template.context import Context, RequestContext

import xml.etree.ElementTree as ET

def check(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.cleaned_data['docfile']
            appns = form.cleaned_data['appns']
            result = check_all(f, appns)
            return render_to_response(
                'index.html',
                {'form': form, 'result': result,
                 'bp_file':{'name':f.name, 'size':f.size},
                 'appns': appns,
                 'testing_time': strftime("%Y-%m-%d %H:%M:%S", gmtime())
                },
                context_instance=RequestContext(request)
            )
        else:
            print("Invalid Input")

    return render_to_response(
        'index.html',
        {'form': DocumentForm()},
        context_instance=RequestContext(request)
    )


def check_all(f, appns):
    root, ns = parse_and_get_ns(f)

    if appns not in ns: return None

    bp = BusinessProcess(root, ns, appns)
    lgs = bp.lgs

    el_validator = EssentialElementValidator()
    lg_validator = LinkGraphValidator()

    validity_part_importing, errors_part_importing = el_validator.check_part_importing(bp.importing)
    validity_part_linkgraphassignment, errors_part_linkgraphassignment = el_validator.check_part_linkgraphassignment(bp.lg_assignments)
    validity_part_invokation, errors_part_invokation = el_validator.check_part_invokation(bp.invokations)

    if lgs:
        for lg in lgs:
            validity_resources, errors_linkgraph_resources = lg_validator.check_linkgraph_resources(lg.nodes, ns, appns)
            validity_topics_actions_services, errors_linkgraph_topics_actions_services = \
                lg_validator.check_linkgraph_topics_actions_services(lg.topics, lg.actions, lg.services, ns, appns)
            validity_edges, errors_linkgraph_edges = lg_validator.check_linkgraph_edges(lg.edges, lg.nodes, lg.topics, lg.actions, lg.services, ns, appns)
    else:
        validity_resources, errors_linkgraph_resources = False, ["Parsing error."]
        validity_topics_actions_services, errors_linkgraph_topics_actions_services = False, ["Parsing error."]
        validity_edges, errors_linkgraph_edges = False, ["Parsing error."]

    return {
        "a1": {'status': 'valid' if validity_part_importing else 'error', 'errors': errors_part_importing },
        "a2": {'status': 'valid' if validity_part_linkgraphassignment else 'error', 'errors': errors_part_linkgraphassignment },
        "a3": {'status': 'valid' if validity_part_invokation else 'error', 'errors': errors_part_invokation },
        "b1": {'status': 'valid' if validity_resources else 'error', 'errors': errors_linkgraph_resources },
        "b2": {'status': 'valid' if validity_topics_actions_services else 'error', 'errors': errors_linkgraph_topics_actions_services },
        "b3": {'status': 'valid' if validity_edges else 'error', 'errors': errors_linkgraph_edges }
    }


def parse_and_get_ns(file):
    events = "start", "start-ns"
    root = None
    ns = {}
    for event, elem in ET.iterparse(file, events):
        if event == "start-ns":
            ns[elem[0]] = "{%s}" % elem[1]
        elif event == "start":
            if root is None:
                root = elem
    return ET.ElementTree(root), ns


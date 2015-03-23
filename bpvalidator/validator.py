import json
import requests

__author__ = 'Moon Kwon Kim <mkdmkk@gmail.com>'


CONCERT_ADAPTER_NS = 'http://smartylab.co.kr/products/op/adapter'
MESSAGE_DATABASE_SERVER_URL = 'http://172.16.113.205:10000/api/rocon_app'

class EssentialElementValidator:
    def __init__(self):
        pass


    def check_part_importing(self, parts):
        validity = False

        for p in parts:
            if p.attrib['namespace'] == CONCERT_ADAPTER_NS:
                # print(p.tag)
                # print(p.attrib)
                validity = True

        return validity, None if validity else ["No Concert Adapter WSDL."]


    def check_part_linkgraphassignment(self, linkgraphes):
        validity = False

        # print(subp)
        if len(linkgraphes):
            # print(subp.tag)
            # print(subp.attrib)
                validity = True

        return validity, None if validity else ["No Link Graph Assignment."]


    def check_part_invokation(self, parts):
        validity = False
        errors = []

        for p in parts:
            # print(p.tag)
            # print(p.attrib)
            if p.attrib['operation'] == "invoke_adapter":
                validity = True

        return validity, None if validity else ["No Concert Adapter Invocation."]


class LinkGraphValidator:
    def __init__(self):
        pass


    def check_linkgraph_resources(self, nodes, ns, appns):
        validity = True
        errors = []

        # print(subp.tag)
        # print(subp.attrib)
        for n in nodes:
            min = n.find(ns[appns]+"min")
            max = n.find(ns[appns]+"max")
            if min is not None and max is not None:
                if min.text > max.text:
                    validity = False
                    errors.append("Invalid Min and Max Values.")

        return validity, None if validity else errors


    def check_linkgraph_topics(self, topics, ns, appns):
        validity = True
        errors = []

        try:
            r = requests.get(MESSAGE_DATABASE_SERVER_URL, timeout=2)

            data = r.json()
            for t in topics:
                tname = t.find(ns[appns]+'id').text
                if not tname:
                    validity = False
                    errors.append("No Topic Name Specified.")
                if not self.search_topic(data, tname):
                    validity = False
                    errors.append("No Matched Topic: ["+tname+"]")

            return validity, None if validity else errors
        except:
            return False, ["Message DB is not available."]


    def check_linkgraph_edges(self, edges, nodes, topics, ns, appns):
        validity = True
        errors = []

        for edge in edges:
            start = edge.find(ns[appns]+"start")
            finish = edge.find(ns[appns]+"finish")
            remap_from = edge.find(ns[appns]+"remap_from")
            remap_to = edge.find(ns[appns]+"remap_to")

            if start != None and finish != None:
                # Check Start Statement
                tmp = False
                for node in nodes:
                    if node.find(ns[appns]+"id").text == start.text:
                        tmp = True
                        break
                if not tmp:
                    for topic in topics:
                        if topic.find(ns[appns]+"id").text == start.text:
                            tmp = True
                            break
                if not tmp:
                    validity = False
                    errors.append("Invalid Start Statement: ["+start.text+"].")
                # Check Finish Statement
                tmp = False
                for node in nodes:
                    if node.find(ns[appns]+"id").text == finish.text:
                        tmp = True
                        break
                if not tmp:
                    for topic in topics:
                        if topic.find(ns[appns]+"id").text == finish.text:
                            tmp = True
                            break
                if not tmp:
                    validity = False
                    errors.append("Invalid Finish Statement: ["+finish.text+"].")
            else:
                validity = False
                errors.append("Invalid Start and Finish Statements.")
        return validity, None if validity else errors


    def search_topic(self, data, value):
        if type(data) is list:
            for d in data:
                if self.search_topic(d, value):
                    return True
        elif type(data) is dict:
            for k, v in data.iteritems():
                if type(v) is list or type(v) is dict:
                    if self.search_topic(v, value):
                        return True
                else:
                    if k == 'name' and v == value:
                        return True
        return False
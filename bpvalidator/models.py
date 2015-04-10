# -*- coding: utf-8 -*-

__author__ = 'Moon Kwon Kim <mkdmkk@gmail.com>'

from django.db import models

class Document(models.Model):
    docfile = models.FileField(upload_to='bp/%Y/%m/%d')
    appns = models.TextField()


class BusinessProcess():
    __slot__ = [
        "root",
        "ns",
        "appns",
        "importing",
        "lg_assignments",
        "invokations",
        "lgs"
    ]


    def __init__(self, root, ns, appns):
        self.root = root
        self.ns = ns
        self.appns = appns
        self.lgs = None
        self.parse()


    def parse(self):
        print("Parsing...")
        self.importing = self.root.findall('.//'+self.ns['bpel']+'import')
        print("Importing: %s" % self.importing)

        self.lg_assignments = self.root.findall('.//'+
                                                self.ns['bpel']+'sequence'+'/'+
                                                self.ns['bpel']+'assign'+'/'+
                                                self.ns['bpel']+'copy'+'/'+
                                                self.ns['bpel']+'from'+'/'+
                                                self.ns['bpel']+'literal'+'/'+
                                                self.ns[self.appns]+'invoke_adapter')
        print("Assigning (invoke_adapter): %s" % self.lg_assignments)

        self.invokations = self.root.findall('.//'+
                                             self.ns['bpel']+'sequence'+'/'+
                                             self.ns['bpel']+'invoke[@operation="invoke_adapter"]')
        print("Invoking (invoke_adapter): %s" % self.invokations)

        self.lgs = []
        for p in self.lg_assignments:
            subp = None
            try:
                subp = p.find(self.ns[self.appns]+'LinkGraph')
            except: continue
            if subp is not None:
                self.lgs.append(LinkGraph(subp, self.ns, self.appns))


class LinkGraph:
    __slot__ = [
        "root",
        "ns",
        "appns",
        "nodes",
        "topics",
        "edges"
    ]


    def __init__(self, root, ns, appns):
        self.root = root
        self.ns = ns
        self.appns = appns

        self.parse()


    def parse(self):
        try: self.nodes = self.root.find(self.ns[self.appns]+"nodes").findall(self.ns[self.appns]+"Node")
        except: self.nodes = None
        try: self.topics = self.root.find(self.ns[self.appns]+"topics").findall(self.ns[self.appns]+"Topic")
        except: self.topics = None
        try: self.actions = self.root.find(self.ns[self.appns]+"actions").findall(self.ns[self.appns]+"Action")
        except: self.actions = None
        try: self.services = self.root.find(self.ns[self.appns]+"services").findall(self.ns[self.appns]+"Service")
        except: self.services = None
        try: self.edges = self.root.find(self.ns[self.appns]+"edges").findall(self.ns[self.appns]+"Edge")
        except: self.edges = None
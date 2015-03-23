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

        self.parse()


    def parse(self):
        self.importing = self.root.findall(self.ns['bpel']+'import')
        self.lg_assignments = self.root.findall('./'+self.ns['bpel']+'sequence'+'/'+self.ns['bpel']+'assign')
        self.invokations = self.root.findall('./'+self.ns['bpel']+'sequence'+'/'+self.ns['bpel']+'invoke')

        self.lgs = []
        for p in self.lg_assignments:
            subp = None
            try:
                subp = p.find(self.ns['bpel']+"copy")\
                    .find(self.ns['bpel']+"from")\
                    .find(self.ns['bpel']+'literal')\
                    .find(self.ns[self.appns]+'invoke_adapter')\
                    .find(self.ns[self.appns]+'LinkGraph')
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
        self.nodes = self.root.find(self.ns[self.appns]+"nodes").findall(self.ns[self.appns]+"Node")
        self.topics = self.root.find(self.ns[self.appns]+"topics").findall(self.ns[self.appns]+"Topic")
        self.edges = self.root.find(self.ns[self.appns]+"edges").findall(self.ns[self.appns]+"Edge")

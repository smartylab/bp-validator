# -*- coding: utf-8 -*-

__author__ = 'Moon Kwon Kim <mkdmkk@gmail.com>'

from django import forms

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file'
    )
    appns = forms.CharField()
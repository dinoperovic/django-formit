# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.template import Template, Context
from django.test import TestCase
from django import forms


class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)


class FormitTest(TestCase):
    TEMPLATE = Template("""
        {% load formit_tags %}
        {% form contact_form %}
        {% form_block contact_form %}{% fieldset %}{% endform_block %}
        {% fieldset fields=contact_form.visible_fields %}
        {% field contact_form.visible_fields.0 placeholder="Enter your name" %}
    """)

    def test_formit_tags(self):
        rendered = self.TEMPLATE.render(Context({'contact_form': ContactForm()}))  # noqa
        # TODO: Check if rendered html appears as expected.

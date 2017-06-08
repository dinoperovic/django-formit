# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from classytags.arguments import Argument, MultiKeywordArgument
from classytags.core import Options
from classytags.helpers import InclusionTag
from django import template
from django.utils.encoding import smart_text
from django.utils.module_loading import import_string
from django.utils.six import string_types

from formit import settings as fs

register = template.Library()


class Form(InclusionTag):
    name = 'form'
    template = 'formit/form.html'

    options = Options(
        Argument('form'),
        MultiKeywordArgument('attrs', required=False),
    )

    def get_context(self, context, form, attrs):
        flags = [x for x in attrs if attrs[x] is True]

        if isinstance(form, string_types):
            form = import_string(form)()

        context.update({
            'form': form,
            'action': attrs.get('action', ''),
            'method': attrs.get('method', 'get'),
            'enctype': attrs.get('enctype', None),
            'button': smart_text(attrs.get('button', fs.DEFAULT_BUTTON)),
            'novalidate': 'novalidate' in flags or fs.DEFAULT_NOVALIDATE,
            'show_csrf_token': 'hide_csrf_token' not in flags,
            'show_non_field_errors': 'hide_non_field_errors' not in flags,
            'show_button': 'hide_button' not in flags,
        })
        return context


class FormBlock(Form):
    name = 'form_block'

    options = Options(
        Argument('form'),
        MultiKeywordArgument('attrs', required=False),
        blocks=[('endform_block', 'nodelist')]
    )

    def get_context(self, context, form, attrs, nodelist):
        flags = [x for x in attrs if attrs[x] is True]

        context = super(FormBlock, self).get_context(context, form, attrs)
        context.update({
            'is_block': True,
            'is_blank': 'blank' in flags,
            'block_content': nodelist.render(context),
        })
        return context


class Fieldset(InclusionTag):
    name = 'fieldset'
    template = 'formit/fieldset.html'

    options = Options(
        MultiKeywordArgument('attrs', required=False),
    )

    def get_context(self, context, attrs):
        form = attrs.get('form', None)
        fields = attrs.get('fields', None)
        visible_fields = attrs.get('visible_fields', None)
        hidden_fields = attrs.get('hidden_fields', None)

        if not form and not any(attrs):
            # If no arguments use 'form' from context.
            form = context.get('form', None)

        context.update({
            'fields': fields,
            'visible_fields': visible_fields,
            'hidden_fields': hidden_fields,
        })
        if form and not fields and not visible_fields and not hidden_fields:
            context['fields'] = [x for x in form]
        return context


class Field(InclusionTag):
    name = 'field'
    template = 'formit/field.html'

    options = Options(
        Argument('field'),
        MultiKeywordArgument('attrs', required=False),
    )

    def get_context(self, context, field, attrs):
        flags = [x for x in attrs if attrs[x] is True]

        field_type = field.field.widget.__class__.__name__.lower()
        field_label = attrs.get('label', field.label)
        field_help_text = attrs.get('help_text', field.help_text)

        # Add 'placeholder' attribute to fields that support it.
        placeholder_fields = ['textinput', 'emailinput', 'numberinput', 'passwordinput', 'textarea']
        if 'placeholder' in attrs and field_type in placeholder_fields:
            field.field.widget.attrs['placeholder'] = attrs['placeholder']

        context.update({
            'field': field,
            'field_type': field_type,
            'field_label': field_label,
            'field_help_text': field_help_text,
            'is_required': field.field.required,
            'has_errors': len(field.errors) > 0,
            'show_label': 'hide_label' not in flags,
            'show_help_text': 'hide_help_text' not in flags,
            'show_errors': 'hide_errors' not in flags,
        })
        return context


register.tag(Form)
register.tag(FormBlock)
register.tag(Fieldset)
register.tag(Field)

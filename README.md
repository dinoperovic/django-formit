# Formit

[![Build Status](https://img.shields.io/travis/dinoperovic/django-formit.svg)](https://travis-ci.org/dinoperovic/django-formit)
[![Codecov](https://img.shields.io/codecov/c/github/dinoperovic/django-formit.svg)](http://codecov.io/github/dinoperovic/django-formit)
[![PyPI version](https://img.shields.io/pypi/v/django-formit.svg)](https://pypi.python.org/pypi/django-formit)

**Smiple [Django] form formating.**

Formit provides a template tag library for django to ease the formating of forms.

---

## Requirements

* [Django] 1.11, 1.10
* [django-classy-tags] for managing template tags.

## Installation

Install using *pip*:

```bash
pip install django-formit
```

Then add `formit` to `INSTALLED_APPS`.

## Usage

To use **Formit** add your templates:

```django
{% load formit_tags %}

{# To render the form pass in the string path or form instance. #}
{% form 'contact.forms.ContactForm' action="/" method="get" button="Send" %}

{# To render the form with custom contents. #}
{% form_block instance %}
  <h3>Contact form</h3>
  {% fieldset %}
{% endform_block %}

{# To render a custom form without any formating. #}
{% form_block instance blank=True %}
  {% csrf_token %}
  <h3>Contact form</h3>
  <div class="column">
    {% fieldset fields=form.visible_fields|slice:":3" %}
  </div>
  <div class="column">
    {% fieldset fields=form.visible_fields|slice:"3:" %}
  </div>
  {% fieldset fields=form.hidden_fields %}
  <button>Send</button>
{% endform_block %}

{# You can separate the rendering of visible and hidden fields. #}
{% fieldset visible_fields=instance.visible_fields hidden_fields=instance.hidden_fields %}
{# or to automatically extract them from a form. #}
{% fieldset form=instance %}

{# To render a single field #}
{% field instance.visible_fields.0 placeholder="Enter your name" %}
```

Fieldset tags can also be used without any arguments. In that case ``form`` from the context will be used,
which is automatically available inside the ``form`` or ``form_block`` tag.

## Templates

Templates available to override in ``templates/formit/*``:

* ``form.html``
* ``fieldset.html``
* ``field.html``


[Django]: https://www.djangoproject.com/
[django-classy-tags]: https://github.com/ojii/django-classy-tags

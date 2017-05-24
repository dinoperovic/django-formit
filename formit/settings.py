# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

# Default value for novalidate attribute on forms.
DEFAULT_NOVALIDATE = getattr(settings, 'FORMIT_DEFAULT_NOVALIDATE', False)

# Default form button text.
DEFAULT_BUTTON = getattr(settings, 'FORMIT_DEFAULT_BUTTON', _('Submit'))

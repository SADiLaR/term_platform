import re

from django import template
from django.utils.safestring import mark_safe

"""A simple template tag to add a single Bootstrap icon.

If our needs grow, we should probably switch to something like
django-bootstrap-icons:
https://pypi.org/project/django-bootstrap-icons/
"""


register = template.Library()
icon_name_re = re.compile(r"[a-z0-9\-]+")


@register.simple_tag
def bs_icon(name):
    assert icon_name_re.fullmatch(name)
    return mark_safe(f'<i class="project-icon bi-{name}"></i>')

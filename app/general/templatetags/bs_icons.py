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


def _bs_icon(name):
    assert icon_name_re.fullmatch(name)
    return mark_safe(f'<i aria-hidden="true" class="icon bi-{name}"></i> ')
    # The trailing space is intentional: Since this is an inline element
    # usually followed by text, the absence/presence of a space is significant,
    # and usually wanted for layout. That's too hard to remember, so we always
    # add it. Multiple spaces are equal to one. That way the exact layout of
    # code in the templates doesn't matter. Beware of using {% spaceless %}
    # which will negate this. A pure CSS solution escaped me thus far, since a
    # space will take additional space in addition to a margin.


@register.simple_tag
def bs_icon(name):
    """Any of the Bootstrap icons"""
    return _bs_icon(name)


# a mapping from project types to Bootstrap icon names:
_icons = {
    "date": "calendar3",
    "document": "file-earmark",
    "language": "vector-pen",
    "project": "clipboard2",
    "subject": "book",
}


@register.simple_tag
def icon(name):
    """An "official" project-specific icon for the common cases"""
    if not (bs_name := _icons.get(name)):
        raise template.TemplateSyntaxError(f"'icon' requires a registered icon name (got {name!r})")

    return _bs_icon(bs_name)

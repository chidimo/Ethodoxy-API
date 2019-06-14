"""Custom template tags and filters"""
import re
import markdown
from django import template
from django.shortcuts import reverse
from django.template.defaultfilters import slugify
from django.utils.safestring import mark_safe

# pylint: disable = E1102

register = template.Library()

def hyperlink_underlined_markdown(string_to_process):
    """Added href to underline strings"""

    underline_string = re.search(r"<u>(.+)<\/u>", string_to_process)
    if underline_string:

        commentary_slug = slugify(underline_string.group(1))
        commentary_href = reverse("douay-rheims:commentary_detail", args=[commentary_slug])

        replacement_string = "[{}]({})".format(underline_string.group(1), commentary_href)

        new_string = re.sub(r"\<u\>(.+)\<\/u\>", replacement_string, string_to_process)
        new_string = new_string.replace(" :", "")
        return new_string
    return string_to_process

def hyperlink_underlined(string_to_process):
    """Added href to underline strings"""

    underline_string = re.search(r"<u>(.+)<\/u>", string_to_process)
    if underline_string:

        commentary_slug = slugify(underline_string.group(1))
        commentary_href = reverse("douay-rheims:commentary_detail", args=[commentary_slug])

        replacement_string = "<a href='{}' class='commentary'>{}</a>".format(commentary_href, underline_string.group(1))

        new_string = re.sub(r"<u>(.+)<\/u>", replacement_string, string_to_process)
        new_string = new_string.replace(" :", "")
        return new_string
    return string_to_process

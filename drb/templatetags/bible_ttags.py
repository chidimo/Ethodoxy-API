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
        commentary_href = reverse("bible:commentary_detail", args=[commentary_slug])

        replacement_string = "[{}]({})".format(underline_string.group(1), commentary_href)

        new_string = re.sub(r"<u>(.+)<\/u>", replacement_string, string_to_process)
        new_string = new_string.replace(" :", "")
        return new_string
    return string_to_process

# @register.filter()
# def markdown_format(text):
#     convert_underlines = hyperlink_underlined_markdown(text)
#     return mark_safe(markdown.markdown(convert_underlines))


modal = """
<a href="" data-toggle="modal" data-target="#Commentary">Here</a>

<div class="modal fade" id="Commentary" tabindex="-1" role="dialog" aria-labelledby="commentaryDetail" aria-hidden="true">
    <div class="modal-dialog" role="document">
        <div class="modal-content">
        
            <div class="modal-header">
                <h4 class="modal-title" id="commentaryDetail">{{ commentary.heading }} heading here</h4>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>

            <div class="modal-body">
                <p>{{ commentary.text }} some text here</p>
                
            </div>

            <div class="modal-footer">
                <button type="button" class="btn btn-primary" data-dismiss="modal">Close</button>
            </div>
        </div>
    </div>
</div>
"""


def hyperlink_underlined(string_to_process):
    """Added href to underline strings"""

    underline_string = re.search(r"<u>(.+)<\/u>", string_to_process)
    if underline_string:

        commentary_slug = slugify(underline_string.group(1))
        commentary_href = reverse("bible:commentary_detail", args=[commentary_slug])

        replacement_string = "<a href='{}' class='commentary'>{}</a>".format(commentary_href, underline_string.group(1))

        new_string = re.sub(r"<u>(.+)<\/u>", replacement_string, string_to_process)
        new_string = new_string.replace(" :", "")
        return new_string
    return string_to_process


@register.filter()
def markdown_format(text):
    convert_underlines = hyperlink_underlined(text)
    return mark_safe(convert_underlines)

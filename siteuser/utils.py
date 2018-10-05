# source: https://simpleisbetterthancomplex.com/tutorial/2017/02/21/how-to-add-recaptcha-to-django-site.html

import os
from functools import wraps

from django.template.defaultfilters import slugify
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.contrib import messages

import requests


def star_or_unstar_object(siteuser, pk, app_label, model):
    """
    Generic function for starring objects

    Parameters
    ------------
    app_label : str
        Sent with ajax request
    model_name : str
        Sent with ajax request
    """
    # Get the object
    obj_ct = ContentType.objects.get(app_label=app_label, model=model)
    model_instance = obj_ct.get_object_for_this_type(pk=pk)

    if model_instance.likes.filter(screen_name=siteuser.screen_name).exists():
        model_instance.likes.remove(siteuser)
        data = {'success' : True, 'message' : 'You disliked this {}'.format(model)}
    else:
        model_instance.likes.add(siteuser)
        data = {'success' : True, 'message' : 'You liked this {}'.format(model)}

    like_count = model_instance.likes.count()
    model_instance.save(update_fields=['like_count'])
    return data

def check_recaptcha(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        request.recaptcha_is_valid = None
        if request.method == 'POST':
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            if result['success']:
                request.recaptcha_is_valid = True
            else:
                request.recaptcha_is_valid = False
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def save_avatar(instance, filename):
    _, ext = os.path.splitext(filename)
    return "avatars/{}{}".format(instance.screen_name.lower(), ext)

def badge_icon(instance, filename):
    _, ext = os.path.splitext(filename)
    return "badges/{}_{}{}".format(instance.hierarchy, instance.name.lower(), ext)

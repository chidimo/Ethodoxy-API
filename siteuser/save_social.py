# from django.core.files import File
import json
from random import randint

import requests

from django.template.defaultfilters import slugify

from django.db import IntegrityError
from django.core.files.base import ContentFile
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.contrib import messages

from social_django.models import UserSocialAuth

from .models import SiteUser
from .views import send_email_upon_registration

CustomUser = get_user_model()

login_backends = {}
login_backends['django'] = 'django.contrib.auth.backends.ModelBackend'
login_backends['twitter'] = 'social_core.backends.twitter.TwitterOAuth'
login_backends['google_oauth2'] = 'social_core.backends.google.GoogleOAuth2'
login_backends['facebook'] = 'social_core.backends.facebook.FacebookOAuth2'

def save_avatar(image_url, model_object):
    response = requests.get(image_url)
    if response.status_code == 200:
        name = model_object.screen_name.lower()
        model_object.avatar.save(name, ContentFile(response.content), save=True)

def process_response(request, backend, response):
    """Process the response returned by a backend"""

    save_name = "response-{}.json".format(backend.name)
    with open(save_name, "w+") as fh:
        json.dump(response, fh)

    if backend.name == "twitter":
        screen_name = slugify(response['screen_name']) # twitter response contains a screen_name
        email = response.get('email', None)
        image = response['profile_image_url']
        location = response['location']
        first_name = response['name'].split()[0]
        try:
            last_name = response['name'].split()[1]
        except IndexError:
            last_name = ''
        if email is None:
            messages.error(request, "It appears you have no email connected with your twitter account. Registration not completed.")
        if not location:
            location = 'Unknown location'
        id_current_resp = response['id']

    elif backend.name == 'google-oauth2':
        screen_name = slugify(response['displayName'].strip())
        email = response['emails'][0]['value']
        first_name = response['name']['givenName']
        last_name = response['name']['familyName']
        image = response['image']['url'].split('?')[0]
        location = "Unknown location"
        id_current_resp = email
        try:
            url = response['url']
        except KeyError:
            pass # user has no google plus profile

    elif backend.name == 'facebook':
        first_name = response['name'].split()[0]
        try:
            last_name = response['name'].split()[1]
        except IndexError:
            last_name = ''
        screen_name = slugify("{}-{}".format(first_name, last_name))
        email = response.get('email', None)
        image = 'https://graph.facebook.com/{}/picture?type=large'.format(response['id'])
        location = "Unknown location"
        id_current_resp = response['id']
    else:
        return
    return screen_name, email, image, first_name, last_name, location, id_current_resp

def get_and_login_siteuser(request, user, screen_name, email, image, first_name, last_name, location):
    """If siteuser exists, just log in and move on, else create it and log in"""
    if SiteUser.objects.filter(user=user).exists():
        pass
    else:
        # keep looping until a SiteUser is successfully created
        while True:
            try:
                su = SiteUser.objects.create(user=user, screen_name=screen_name[:20], first_name=first_name, last_name=last_name, location=location)
                save_avatar(image, su)
                # send registration email
                send_email_upon_registration(request, su, via_social=True)
                messages.success(request, 'Your account has been successfully created and an email has been sent to you.')
                break
            except IntegrityError:
                screen_name = "{}{}".format(screen_name[:16], randint(1, 1000)) # append a random string
                continue
    login(request, user, backend=login_backends['django'])

def get_or_create_user_from_social_detail(request, provider, backend_name, screen_name, email, image, first_name, last_name, location, id_current_resp):
    """
    Create new user from social profile details
    """
    if CustomUser.objects.filter(email=email).exists():
        user = CustomUser.objects.get(email=email)

        # check whether account is already associated with a social account.
        # if yes, delete the association so that a new one can be established later in the pipeline.               
        try:
            social_account = user.social_auth.get(provider=provider)
            if social_account.uid != id_current_resp:
                messages.success(request, 'The {} account, {}, previously associated with {} was replaced.'.format(backend_name, social_account.uid, str(user)))
                social_account.delete()
        except UserSocialAuth.DoesNotExist:
            pass
        get_and_login_siteuser(request, user, screen_name, email, image, first_name, last_name, location)
    else:
        # uid field of UserSocialAuth for google is the email address. So this line specifically applies to google logins.
        # here the user tries to create a new primary account with an email that is already secondary to another account.
        social_ids = [each.uid for each in UserSocialAuth.objects.all()]
        if email in social_ids:
            connected_user = str(UserSocialAuth.objects.get(uid=email))
            messages.error(request, '{} is already connected to account {}'.format(email, connected_user))
            return
        else:
            try:
                user = CustomUser.objects.create_user(email=email, password=None)
                user.is_active = True
                user.save()
                get_and_login_siteuser(request, user, screen_name, email, image, first_name, last_name, location)
            except ValueError:
                messages.error(request, "Invalid email")
                return

def save_social_profile(backend, user, response, *args, **kwargs):
    """
    Create a user account via social media account
    If user is already logged in, simply connect the invoked social media account.
    If a social media account from same provide has already been connect with the user, then don't connect another one
    to avoid MultipleObjectsReturned error in account management view. Exit the pipeline
    """
    request = kwargs['request']

    provider = backend.name
    backend_name = backend.name
    if backend.name == 'google-oauth2':
        backend_name = 'google'

    if request.user.is_authenticated:
        messages.success(request, 'Your {} account has been successfully connected.'.format(backend_name))
        login(request, request.user, backend=login_backends['django'])
    else:
        screen_name, email, image, first_name, last_name, location, id_current_resp = process_response(request, backend, response)
        get_or_create_user_from_social_detail(request, provider, backend_name, screen_name, email, image, first_name, last_name, location, id_current_resp)

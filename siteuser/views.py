
"""Views"""

import uuid
import operator
from functools import reduce
from collections import OrderedDict, namedtuple, deque

from django.http import JsonResponse
from django.db.models import Q, Count, Prefetch
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.views import generic
from django.shortcuts import render, reverse, redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from django_addanother.views import CreatePopupMixin
from pure_pagination.mixins import PaginationMixin
from social_django.models import UserSocialAuth

from .utils import star_or_unstar_object, check_recaptcha
from .models import SiteUser, Role, Message
from .forms import PassWordGetterForm, EmailAndPassWordGetterForm, SiteUserRegistrationForm, SiteUserEditForm, NewRoleForm

CustomUser = get_user_model()

def get_api_key(request):
    siteuser = request.user.siteuser
    if siteuser.key:
        msg = "You already have an API key. Maybe you want to reset it."
    else:
        siteuser.key = uuid.uuid4()
        siteuser.save(update_fields=['key'])
        msg = "Your API key is {}".format(siteuser.key)
    messages.success(request, msg)
    return redirect(reverse("siteuser:account_management"))

def reset_api_key(request):
    siteuser = request.user.siteuser
    siteuser.key = uuid.uuid4()
    siteuser.save(update_fields=['key'])
    msg = "Your new API key is {}. Don't forget to update your applications".format(siteuser.key)
    messages.warning(request, msg)
    return redirect(reverse("siteuser:account_management"))

class SiteUserIndex(PaginationMixin, generic.ListView):
    model = SiteUser
    context_object_name = 'siteuser_list'
    template_name = "siteuser/index.html"
    paginate_by = 20

class SiteUserCommonLocation(PaginationMixin, generic.ListView):
    model = SiteUser
    context_object_name = 'siteuser_list'
    template_name = "siteuser/siteuser_common_location.html"
    paginate_by = 20

    def get_queryset(self):
        locations = self.kwargs['location'].split(" ")
        query = []
        for each in locations:
            query.append(Q(location__contains=each))
        query = reduce(operator.or_, query)
        return SiteUser.objects.filter(query)

    def get_context_data(self, *args):
        context = super().get_context_data(*args)
        context['location'] = self.kwargs['location']
        return context

def validate_screen_name(request):
    screen_name = request.GET.get('screen_name', None)
    data = {'is_taken': SiteUser.objects.filter(screen_name=screen_name).exists()}
    if data['is_taken']:
        data['error_message'] = 'Sorry, this screen name is not available.'
    return JsonResponse(data)

def send_email_upon_registration(request, new_siteuser, via_social=False):
    """Sends an email to a newly registered user"""

    screen_name = new_siteuser.screen_name
    email = new_siteuser.user.email
    subject = "Accessible Orthodoxy - Welcome {}.".format(screen_name)
    from_email = settings.EMAIL_HOST_USER

    if via_social:
        context = {'screen_name' : screen_name}
        text_email = render_to_string("siteuser/welcome_email_social.txt", context)
        html_email = render_to_string("siteuser/welcome_email_social.html", context)
    else:
        activation_link = request.build_absolute_uri(new_siteuser.get_user_creation_url())
        context = {'screen_name' : screen_name, 'activation_link' : activation_link}
        text_email = render_to_string("siteuser/welcome_email.txt", context)
        html_email = render_to_string("siteuser/welcome_email.html", context)

    for each in [email, "accessibleorthodoxy@outlook.com"]:
        msg = EmailMultiAlternatives(subject, text_email, from_email, [each])
        msg.attach_alternative(html_email, "text/html")
        msg.send()

@check_recaptcha
def new_siteuser(request):
    template = "siteuser/new_siteuser.html"
    if request.method == 'POST':
        form = SiteUserRegistrationForm(request.POST)
        if form.is_valid():
            if request.recaptcha_is_valid:
                form = form.cleaned_data
                email = form['email']
                screen_name = form['screen_name']
                password1 = form['password1']

                user = CustomUser(email=email)
                user.set_password(password1)
                user.save()
                new_siteuser = SiteUser(user=user, screen_name=screen_name)
                new_siteuser.save()

                send_email_upon_registration(request, new_siteuser)
            else:
                form.add_error(None, 'Error: Please complete the reCAPTCHA.')
                return render(request, template, {'form' : form})

            return redirect(reverse('siteuser:new_success', args=[screen_name]))
        else:
            return render(request, template, {'form' : form})
    return render(request, template, {'form' : SiteUserRegistrationForm()})

def welcome_siteuser(request, screen_name):
    template = 'siteuser/new_success.html'
    context = {'screen_name' : screen_name}
    return render(request, template, context)

def activate_siteuser(request, screen_name, pk):
    # check time to see if link has expired.
    user = CustomUser.objects.get(pk=pk)
    context = {}
    if user.is_active:
        siteuser = SiteUser.objects.get(user=user)
        context["active"] = "active"
        context["siteuser"] = siteuser
    else:
        user.is_active = True
        user.save()
        siteuser = SiteUser.objects.get(user=user)
        context["siteuser"] = siteuser
    context["screen_name"] = screen_name
    return render(request, "siteuser/new_activation.html", context)

class SiteUserEdit(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = SiteUser
    form_class = SiteUserEditForm
    template_name = 'siteuser/edit.html'
    success_message = "Profile updated successfully."

    def get_object(self):
        return self.request.user.siteuser

    def get_success_url(self):
        return reverse('siteuser:account_management')

def delete_account(request):
    template = 'siteuser/delete_account.html'
    user = request.user
    siteuser = user.siteuser
    if request.method == 'POST':
        form = PassWordGetterForm(request.POST, user=user)
        if form.is_valid():
            siteuser.delete()
            user.delete()
            msg = "Your account has been permanently deleted"
            messages.success(request, msg)
            return redirect('/')
        else:
            # return render(request, template, {'form' : form })
            msg = "You entered a wrong password"
            messages.error(request, msg)
            return redirect('/')
    return render(request, template, {'form' : PassWordGetterForm(user=user) })

def deactivate_account(request):
    template = 'siteuser/deactivate_account.html'
    user = request.user
    if request.method == 'POST':
        form = PassWordGetterForm(request.POST, user=user)
        if form.is_valid():
            user.is_active = False
            user.save()
            msg = "Your account has been deactivated"
            messages.success(request, msg)
            return redirect('/')
        else:
            # return render(request, template, {'form' : form })
            msg = "You entered a wrong password"
            messages.error(request, msg)
            return redirect('/')
    return render(request, template, {'form' : PassWordGetterForm(user=user) })

# complete later
def activate_account(request):
    template = 'siteuser/activate_account.html'
    if request.method == 'POST':
        form = EmailAndPassWordGetterForm(request.POST)
        if form.is_valid():
            user.is_active = False
            user.save()
            msg = "Your account has been deactivated"
            messages.success(request, msg)
            return redirect('/')
        else:
            msg = "You entered a wrong password"
            messages.error(request, msg)
            return redirect('/')
    return render(request, template, {'form' : PassWordGetterForm(user=user) })

@login_required
def account_management(request):
    template = "siteuser/account_management.html"
    context = {}
    user = request.user
    siteuser = user.siteuser

    try:
        context['facebook_login'] = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        context['facebook_login'] = None

    try:
        context['google_login'] = user.social_auth.get(provider='google-oauth2')
    except UserSocialAuth.DoesNotExist:
        context['google_login'] = None

    try:
        context['twitter_login'] = user.social_auth.get(provider='twitter')
    except UserSocialAuth.DoesNotExist:
        context['twitter_login'] = None

    context['can_disconnect'] = (user.social_auth.count() > 1 or user.has_usable_password())

    context['siteuser'] = siteuser
    context['user_songs'] = Song.objects.filter(creator=siteuser)
    context['user_posts'] = Post.objects.filter(creator=siteuser)
    context['inbox_messages'] = Message.objects.filter(receiver=siteuser)
    context['outbox_messages'] = Message.objects.filter(creator=siteuser)
    context['total_likes'] = "y"

    return render(request, template, context)

@login_required
def social_password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            login(request, request.user, backend='django.contrib.auth.backends.ModelBackend',)
            return redirect('/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'siteuser/social_password_change_form.html', {'form': form})

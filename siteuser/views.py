
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

from song.models import Song
from blog.models import Post, Comment
from request.models import Request
from author.models import Author
from song_media.models import Score, Midi, VideoLink

from .utils import star_or_unstar_object, check_recaptcha
from .models import SiteUser, Role, Message
from .forms import (PassWordGetterForm, EmailAndPassWordGetterForm, SiteUserRegistrationForm,
    SiteUserEditForm, NewRoleForm, NewMessageForm, ReplyMessageForm
)

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

    def get_queryset(self):
        siteusers = SiteUser.objects.prefetch_related('roles').exclude(user__email='unknown@user.net')
        return_val = []
        for siteuser in siteusers:
            stats = {}
            stats['siteuser'] = siteuser
            stats['song_count'] = Song.objects.filter(creator=siteuser, publish=True).count()
            stats['post_count'] = Post.objects.filter(creator=siteuser, publish=True).count()
            stats['comment_count'] = Comment.objects.filter(creator=siteuser).count()
            stats['score_count'] = Score.objects.filter(creator=siteuser).count()
            stats['midi_count'] = Midi.objects.filter(creator=siteuser).count()
            stats['siteuser_roles'] = siteuser.roles.all()
            return_val.append(stats)
        return return_val

class SiteUserCommonRoles(PaginationMixin, generic.ListView):
    model = SiteUser
    context_object_name = 'siteuser_list'
    template_name = "siteuser/siteuser_common_roles.html"
    paginate_by = 20

    def get_queryset(self):
        role = self.kwargs['role']
        return SiteUser.objects.filter(roles__name__in=[role])

    def get_context_data(self, *args):
        context = super().get_context_data(*args)
        context['role'] = self.kwargs['role']
        return context

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

class SongLikers(PaginationMixin, generic.ListView):
    model = SiteUser
    context_object_name = 'siteuser_list'
    template_name = 'siteuser/likers_song.html'
    paginate_by = 24

    def get_queryset(self):
        song = Song.objects.get(pk=self.kwargs['pk'])
        return song.likes.all()

    def get_context_data(self, *args):
        context = super().get_context_data(*args)
        context['song'] = Song.objects.get(pk=self.kwargs['pk'])
        return context

class PostLikers(PaginationMixin, generic.ListView):
    model = SiteUser
    context_object_name = 'siteuser_list'
    template_name = 'siteuser/likers_post.html'
    paginate_by = 24

    def get_queryset(self):
        post = Post.objects.get(pk=self.kwargs['pk'])
        return post.likes.all()

    def get_context_data(self, *args):
        context = super().get_context_data(*args)
        context['post'] = Post.objects.get(pk=self.kwargs['pk'])
        return context

class CommentLikers(PaginationMixin, generic.ListView):
    model = SiteUser
    context_object_name = 'siteuser_list'
    template_name = 'siteuser/likers_comment.html'
    paginate_by = 24

    def get_queryset(self):
        comment = Comment.objects.get(pk=self.kwargs['pk'])
        return comment.likes.all()

    def get_context_data(self, *args):
        context = super().get_context_data(*args)
        context['comment'] = Comment.objects.get(pk=self.kwargs['pk'])
        return context

class SiteUserComments(PaginationMixin, generic.ListView):
    model = Comment
    context_object_name = 'user_comments'
    template_name = "siteuser/comments.html"
    paginate_by = 20

    def post(self, request, *args, **kwargs):
        if request.is_ajax():        
            pk  = int(request.POST.get('pk')) # need to send this since I have multiple like buttons on this page
            model = request.POST.get('model')
            app_label = request.POST.get('app_label')
            siteuser = request.user.siteuser
            data = star_or_unstar_object(siteuser, pk, app_label, model)
            return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["siteuser"] = SiteUser.objects.get(pk=self.kwargs.get("pk", None))
        return context

    def get_queryset(self):
        creator = SiteUser.objects.get(pk=self.kwargs.get("pk", None))
        return Comment.objects.filter(creator=creator)

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
    subject = "ChoralCentral - Welcome {}.".format(screen_name)
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

    for each in [email, "choralcentral@gmail.com"]:
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

class NewRole(LoginRequiredMixin, SuccessMessageMixin, CreatePopupMixin, generic.CreateView):
    form_class = NewRoleForm
    template_name = 'siteuser/role_new.html'
    success_message = "New role added successfully"

class RoleIndex(generic.ListView):
    model = Role
    context_object_name = 'role_list'
    template_name = 'siteuser/role_index.html'

def admin_media_index(request):
    try:
        if request.user.is_admin is False:
            return redirect('/')
    except AttributeError:
        return redirect('/')
    template = "siteuser/admin_media_index.html"
    context = {}
    context['scores'] = Score.objects.all()
    context['midis'] = Midi.objects.all()
    context['siteuser'] = request.user.siteuser
    return render(request, template, context)

class SiteUserLibrary(LoginRequiredMixin, generic.DetailView):
    model = SiteUser
    context_object_name = 'siteuser'
    template_name = "siteuser/library.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk', None)
        slug = self.kwargs.get('slug', None)
        siteuser = SiteUser.objects.get(pk=pk, slug=slug)

        if self.request.user == siteuser.user: # requester is user of interest
            context['is_library_owner'] = True
            context['user_songs'] = Song.objects.filter(creator__pk=pk).order_by('publish')
            context['user_posts'] = Post.objects.filter(creator__pk=pk).order_by('publish')
        else:
            q = Q(publish=True) and Q(creator__pk=pk)
            context['user_songs'] = Song.objects.filter(creator__pk=pk, publish=True).order_by('-created').values('pk', 'title', 'publish', 'like_count', 'slug')
            context['user_posts'] = Post.objects.filter(creator__pk=pk, publish=True).order_by('-created').values('pk', 'title', 'publish', 'slug')

        context['user_requests'] = Request.objects.filter(creator__pk=pk)
        context['user_authors'] = Author.objects.filter(creator__pk=pk)
        context['scores'] = Score.objects.filter(creator__pk=pk).select_related('song').order_by("song", "-fsize", "-created", "downloads")
        context['midis'] = Midi.objects.filter(creator__pk=pk).select_related('song').order_by("song", "-fsize", "-created", "downloads")
        context['user_videos'] = VideoLink.objects.filter(creator__pk=pk).select_related('song')
        context['total_likes'] = "x"
        return context

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

class NewMessage(LoginRequiredMixin, generic.CreateView):
    form_class = NewMessageForm
    template_name = 'siteuser/message_new.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['receiver'] = SiteUser.objects.get(pk=self.kwargs['pk'], slug=self.kwargs['slug'])
        return context

    def form_valid(self, form):
        form.instance.creator = self.request.user.siteuser
        form.instance.receiver = SiteUser.objects.get(pk=self.kwargs['pk'], slug=self.kwargs['slug'])
        form.save()
        return redirect('siteuser:account_management')

def reply_message(request, pk):
    template = 'siteuser/message_reply.html'
    context = {}
    msg = Message.objects.get(pk=pk)
    thread_id = msg.thread_id
    creator = request.user.siteuser
    receiver = msg.creator

    if request.method == 'POST':
        form = ReplyMessageForm(request.POST)
        if form.is_valid():
            body = form.cleaned_data['body']
            msg = Message.objects.create(body=body, creator=creator, receiver=receiver, thread_id=thread_id)
            return redirect('siteuser:account_management')
        else:
            return render(request, template, {'form' : form, 'receiver' : receiver})
    return render(request, template, {'form' : ReplyMessageForm(), 'receiver' : receiver})

class ViewMessage(LoginRequiredMixin, generic.DetailView):
    model = Message
    template_name = 'siteuser/message_view.html'
    context_object_name = 'message'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset=None)

        # if the receiver is the one to read it, then mark it read
        if self.object.receiver == self.request.user.siteuser:
            self.object.read = True
            self.object.save(update_fields=['read'])
        return self.object

class ViewMessageThread(LoginRequiredMixin, generic.ListView):
    model = Message
    template_name = 'siteuser/message_view_thread.html'
    context_object_name = 'message_list'

    def get_queryset(self, queryset=None):
        thread_id = Message.objects.get(pk=self.kwargs['pk']).thread_id
        return Message.objects.filter(thread_id=thread_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['partner'] = Message.objects.get(pk=self.kwargs['pk']).creator
        return context

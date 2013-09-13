from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import FormView, CreateView
from django.views.generic.dates import ArchiveIndexView
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.db.models import Q
from django.shortcuts import get_object_or_404
from foxie.apps.main.forms import MyAuthenticationForm, YipForm, FollowForm, MyPasswordChangeForm, ContactForm
from foxie.apps.registration.forms import RegistrationForm
from foxie.apps.main.models import Yip, Follower, Tag

import logging
from random import choice
import re

logger = logging.getLogger(__name__)

class Account(FormView):
    form_class = MyPasswordChangeForm
    template_name = "main/account.html"

    def get_form_kwargs(self):
        kwargs = super(Account, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(Account, self).dispatch(*args, **kwargs)

class Login(FormView):
    form_class = MyAuthenticationForm
    template_name = "main/signin.html"

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

    def form_invalid(self, form):
        return HttpResponseRedirect(self.request.META['HTTP_REFERER'])

    def dispatch(self, request, *args, **kwargs):
        request.session.set_test_cookie()
        return super(Login, self).dispatch(request, *args, **kwargs)

class Logout(View):
    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return HttpResponseRedirect(settings.LOGOUT_REDIRECT_URL)
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(Logout, self).dispatch(*args, **kwargs)

class YipView(CreateView, TemplateView):
    model = Yip
    form_class = YipForm
    success_url = '/'
    template_name = 'main/yip_feed.html'

    def form_valid(self, form):
        form.instance.user = User.objects.get(username=self.request.user)
        form.save()
        matches = re.findall(r'#\w*', form.instance.text)
        for match in matches:
            obj, created = Tag.objects.get_or_create(text=match[1:], tag_type="HASHTAG")
            form.instance.tags.add(obj)
        matches = re.findall(r'@\w*', form.instance.text)
        for match in matches:
            if User.objects.filter(username=match[1:]).exists():
                obj, created = Tag.objects.get_or_create(text=match[1:], tag_type="AT")
                form.instance.tags.add(obj)
        context = self.get_context_data()
        following = [ relationship.followee for relationship in Follower.objects.filter(follower__username=self.request.user)]
        following.append(self.request.user.username)
        context['yips'] = Yip.objects.filter(Q(user__username__in=following) | Q(tags__tag_type="AT", tags__text=self.request.user)).order_by('-dt')
        return self.render_to_response(context)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(YipView, self).dispatch(*args, **kwargs)

class Profile(TemplateView):
    template_name = "main/profile.html"

    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data(**kwargs)
        context['profile_user'] =  self.kwargs['profile_user']
        user = get_object_or_404(User, username=self.kwargs['profile_user'])
        context['yips'] = Yip.objects.filter(Q(user__username=self.kwargs['profile_user']) | Q(tags__tag_type="AT", tags__text=self.kwargs['profile_user'])).order_by('-dt')
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(Profile, self).dispatch(*args, **kwargs)

class FollowView(CreateView):
    model = Follower
    form_class = FollowForm
    success_url = '/home/'
    template_name = 'main/home.html'

    def form_valid(self, form):
        form.instance.follower = User.objects.get(username=self.request.user)
        return super(FollowView, self).form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(Profile, self).dispatch(*args, **kwargs)

class TrendingView(ArchiveIndexView):
    model = Yip
    template_name = "main/trending.html"
    date_field = 'dt'
    allow_empty = True

    def get_context_data(self, **kwargs):
        context = super(TrendingView, self).get_context_data(**kwargs)
        if self.request.GET:
            context['name'] = self.request.GET.get('search', "")
        else:
            context['name'] = self.kwargs['name']
        return context

    def get_dated_items(self):
        if self.request.GET:
            qs = self.get_dated_queryset(ordering='-%s' % self.get_date_field(), tags__text__iexact=self.request.GET.get('search', ""))
            date_list = self.get_date_list(qs, ordering='DESC')

            if not date_list:
                qs = qs.none()
            return (date_list, qs, {})
        else:
            qs = self.get_dated_queryset(ordering='-%s' % self.get_date_field(), tags__text__iexact=self.kwargs['name'])
            date_list = self.get_date_list(qs, ordering='DESC')

            if not date_list:
                qs = qs.none()
            return (date_list, qs, {})

class Home(TemplateView):
    template_name = "main/home.html"
    fox_sayings = ["Ring-ding-ding-ding-dingeringeding",
                   "Wa-pa-pa-pa-pa-pa-pow",
                   "Hatee-hatee-hatee-ho",
                   "Joff-tchoff-tchoffo-tchoffo-tchoff",
                   "Jacha-chacha-chacha-chow",
                   "Fraka-kaka-kaka-kaka-kow",
                   "A-hee-ahee ha-hee",
                   "A-oo-oo-oo-ooo"]


    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        if not self.request.user.is_authenticated():
            context['registration_form'] = RegistrationForm()
            context['signin_form'] = MyAuthenticationForm()
        else:
            context['what_does_the_fox_say'] = choice(self.fox_sayings)
            following = [ relationship.followee for relationship in Follower.objects.filter(follower__username=self.request.user)]
            following.append(self.request.user.username)
            context['yips'] = Yip.objects.filter(Q(user__username__in=following) | Q(tags__tag_type="AT", tags__text=self.request.user)).order_by('-dt')
        return context

class About(TemplateView):
    template_name = "main/about.html"

class Contact(FormView):
    form_class = ContactForm
    template_name = "main/contact.html"

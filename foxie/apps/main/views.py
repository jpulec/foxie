from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import FormView, CreateView
from django.views.generic.dates import ArchiveIndexView
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from foxie.apps.main.forms import MyAuthenticationForm, YipForm, FollowForm
from foxie.apps.main.models import Yip, Follower, Tag

import logging
from random import choice
import re

logger = logging.getLogger(__name__)

class Login(FormView):
    form_class = MyAuthenticationForm

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

    def dispatch(self, request, *args, **kwargs):
        request.session.set_test_cookie()
        return super(Login, self).dispatch(request, *args, **kwargs)

class Logout(View):
    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return HttpResponseRedirect(settings.LOGOUT_REDIRECT_URL)

class YipView(CreateView):
    model = Yip
    form_class = YipForm
    success_url = '/profile/'
    template_name = 'main/profile.html'

    def form_valid(self, form):
        form.instance.user = User.objects.get(username=self.request.user)
        matches = re.findall(r'#\w*', form.instance.text)
        for match in matches:
            obj, created = Tag.objects.get_or_create(text=match)
            form.instance.tags.add(obj)
        return super(YipView, self).form_valid(form)

class Profile(TemplateView):
    template_name = "main/profile.html"
    fox_sayings = ["Ring-ding-ding-ding-dingeringeding",
                   "Wa-pa-pa-pa-pa-pa-pow",
                   "Hatee-hatee-hatee-ho",
                   "Joff-tchoff-tchoffo-tchoffo-tchoff",
                   "Jacha-chacha-chacha-chow",
                   "Fraka-kaka-kaka-kaka-kow",
                   "A-hee-ahee ha-hee",
                   "A-oo-oo-oo-ooo"]


    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data(**kwargs)
        context['what_does_the_fox_say'] = choice(self.fox_sayings)
        following = [ relationship.followee for relationship in Follower.objects.filter(follower__username=self.request.user)]
        following.append(self.request.user.username)
        context['yips'] = Yip.objects.filter(user__username__in=following).order_by('-dt')
        context['yip_form'] = YipForm()
        context['follow_form'] = FollowForm()
        return context

class FollowView(CreateView):
    model = Follower
    form_class = FollowForm
    success_url = '/profile/'
    template_name = 'main/profile.html'

    def form_valid(self, form):
        form.instance.follower = User.objects.get(username=self.request.user)
        return super(FollowView, self).form_valid(form)

class TrendingView(ArchiveIndexView):
    model = Yip
    template_name = "main/trending.html"
    date_field = 'dt'

    def get_dated_items(self):
        if self.request.GET:
            qs = self.get_dated_queryset(ordering='-%s' % self.get_date_field(), tag__text__eq=self.request.GET.get('search', ""))
            date_list = self.get_date_list(qs, ordering='DESC')

            if not date_list:
                qs = qs.none()
            return (date_list, qs, {})

class Home(FormView):
    template_name = "main/home.html"
    form_class = MyAuthenticationForm
    success_url = '.'

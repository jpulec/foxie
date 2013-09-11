from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import FormView
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from foxy.apps.main.forms import MyAuthenticationForm, YipForm

import logging
from random import choice

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

class Profile(FormView):
    template_name = "main/profile.html"
    form_class = YipForm
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
        return context

class Home(FormView):
    template_name = "main/home.html"
    form_class = MyAuthenticationForm
    success_url = '.'

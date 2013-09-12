from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.http import HttpResponseRedirect
from foxie.apps.registration.forms import RegistrationForm

class Register(CreateView):
    model = User
    form_class = RegistrationForm
    success_url = "/profile/"

    def form_valid(self, form):
        form.instance.backend = 'django.contrib.auth.backends.ModelBackend'
        self.object = form.save()
        auth_login(self.request, self.object)
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
        return HttpResponseRedirect(self.get_success_url())

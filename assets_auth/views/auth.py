from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from assets_auth.forms.forms import SignUpForm


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('assets_auth:login')
    template_name = 'sign-up/sign-up.html'

    def form_valid(self, form):
        self.object = form.save()

        user = authenticate(
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password1'],
        )
        login(self.request, user)

        return HttpResponseRedirect(self.get_success_url())

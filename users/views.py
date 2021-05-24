import json
from json import JSONEncoder

from django.contrib import messages
from django.contrib.auth import logout, get_user_model
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordChangeView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from .tasks import sent_activation_mail
from .forms import LoginForm, SignUpForm
from .tokens import account_activation_token

User = get_user_model()


class SignUpView(View):
    form_class = SignUpForm
    success_url = reverse_lazy('users:signin')
    template_name = 'account/signup.html'

    def get(self, request):
        form = SignUpForm()
        return render(request, 'account/signup.html', {'form': form})

    def post(self, request):
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                context = {
                    'protocol': request.scheme,
                    'domain': current_site.domain,
                }
                sent_activation_mail.delay(user.id, context)
                return HttpResponse('Please confirm your email address to '
                                    'complete the registration')
        else:
            form = SignUpForm()
        return render(request, 'account/signup.html', {'form': form})


class Activate(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user,
                                                                     token):
            user.is_active = True
            user.save()
            messages.success(request, "Your account have been confirmed.")
            return redirect('users:signin')
        else:
            messages.warning(request, "The confirmation link was invalid, "
                                      "possibly because it has already been "
                                      "used.")
            return redirect('users:signup')


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'account/login.html'


class LoginOutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('polls:index', ))


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'account/change-password.html'
    success_url = reverse_lazy('polls:index')

    def form_valid(self, form):
        messages.success(self.request, 'Your password has been changed.')
        return super().form_valid(form)

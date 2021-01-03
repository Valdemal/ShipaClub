from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from .forms import AuthUserForm, RegisterUserForm, ProfileForm
from .models import Profile
# Для подтверждения по мейлу
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.contrib import messages
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from django.conf import settings
from django.views.generic import DetailView
from django.views.generic.base import View
from django.views.generic.edit import FormView, UpdateView
from django.http.response import JsonResponse

def profile_form(request):
    form = ProfileForm()

    if request.is_ajax():
        form = ProfileForm(request.POST)
        if form.is_valid():
            data = {
                'first_name':form.cleaned_data['first_name'],
                'last_name':form.cleaned_data['last_name'],
                'avatar':form.cleaned_data['avatar'],
            }
            return JsonResponse({'success':data})
        else:
            return JsonResponse({'errors':form.errors})

class ProfileView(DetailView):
    model = Profile
    template_name = 'profile/profile.html'
    
class AccPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm_form.html'
    success_url= reverse_lazy('accounts:login')


class AccPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset.html'
    email_template_name = 'messages/reset.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    



class AccPasswordChangeView(PasswordChangeView):
    template_name = 'registration/password_change.html'
    success_url = reverse_lazy('accounts:login')


class AccLoginView(UserPassesTestMixin, LoginView):
    template_name = 'registration/login.html'
    form_class = AuthUserForm
    redirect_authenticated_user = True  # Классно, но небезопасно

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['next'] = reverse_lazy('main:index')
        return context

    def test_func(self):
        return True


class AccRegisterView(UserPassesTestMixin,FormView):
    model = User
    template_name = 'registration/registration.html'
    form_class = RegisterUserForm

    def post(self, request):
        
        form = self.get_form(form_class=RegisterUserForm)
        if form.is_valid():
            
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = User.objects.create_user(username=username, email=email)
            user.set_password(password)
            user.is_active = False
            user.save()

            current_site = get_current_site(self.request)
            message = render_to_string('messages/activate.html',{
                'user':user,
                    'domain':current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':PasswordResetTokenGenerator().make_token(user),
            })
            email_message = EmailMessage(
                'Activate your Account',
                message,
                settings.EMAIL_HOST_USER,
                [email],
            )
            email_message.send()
            return render(request, 'messages/activate_success.html', context={'username':username, 'email':email})
            # return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def test_func(self):
        "Безопасно, но не классно"
        
        return self.request.user.is_anonymous

    def get_context_data(self, *args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['next'] = reverse_lazy('main:index')
        return context

class AccActivateView(View):
    def get(self, request, uid64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uid64))
            user = User.objects.get(pk=uid)
        except:
            user = None

        if user is not None and PasswordResetTokenGenerator().check_token(user, token):
            user.is_active = True
            user.save()
            profile = Profile.objects.create(user= user)
            profile.save()

            return redirect('accounts:login')
        return render(request, 'messages/activate_failed.html', status=401)


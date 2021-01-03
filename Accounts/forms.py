from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from Accounts.models import Profile
from django.forms import widgets


class ProfileForm(forms.Form):
    # first_name = forms.CharField(max_length=30)
    # last_name = forms.CharField(max_length=150)
    # avatar = 

    class Meta:
        model = Profile
        is_multipart = True
        fields = ('avatar', 'user__first_name', 'user__last_name')
        widgets = {
            'first_name':widgets.Input(attrs={}),
            'last_name':widgets.Input(attrs={}),
            'avatar': widgets.FileInput(attrs={}),
        }



class AuthUserForm(AuthenticationForm,forms.ModelForm):
    username = forms.CharField(max_length=20,
    widget=forms.widgets.Input(attrs={'class':"row", 'placeholder':"Имя пользователя", 'type':"text"}))
    password = forms.CharField(
    widget=forms.widgets.PasswordInput(attrs={'class':"row", 'placeholder':"Пароль",'type':"password"}))


    class Meta:
        model = User
        fields = ('username', 'password')
    


class RegisterUserForm(forms.ModelForm):
    username = forms.CharField(max_length=20,
    widget=forms.widgets.Input(attrs={'class':"row", 'placeholder':"Имя пользователя", 'type':"text"}))
    
    email = forms.EmailField(required=True,widget = forms.widgets.EmailInput(attrs={'class':"row", 'placeholder':"Email", 'type':"email"}))

    password = forms.CharField(
    widget=forms.widgets.PasswordInput(attrs={'class':"row", 'placeholder':"Пароль",'type':"password"}))

    password2 = forms.CharField(
    widget=forms.widgets.PasswordInput(attrs={'class':"row", 'placeholder':"Повторите пароль",'type':"password"}))
    field_order = ['username', 'email', 'password']
    class Meta:
        model = User
        fields = ('username','email', 'password')
    
    def clean(self):
        super().clean()
        errors = {}
 
        for user in User.objects.all():
            if self.cleaned_data['username'] == user.username:
                errors['username'] = ValidationError('Пользователь с таким именем уже существует.')
            if self.cleaned_data['email'] == user.email:
                errors['email'] = ValidationError('Пользователь с таким email уже существует.')

        if self.cleaned_data['password'] != self.cleaned_data['password2']:
            errors['password'] = ValidationError('Пароли не совпадают.')

        if len(self.cleaned_data['password']) < 8:
            errors['password'] = ValidationError('Пароль должен содержать не менее 8 символов.')

        if errors:
            raise ValidationError(errors)

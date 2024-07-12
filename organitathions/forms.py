from .models import Account, Organitathion, AdressOrg, Tag, Comment
from django import forms
from django.forms import ModelForm
from django.core.validators import ValidationError
from string import ascii_uppercase, punctuation as punc

class RegisterForm(ModelForm):
    class Meta:
        model = Account
        fields = ['username', 'password', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control rows-3 col-xs-2'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control',}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def clean_username(self):
        username = self.cleaned_data["username"]
        if Account.objects.filter(username=username).exists():
            raise ValidationError("Такой логин уже существует")
        return username
    
    def clean_password2(self):
        slovo = ascii_uppercase 
        password = self.cleaned_data["password"]
        password2 = self.cleaned_data["password2"]
        if password != password2:
            raise ValidationError("Пароли не совпадают")
        if len(password) < 8:
            raise ValidationError("Пароль должен содержать не менее 8 символов")
        if " " in password:
            raise ValidationError("Пароль не должен содержать пробелов")
        if not any(char in slovo for char in password):
            raise ValidationError("Пароль должен содержать хотя бы одну заглавную букву")
        if not any(dig in punc for dig in password):
            raise ValidationError("Пароль должен содержать хотя бы один специальный символ")
        return password
    

class LoginForm(ModelForm):
    class Meta:
        model = Account
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control rows-3 col-xs-2'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control',}),
        }

class AddOrgForm(ModelForm):
    class Meta:
        model = Organitathion
        fields = ['name', 'content', 'web_site', 'phone', 'photo', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'web_site': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }
    
    def clean_email(self):
        email = self.cleaned_data["email"]
        if "@" not in email:
            raise ValidationError("Поле должно содержать знак @")
        return email

class OrgAdressForm(ModelForm):
    class Meta:
        model = AdressOrg
        fields = ['country', 'city', 'street', 'region']
        widgets = {
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'street': forms.TextInput(attrs={'class': 'form-control'}),
            'region': forms.TextInput(attrs={'class': 'form-control'}),
        }


class OrgTagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['title']
        widgets = {
            'title': forms.Textarea(attrs={'class': 'form-control', "placeholder": "Продажа авто"}),
        }
        

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'text']
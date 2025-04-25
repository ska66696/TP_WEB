from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your login'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'})
    )

class SignUpForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        label="Login",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'dr_pepper'})
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'drpepper@mail.ru'})
    )
    nickname = forms.CharField(
        max_length=50,
        label="NickName",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dr. Pepper'})
    )
    password = forms.CharField(
        label="Password",
        min_length=8,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '********'})
    )
    password_confirm = forms.CharField(
        label="Repeat password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '********'})
    )
    avatar = forms.ImageField(
        label="Upload avatar",
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("A user with that username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already registered.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Passwords do not match.")
        return cleaned_data
    
class ProfileEditForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'drpepper@mail.ru'})
    )
    nickname = forms.CharField(
        max_length=50,
        required=True,
        label="NickName",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dr. Pepper'})
    )
    avatar = forms.ImageField(
        label="Upload avatar",
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.user and email:
            other_users = User.objects.filter(email=email).exclude(pk=self.user.pk)
            if other_users.exists():
                raise ValidationError("This email address is already in use by another user.")
        return email
    
class AskForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        label="Title",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter question title'})
    )
    text = forms.CharField(
        label="Text",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Describe your question'})
    )
    tags = forms.CharField(
        max_length=100,
        label="Tags",
        required=False,
        help_text="Enter tags separated by commas. No more than 5 tags.",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., python, java, go'})
    )

    def clean_tags(self):
        tags_string = self.cleaned_data.get('tags', '')
        tag_names = [tag.strip().lower() for tag in tags_string.split(',') if tag.strip()]

        if len(tag_names) > 5:
            raise ValidationError("Please enter no more than 5 tags.")
        
        return tag_names
    
class AnswerForm(forms.Form):
    text = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={
            'class': 'form-control', 'rows': 5, 'placeholder': 'Enter your answer here...'})
    )
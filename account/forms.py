from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput,
    )


class UserRegister(forms.ModelForm):
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Repeat password"), widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "email")

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError(_("Пароли не одинаковые"))
        return cd["password2"]

    def clean_email(self):
        data = self.cleaned_data
        if not User.objects.filter(email=data["email"]):
            return data["email"]
        else:
            raise forms.ValidationError(_("Данный email уже зарегистрирован"))


class UserEdit(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

    def clean_email(self):
        data = self.cleaned_data["email"]
        qs = User.objects.exclude(id=self.instance.id).filter(email=data)
        if qs.exists():
            raise forms.ValidationError(
                _("Данный email уже зарегистрирован, если это вы, войдите")
            )
        return data


class ProfileEdit(forms.Form):
    profile_photo = forms.ImageField(required=False)

from django.shortcuts import render
from PIL import Image
from io import BytesIO
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.views import View
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .forms import (
    UserRegister,
    UserEdit,
    ProfileEdit,
    LoginForm,
    CustomPasswordChangeForm,
)
from .models import Profile
from django.utils.decorators import method_decorator
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm


class UserSettings(View):
    template_name = "registration/user_settings.html"

    @method_decorator(login_required)
    def get(self, request):
        return render(request, self.template_name)


class UserRegistration(View):
    template_name = "registration/registration.html"
    form_class = UserRegister

    def render_template(self, request, form):
        return render(request, self.template_name, {"form": form})

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data["password"])
            new_user.save()
            Profile.objects.create(user=new_user)
            messages.success(request, _("Вы успешно зарегистрировались ✓"))
            messages.success(request, _("Вы можете войти в аккаунт в меню"))
            return HttpResponseRedirect("/")
            # return render(
            #     request, "registration/registration_done.html", {"form": form}
            # )
        else:
            return self.render_template(request, form)


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd["username"], password=cd["password"]
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, _("Вы успешно вошли в аккаунт ✓"))
                    return HttpResponseRedirect("/")
                else:
                    messages.warning(request, _("Ваш аккаунт отключен"))
                    return HttpResponseRedirect(".")
            else:
                return render(request, "registration/login.html", {"form": form})
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})


class UserEditView(View):
    template_name = "registration/user_and_profile_edit.html"
    user_form_class = UserEdit
    profile_form = ProfileEdit

    @method_decorator(login_required)
    def get(self, request):
        form = self.user_form_class(instance=request.user)
        second_form = self.profile_form()
        return render(
            request,
            self.template_name,
            {
                "user_form": form,
                "profile_form": second_form,
            },
        )

    @method_decorator(login_required)
    def post(self, request):
        form = self.user_form_class(instance=request.user, data=request.POST)
        second_form = self.profile_form(request.POST, files=request.FILES)
        if form.is_valid():
            user_updated = form.save(commit=False)
            if second_form.is_valid() and second_form.cleaned_data["profile_photo"]:
                uploaded_image = second_form.cleaned_data["profile_photo"]
                image = Image.open(uploaded_image)
                image.thumbnail(
                    (int(image.size[0] * 0.3), int(image.size[1] * 0.3)), Image.BICUBIC
                )
                buffer = BytesIO()
                image.save(buffer, format="JPEG")
                request.user.profile.photo.save(
                    uploaded_image.name,
                    ContentFile(
                        buffer.getvalue()
                    ),  # This is necessary for saving from in-memory buffer
                )
                request.user.profile.save()
            user_updated.save()
            messages.success(request, _("Изменения сохранены успешно"))
            return HttpResponseRedirect("/")
        return render(
            request,
            self.template_name,
            {"user_form": form, "profile_form": second_form},
        )

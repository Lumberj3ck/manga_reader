from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.views import View
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .forms import UserRegister, UserEdit, ProfileEdit
from .models import Profile
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


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
            messages.success(request, _("Вы успешно зарегистрировались"))
            return HttpResponseRedirect("/")
            # return render(
            #     request, "registration/registration_done.html", {"form": form}
            # )
        else:
            messages.warning(request, _("Обнаружены неправильно заполненые поля"))
            return self.render_template(request, form)


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
                "profile_photo": request.user.profile.photo,
            },
        )

    @method_decorator(login_required)
    def post(self, request):
        form = self.user_form_class(instance=request.user, data=request.POST)
        second_form = self.profile_form(request.POST, files=request.FILES)
        if form.is_valid():
            user_updated = form.save(commit=False)
            if second_form.is_valid() and second_form.cleaned_data["profile_photo"]:
                request.user.profile.photo = second_form.cleaned_data["profile_photo"]
                request.user.profile.save()
            user_updated.save()
            messages.success(request, _("Изменения сохранены успешно"))
            return HttpResponseRedirect("/")
        return render(
            request,
            self.template_name,
            {"user_form": form, "profile_form": second_form},
        )

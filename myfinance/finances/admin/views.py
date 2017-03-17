from decimal import Decimal
from functools import reduce

import requests
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, reverse
from django.views import generic

from .forms import UserEditForm, UserDeleteForm
from ..models import UserProfile


class AdminMainView(generic.TemplateView):
    template_name = 'main.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            return render(request, self.template_name, {
                "title": "Main page"
            })
        raise PermissionDenied


class AdminUserListView(generic.TemplateView):
    template_name = "user_list.html"
    form_class = UserEditForm
    delete_form_class = UserDeleteForm

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            user_list = UserProfile.objects.filter(is_staff=False)
            paginator = Paginator(user_list, 10)
            page_next = None
            page_previous = None
            page = request.GET.get('page')
            try:
                users = paginator.page(page)
                page_next = page - 1
                page_previous = page + 1
            except PageNotAnInteger:
                users = paginator.page(1)
                page_next = 2
                page_next = None
            except EmptyPage:
                users = paginator.page(paginator.num_pages)
                page_previous = paginator.num_pages - 1
                page_next = None
            return render(request, self.template_name, {
                'users': users,
                'page_next': page_next,
                'page_previous': page_previous,
                'form': self.form_class,
                'delete_form': self.delete_form_class
            })
        raise PermissionDenied


class AdminEditUserView(generic.View):
    form_class = UserEditForm

    def post(self, request):
        if request.user.is_staff:
            form = self.form_class(request.POST)
            if form.is_valid():
                headers = {'Authorization': 'JWT ' + request.session["token"]}
                username = form.cleaned_data['username']
                data = {
                    'first_name': form.cleaned_data['first_name'],
                    'last_name': form.cleaned_data['last_name'],
                    'email': form.cleaned_data['email'],
                    'address': form.cleaned_data['address'],
                    'phone': form.cleaned_data['phone'].country_code + form.cleaned_data['phone'].national_number,
                }
                put = requests.put(
                    "http://localhost:8000" + reverse("api:user_detail", args={username}),
                    data=data,
                    headers=headers
                )
                if put.status_code == 200:
                    success_message = "You have updated user data!"
                    messages.success(request, success_message)
                else:
                    error_message = "Something went wrong with the update :("
                    messages.error(request, error_message)
                return redirect(reverse("admin:user_list"))
            else:
                error_message = form.errors
                messages.error(request, error_message)
                return redirect(reverse("admin:user_list"))
        raise PermissionDenied


class AdminDeleteUserView(generic.View):
    form_class = UserDeleteForm

    def post(self, request):
        if request.user.is_staff:
            form = self.form_class(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get("username")
                headers = {'Authorization': 'JWT ' + request.session["token"]}
                delete = requests.delete(
                    "http://localhost:8000" + reverse("api:user_detail", args={username}),
                    headers=headers
                )
                if delete.status_code == 204:
                    success_message = "The user " + username + " has been deleted successfully!"
                    messages.success(request, success_message)
                else:
                    error_message = "Something went wrong with the deleting"
                    messages.error(request, error_message)
            else:
                error_message = form.errors
                messages.error(request, error_message)
            return redirect(reverse("admin:user_list"))
        raise PermissionDenied


class AdminSearchUserView(generic.TemplateView):
    template_name = "user_detail.html"

    def get(self, request, *args, **kwargs):
        username = request.GET.get('username')
        headers = {'Authorization': 'JWT ' + request.session["token"]}
        get_user = requests.get(
            "http://localhost:8000" + reverse("api:user_list") + "?search=" + username,
            headers=headers
        )
        if get_user.status_code != 200:
            return render(request, '404.html')
        else:
            users = get_user.json()
            if len(users) != 1:
                return render(request, '404.html')
            else:
                user = users[0]
            headers = {'Authorization': 'JWT ' + request.session["token"]}
            response = requests.get(
                "http://localhost:8000" + reverse("api:account_list") + "?search=" + username,
                headers=headers
            )
            accounts = response.json()
            for elem in accounts:
                get_charges = requests.get(
                    "http://localhost:8000" + reverse("api:charge_list") + "?search=" + elem["number"],
                    headers=headers
                )
                account_charges = get_charges.json()
                if len(account_charges) == 0:
                    elem["total"] = None
                else:
                    elem["total"] = reduce(
                        lambda x, y: Decimal(x) + Decimal(y),
                        map(lambda x: x["value"], account_charges),
                        0.00
                    )
            return render(request, self.template_name, {
                "title": "User detail view",
                "user": user,
                "accounts": accounts
            })

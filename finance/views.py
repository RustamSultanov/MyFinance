import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.views import generic

from finance.calendar import get_month_name
from finance.forms import ChargeForm, AccountForm, RegisterForm, LoginForm, ProfileUpdateForm
from finance.models import UserProfile


class MainPageView(generic.TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            "title": "Main Page"
        })


class RegisterView(generic.TemplateView):
    template_name = 'register.html'
    form_class = RegisterForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            "title": "Register",
            "form": self.form_class,
        })

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['username']
            UserProfile.objects.create_user(
                username=user_name,
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address']
            )
            success_message = "You have been registered"
            info_message = "You registered new User(" \
                           "login: " + str(user_name) \
                           + ")"
            messages.success(request, success_message)
            messages.info(request, info_message)
            return render(request, self.template_name, {
                "title": "Register",
                "form": self.form_class
            })
        return render(request, self.template_name, {
            "title": "Register",
            "form": form
        })


class LoginView(generic.TemplateView):
    template_name = 'auth.html'
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            "title": "Login",
            "form": self.form_class,
        })

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                userdata = {'username': username, 'password': password}
                response = requests.post("http://localhost:8000/api-token-auth/", data=userdata)
                obj = response.json()
                request.session["token"] = obj["token"]
                return redirect(reverse("finances:profile"))
            else:
                messages.error(request, "Your login data is not valid")
                return render(request, self.template_name, {
                    "title": "Login",
                    "form": form
                })
        messages.error(request, "Incorrect data")
        return render(request, self.template_name, {
            "title": "Login",
            "form": form
        })


class LogoutView(generic.TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
            return redirect("finances:main")
        else:
            raise PermissionDenied


class ProfileView(generic.TemplateView):
    template_name = 'profile.html'
    form_class = AccountForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(request, self.template_name, {
                "title": "Profile",
                "form": self.form_class,
            })
        else:
            return redirect("finances:main")

    @staticmethod
    def post(request):
        if request.user.is_authenticated:
            address = request.POST.get('address')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            headers = {'Authorization': 'JWT ' + request.session["token"]}
            data = {'address': address, 'first_name': first_name, 'last_name': last_name}
            put = requests.put(
                "http://localhost:8000" + reverse("api:user_detail", args={request.user.username}),
                data=data,
                headers=headers
            )
            if put.status_code != 200:
                error_message = "Update have not been succeeded"
                messages.error(request, error_message)
            else:
                success_message = "Update have been succeeded!"
                messages.success(request, success_message)
            return redirect(reverse("finances:profile"))


class AccountInsertView(generic.TemplateView):
    template_name = 'profile.html'
    form_update_class = ProfileUpdateForm
    form_class = AccountForm

    def post(self, request):
        if request.user.is_authenticated:
            form = self.form_class(request.POST)
            form_update = self.form_update_class

            if form.is_valid():

                number = form.cleaned_data['number']
                headers = {'Authorization': 'JWT ' + request.session["token"]}
                data = {'number': number}
                post = requests.post("http://localhost:8000" + reverse("api:account_list"), headers=headers, data=data)

                if post.status_code != 201:
                    raise PermissionDenied

                success_message = "Form successfully validated!"
                info_message = "You created new Account(" \
                               "number: " + str(request.POST.get('number')) \
                               + ")"
                messages.success(request, success_message)
                messages.info(request, info_message)

            return render(request, self.template_name, {
                "title": "Profile",
                "form": form,
                "form_update": form_update
            })
        else:
            raise PermissionDenied


class AccountView(generic.FormView):
    template_name = "account.html"

    def get(self, request, number=None, *args, **kwargs):
        if request.user.is_authenticated:
            headers = {'Authorization': 'JWT ' + request.session["token"]}
            get_account = requests.get(
                "http://localhost:8000" + reverse("api:account_detail", kwargs={'number': number}),
                headers=headers
            )
            if get_account.status_code == 200:
                account = get_account.json()
                if account.get('user') == request.user.id:
                    get_charges = requests.get(
                        "http://localhost:8000" + reverse("api:charge_list") + "?search=" + number,
                        headers=headers
                    )
                    all_account_charges = get_charges.json()
                    deposit = []
                    withdraw = []
                    for charge in all_account_charges:
                        if float(charge.get('value')) > 0.0:
                            deposit.append(charge)
                        else:
                            withdraw.append(charge)
                    deposit.sort(key=lambda x: x['date'])
                    withdraw.sort(key=lambda x: x['date'])
                    return render(request, self.template_name, {
                        "title": "Account page",
                        "deposit": deposit,
                        "withdraw": withdraw,
                        "account_number": number
                    })
                else:
                    raise PermissionDenied
            else:
                return render(request, '404.html')
        else:
            raise PermissionDenied


class AddChargeView(generic.FormView):
    template_name = "add_charge.html"
    form_class = ChargeForm
    title_name = "Add new Charge"

    def get(self, request, number=None, *args, **kwargs):
        if request.user.is_authenticated:
            headers = {'Authorization': 'JWT ' + request.session["token"]}
            get_account = requests.get(
                "http://localhost:8000" + reverse("api:account_detail", kwargs={'number': number}),
                headers=headers
            )
            if get_account.status_code == 200:
                account = get_account.json()
                if account.get('user') == request.user.id:
                    return render(request, self.template_name, {
                        "title": self.title_name,
                        "form": self.form_class,
                        "account_number": number
                    })
                else:
                    raise PermissionDenied
            else:
                return render(request, '404.html')
        else:
            raise PermissionDenied

    def post(self, request, number=None, *args, **kwargs):
        if request.user.is_authenticated:
            form = self.form_class(request.POST)
            if form.is_valid():
                headers = {'Authorization': 'JWT ' + request.session["token"]}
                data = {
                    'value': form.cleaned_data['value'],
                    'date': form.cleaned_data['date'],
                    'account': number
                }
                post = requests.post("http://localhost:8000" + reverse("api:charge_list"), headers=headers, data=data)

                if post.status_code != 201:
                    raise PermissionDenied

                success_message = "Form successfully validated!"
                info_message = "You created new Charge(" \
                               "value: " + str(request.POST.get('value')) + \
                               ", date: " + request.POST.get('date') + ")"

                messages.success(request, success_message)
                messages.info(request, info_message)
            return render(request, self.template_name, {
                "title": self.title_name,
                "form": form,
                "account_number": number
            })
        else:
            raise PermissionDenied


class AccountStatisticsView(generic.FormView):
    template_name = "statistics.html"

    def transform_data(self, variables, acc=None):
        if len(variables) == 0:
            return acc
        else:
            year, month, total = variables.pop(-1)
            if acc is None:
                acc = {year: {get_month_name(month): total}}
            else:
                if acc.get(year) is not None:
                    if get_month_name(month) not in acc[year]:
                        acc[year][get_month_name(month)] = total
                else:
                    acc[year] = {get_month_name(month): total}
            acc_new = self.transform_data(variables, acc)
            return acc_new

    def get(self, request, number=None, *args, **kwargs):
        if request.user.is_authenticated:
            headers = {'Authorization': 'JWT ' + request.session["token"]}
            get_account = requests.get(
                "http://localhost:8000" + reverse("api:account_detail", kwargs={'number': number}),
                headers=headers
            )
            if get_account.status_code == 200:
                account = get_account.json()
                if account.get('user') == request.user.id:
                    headers = {'Authorization': 'JWT ' + request.session["token"]}
                    get_statistic = requests.get(
                        "http://localhost:8000" + reverse("api:statistics", kwargs={'number': number}),
                        headers=headers
                    )
                    raw_stats = get_statistic.json()
                    stats = self.transform_data(list(raw_stats))
                    return render(request, self.template_name, {
                        "title": "Account Statistics",
                        "data": stats,
                        "account_number": number
                    })
                else:
                    raise PermissionDenied
            else:
                return render(request, '404.html')
        else:
            raise PermissionDenied


class UserSearchView(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        headers = {'Authorization': 'JWT ' + request.session["token"]}
        get_user = requests.get(
            "http://localhost:8000" + reverse("api:user_list") + "?search=" + request.GET.get('username'),
            headers=headers
        )
        user = get_user.json()
        if len(user) == 1:
            return redirect("finances:public_profile", username=user[0].get('username'))
        else:
            return render(request, '404.html')


class PublicProfileView(generic.TemplateView):
    template_name = "public_profile.html"

    def get(self, request, username=None, *args, **kwargs):
        if username is not None:
            headers = {'Authorization': 'JWT ' + request.session["token"]}
            get_user = requests.get(
                "http://localhost:8000" + reverse("api:user_list") + "?search=" + username,
                headers=headers
            )
            user = get_user.json()
            if len(user) == 1:
                return render(request, self.template_name, {
                    "title": "Public profile",
                    "user": user[0]
                })
            else:
                return render(request, "404.html")
        else:
            return render(request, "404.html")

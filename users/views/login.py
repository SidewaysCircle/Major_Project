from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect

class login_view(View):
    html_Template = "login.html"

    def get(self, request):
        #Provide user with login screen
        if request.user.is_authenticated:
            return redirect("index")
        form = AuthenticationForm()
        return render(request, self.html_Template, {"form": form})

    def post(self, request):
        #Validate user account
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("index")
        return render(request, self.html_Template, {"form": form},status=401)
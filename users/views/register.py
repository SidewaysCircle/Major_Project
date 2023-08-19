from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect

class register_view(View):
    template_name = 'reg_new_user.html'

    def get(self, request):
        #Open the register page
        if request.user.is_authenticated:
            return redirect("index")
        form = UserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        #Register the user
        if not request.user.is_authenticated:
            form = UserCreationForm(data=request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect("index")
            return render(request, self.template_name, {'form': form}, status=401)

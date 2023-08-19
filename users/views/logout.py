from django.views import View
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import HttpResponse
# Create your views here.

class logout_view(View):
    logout_redirect = "users:login"

    def post(self, request):
        #Logs user out
        if request.user.is_authenticated:
            logout(request)
            return redirect(self.logout_redirect)
        return HttpResponse(status=401)
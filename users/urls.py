from django.urls import path
from .views.login import login_view
from .views.logout import logout_view
from .views.register import register_view

app_name = 'users'
urlpatterns = [
    path("login/", login_view.as_view(), name = "login"),
    path("logout/", logout_view.as_view(), name = "logout"),
    path("register/", register_view.as_view(), name = "register"),
]
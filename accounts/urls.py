from django.urls import path

from .views import register, login_view, dashboard,logout_view,add_family_member,family_members

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("dashboard/", dashboard, name="dashboard"),
    path("logout/", logout_view, name="logout"),
    path("family/add/", add_family_member, name="add_family_member"),
    path("family/", family_members, name="family_members"),
]
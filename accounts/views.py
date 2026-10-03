from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .models import FamilyMember
User = get_user_model()


def register(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            return render(
                request,
                "accounts/register.html",
                {"error": "Passwords do not match."}
            )

        if User.objects.filter(email=email).exists():
            return render(
                request,
                "accounts/register.html",
                {"error": "Email already registered."}
            )

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect("login")

    return render(request, "register.html")


def login_view(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        return render(
            request,
            "accounts/login.html",
            {"error": "Invalid email or password."}
        )

    return render(request, "login.html")

from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    return render(
        request,
        "dashboard.html"
    )

def logout_view(request):

    if request.method == "POST":
        logout(request)
        return redirect("login")

    return redirect("dashboard")

@login_required
def add_family_member(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        relation = request.POST.get("relation")

        FamilyMember.objects.create(
            user=request.user,
            name=name,
            email=email,
            phone=phone,
            relation=relation
        )

        return redirect("family_members")

    return render(request, "add_family_member.html")

@login_required
def family_members(request):
    members = FamilyMember.objects.filter(
        user=request.user
    )

    return render(
        request,
        "family_members.html",
        {"members": members}
    )
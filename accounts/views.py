from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .models import FamilyMember
from datetime import date, timedelta
from django.db.models import Count
from medicines.models import DoseRecord
from medicines.utils import generate_today_doses
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

    # Generate today's dose records
    generate_today_doses(request.user)

    today = date.today()

    # First day of current month
    month_start = today.replace(day=1)

    # All doses of current month
    doses = DoseRecord.objects.filter(
        schedule__medicine__user=request.user,
        date__gte=month_start,
        date__lte=today
    )

    total_doses = doses.count()

    taken_doses = doses.filter(
        status="taken"
    ).count()

    missed_doses = doses.filter(
        status="missed"
    ).count()

    pending_doses = doses.filter(
        status="pending"
    ).count()

    # Pending doses are not included in adherence calculation
    completed_doses = taken_doses + missed_doses

    if completed_doses > 0:
        adherence_percentage = round(
            (taken_doses / completed_doses) * 100,
            2
        )
    else:
        adherence_percentage = 0

    context = {
        "total_doses": total_doses,
        "taken_doses": taken_doses,
        "missed_doses": missed_doses,
        "pending_doses": pending_doses,
        "adherence_percentage": adherence_percentage,
    }

    return render(
        request,
        "dashboard.html",
        context
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
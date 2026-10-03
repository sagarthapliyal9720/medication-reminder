from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404
from datetime import date
from .models import Medicine, MedicineSchedule, DoseRecord
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from .utils import (
    generate_today_doses,
    send_daily_summary_to_all_users
)

@login_required
def add_medicine(request):

    if request.method == "POST":

        name = request.POST.get("name")
        dosage = request.POST.get("dosage")
        instructions = request.POST.get("instructions")

        medicine = Medicine.objects.create(
            user=request.user,
            name=name,
            dosage=dosage,
            instructions=instructions
        )

        times = request.POST.getlist("times")

        for time in times:
            if time:
                MedicineSchedule.objects.create(
                    medicine=medicine,
                    time=time
                )

        return redirect("dashboard")

    return render(
        request,
        "add_medicine.html"
    )
@login_required
def my_medicines(request):
    medicines = Medicine.objects.filter(
        user=request.user,
        is_active=True
    ).prefetch_related("schedules")

    return render(
        request,
        "my_medicines.html",
        {"medicines": medicines}
    )




# def generate_today_doses(user):
#     today = date.today()

#     medicines = Medicine.objects.filter(
#         user=user,
#         is_active=True
#     ).prefetch_related("schedules")

#     for medicine in medicines:
#         for schedule in medicine.schedules.all():
#             DoseRecord.objects.get_or_create(
#                 schedule=schedule,
#                 date=today
#             )


@login_required
def todays_doses(request):

    generate_today_doses(request.user)

    today = date.today()

    doses = DoseRecord.objects.filter(
        schedule__medicine__user=request.user,
        date=today
    ).select_related(
        "schedule",
        "schedule__medicine"
    )

    return render(
        request,
        "todays_doses.html",
        {"doses": doses}
    )
@login_required
def update_dose_status(request, dose_id, status):
    if request.method == "POST":
        dose = get_object_or_404(
            DoseRecord,
            id=dose_id,
            schedule__medicine__user=request.user
        )

        if status in ["taken", "missed"]:
            dose.status = status
            dose.save()

    return redirect("todays_doses")



@login_required
def test_email(request):
    send_mail(
        subject="Medication Reminder Test",
        message="Bhai, Django se email successfully aa rahi hai! 🎉",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[request.user.email],
    )

    return redirect("dashboard")

@login_required
def test_daily_summary(request):
    send_daily_summary_to_all_users()

    return redirect("dashboard")


def cron_daily_summary(request):
    token = request.GET.get("token")

    if token != settings.CRON_SECRET:
        return JsonResponse(
            {"error": "Unauthorized"},
            status=401
        )

    sent_count = send_daily_summary_to_all_users()

    return JsonResponse({
        "message": "Daily summaries sent",
        "sent_count": sent_count
    })
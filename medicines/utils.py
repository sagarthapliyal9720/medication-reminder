from datetime import date

from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

from .models import Medicine, DoseRecord


def generate_today_doses(user):
    today = date.today()

    medicines = Medicine.objects.filter(
        user=user,
        is_active=True
    ).prefetch_related("schedules")

    for medicine in medicines:
        for schedule in medicine.schedules.all():
            DoseRecord.objects.get_or_create(
                schedule=schedule,
                date=today
            )


def send_daily_medication_summary(user):

    generate_today_doses(user)

    today = date.today()

    doses = DoseRecord.objects.filter(
        schedule__medicine__user=user,
        date=today
    ).select_related(
        "schedule",
        "schedule__medicine"
    ).order_by(
        "schedule__time"
    )

    if not doses:
        return False

    message = f"Hello {user.username},\n\n"
    message += "Here is your medication summary for today:\n\n"

    for dose in doses:
        medicine_name = dose.schedule.medicine.name
        time = dose.schedule.time.strftime("%I:%M %p")
        status = dose.status.title()

        message += f"- {medicine_name} | {time} | {status}\n"

    message += "\n"
    message += "Please visit the link below to view and mark your doses:\n\n"
    message += "https://medication-reminder-cyan.vercel.app/medicines/today/\n\n"
    message += "Take care!"

    send_mail(
        subject="Today's Medication Summary",
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )

    return True

def send_daily_summary_to_all_users():

    User = get_user_model()

    users = User.objects.filter(
        is_active=True
    ).exclude(
        email=""
    )

    sent_count = 0

    for user in users:

        sent = send_daily_medication_summary(user)

        if sent:
            sent_count += 1

    return sent_count
from django.urls import path
from .views import add_medicine, my_medicines,todays_doses,update_dose_status,test_email,test_daily_summary,cron_daily_summary

urlpatterns = [
    path("add/", add_medicine, name="add_medicine"),
    path("", my_medicines, name="my_medicines"),
    path("today/", todays_doses, name="todays_doses"),
    path(
    "today/<int:dose_id>/<str:status>/",
    update_dose_status,
    name="update_dose_status"
),
path("test-email/", test_email, name="test_email"),
path(
    "test-daily-summary/",
    test_daily_summary,
    name="test_daily_summary"
),


path(
    "cron/daily-summary/",
    cron_daily_summary,
    name="cron_daily_summary"
),

]
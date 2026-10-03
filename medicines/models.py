from django.conf import settings
from django.db import models


class Medicine(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="medicines"
    )

    name = models.CharField(max_length=100)

    dosage = models.CharField(max_length=100)

    instructions = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name


class MedicineSchedule(models.Model):

    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.CASCADE,
        related_name="schedules"
    )

    time = models.TimeField()

    class Meta:
        ordering = ["time"]

    def __str__(self):
        return f"{self.medicine.name} - {self.time}"


class DoseRecord(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("taken", "Taken"),
        ("missed", "Missed"),
    ]

    schedule = models.ForeignKey(
        MedicineSchedule,
        on_delete=models.CASCADE,
        related_name="dose_records"
    )
    date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("schedule", "date")

    def __str__(self):
        return f"{self.schedule.medicine.name} - {self.date} - {self.status}"
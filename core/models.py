from datetime import timezone

from django.core.exceptions import ValidationError
from django.db import models

from accounts.models import User
from common.models import BaseModel


class VehicleType(BaseModel):
    name = models.CharField(max_length=250, blank=True)
    parking_fee = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self) -> str:
        return str(self.name)


class Spot(BaseModel):
    class Floor(models.TextChoices):
        BASEMENT = "Basement"
        GROUND = "Ground"
        FIRST = "First"
        SECOND = "Second"
        THIRD = "Third"

    floor = models.CharField(
        choices=Floor.choices, max_length=15, default=Floor.BASEMENT
    )
    vehicle_type = models.ManyToManyField(VehicleType, related_name="vehicle_types")
    spot_number = models.CharField(max_length=250, unique=True)
    is_available = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.spot_number} {self.floor}"


class Booking(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")
    spot = models.ForeignKey(Spot, on_delete=models.CASCADE, related_name="bookings")
    vehicle_type = models.ForeignKey(
        VehicleType, on_delete=models.CASCADE, related_name="vehicles"
    )
    registration_number = models.CharField(max_length=250, blank=True)
    booking_number = models.CharField(max_length=250, blank=True)
    is_paid = models.BooleanField(default=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("start date cannot be after end date.")

    @property
    def has_expired(self):
        now = timezone.now()

        return self.end_date.time > now.time()

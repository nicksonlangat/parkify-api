# Generated by Django 5.0.3 on 2024-03-21 04:53

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="VehicleType",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(blank=True, max_length=250)),
                ("parking_fee", models.DecimalField(decimal_places=2, max_digits=9)),
            ],
            options={
                "ordering": ["-updated_at"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Spot",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "floor",
                    models.CharField(
                        choices=[
                            ("Basement", "Basement"),
                            ("Ground", "Ground"),
                            ("First", "First"),
                            ("Second", "Second"),
                            ("Third", "Third"),
                        ],
                        default="Basement",
                        max_length=15,
                    ),
                ),
                ("spot_number", models.CharField(max_length=250, unique=True)),
                ("is_available", models.BooleanField(default=True)),
                (
                    "vehicle_type",
                    models.ManyToManyField(
                        related_name="vehicle_types", to="core.vehicletype"
                    ),
                ),
            ],
            options={
                "ordering": ["-updated_at"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Booking",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("registration_number", models.CharField(blank=True, max_length=250)),
                ("booking_number", models.CharField(blank=True, max_length=250)),
                ("start_date", models.DateTimeField()),
                ("end_date", models.DateTimeField()),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="users",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "spot",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bookings",
                        to="core.spot",
                    ),
                ),
                (
                    "vehicle_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="vehicles",
                        to="core.vehicletype",
                    ),
                ),
            ],
            options={
                "ordering": ["-updated_at"],
                "abstract": False,
            },
        ),
    ]
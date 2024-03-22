import datetime

from rest_framework import serializers

from accounts.serializers import UserSerializer

from .models import Booking, Spot, VehicleType


class VehicleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleType
        fields = ["id", "name", "parking_fee", "created_at", "updated_at"]


class SpotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spot
        fields = [
            "id",
            "floor",
            "vehicle_type",
            "spot_number",
            "is_available",
            "created_at",
            "updated_at",
        ]


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            "id",
            "user",
            "spot",
            "vehicle_type",
            "registration_number",
            "booking_number",
            "start_date",
            "end_date",
            "created_at",
            "updated_at",
            "is_paid",
        ]

    def validate(self, data):
        if not self.partial:
            # validate logical datetimes
            if data["start_date"] > data["end_date"]:
                raise serializers.ValidationError(
                    "Start date must come before end date"
                )

            today = datetime.date.today()
            registration_number = data["registration_number"]

            # prevent double booking
            if Booking.objects.filter(
                start_date__date=today,
                registration_number=registration_number,
                is_paid=False,
            ).exists():
                raise serializers.ValidationError(
                    f"You have already booked a spot for {registration_number}"
                )

            # prevent booking unavailable slot
            if Booking.objects.filter(
                start_date__date=today, spot=data["spot"], is_paid=False
            ).exists():
                raise serializers.ValidationError(
                    f"There already exists an active booking for the selected spot {data['spot']}"
                )

            # prevent booking a spot for a wrong vehicle type
            spot = data["spot"]
            vehicle = data["vehicle_type"]
            if vehicle.id not in list(
                {vehicle_type.id for vehicle_type in spot.vehicle_type.all()}
            ):
                raise serializers.ValidationError(
                    f"The spot {data['spot']} selected is not available for your vehicle type, {vehicle}"
                )

        return data

    def create(self, validated_data):
        booking = Booking.objects.create(**validated_data)

        # mark spot as unavailable
        booking.spot.is_available = False
        booking.spot.save(update_fields=["is_available"])

        return booking

    def update(self, instance, validated_data):
        booking = super().update(instance, validated_data)

        # a booking is marked paid when the vehicle leaves the facility
        # and the user makes a payment.
        if "is_paid" in validated_data and validated_data["is_paid"]:
            # mark spot as available
            instance.spot.is_available = True
            instance.spot.save(update_fields=["is_available"])

        return booking

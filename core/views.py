import random

from rest_framework import permissions, viewsets

from common.permissions import IsAdminOrAuthenticatedReadOnly

from .models import Booking, Spot, VehicleType
from .serializers import BookingSerializer, SpotSerializer, VehicleTypeSerializer


class VehicleApi(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrAuthenticatedReadOnly]
    queryset = VehicleType.objects.all()
    serializer_class = VehicleTypeSerializer


class SpotApi(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrAuthenticatedReadOnly]
    queryset = Spot.objects.all()
    serializer_class = SpotSerializer


class BookingApi(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        booking_number = "".join(random.choice("0123456789ABCDEF") for i in range(6))
        serializer.save(booking_number=booking_number.upper())

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        return self.queryset.filter(user=self.request.user)

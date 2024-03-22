from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"vehicle-types", views.VehicleApi, basename="vehicle-types")
router.register(r"spots", views.SpotApi, basename="spots")
router.register(r"bookings", views.BookingApi, basename="bookings")

urlpatterns = [path("", include(router.urls))]

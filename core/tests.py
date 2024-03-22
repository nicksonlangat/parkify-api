from common.test_helpers import BaseTest
from core.models import VehicleType


# Create your tests here.
class CoreTest(BaseTest):
    def setUp(self) -> None:
        self.login()

    @staticmethod
    def _get_new_vehicle_type_data():
        return {"name": "compact", "parking_fee": "2.00"}

    def test_add_vehicle_type(self):
        path = "/vehicle-types/"

        data = self._get_new_vehicle_type_data()

        response = self.http.post(path, data, **self.bearer_token)
        type = VehicleType.objects.get(name=data["name"])

        self.assertIsNotNone(type)
        self.assertNotIn(response.content.__str__(), "Error")
        self.assertEqual(201, response.status_code)
        self.assertNotIn("None", type.name)

    def test_view_vehicle_types(self):
        response = self.http.get("/vehicle-types/", **self.bearer_token)
        self.assertEqual(200, response.status_code)

    def test_view_spots(self):
        response = self.http.get("/spots/", **self.bearer_token)
        self.assertEqual(200, response.status_code)

    def test_view_bookings(self):
        response = self.http.get("/bookings/", **self.bearer_token)
        self.assertEqual(200, response.status_code)

from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_with_first_last_name_license_number(self):
        form_data = {
            "username": "test1",
            "password1": "user223s",
            "password2": "user223s",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "ASD23456"
        }
        form = DriverCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

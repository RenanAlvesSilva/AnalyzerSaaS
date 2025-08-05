from django.test import TestCase

class test_api_v1(TestCase):
    def test_change_password_success(self):
        self.client.login(username='test', password='old12345')
        response = self.client.patch('/api/change-password/', {
            'old_password': 'old12345',
            'new_password': 'newStrongPass1!',
            'confirm_password': 'newStrongPass1!'
        })
        self.assertEqual(response.status_code, 200)


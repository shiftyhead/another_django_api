import json
from datetime import date, timedelta
from django.test import TestCase, Client


class AccountTestCase(TestCase):
    correct_trial = date.today() + timedelta(weeks=2)

    def test_creation(self):
        user_data = {"name": "Maria", "birthday": "2002-10-30"}
        c = Client()
        response = c.post(
            '/users/new/',
            user_data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

        response_json = json.loads(response.content)
        self.assertEqual(response_json.get('status'), 'success')
        new_user_id = response_json.get('user_id')

        new_user_data = c.get(f'/users/{new_user_id}/')
        new_user_data_json = json.loads(new_user_data.content.decode())
        for field, value in user_data.items():
            self.assertEqual(
                new_user_data_json.get(field),
                value
            )

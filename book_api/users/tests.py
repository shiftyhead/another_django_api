import json
from datetime import date, timedelta
from django.test import TestCase, Client


class AccountTestCase(TestCase):
    client = Client()
    correct_trial = date.today() + timedelta(weeks=2)

    def test_creation(self):
        user_data = {'name': 'Maria', 'birthday': '2002-10-30'}
        response = self.client.post('/users/new/', user_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        response_json = json.loads(response.content)
        self.assertEqual(response_json.get('status'), 'success')
        new_user_id = response_json.get('user_id')

        new_user_data = self.client.get(f'/users/{new_user_id}/')
        new_user_data_json = json.loads(new_user_data.content.decode())
        for field, value in user_data.items():
            self.assertEqual(
                new_user_data_json.get(field),
                value
            )
    
    def test_creation_wrong(self):
        wrong_data = [
            {'na!!e': 'Ivan', 'birthday': '2002-12-30'},
            {'name': 'Petr', 'birthday': '2002-14-30'},
        ]
        for user_data in wrong_data:
            response = self.client.post('/users/new/', user_data, content_type='application/json')
            self.assertEqual(response.status_code, 200)
            response_json = json.loads(response.content)
            self.assertEqual(response_json.get('status'), 'error')

    def test_user_subscription(self):
        users_data = [
            {'name': 'Maria', 'birthday': '2002-10-30'},
            {'name': 'Cheater', 'birthday': '2000-12-20', 'subscription_end': '3000-12-31'},
        ]
        for user_data in users_data:
            response = self.client.post('/users/new/', user_data, content_type='application/json')

            response_json = json.loads(response.content)
            new_user_id = response_json.get('user_id')
            new_user_data = self.client.get(f'/users/{new_user_id}/')
            new_user_data_json = json.loads(new_user_data.content.decode())

            self.assertEqual(new_user_data_json.get('subscription_end'), str(self.correct_trial))

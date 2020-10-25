from datetime import date, timedelta
from django.test import TestCase, Client


class AccountTestCase(TestCase):
    client = Client()
    correct_trial = date.today() + timedelta(weeks=2)

    def test_creation(self):
        user_data = {'name': 'Maria', 'birthday': '2002-10-30'}
        creation_response = self.client.post('/users/new/', user_data, content_type='application/json')
        self.assertEqual(creation_response.status_code, 200)

        creation_response_data = creation_response.json()
        self.assertEqual(creation_response_data['status'], 'success')

        new_user_id = creation_response_data['user_id']
        new_user_response = self.client.get(f'/users/{new_user_id}/')
        new_user_data = new_user_response.json()
        for field, value in user_data.items():
            self.assertEqual(new_user_data[field], value)
    
    def test_creation_wrong(self):
        wrong_data = [
            {'na!!e': 'Ivan', 'birthday': '2002-12-30'},
            {'name': 'Petr', 'birthday': '2002-14-30'},
        ]
        for user_data in wrong_data:
            creation_response = self.client.post('/users/new/', user_data, content_type='application/json')
            self.assertEqual(creation_response.status_code, 200)
            creation_response_data = creation_response.json()
            self.assertEqual(creation_response_data['status'], 'error')

    def test_user_subscription(self):
        users_data = [
            {'name': 'Maria', 'birthday': '2002-10-30'},
            {'name': 'Cheater', 'birthday': '2000-12-20', 'subscription_end': '3000-12-31'},
        ]
        for user_data in users_data:
            creation_response = self.client.post('/users/new/', user_data, content_type='application/json')
            creation_response_data = creation_response.json()

            new_user_id = creation_response_data['user_id']
            new_user_response = self.client.get(f'/users/{new_user_id}/')
            new_user_response_data = new_user_response.json()
            self.assertEqual(
                new_user_response_data['subscription_end'],
                str(self.correct_trial)
            )

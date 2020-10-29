from datetime import date, timedelta
from django.test import TestCase, Client

from .models import Account


class AccountTestCase(TestCase):
    client = Client()
    correct_user_data = {'name': 'Maria', 'birthday': '2002-10-30'}

    def test_creation(self):
        user_data = self.correct_user_data
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
            self.correct_user_data,
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
                str(date.today() + timedelta(weeks=2))
            )

    def test_pay_month_subscription(self):
        creation_response = self.client.post('/users/new/', self.correct_user_data, content_type='application/json')
        creation_response_data = creation_response.json()
        new_user_id = creation_response_data['user_id']

        new_user_entity = Account.objects.get(pk=new_user_id)
        new_user_entity.subscription_end = date(2020, 12, 5)
        new_user_entity.save()

        pay_month = {'status': 'ok', 'period': 'month', 'user_id': new_user_id}
        pay_response = self.client.post('/users/pay/', pay_month, content_type='application/json')
        pay_response_data = pay_response.json()
        self.assertEqual(pay_response_data['status'], 'success')

        paid_user_response = self.client.get(f'/users/{new_user_id}/')
        paid_user_response_data = paid_user_response.json()

        month_pay_date = date.fromisoformat(paid_user_response_data['subscription_end'])
        self.assertEqual(
            month_pay_date,
            date(2021, 1, 5)
        )

    def test_get_all_users(self):
        for n in range(10):
            users = self.client.get('/users/').json()
            self.assertEqual(len(users), n)
            self.client.post('/users/new/', self.correct_user_data, content_type='application/json')

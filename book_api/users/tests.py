import json
from collections import namedtuple

from datetime import date, timedelta
from django.test import TestCase

from .views import create_user, get_user_detail


class AccountTestCase(TestCase):
    def setUp(self):
        Request = namedtuple('Request', ['method', 'body'])
        request = Request('POST', '{"name": "Maria", "birthday": "2002-10-30"}')
        create_user(request)
        request = Request('POST', '{"name": "Cheater", "birthday": "2002-10-30", "subscription_end": "3002-10-30"}')
        create_user(request)

    def test_animals_can_speak(self):
        correct_trial = date.today() + timedelta(weeks=2)

        maria = get_user_detail('', 1)
        content = json.loads(maria.content.decode())
        self.assertEqual(content.get('subscription_end'), str(correct_trial))

        cheater = get_user_detail('', 2)
        content = json.loads(cheater.content.decode())
        self.assertEqual(content.get('subscription_end'), str(correct_trial))

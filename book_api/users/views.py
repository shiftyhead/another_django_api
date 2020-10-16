import json

from django.core import serializers
from django.http import JsonResponse
from .models import Account
from books.views import get_all_books, get_book_detail


def build_result(data):
    return {item['pk']: item['fields'] for item in json.loads(data)}


def get_all_users(request):
    users = Account.objects.all()
    data = serializers.serialize('json', users)
    result_data = build_result(data)
    return JsonResponse(result_data)


def get_user_detail(request, user_id):
    user = Account.objects.get(pk=user_id)
    data = serializers.serialize('json', [user, ])
    result_data = build_result(data)[user_id]
    return JsonResponse(result_data)


def get_books(request, user_id):
    return get_all_books(request)


def get_book(request, user_id, book_id):
    user = Account.objects.get(pk=user_id)
    if not user.subscription_is_active():
        return JsonResponse(
                {
                    'error': 'To access the book, pay for a subscription'
                }
            )
    book = get_book_detail(request, book_id)
    return book


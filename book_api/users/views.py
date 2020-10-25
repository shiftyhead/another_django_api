import json
from datetime import date, timedelta

from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import JsonResponse
from .models import Account
from books.views import get_all_books, get_book_detail


def build_result(data):
    return {item['pk']: item['fields'] for item in json.loads(data)}


def get_all_users(request):
    users = Account.objects.all()
    data = serializers.serialize('json', users, fields=['name', ])
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


def create_user(request):
    if request.method != 'POST':
        return JsonResponse({})
    data = json.loads(request.body)
    try:
        new_user = Account(**data)
        new_user.subscription_end = update_subscription(date.today(), 'trial')
        new_user.save()
    except (TypeError, ValidationError):
        return JsonResponse(
            {
                'status': 'error',
                'msg': 'Check your data'
            }
        )

    return JsonResponse(
        {
            'status': 'success',
            'msg': 'User created',
            'user_id': new_user.id
        }
    )


def update_subscription(current_subscription_end, period):
    new_value = current_subscription_end

    if period == 'year':
        new_value = new_value.replace(year=new_value.year + 1)
    elif period == 'month':
        try:
            new_value = new_value.replace(month=new_value.month + 1)
        except ValueError:
            new_value = new_value.replace(year=new_value.year + 1).replace(month=1)
    elif period == 'trial':
        new_value += timedelta(weeks=2)
    return new_value


def pay_subscription(request):
    if request.method != 'POST':
        return JsonResponse({})
    data = json.loads(request.body)
    status = data.get('status')
    if status == 'ok':
        user_id = data.get('user_id')
        try:
            user = Account.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            return JsonResponse(
                {
                    'status': 'error',
                    'msg': f'User ID {user_id} does not exist'
                }
            )
        period = data.get('period')

        user.subscription_end = update_subscription(user.subscription_end, period)
        user.save()
        return JsonResponse(
            {
                'status': 'success',
                'msg': f'Subscription extended until {user.subscription_end}'
            }
        )
    else:
        error = data.get('msg')
        return JsonResponse(
            {
                'status': 'error',
                'msg': f'Subscription not renewed because "{error}"'
            }
        )

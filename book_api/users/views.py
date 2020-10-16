from django.http import JsonResponse
from .models import User
from books.views import get_all_books, get_book_detail


def get_all_users(request):
    users = User.objects.all()
    return JsonResponse({user.id: user.name for user in users})


def get_user_detail(request, user_id):
    user = User.objects.get(pk=user_id)
    return JsonResponse(
        {
            'name': user.name,
            'subscription_status': user.subscription_status
        }
    )


def get_books(request, user_id):
    return get_all_books(request)


def get_book(request, user_id, book_id):
    user = User.objects.get(pk=user_id)
    if not user.subscription_status:
        return JsonResponse(
                {
                    'error': 'Для доступа к книге оплатите подписку'
                }
            )
    book = get_book_detail(request, book_id)
    return book


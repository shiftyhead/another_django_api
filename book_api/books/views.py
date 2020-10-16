from django.http import JsonResponse
from .models import Book


def get_all_books(request):
    books = Book.objects.all()
    return JsonResponse({book.id: book.title for book in books})


def get_book_detail(request, book_id):
    book = Book.objects.get(pk=book_id)
    return JsonResponse(
        {
            'title': book.title,
            'cost': book.cost
        }
    )

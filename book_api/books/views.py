import json

from django.http import JsonResponse
from .models import Book
from django.core import serializers


def build_result(data):
    return {item['pk']: item['fields'] for item in json.loads(data)}


def get_all_books(request):
    books = Book.objects.all()
    data = serializers.serialize('json', books, fields=['title', ])
    result_data = build_result(data)
    return JsonResponse(result_data)


def get_book_detail(request, book_id):
    book = Book.objects.get(pk=book_id)
    data = serializers.serialize('json', [book, ])
    result_data = build_result(data)[book_id]
    return JsonResponse(result_data)

# another_django_api

API книжного магазина написано на django.
Создавать объекты (пользователей и книги) можно через админ панель (admin/)

Endpoints:
- GET users/ - список пользователей
- GET users/<user_id>/ - получение информации о пользователе
- POST users/new/ - создание нового пользователя (пример: {"name": "Maria", "birthday": "2002-10-30"})
- POST users/pay/ - получение платежа от пользователя (пример: {"user_id": 1, "status": "ok", "period": "month"})
- GET users/<user_id>/books/ - запрос списка книг для пользователя
- GET users/<user_id>/books/<book_id>/ - запрос подробных данных книги для пользователя

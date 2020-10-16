from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_all_users),
    path('<int:user_id>/', views.get_user_detail, name='detail'),
    path('<int:user_id>/books/', views.get_books, name='books'),
    path('<int:user_id>/books/<int:book_id>/', views.get_book, name='book'),

]

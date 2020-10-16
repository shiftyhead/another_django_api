from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('', views.get_all_users),
    path('new/', csrf_exempt(views.create_user)),
    path('pay/', csrf_exempt(views.pay_subscription)),
    path('<int:user_id>/', views.get_user_detail, name='detail'),
    path('<int:user_id>/books/', views.get_books, name='books'),
    path('<int:user_id>/books/<int:book_id>/', views.get_book, name='book'),

]

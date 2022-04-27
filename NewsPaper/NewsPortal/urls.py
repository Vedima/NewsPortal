from django.urls import path
# Импортируем созданные нами представления
from .views import NewsList, NewDetail, SearchList, PostCreate, PostUpdate, PostDelete

urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', NewsList.as_view(), name='new_list'),
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('<int:pk>', NewDetail.as_view(), name='new_detail'),
   path('search/', SearchList.as_view()),
   path('create/', PostCreate.as_view(), name='product_create'),
   path('<int:pk>/edit/', PostUpdate.as_view(), name='product_update'),
   path('<int:pk>/delete/', PostDelete.as_view()),



]
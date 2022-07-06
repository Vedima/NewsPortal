from django.urls import path
# Импортируем созданные нами представления
from .views import NewsList, NewDetail, SearchList, PostCreate, PostUpdate, PostDelete, UserUpdate, upgrade_me, Subscribe, subscribe_me
# Импортируем декортатор для кэширования
from django.views.decorators.cache import cache_page

urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', cache_page(60*2)(NewsList.as_view()), name='new_list'),
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('<int:pk>', NewDetail.as_view(), name='new_detail'),
   path('search/', SearchList.as_view()),
   path('create/', PostCreate.as_view(), name='post_create'),
   path('<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', PostDelete.as_view()),
   path('user/', UserUpdate.as_view(), name='user_update'),
   path('upgrade/', upgrade_me, name='upgrade'),
   path('subscribe_me/<int:id>/', subscribe_me, name='subscribe_me'),
   path('subscribe/', Subscribe.as_view(), name='subscribe')
]




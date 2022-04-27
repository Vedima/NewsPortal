from django_filters import FilterSet, DateFilter
from .models import Post
from django import forms

# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class PostFilter(FilterSet):
    time_create = DateFilter(
        lookup_expr='gt',
        widget=forms.DateInput(
            attrs={
                'type': 'date'
            }
        )
    )

    class Meta:
       # В Meta классе мы должны указать Django модель,
       # в которой будем фильтровать записи.
       model = Post
       # В fields мы описываем по каким полям модели
       # будет производиться фильтрация.

       #dat_inicial = DateTimeFilter(name='dat_transacao', lookup_type=('gte'))

       fields = {
           # поиск по названию
           'header': ['icontains'],
           # количество товаров должно быть больше или равно
           'author__user__username': ['exact'],

       }
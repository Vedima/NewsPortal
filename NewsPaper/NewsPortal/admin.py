from django.contrib import admin
from .models import Post, Category
# Register your models here.




# создаём новый класс для представления товаров в админке
class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('author', 'header', 'rating_content')  # оставляем только имя и цену товара
    list_filter = ('author', 'rating_content')  # добавляем примитивные фильтры в нашу админку
    search_fields = ('author', 'header')  # тут всё очень похоже на фильтры из запросов в базу





# Register your models here.

admin.site.register(Post, PostAdmin)
admin.site.register(Category)
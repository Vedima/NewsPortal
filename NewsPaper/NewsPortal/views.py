from django.shortcuts import render
import datetime
#from datetime import datetime
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Post, User, Author, Category,PostCategory
from .filters import PostFilter
from django.urls import reverse_lazy
from .forms import PostForm, UserForm, SubscribeForm
from django.http import HttpRequest
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
# Create your views here.
# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД

class NewsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-time_create'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'flatpages/news.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news'
    paginate_by = 10  # вот так мы можем указать количество записей на странице

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_create'] = datetime.datetime.utcnow()

        return context

class SearchList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-time_create'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'flatpages/search.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news'

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_create'] = datetime.datetime.utcnow()
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context

class NewDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'flatpages/new.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'new'

class PostCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'
    # Разрешение на добавление новостей и статей
    permission_required = ('NewsPortal.add_post')

    def form_valid(self, form):
        fields = form.save(commit=False)
        # print(HttpRequest.scheme)
        user = User.objects.get(id=self.request.user.id)
        author = Author.objects.get(user=user)
        cur_time = datetime.datetime.now()
        print(cur_time)
        time_day = cur_time - datetime.timedelta(days=1)
        print(time_day)

        # Новости за день от данного автора
        post_day = Post.objects.filter(author=author, time_create__range=(time_day, cur_time))
        print(author, user)
        print(len(post_day))
        if 'article' in self.request.path:
            fields.position = 'article'
        else:
            fields.position = 'new'
        fields.author = author
        # Нельзя больше 3 новостей в день создавать
        if len(post_day) < 3:
            fields.save()
            return super().form_valid(form)
        else:
            return redirect ('post_create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(id=self.request.user.id)
        author = Author.objects.get(user=user)
        cur_time = datetime.datetime.now()
        time_day = cur_time - datetime.timedelta(days=1)
        post_day = Post.objects.filter(author=author, time_create__range=(time_day, cur_time))
        context['cnt1'] = len(post_day)
        return context


class PostUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'
    # Разрешение на изменение новостей и статей
    permission_required = ('NewsPortal.change_post')
# Представление удаляющее товар.
class PostDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('new_list')


# Представление страницы пользователя
class UserUpdate(LoginRequiredMixin, UpdateView):
    form_class = UserForm
    model = User
    template_name = 'user.html'
    #URL - адрес для перенаправления после успешной обработки формы.
    success_url = reverse_lazy('new_list')

    def get_object(self, **kwargs):
        return self.request.user
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context

# Делаем пользователя автором
@login_required
def upgrade_me(request):
    user = request.user
    if not user.groups.filter(name='authors').exists():
        authors_group = Group.objects.get(name='authors')
        authors_group.user_set.add(user)
        Author.objects.create(user=user)
    return redirect('user_update')

#Представление формы для подписки на категории
class Subscribe(LoginRequiredMixin, UpdateView):
    form_class = SubscribeForm
    model = PostCategory
    template_name = 'subscribe.html'

    def get_object(self, **kwargs):
        return self.request.user

# Подписываем пользователя на категорию
@login_required
def subscribe_me(request, id):
    user = request.user
    cat = Category.objects.get(pk=id)
    cat.subscribers.add(user)

    print(id)
    return redirect('subscribe')
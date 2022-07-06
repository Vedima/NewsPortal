from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse
from django.core.cache import cache

# Create your models here.
article = 'art'
news = 'new'
content = [
    (article, 'Статья'),
    (news, 'Новость'),
]
class Author(models.Model):
    rating_user = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.user.username}'
    def update_rating(self):
        post_rat = (self.post_set.aggregate(post_rating=Sum('rating_content')))
        pRat = 0
        pRat += post_rat.get('post_rating')
        aut_rat = self.user.comment_set.aggregate(aut_rating=Sum('rating_comments'))
        aRat = 0
        aRat += aut_rat.get('aut_rating')

        posts1 = self.post_set.all()
        cRat = 0
        for item in posts1:
            com_rat = item.comment_set.aggregate(com_rating=Sum('rating_comments'))
            cRat += com_rat.get('com_rating')

        self.rating_user = pRat * 3 + aRat + cRat
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, through='Subscribe')
    def __str__(self):
        return f'{self.name}'

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    position = models.CharField(max_length=3,
                                choices=content,
                                default=article)
    post_cat = models.ManyToManyField(Category, through='PostCategory')
    time_create = models.DateTimeField(auto_now_add=True)
    header = models.TextField()
    text = models.TextField()
    rating_content = models.IntegerField(default=0)
    def __str__(self):
        return f'{self.header.title()}: {self.text[:25]}'
    def like(self):
        self.rating_content += 1
        self.save()

    def dislike(self):
        self.rating_content -= 1
        self.save()

    def preview(self):
        return self.text[0:124] + '...'

    def get_absolute_url(self):
        return reverse('new_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}') # затем удаляем его из кэша, чтобы сбросить его

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
class Subscribe (models.Model):
    userSub = models.ForeignKey(User, on_delete=models.CASCADE)
    categorySub = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    comPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    comUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text_comment = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    rating_comments = models.IntegerField(default=0)

    def like(self):
        self.rating_comments += 1
        self.save()

    def dislike(self):
        self.rating_comments -= 1
        self.save()


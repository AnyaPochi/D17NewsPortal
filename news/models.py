from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce

from django.core.validators import MinValueValidator
from django.urls import reverse

# Модель Author
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username.title()}: {self.rating}'

    # Метод update_rating() модели Author, который обновляет рейтинг текущего автора

    def update_rating(self):
        post_rating = Post.objects.filter(author=self).aggregate(pr=Coalesce(Sum('rating'), 0))['pr']
        comments_rating = Comment.objects.filter(user=self.user).aggregate(cr=Coalesce(Sum('rating'), 0))['cr']
        post_comments_rating = Comment.objects.filter(post_id__author=self).aggregate(pcr=Coalesce(Sum('rating'), 0))[
            'pcr']

        self.rating = post_rating * 3 + comments_rating + post_comments_rating
        self.save()

        print(f' Рейтинг постов  - {post_rating}, \n '
              f'Рейтинг комментариев автора - {comments_rating}, \n'
              f' Рейтинг комментариев постов автора - {post_comments_rating}, \n'
              f' Общий рейтинг - {self.rating} ')


# Модель Category
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, blank=True,null=True, related_name='categories')
    def __str__(self):
        return self.name
class UserCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    categoty_id = models.ForeignKey(Category, on_delete=models.CASCADE)



class Post(models.Model):
    NEWS = 'NW'
    ARTICLE = "AR"
    POSITIONS = [
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья')
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=POSITIONS, default=NEWS)
    time_in = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(
        max_length=255,
        unique=True,
    )
    text = models.TextField()
    rating = models.IntegerField(default=0)

    # Методы like() и dislike() в моделях Comment и Post, которые увеличивают/уменьшают рейтинг на единицу.
    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    # Метод preview() модели Post, который возвращает
    # начало статьи (предварительный просмотр) длиной 124 символа и добавляет многоточие в конце.
    def __str__(self):
        return self.title

    def preview(self):
        return f'{self.text[:123]}...'

    def get_absolute_url(self):
        return reverse('post', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # cache.delete(f'post-{self.pk}')



# Модель PostCategory
class PostCategory(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)


# Модель Comment
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    time_in = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

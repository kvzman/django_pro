from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


# Create your models here.
class Author(models.Model):
    author_rate = models.SmallIntegerField(default=0)
    author_user = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        post_rat = self.post_set.all().aggregate(post_rating=Sum('post_rate'))
        p_rat = 0
        p_rat += post_rat.get('post_rating')

        com_rat = self.author_user.comment_set.all().aggregate(comment_rating=Sum('com_rate'))
        c_rat = 0
        c_rat += com_rat.get('comment_rating')

        auth_post = self.post_set.all()

        ap_rat = 0
        for post in auth_post:
            auth_post_rat = post.comment_set.aggregate(comment_rating=Sum('com_rate'))
            ap_rat += auth_post_rat.get('comment_rating')

        self.author_rate = p_rat * 3 + c_rat + ap_rat
        self.save()


class Category(models.Model):
    cat_name = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    NEWS = 'NW'
    ARTICLE = 'AR'
    CAT_CHOICES = [
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    ]
    cat_type = models.CharField(max_length=2, default=ARTICLE, choices=CAT_CHOICES)

    post_title = models.CharField(max_length=128)
    post_text = models.TextField()
    post_rate = models.SmallIntegerField(default=0)
    post_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.post_rate += 1
        self.save()

    def dislike(self):
        self.post_rate -= 1
        self.save()

    def preview(self):
        return self.post_text[0:124] + '...'


class PostCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    com_text = models.TextField()
    com_rate = models.SmallIntegerField(default=0)
    com_time = models.DateTimeField(auto_now_add=True)

    def like(self):
        self.com_rate += 1
        self.save()

    def dislike(self):
        self.com_rate -= 1
        self.save()

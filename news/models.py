from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField


class Topic(models.Model):
    """ Topic model to create categories for posts """
    name = models.CharField(max_length=200, unique=True)


    def __str__(self):
        return self.name


class Post(models.Model):
    """ Post model to create instances of posts """
    title = models.CharField(max_length=200, unique=True)
    slug = AutoSlugField(populate_from='title')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_author_set')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='post_topic_set')
    last_updated = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    upvotes = models.ManyToManyField(User, related_name='post_upvotes_set', blank=True)

    class Meta:
        ordering = ['-created_on']
    

    def __str__(self):
        return self.title

    def number_of_upvotes(self):
        return self.upvotes.count()
    

class Comment(models.Model):
    """ Comment model for comments inside posts """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment_post_set')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_user_set')
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

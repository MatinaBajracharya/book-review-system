from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE) 
    likes = models.ManyToManyField(User, default= None, blank=True, related_name='liked')
    comments = models.ManyToManyField(User, default= None, blank=True, related_name='commented')

    def __str__(self):
        return self.title

    # redirecting to post_detail page once it's created.
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    @property
    def num_likes(self):
        return self.likes.all().count()
    
    @property
    def num_comments(self):
        return self.comments.all().count()

# Creating Tuple
LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, default='Like', max_length=10)

    def __str__(self):
        return str(self.post)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)
    comment = models.TextField(blank=False)

    def __str__(self):
        return str(self.post)

class SubComment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)
    comment = models.TextField()
    comment_reply = models.ForeignKey(Comment, on_delete=models.CASCADE)

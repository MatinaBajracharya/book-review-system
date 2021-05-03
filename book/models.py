from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class BookDetail(models.Model):
    ISBN = models.CharField(max_length=200, null = True)
    Book_Title = models.CharField(max_length=200, null = True)
    Book_Author = models.CharField(max_length = 100, null = True)
    Year_Of_Publication = models.CharField(max_length = 100, null = True)
    Publisher = models.CharField(max_length = 200, null = True)
    Image_URL_S = models.CharField(max_length = 200, null = True)
    Image_URL_M = models.CharField(max_length = 200, null = True)
    Image_URL_L = models.CharField(max_length = 200, null = True)

    def __str__(self):
        return f'{self.Book_Title}'

class Review(models.Model):
    ISBN = models.ForeignKey(BookDetail, on_delete=models.CASCADE)
    rating = models.IntegerField(default = 1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    review = models.CharField(max_length=500)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.rating}-{self.user}'

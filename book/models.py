from django.db import models

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
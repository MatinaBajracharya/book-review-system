from django.test import TestCase
from book.models import BookDetail, Review
from django.contrib.auth.models import User

# Create your tests here.
class BookDetailTestCase(TestCase):
    def setUp(self):
        self.detail = BookDetail()
        self.user = User()
        
        self.detail.ISBN="12345"
        self.user.id = 1

        self.user.save()
        self.detail.save()
        

    def test_fields(self):
        detail = BookDetail()
        detail.ISBN="12345"
        detail.Book_Title="New Book"
        detail.Book_Author="Jannet Kain"
        detail.Year_Of_Publication="2002"
        detail.Publisher="IEEE"
        detail.Image_URL_S="http://image1.com"
        detail.Image_URL_M="http://image2.com"
        detail.Image_URL_L="http://image3.com"
        detail.save()

        record = BookDetail.objects.get(pk=detail.pk)
        self.assertEqual(record, detail)

    def test_review(self):
        user = User()
        review = Review()
        review.ISBN = BookDetail.objects.get(ISBN = "12345")
        review.rating = 3
        review.user = User.objects.get(pk = 1)
        review.review = "It's a great book."
        review.date_posted = '2021-04-28'
        review.save()

        review_rec = Review.objects.get(pk=review.pk)
        self.assertEqual(review_rec, review)

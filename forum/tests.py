from django.test import TestCase
from .models import Post, Comment, Like, SubComment
from django.contrib.auth.models import User
from django.utils import timezone
from user.models import Profile
from datetime import datetime

# Create your tests here.
class ForumTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(id = 1, username='matinaa', email='matinaaaa@gmail.com', password='p1234567')
        Comment.objects.create(user_id = 1, post_id = 1, comment = "This is a comment")

        self.post = Post()
        self.post.id = 1
        self.post.author = User.objects.get(username = 'matinaa')
        self.post.save()

        self.like = Like()
        self.like.id = 1
        self.like.value = "LIKE"
        self.like.post_id = 1
        self.like.user_id = 1
        self.like.save()


    def test_comment(self):
        comment = Comment.objects.get(post_id=1)
        self.assertEqual(comment.comment, "This is a comment")

    def test_comment1(self):
        comment = Comment.objects.get(post_id=1)
        self.assertEqual(comment.user_id, 1)

    def test_post(self):
        post = Post.objects.get(id=1)
        
        user = User.objects.get(username = 'matinaa')
        self.assertEqual(post.author, user)

    def test_subcomment(self):
        sub = SubComment()
        sub.post = Post.objects.get(id=1)
        sub.user = User.objects.get(id = 1)
        sub.time = datetime.now()
        sub.comment_reply = Comment.objects.get(id = 1)
        sub.comment = "Comment Reply"

        sub.save()
        self.assertEqual(sub.comment, "Comment Reply")
        
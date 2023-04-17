from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    followers = models.ManyToManyField("self", blank=True, related_name="user_followers", symmetrical=False)
    following = models.ManyToManyField("self", blank=True, related_name="user_following", symmetrical=False)
    def __str__(self):
        return f"{self.username}"

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=128)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField()

    def serialize(self):
        return {
            "id": self.id,
            "author": self.author,
            "content": self.content,
            "date": self.date.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.likes
        }

    def __str__(self):
        return f"{self.content}"
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import DateTimeField


class User(AbstractUser):
    pass


# code adapted from https://stackoverflow.com/questions/40069192/django-models-database-design-for-user-and-follower
class Following(models.Model):
    follows = models.ForeignKey('User',
                                on_delete=models.CASCADE,
                                related_name='follower')
    follower = models.ForeignKey('User',
                                 on_delete=models.CASCADE,
                                 related_name='follows')


class Post(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="posts")
    message = models.CharField(max_length=512)
    created_on = DateTimeField(auto_now_add=True)
    likers = models.ManyToManyField(User,
                                    blank=True,
                                    related_name="likes")

    def serialize(self, liked, allow_edit):
        return {
            "id": self.id,
            "user": self.user.username,
            "message": self.message,
            "created_on": self.created_on,
            "number_likes": len(self.likers.all()),
            "liked": liked,
            "allow_edit": allow_edit
        }

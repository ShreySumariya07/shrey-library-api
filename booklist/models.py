from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class AppUser(AbstractUser):
    account_type = models.IntegerField(null=False, default=0)
    middle_name = models.CharField(max_length=32, null=True, default=None)

    def get_full_name(self):
        if self.middle_name:
            return self.first_name+"."+self.middle_name+"."+self.last_name
        else:
            return self.first_name+"."+self.last_name

    def __str__(self):
        return self.username


class Books(models.Model):
    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, null=False, default=None)
    genre = models.CharField(max_length=50, null=False, default=None)
    author = models.CharField(max_length=100, null=False)
    publication = models.CharField(max_length=130, null=False)
    description = models.CharField(max_length=1000)
    image = models.CharField(max_length=2000)
    pdf = models.CharField(max_length=2000)

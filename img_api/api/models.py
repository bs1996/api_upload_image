from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Tiers(models.Model):
    name = models.CharField('name', max_length=1000)
    thumbnail_size = models.IntegerField('thumbnail_size')
    # originally uploaded file link
    original_file = models.BooleanField('original file link', max_length=1000)
    expiring_links = models.BooleanField('expiring links', max_length=1000)

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_type = models.ForeignKey(Tiers, on_delete=models.CASCADE)
    link = models.URLField(name='url', null=True, blank=True)




class Images(models.Model):
    number = models.IntegerField('number', null=True)
    User = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', null=True)
    link1 = models.CharField('link', null=True,  max_length=1000)
    link2 = models.CharField('link', null=True,  max_length=1000)
    link3 = models.CharField('link', null=True,  max_length=1000)
    link4 = models.CharField('link', null=True,  max_length=1000)

    def __str__(self):
        return self.number


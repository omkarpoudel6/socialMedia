from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):

    COUNTRY=(
        ('NEPAL','NEPAL'),
        ('AMERICA','AMERICA'),
        ('SPAIN','SPAIN'),
        ('ENGLAND','ENGLAND'),
        ('JAPAN','JAPAN'),
    )

    username=models.OneToOneField(User,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=30, blank=True)
    middle_name=models.CharField(max_length=30, blank=True)
    last_name=models.CharField(max_length=30, blank=True)
    avatar=models.ImageField(upload_to='useravatar')
    country=models.CharField(choices=COUNTRY,max_length=30)
    phone=models.CharField(max_length=13)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name+self.middle_name+self.last_name

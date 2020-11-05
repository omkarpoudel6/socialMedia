from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.
from django.dispatch import receiver


class Profile(models.Model):

    COUNTRY=(
        ('NEPAL','NEPAL'),
        ('AMERICA','AMERICA'),
        ('SPAIN','SPAIN'),
        ('ENGLAND','ENGLAND'),
        ('JAPAN','JAPAN'),
    )

    username=models.OneToOneField(User,on_delete=models.CASCADE,related_name='user')
    first_name=models.CharField(max_length=30, blank=True)
    middle_name=models.CharField(max_length=30, blank=True)
    last_name=models.CharField(max_length=30, blank=True)
    avatar=models.ImageField(upload_to='useravatar', default='default_avatar.jpg')
    country=models.CharField(choices=COUNTRY,max_length=30, blank=True)
    phone=models.CharField(max_length=13, blank=True)
    friends=models.ManyToManyField(User,blank=True,related_name='friends')
    online=models.BooleanField(default='False')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def get_friends(self):
        return self.friends.all()

    def get_friends_count(self):
        return self.friends.all().count()

    def __str__(self):
        return str(self.username)

class RelationShip(models.Model):

    CHOICES=(
        ('send','send'),
        ('accepted','accepted')
    )

    sender=models.ForeignKey(User,on_delete=models.CASCADE,related_name='sender')
    receiver=models.ForeignKey(User,on_delete=models.CASCADE,related_name='receiver')
    status=models.CharField(choices=CHOICES,max_length=8,default='send')

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"

@receiver(post_save,sender=User)
def post_save_create_user_profile(sender,created,instance,**kwargs):
    if created:
        Profile.objects.create(username=instance)

@receiver(post_save,sender=RelationShip)
def post_save_add_to_friends(sender,instance,created,**kwargs):
    sender_=instance.sender
    receiver_=instance.receiver
    if instance.status=='accepted':
        sender_.friends.add(receiver_.user)
        receiver_.friends.add(sender_.user)
        sender_.save()
        receiver_.save()

from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from .utils import get_random_code
from django.template.defaultfilters import slugify
from django.db.models import Q

# Create your models here.
class ProfileManager(models.Manager):

    def get_all_profiles_to_invite(self, sender):
        profiles = UserFollow.objects.all().exclude(user=sender)
        profile = UserFollow.objects.get(user=sender)
        qs = Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile))
        accepted = set([])
        for rel in qs:
            if rel.status == 'accepted':
                accepted.add(rel.receiver)
                accepted.add(rel.sender)
        available = [profile for profile in profiles if profile not in accepted]
        return available
        

    def get_all_profiles(self, me):
        profiles = UserFollow.objects.all().exclude(user=me)
        return profiles

class UserFollow(models.Model):
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='avatar.png', upload_to='avatars/')
    followed_user = models.ManyToManyField(User, blank=True, related_name='followed_user')
    slug = models.SlugField(unique=True, blank=True)    
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = ProfileManager()
    def __str__(self):
        return f"{self.user.username}"

    def get_absolute_url(self):
        return reverse("UserFollows: profile-detail-view", kwargs={"slug": self.slug})
    
    def get_followers(self):
        return self.followed_user.all()

    def get_followers_no(self):
        return self.followed_user.all().count()

    def get_Ticket_no(self):
        return self.tickets.all().count() #non resolue

    def get_all_authors_Ticket(self):
        return self.tickets.all()

    __initial_first_name = None
    __initial_last_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initial_first_name = self.first_name
        self.__initial_last_name = self.last_name

    def save(self, *args, **kwargs):
        ex = False
        to_slug = self.slug
        if self.first_name != self.__initial_first_name or self.last_name != self.__initial_last_name or self.slug=="":
            if self.first_name and self.last_name:
                to_slug = slugify(str(self.first_name) + " " + str(self.last_name))
                ex = UserFollow.objects.filter(slug=to_slug).exists()
                while ex:
                    to_slug = slugify(to_slug + " " + str(get_random_code()))
                    ex = UserFollow.objects.filter(slug=to_slug).exists()
            else:
                to_slug = str(self.user)
        self.slug = to_slug
        super().save(*args, **kwargs)

    
STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted'))

class RelationshipManager(models.Manager):
    def invatations_received(self, receiver):
        qs = Relationship.objects.filter(receiver=receiver, status='send')
        return qs    

 
class Relationship(models.Model):
    sender = models.ForeignKey(UserFollow, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(UserFollow, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)   
    objects = RelationshipManager()


    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"
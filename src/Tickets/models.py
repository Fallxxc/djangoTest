from django.db import models
from django.core.validators import  MinValueValidator, MaxValueValidator
from UserFollows.models import UserFollow
# Create your models here.

class Ticket(models.Model):
    Title = models.CharField(max_length=128)
    Description = models.TextField()
    author = models.ForeignKey(UserFollow, on_delete=models.CASCADE, related_name='tickets')
    image = models.ImageField(upload_to='tickets',null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.Title}-{str(self.Description[:20])}"
        # return str(self.Description[:20])


    def num_reviews(self):
        return self.review_set.all().count()

    class Meta:
        ordering = ('-created',)

class Review(models.Model):
    user = models.ForeignKey(UserFollow, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    headline = models.CharField(max_length=128)
    body = models.CharField(max_length=8192, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)

    
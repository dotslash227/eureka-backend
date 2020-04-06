from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Category object for clubs (dynamic, input through CMS)
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Schema object for user profile
# ToDo - Nothing in mind right now
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    quizzes_taken = models.IntegerField(default=0)
    quiz_won = models.IntegerField(default=0)
    quiz_loss = models.IntegerField(default=0)
    coins = models.FloatField(default=100.00)
    is_club_creator = models.BooleanField(default=False)

    def __str__(self):
        return "Profile object for User Id: %s" % (self.user.pk)

# Schema object for a quiz club
# Todo - Nothing right now
class Club(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, blank=True, null=True)
    created_on = models.DateField(default=timezone.now)    
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="creator")
    members = models.ManyToManyField(User, related_name="members")
    club_admins = models.ManyToManyField(User, related_name="admins")
    club_rating = models.FloatField(default=5.00)

    def __str__(self):
        return self.name
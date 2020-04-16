from django.db import models
from django.utils import timezone
from quizzers.models import Club #Club model is part of the quizzers app
from django.contrib.auth.models import User


# Model for the club owner to send invitations
# An action has to be made in schema.py via graphql
# that would accept or reject the user and change member list of the club
class Invitation(models.Model):
    date_created = models.DateField(default=timezone.now)
    sent_by = models.ForeignKey(User, related_name="sender", on_delete=models.DO_NOTHING)
    sent_to = models.ForeignKey(User, related_name="receiver", on_delete=models.DO_NOTHING)
    club = models.ForeignKey(Club, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "Invitation to join a club from %s to %s for club id: %s" % (self.sent_by, self.sent_to, self.club.pk)


# Model for the club owner to receive join requests by other users
# An action has to be made in schema.py via graphql
# that would accept or reject the user and change member list of the club by admins of the club
class JoinRequest(models.Model):
    date = models.DateField(default=timezone.now)
    club = models.ForeignKey(Club, on_delete=models.DO_NOTHING)
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "Request to join club from %s for club id: %s" % (self.sender, self.club.pk)


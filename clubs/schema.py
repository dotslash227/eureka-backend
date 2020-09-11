import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.auth.models import User
from quizzers.models import Club
from quizzers.schema import UserType, ClubType
from .models import Invitation, JoinRequest


# Start of Object Types
class InvitationType(DjangoObjectType):
    class Meta:
        model = Invitation


class JoinRequestType(DjangoObjectType):
    class Meta:
        model = JoinRequest


class JoinStatusType(graphene.ObjectType):
    status = graphene.String()


class JoinRequestResponseType(graphene.ObjectType):
    status = graphene.String()


# End of Object Types

# Start of queries
class Query(object):
    invitations_byclub = graphene.List(InvitationType, clubdId=graphene.Int())
    join_requests_byclub = graphene.List(JoinRequestType, clubId=graphene.Int())
    join_status = graphene.Field(JoinStatusType, clubId=graphene.Int(required=True),
                                 senderId=graphene.Int(required=True))

    def resolve_invitations_by_club(self, info, **kwargs):
        club_id = kwargs.get("clubdId")
        club = Club.objects.get(pk=club_id)
        invites = Invitation.objects.filter(club=club)

        return invites

    def resolve_join_requests_byclub(self, info, **kwargs):
        club_id = kwargs.get("clubId")
        club = Club.objects.get(pk=club_id)
        requests = JoinRequest.objects.filter(club=club)

        return requests

    def resolve_join_status(self, info, **kwargs):
        club_id = kwargs.get("clubId")
        sender_id = kwargs.get("senderId")
        club = Club.objects.get(id=club_id)
        user = User.objects.get(id=sender_id)
        club_members = club.members.all()
        if user in club_members:
            response = "Already a Member"
        else:
            try:
                join = JoinRequest.objects.get(club=club, sender=user)
            except:
                response = "showjoin"
            else:
                response = "Pending Request"

        return {"status": response}


# End of Queries


# Start of Mutations

# Mutation for creating an invitation
# Parameters to be sent (required) -> Inviter Id, Invitee's email and clUB ID
class CreateInvitationMutation(graphene.Mutation):
    class Arguments:
        inviter_id = graphene.Int(required=True)
        invitee_email = graphene.String(required=True)
        club_id = graphene.Int(required=True)

    invitation = graphene.Field(InvitationType)

    def mutate(self, info, inviter_id, invitee_email, club_id):
        inviter = User.objects.get(pk=inviter_id)
        club = Club.objects.get(pk=club_id)

        try:
            invitee = User.objects.get(email=invitee_email)
        except:
            raise Exception("Invitation being sent to user that does not exist on platform")
        else:
            try:
                invitation_object = Invitation.objects.get(sent_by=inviter, sent_to=invitee, club=club)
            except:
                invitation_object = Invitation.objects.create(sent_by=inviter, sent_to=invitee, club=club)
                return CreateInvitationMutation(invitation=invitation_object)
            else:
                raise Exception("An invitation has already been sent to the user for this  club")


# Mutation for Join request creation
# Parameters to be sent (required) => Club Id and Sender Id
class JoinRequestMutation(graphene.Mutation):
    class Arguments:
        club_id = graphene.Int(required=True)
        sender_id = graphene.Int(required=True)

    join_request = graphene.Field(JoinRequestType)

    def mutate(self, info, club_id, sender_id):
        club = Club.objects.get(pk=club_id)
        sender = User.objects.get(pk=sender_id)

        try:
            JoinRequest.objects.get(club=club, sender=sender)
        except:
            jr = JoinRequest.objects.create(club=club, sender=sender)
            return JoinRequestMutation(join_request=jr)
        else:
            raise Exception("A pending request has already been sent to the admin of this club")


# Mutation for accepting or rejecting a join request by a user for a club
# Parameters to be sent: ClubId, senderId, Response as "yes" or "no"
class JoinRequestResponseMutation(graphene.Mutation):
    class Arguments:
        club_id = graphene.Int(required=True)
        sender_id = graphene.Int(required=True)
        decision = graphene.String(required=True)

    response = graphene.Field(JoinRequestResponseType)

    def mutate(self, info, club_id, sender_id, decision):
        club = Club.objects.get(pk=club_id)
        sender = User.objects.get(pk=sender_id)
        instance = JoinRequest.objects.get(club=club, sender=sender)
        response = "deleted"
        if decision == "yes":
            club.members.add(sender)
            response = "added"
        instance.delete()

        return JoinRequestResponseMutation(response={"status": response})


class Mutation(graphene.ObjectType):
    create_club_invitation = CreateInvitationMutation.Field()
    create_club_joinrequest = JoinRequestMutation.Field()
    join_request_repond = JoinRequestResponseMutation.Field()

# End of Mutations

from django.contrib import admin
from .models import Invitation, JoinRequest

admin.site.register(Invitation)
admin.site.register(JoinRequest)
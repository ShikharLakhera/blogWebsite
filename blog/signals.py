from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from .models import Profile

@receiver(user_signed_up)
def create_user_profile(request, user, **kwargs):
    # Create profile only if it doesn't exist
    Profile.objects.get_or_create(user=user)

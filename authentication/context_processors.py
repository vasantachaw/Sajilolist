from authentication.models import Profile
import logging

logger = logging.getLogger(__name__)  # Use logger instead of print for production

def profile_context(request):
    """
    Context processor to add the authenticated user's profile to the template context.
    """
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.select_related('user').get(user=request.user)
            logger.debug(f"Profile found for user: {request.user.username}")
            return {'profile': profile}
        except Profile.DoesNotExist:
            logger.warning(f"No profile found for user: {request.user.username}")
            return {'profile': None}
    return {'profile': None}

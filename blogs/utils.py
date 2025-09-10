from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    if not user.is_active:
        raise AuthenticationFailed('User is not active')
    refresh_token = RefreshToken.for_user(user)
    return {
        'access_token': str(refresh_token.access_token),
        'refresh_token': str(refresh_token)
    }

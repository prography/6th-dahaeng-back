from firebase_admin import auth
from core.models import FirebaseUID


class FirebaseBackend:
    def authenticate(self, request, uid=None):
        try:
            auth.get_user(uid)
            return FirebaseUID.objects.get(uid=uid)
        except FirebaseUID.DoesNotExist:
            return FirebaseUID.objects.create(uid=uid)
        except (auth.AuthError, ValueError):
            return None

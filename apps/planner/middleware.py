from django.contrib.auth.models import User


class AutoUserMiddleware:
    """
    Ensures that every request has an authenticated user attached.
    Picks an existing user (preferring one with existing data) or creates
    a default 'Student' user. This eliminates the login page requirement
    while maintaining complete model and database compatibility.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not getattr(request, "user", None) or not request.user.is_authenticated:
            user = User.objects.filter(subjects__isnull=False).distinct().first()
            if not user:
                user = User.objects.first()
            if not user:
                user = User.objects.create_user(
                    username="Student",
                    email="student@focusforge.local",
                )
            request.user = user
        return self.get_response(request)


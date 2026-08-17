from django.contrib.auth.decorators import user_passes_test

staff_required = user_passes_test(
    lambda user: user.is_active and user.is_staff,
    login_url="operations:login",
)

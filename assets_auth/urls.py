from django.urls import path
from django.contrib.auth import views as auth_views
from assets_auth.views import SignUpView

app_name = 'assets_auth'

urlpatterns = [
    path(
        'login/',
        auth_views.LoginView.as_view(redirect_authenticated_user=True),
        name='login',
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout',
    ),
    path(
        'sign-up/',
        SignUpView.as_view(),
        name='sign-up',
    ),
]

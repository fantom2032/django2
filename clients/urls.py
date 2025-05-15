from django.urls import path

from clients.views import (
    RegistrationView, 
    LoginView,
    LogoutView,
    ActivationView,
    ProfileView,
    DeleteProfileView,
    ForgotPasswordView,
)


urlpatterns = [
    path(route="reg/", view=RegistrationView.as_view(), name="reg"),
    path(route="login/", view=LoginView.as_view(), name="login"),
    path(route="logout/", view=LogoutView.as_view(), name="logout"),
    path(
        route="activation/<str:username>/<str:code>", 
        view=ActivationView.as_view(), name="activate"
    ),
    path(route="profile/", view=ProfileView.as_view(), name="profile"),
    path(route="profile/delete/", view=DeleteProfileView.as_view(), name="delete_profile"),
    path(route="forgot_password/", view=ForgotPasswordView.as_view(), name="forgot_password"),
]

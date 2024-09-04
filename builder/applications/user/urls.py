from django.urls import include, path
from rest_framework import routers

from builder.applications.user import views

router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api/user/', include([
        path('create/', views.UserCreateView.as_view(), name="user-create"),
        path('<int:pk>/details/', views.UserProfileView.as_view(), name="user-details"),
        path('email-verify/', views.EmailVerifyView.as_view(), name="email-verify"),
        path('email-resend-verification/', views.ResendVerificationEmailView.as_view(), name= "email-resend-verification"),
        path('invite-user/', views.InvitationCreateView.as_view(), name= "invite-user"),
        path('invite-user-validation/', views.InvitationValidationView.as_view(), name= "invite-user-validation"),
        path('address/', include([
            path('create/', views.UserAddressCreateView.as_view(), name="user-address-create"),
            path('<int:pk>/details/', views.UserAddressDetailsView.as_view(), name="user-address-details"),
        ]))
    ])),
]
from django.urls import include, path
from rest_framework import routers

from builder.applications.user import views

router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api/user/', include([
        path('create/', views.UserCreateView.as_view(), name="user-create"),
        path('<int:pk>/profile/', views.UserProfileView.as_view(), name="user-profile")
    ])),
]
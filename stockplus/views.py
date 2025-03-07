from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from stockplus.serializer import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
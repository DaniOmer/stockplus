"""
Avatar views for the user application.
"""
from rest_framework import status, permissions, parsers
from rest_framework.response import Response
from rest_framework.views import APIView

from stockplus.modules.user.application.user_service import UserService
from stockplus.modules.user.infrastructure.repositories import UserRepository
from stockplus.modules.user.domain.exceptions import UserNotFoundException


class AvatarUploadView(APIView):
    """
    API endpoint for uploading user avatars.
    """
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    
    def post(self, request):
        """
        Upload a user avatar.
        
        Args:
            request: The HTTP request
            
        Returns:
            Response: The HTTP response
        """
        if 'avatar' not in request.FILES:
            return Response(
                {'error': 'No avatar file provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        avatar = request.FILES['avatar']
        
        # Check file size (limit to 5MB)
        if avatar.size > 5 * 1024 * 1024:
            return Response(
                {'error': 'Avatar file too large (max 5MB)'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check file type
        allowed_types = ['image/jpeg', 'image/png', 'image/gif']
        if avatar.content_type not in allowed_types:
            return Response(
                {'error': 'Invalid file type. Only JPEG, PNG, and GIF are allowed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user_service = UserService(UserRepository())
        
        try:
            user = user_service.get_user_by_id(request.user.id)
            
            if not user:
                return Response(
                    {'error': 'User not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Save the avatar to the user's profile
            # In a real implementation, you would save the file to a storage service
            # and update the user's avatar field with the file URL
            user.avatar = avatar
            user_service.user_repository.save(user)
            
            return Response(
                {'message': 'Avatar uploaded successfully'},
                status=status.HTTP_200_OK
            )
        except UserNotFoundException:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

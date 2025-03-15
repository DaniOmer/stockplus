"""
Management command to test the avatar upload API.
"""

import io
import json
from PIL import Image
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class Command(BaseCommand):
    help = 'Test the avatar upload API'

    def create_test_image(self, width=200, height=200, color=(255, 0, 0)):
        """Create a test image in memory."""
        image = Image.new('RGB', (width, height), color)
        image_io = io.BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)
        return image_io

    def get_tokens_for_user(self, user):
        """Get JWT tokens for a user."""
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def handle(self, *args, **options):
        # Create a test user
        username = 'testuser'
        email = 'testuser@example.com'
        password = 'testpassword'
        
        try:
            user = User.objects.get(email=email)
            self.stdout.write(self.style.SUCCESS(f"Using existing user: {email}"))
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_active=True,
                is_verified=True
            )
            self.stdout.write(self.style.SUCCESS(f"Created new user: {email}"))
        
        # Get tokens for the user
        tokens = self.get_tokens_for_user(user)
        access_token = tokens['access']
        
        # Create a test client
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        self.stdout.write(self.style.SUCCESS("Successfully authenticated with JWT token."))
        
        # Test get signature
        self.stdout.write(self.style.NOTICE("\n=== Testing Get Signature ==="))
        signature_response = client.get('/api/users/avatar/signature/')
        
        if signature_response.status_code != 200:
            self.stdout.write(self.style.ERROR(f"Failed to get signature: {signature_response.status_code}"))
            self.stdout.write(self.style.ERROR(signature_response.content.decode()))
            return
        
        signature_data = json.loads(signature_response.content.decode())
        self.stdout.write(self.style.SUCCESS(f"Signature Response: {json.dumps(signature_data, indent=2)}"))
        
        signature = signature_data.get('data', {}).get('signature')
        timestamp = signature_data.get('data', {}).get('timestamp')
        
        if not signature or not timestamp:
            self.stdout.write(self.style.ERROR("Failed to extract signature or timestamp. Exiting."))
            return
        
        # Test upload avatar
        self.stdout.write(self.style.NOTICE("\n=== Testing Upload Avatar ==="))
        image_io = self.create_test_image()
        image_file = SimpleUploadedFile(
            "test_avatar.jpg", 
            image_io.getvalue(), 
            content_type="image/jpeg"
        )
        
        upload_data = {
            'signature': signature,
            'timestamp': timestamp,
            'avatar': image_file
        }
        
        upload_response = client.post('/api/users/avatar/upload/', upload_data, format='multipart')
        
        if upload_response.status_code != 200:
            self.stdout.write(self.style.ERROR(f"Failed to upload avatar: {upload_response.status_code}"))
            self.stdout.write(self.style.ERROR(upload_response.content.decode()))
            return
        
        upload_data = json.loads(upload_response.content.decode())
        self.stdout.write(self.style.SUCCESS(f"Upload Response: {json.dumps(upload_data, indent=2)}"))
        
        # Test get avatar URL
        self.stdout.write(self.style.NOTICE("\n=== Testing Get Avatar URL ==="))
        url_response = client.get('/api/users/avatar/url/')
        
        if url_response.status_code != 200:
            self.stdout.write(self.style.ERROR(f"Failed to get avatar URL: {url_response.status_code}"))
            self.stdout.write(self.style.ERROR(url_response.content.decode()))
        else:
            url_data = json.loads(url_response.content.decode())
            self.stdout.write(self.style.SUCCESS(f"URL Response: {json.dumps(url_data, indent=2)}"))
        
        # Test remove avatar
        self.stdout.write(self.style.NOTICE("\n=== Testing Remove Avatar ==="))
        remove_response = client.delete('/api/users/avatar/remove/')
        
        if remove_response.status_code != 200:
            self.stdout.write(self.style.ERROR(f"Failed to remove avatar: {remove_response.status_code}"))
            self.stdout.write(self.style.ERROR(remove_response.content.decode()))
        else:
            remove_data = json.loads(remove_response.content.decode())
            self.stdout.write(self.style.SUCCESS(f"Remove Response: {json.dumps(remove_data, indent=2)}"))
        
        self.stdout.write(self.style.SUCCESS("\nAll tests completed."))

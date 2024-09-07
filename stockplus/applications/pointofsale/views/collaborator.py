from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied

from builder.models import Company, User, Collaboration
from stockplus.models import PointOfSale
from stockplus.permissions import IsManager
from stockplus.applications.pointofsale.serializers import PointOfSaleAddCollaboratorSerializer


class PointOfSaleAddCollaboratorView(generics.GenericAPIView):
    queryset = PointOfSale.objects.all()
    serializer_class = PointOfSaleAddCollaboratorSerializer
    permission_classes = [IsManager]

    def get_object(self):
        user = self.request.user
        try:
            company = Company.objects.get(owner=user)
            point_of_sale = PointOfSale.objects.get(pk=self.kwargs.get('pk'))
        except Company.DoesNotExist:
            raise ValidationError("You must create a company to continue.")
        except PointOfSale.DoesNotExist:
            raise ValidationError("PointOfSale matching query does not exist.")
        
        if point_of_sale.company != company:
            raise PermissionDenied("You do not have permission to access this resource.")
        return point_of_sale
    
    def post(self, request, *args, **kwargs):
        point_of_sale = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        collaborator_email = serializer.validated_data.get('email')
        try:
            collaborator = User.objects.get(email=collaborator_email)
            collaboration = Collaboration.objects.get(manager=self.request.user, collaborator=collaborator)
        except User.DoesNotExist:
            raise ValidationError("There is no user with the given email.")
        except Collaboration.DoesNotExist:
            raise ValidationError("There is no collaborator with the given email.")
        
        if point_of_sale.collaborators.acontains(collaborator):
            return Response({'detail': 'You already add this collaborator to the point of sale.'}, status=status.HTTP_400_BAD_REQUEST)
        point_of_sale.collaborators.add(collaborator)
        point_of_sale.save()
        
        return Response({"detail": "Collaborator added successfully to the point of sale."}, status=status.HTTP_200_OK)
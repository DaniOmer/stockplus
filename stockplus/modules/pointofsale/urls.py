from django.urls import path, include

from stockplus.modules.pointofsale.interfaces.views import (
    PointOfSaleListCreateView,
    PointOfSaleRetrieveUpdateDeleteView,
    PointOfSaleAddCollaboratorView
)

urlpatterns = [
    path('api/', include([
        path('point-of-sale/', PointOfSaleListCreateView.as_view(), name='point_of_sale_list_create'),
        path('point-of-sale/<int:pk>/', PointOfSaleRetrieveUpdateDeleteView.as_view(), name='point_of_sale_retrieve_update_delete'),
        path('point-of-sale/<int:pk>/add-collaborator/', PointOfSaleAddCollaboratorView.as_view(), name='point_of_sale_add_collaborator')
    ]))
]

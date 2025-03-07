from django.urls import path, include

from stockplus.modules.pointofsale.interfaces.views import (
    PointOfSaleListCreateView,
    PointOfSaleRetrieveUpdateDeleteView,
    PointOfSaleAddCollaboratorView
)
from stockplus.modules.pointofsale.interfaces.views.payment_method import (
    PaymentMethodListCreateView,
    PaymentMethodRetrieveUpdateDeleteView,
    PaymentMethodToggleStatusView
)

urlpatterns = [
    path('api/', include([
        # Point of Sale endpoints
        path('point-of-sale/', PointOfSaleListCreateView.as_view(), name='point_of_sale_list_create'),
        path('point-of-sale/<int:pk>/', PointOfSaleRetrieveUpdateDeleteView.as_view(), name='point_of_sale_retrieve_update_delete'),
        path('point-of-sale/<int:pk>/add-collaborator/', PointOfSaleAddCollaboratorView.as_view(), name='point_of_sale_add_collaborator'),
        
        # Payment Method endpoints
        path('point-of-sale/<int:point_of_sale_id>/payment-methods/', PaymentMethodListCreateView.as_view(), name='payment_method_list_create'),
        path('point-of-sale/<int:point_of_sale_id>/payment-methods/<int:payment_method_id>/', PaymentMethodRetrieveUpdateDeleteView.as_view(), name='payment_method_retrieve_update_delete'),
        path('point-of-sale/<int:point_of_sale_id>/payment-methods/<int:payment_method_id>/toggle-status/', PaymentMethodToggleStatusView.as_view(), name='payment_method_toggle_status')
    ]))
]

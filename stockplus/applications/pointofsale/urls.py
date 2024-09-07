from django.urls import path, include

from stockplus.applications.pointofsale import views

urlpatterns = [
    path('api/', include([
        path('point-of-sale/', views.PointOfSaleListCreateView.as_view(), name='point_of_sale_list_create'),
        path('point-of-sale/<int:pk>', views.PointOfSaleRetrievUpdateDeleteView.as_view(), name='point_of_sale_list_create'),
        path('point-of-sale/<int:pk>/add-collaborator/', views.PointOfSaleAddCollaboratorView.as_view(), name='point_of_sale_add_collaborator')
    ]))
]

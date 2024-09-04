from django.urls import include, path

from builder.applications.company import views

urlpatterns = [
    path('api/company/', include([
        path('create/', views.CompanyCreateView.as_view(), name='company-create'),
        path('<int:pk>/details/', views.CompanyDetailsView.as_view(), name='company-details'),
        path('address/', include([
            path('create/', views.CompanyAddressCreateView.as_view(), name="company-address-create"),
        ]))
    ]))
]

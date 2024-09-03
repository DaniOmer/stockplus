from django.urls import include, path

from builder.applications.company import views

urlpatterns = [
    path('api/company/', include([
        path('create/', views.CompanyCreateView.as_view(), name='company-create')
    ]))
]

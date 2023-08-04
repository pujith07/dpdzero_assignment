from django.contrib import admin
from django.urls import path
from api.views import *
urlpatterns = [
    path("admin/", admin.site.urls),
    path('register/',register_user, name='register'),
    path('token/', generate_token, name='generate_token'),
    path('data/', store_data, name='store_data'),
    path('data/<str:key>/',DataDetailView.as_view(),name='data'),
]

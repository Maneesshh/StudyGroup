from django.urls import path
from . import views



urlpatterns =[
    path('', views.getRoutes),
    path('rooms/', views.getRooms),
    path('rooms/<str:pk>/', views.getRoom),
    path('rooms/call-status/active', views.roomCallStatusActive),
    path('rooms/call-status/inactive', views.roomCallStatusInactive),
    path('rooms/call-status/<str:pk>', views.getVideoStatus),
    


]
from django.contrib import admin
from django.urls import path
from . import views
from .views import MyTokenObtainPairView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path('', views.getRoutes),
    path('register/', views.register,name="register"),
    path('messages/', views.getMessages,name="all"),
    path('addmessage/', views.addMessage, name="add"),
    path('single/<int:id>/', views.getSingleMessage, name="single"),
    path('delete/<int:id>/', views.deleteMessage, name="delete"),
    path('unread/<int:id>/', views.getUnreadMessages, name="unread"),
    
    #path('prod/<int:id>', views.prod, name="prod")

    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
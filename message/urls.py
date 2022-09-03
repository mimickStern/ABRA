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
    path('received/', views.getReceivedMessages,name="received"),
    path('sent/', views.getSentMessages,name="sent"),
    path('addmessage/', views.addMessage, name="add"),
    path('message/<int:id>/read/', views.readAMessage, name="single"),
    path('delete/<int:id>/', views.deleteMessage, name="delete"),
    path('messages/unread/', views.getUnreadMessages, name="unread"),
    path('messages/read/', views.getReadMessages, name="read"),

    #Login
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
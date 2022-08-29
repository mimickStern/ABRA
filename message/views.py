from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from .serializers import MessageSerializer
from .models import Message

# Create your views here.

def index(req):
    return JsonResponse('hello', safe=False)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['eeemail'] = user.email
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/token',
        '/token/refresh',
    ]

    return Response(routes)


# register/signup
@api_view(['POST'])
def register(request):
    user=User.objects.create_user(
        username= request.data["username"],
        email=request.data["email"],
        password=request.data["password"])
    return Response("routes")

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMessages(request):
    print("innnn")
    user = request.user
    print(user)
    messages = user.message_set.all()
    print(user.message_set)
    print(messages)
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addMessage (request):
    user = request.user
    receiver = request.data["receiver"]
    subject = request.data["subject"]
    message = request.data["message"]
    Message.objects.create(user=user,receiver=receiver,subject=subject,message=message,unread="True")
    return Response("message added")

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getSingleMessage(request,id):
    user = request.user
    print(user)
    message = Message.objects.get(_id=id)
    serializer = MessageSerializer(message, many=False)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteMessage(request,id):
    user = request.user
    print(user)
    message = Message.objects.get(_id=id).delete()
    serializer = MessageSerializer(message)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUnreadMessages(request,id):
    user = request.user
    print(user)
    messages = Message.objects.filter(unread=id)
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)


from django.shortcuts import render
from django.db.models import Q
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

#Login/SignIn
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

#all routes
@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/register/',
        '/received/',
        '/sent/',
        '/addmessage/',
        'messages/<int:id>/read/',
        '/delete/<int:id>/',
        'messages/unread/',
        'messages/read/',
        '/token/',
        '/token/refresh/',
    ]

    return Response(routes)


# register/signup
@api_view(['POST'])
def register(request):
    user=User.objects.create_user(
        username= request.data["username"],
        email=request.data["email"],
        password=request.data["password"])
    return Response("register succesfull")


#get received messages
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getReceivedMessages(request):
    
    recipient = request.user
    messages = Message.objects.filter(Q(recipient=recipient))
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)


#get sent mesages
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getSentMessages(request):
    
    user = request.user
    messages = Message.objects.filter(Q(user=user))
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)


#adding a messgae
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addMessage (request):
    try:
        user = request.user
        recipient = request.data["recipient"]
        objectRecipient=User.objects.get(username=recipient)
        subject = request.data["subject"]
        message = request.data["message"]
        #unread=true, read=false
        Message.objects.create(user=user,recipient=objectRecipient,subject=subject,message=message,unread=True)
        return Response("message added")
    except:
        return Response("one or more of the attributes is incorrect. check that you've fullfilled hte following (recipient,subject,message,unread")


#getting a single, yet read message, and reversing it to "read"
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def readAMessage(request,id):
    recipient = request.user
    try:
        message = Message.objects.filter(Q(recipient=recipient)).get(_id=id)
        message.unread=False
        message.save()
        serializer = MessageSerializer(message, many=False)
        return Response(serializer.data)
    except:
        return Response("check that recipient matches message-id and vice-versa or message-id no longer exists")


#deleting a message
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteMessage(request,id):
    user = request.user
    try:
        message = Message.objects.filter(Q(user=user)).get(_id=id).delete()
        serializer = MessageSerializer(message)
        return Response("message deleted")
    except:
        return Response("check that user matches message-id and vice-versa or message-id no longer exists")


#getting unread messages
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUnreadMessages(request):
    recipient = request.user
    try:
        messages = Message.objects.filter(Q(recipient=recipient)).filter(unread=True)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    except:
        return Response("something went wrong")

#getting unread messages
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getReadMessages(request):
    recipient = request.user
    try:
        messages = Message.objects.filter(Q(recipient=recipient)).filter(unread=False)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    except:
        return Response("something went wrong")
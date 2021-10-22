from communications.serializers import (
    ChatSerializer, 
    ClientSerializer, 
    ConversationSerializer, 
    DiscountSerializer, 
    OperatorSerializer, 
    StoreSerializer
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, serializers, status
from django.http import Http404
from django.contrib.auth.models import User
from django.template import Context, Template


from . models import *

class StoreList(generics.ListCreateAPIView):
    """
    List all stores or create a new store
    """
    queryset = Store.objects.all()
    serializer_class = StoreSerializer


class ClientList(generics.ListCreateAPIView):
    """
    List all clients or create a new one from logged in user
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    # def post(self, request):
    #     r_data = {
    #         "user": request.user.id, 
    #         "timezone": request.data["timezone"],
    #         "phone_number": request.data["phone_number"]
    #         }
    #     serializer = self.serializer_class(data=r_data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DiscountList(generics.ListCreateAPIView):
    """List all discounts or create a new one"""
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer


class OperatorList(generics.ListCreateAPIView):
    """List all operators or create a new one"""
    queryset = Operator.objects.all()
    serializer_class = OperatorSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class ConversationList(generics.ListCreateAPIView):
    """
    List all conversations, or create a new conversation.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    # def post(self, request):
    #     serializer = ConversationSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class ConversationDetail(APIView):
    """
    Retrieve, update or delete a conversation instance.
    """
    def get_object(self, pk):
        try:
            return Conversation.objects.get(pk=pk)
        except Conversation.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        conv = self.get_object(pk)
        serializer = ConversationSerializer(conv)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        conv = self.get_object(pk)
        serializer = ConversationSerializer(conv, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        conv = self.get_object(pk)
        conv.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChatList(generics.ListCreateAPIView):
    """
    List all chats, or create a new chat.
    """
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    # def get(self, request, format=None):
    #     chats = Chat.objects.all()
    #     serializer = ChatSerializer(chats, many=True)
    #     return Response(serializer.data)

    # def post(self, request, format=None):
    #     serializer = ChatSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChatDetail(APIView):
    """
    Retrieve and update a chat instance
    """
    def get_object(self, pk):
        try:
            return Chat.objects.get(pk=pk)
        except Chat.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = ChatSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        chat = self.get_object(pk)
        serializer = ChatSerializer(chat, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
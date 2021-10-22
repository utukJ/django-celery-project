from communications.models import Chat, Client, Conversation, Discount, Operator, Schedule, Store
from rest_framework import serializers


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = [
            'id', 
            'conversation', 
            'payload',
            'discount',
            'user',
            'created_date',
            'status' 
            ]


class ConversationSerializer(serializers.ModelSerializer):
    chats = ChatSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'store', 'client', 'operator', 'status', 'chats'] ## SHOULD INCLUDE LIST OF CHATS!!!


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'name', 'timezone', 'phone_number']

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ['id', 'store', 'discount_code']

class OperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operator
        fields = ['id', 'user', 'operator_group']

class OperatorPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operator
        fields = ['id', 'operator_group']

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'user', 'timezone', 'phone_number']

class ClientPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'timezone', 'phone_number']

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['id', 'chat', 'sending_date']
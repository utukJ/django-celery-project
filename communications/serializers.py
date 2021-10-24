from communications.models import Chat, Client, Conversation, Discount, Operator, Schedule, Store
from rest_framework import serializers
from django.template import Context, Template
from .tasks import print_to_console, send_email_task
import datetime



def fill_in_context(template_string, context_dict):
    """takes template string and returns the right value"""
    return Template(template_string).render(Context(context_dict))

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

    def create(self, validated_data):
        chat = Chat(**validated_data)
        conversation = chat.conversation
        operator = conversation.operator
        client = conversation.client
        store = conversation.store
        discount = chat.discount

        chat.payload = fill_in_context(chat.payload, {
            "operator": operator,
            "client": client,
            "store": store,
            "discount": discount
        })
        chat.save()
        return chat


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
    
    def create(self, validated_data):
        sch = Schedule(**validated_data)
        print("schedule model created...")
        m_subject = "Conversation " + str(sch.chat.conversation.id)
        msg = sch.chat.payload
        to = [sch.chat.user.email]
        sender = "utukphd@gmail.com"
        print_to_console.apply_async((sch.chat.payload,), countdown=30)
        send_email_task.apply_async((m_subject, msg, sender, to), countdown=60)
        sch.save()
        print("schedule model saved ...")
        return sch


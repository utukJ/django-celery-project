from communications.models import Chat, Client, Conversation, Discount, Operator, Schedule, Store
from rest_framework import serializers
from django.template import Context, Template
from .tasks import print_to_console, send_email_task
import datetime
import string
from django.core.mail import send_mail
from django.utils import timezone
import pytz

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

        ## create new schedule with every new chat message
        schedule = Schedule()
        chat.save()
        return chat

    def validate_payload(self, chat_payload):
        """
        ensures that we have no more than 300 characters 
        and allowed characters ===>   *aA-zZ1234567890{}$%_-\\/~@#$%^&*()!?
        """
        if len(chat_payload) > 300:
            raise serializers.ValidationError("character limit exceeded")
        allowed_characters = " *1234567890{}$%_-\\/~@#$%^&*()!?\r\n" + string.ascii_lowercase
        l_chat_payload = chat_payload.lower()
        for chr in l_chat_payload:
            if chr not in allowed_characters:
                raise serializers.ValidationError(f"character not allowed: '{chr}'")
        return chat_payload


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

        m_subject = "Conversation " + str(sch.chat.conversation.id)
        msg = sch.chat.payload
        to = [sch.chat.user.email]

        # tz = sch.chat.conversation.store.timezone
        # timezone.activate(tz)
        time_diff = sch.sending_date - timezone.now()
        print("time diff: ", time_diff.seconds)

        send_email_task.apply_async(
            (m_subject, msg, None, [sch.chat.user.email], sch.chat.id), 
            countdown=time_diff.seconds
            )
        sch.save()
        
        print("schedule model saved ...")
        return sch

        
    def validate_sending_date(self, sending_date):
        if sending_date < timezone.now():
            raise serializers.ValidationError("cannot schedule to past time")
        return sending_date


    def validate(self, data):
        ## try to get user timezone
        chat = data["chat"]
        sending_date = data["sending_date"]
        try:
            tz = chat.user.timezone
        ## fall back to store timezone
        except AttributeError:
            tz = chat.conversation.store.timezone
        
        realtime = sending_date.astimezone(pytz.timezone(tz))
        print("realtime: ", realtime)
        late = datetime.time(hour=20)
        early = datetime.time(hour=9)
        print("realtime.time: ", realtime.time(), type(realtime.time()))
        print("late: ", late, type(late))
        print("early: ", early, type(early))
        if realtime.time() > late or realtime.time() < early:
            raise serializers.ValidationError("schedule time after 20:00 or before 09:00 not allowed")
        return data

            

                


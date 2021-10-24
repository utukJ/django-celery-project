from django.contrib import admin

from communications.models import Chat, Client, Conversation, Discount, Operator, Schedule, Store

# Register your models here.

admin.site.register(Store)
admin.site.register(Discount)
admin.site.register(Conversation)
admin.site.register(Chat)
admin.site.register(Client)
admin.site.register(Operator)
admin.site.register(Schedule)
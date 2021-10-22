from django.urls import path, include

from communications.views import (
    ChatDetail, 
    ChatList, 
    ClientList, 
    ConversationDetail, 
    ConversationList, 
    DiscountList, 
    OperatorList, 
    StoreList)

urlpatterns = [
    path('conversations', ConversationList.as_view(), name="conversation-list"),
    path('conversations/<int:pk>', ConversationDetail.as_view(), name="conversation-detail"),
    path('chats', ChatList.as_view(), name="chat-list"),
    path('chats/<int:pk>', ChatDetail.as_view(), name="chat-detail"),
    path('discounts', DiscountList.as_view(), name="discount-list"),
    path('stores', StoreList.as_view(), name="store-list"),
    path('clients', ClientList.as_view(), name="client-list"),
    path('operators', OperatorList.as_view(), name="operator-list"),
]

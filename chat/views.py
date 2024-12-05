from django.shortcuts import render
from .models import Group,Chat

def room(request, room_name):
    group_name = room_name
    group,_=Group.objects.get_or_create(
        name = group_name
    )
    chats = Chat.objects.filter(group = group)

    return render(request, "chat/room.html", {"room_name": room_name,'chats':chats})
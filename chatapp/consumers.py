import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "chat_message",
                "message": message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))

    '''
    self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        - Obtains the 'room_name' parameter from the URL route in chat/routing.py that opened the WebSocket connection to the consumer.
        - Every consumer has a scope that contains information about its connection, including in particular any positional or keyword arguments from the URL route and the currently authenticated user if any.
    '''
    '''
    self.room_group_name = "chat_%s" % self.room_name
        - Constructs a Channels group name directly from the user-specified room name, without any quoting or escaping.
        - Group names may only contain alphanumerics, hyphens, underscores, or periods. Therefore this example code will fail on room names that have other characters.
    '''
    '''
    self.channel_layer.group_add(...)        # Joins a group.
    self.channel_layer.group_discard(...)    # Leaves a group.
    self.channel_layer.group_send            # Sends an event to a group.
    
    - await is used to call asynchronous functions that perform I/O.
    '''
    '''
    self.accept()
        - Accepts the WebSocket connection. 
        - If you do not call accept() within the connect() method then the connection will be rejected and closed. You might want to reject a connection for example because the requesting user is not authorized to perform the requested action.
        - It is recommended that accept() be called as the last action in connect() if you choose to accept the connection.
    '''

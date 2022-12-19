import json
from EasyServer.networking.network_message import NetworkMessage

class ClientConnection:
    def __init__(self, socket, address):
        self.socket = socket
        self.address = address

    def send_message(self, message) -> None:
        """
        Attempts to send a message to the client. Will attempt to serialize the message into a 
        NetworkMessage object.
        """
        is_builtin = message.__class__.__module__ == 'builtins'
        if is_builtin:
            # by passing a built in type, we assume the user wants to send a simple message with only a body.
            message = NetworkMessage()
            message.set_body(message)

        elif type(message) != NetworkMessage:
            # if message is a custom type tht is not a NetworkMessage instance,
            # we will attempt to serialize the class into the body of a NetworkMessage.
            message = NetworkMessage()
            
            # convert the message (which is a custom type) into a dictionary
            body = json.dumps(message.__dict__)
            message.set_body(body)


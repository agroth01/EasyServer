import socket
import threading
import EasyServer.server.defaults as DefaultValues
from EasyServer.server.client_connection import ClientConnection
from EasyServer.networking.network_message import NetworkMessage

class EasyServer:
    """
    A high level server class that handles the connection of clients and transportation
    of data between the server and the clients.
    """
    def __init__(self, host, port, tick_rate=DefaultValues.TICK_RATE, buffer_size=DefaultValues.BUFFER_SIZE) -> None:
        self.host = host
        self.port = port
        self.tick_rate = tick_rate
        self.buffer_size = buffer_size

        self.__clients = []
        self.__stop_flag = False

    # starting and stopping the server

    def start(self) -> None:
        """
        Starts the server. This is a blocking call.
        """
        self.__internal_start()

    def start_async(self) -> None:
        """
        Starts the server in a non-blocking way.
        """
        threading.Thread(target=self.__internal_start).start()

    def __internal_start(self) -> None:
        """
        Internal method that starts the server.
        Binds to the host and port and starts accepting connections.
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(0)

    # Connection events

    def on_connection(self, client: ClientConnection) -> None:
        """
        Method meant to be overridden when a client connects to the server.
        """
        pass

    def on_message(self, message: NetworkMessage, client: ClientConnection) -> None:
        """
        Method meant to be overridden when a message is received from a client.
        """
        pass

    def on_disconnect(self, client: ClientConnection) -> None:
        """
        Method meant to be overridden when a client disconnects from the server.
        """
        pass

    def __on_connection(self, client: ClientConnection) -> None:
        """
        Internal method that handles the connection of a client.
        Will store the connection in a list and invoke event.
        """
        self.__clients.append(client)
        self.on_connection(client)

    def __on_message(self, message: NetworkMessage, client: ClientConnection) -> None:
        """
        Internal method that handles the message of a client.
        Will invoke event.
        """
        self.on_message(message, client)

    def __on_disconnect(self, client: ClientConnection) -> None:
        """
        Internal method that handles the disconnection of a client.
        Will remove the connection from the list and invoke event.
        """
        self.__clients.remove(client)
        self.on_disconnect(client)
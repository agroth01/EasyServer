import socket
import threading
import time
import EasyServer.server.defaults as DefaultValues
from EasyServer.server.client_connection import ClientConnection
from EasyServer.networking.network_message import NetworkMessage

class EasyServer:
    """
    A high level server class that handles the connection of clients and transportation
    of data between the server and the clients.
    """
    def __init__(self, host, port, tick_rate=DefaultValues.TICK_RATE, buffer_size=DefaultValues.BUFFER_SIZE,
                 manual_mode=False) -> None:
        self.host = host
        self.port = port
        self.tick_rate = tick_rate
        self.buffer_size = buffer_size
        self.manual_mode = manual_mode

        # set up callbacks
        self.__on_message_callback = self.on_message
        self.__on_connection_callback = self.on_connection
        self.__on_disconnect_callback = self.on_disconnect

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

        # start main loop if not in manual mode
        if not self.manual_mode:
            self.__server_loop()

    # server loop

    def update(self):
        """
        Repeatedly called by the server loop. Can also be called externally to update the server
        if set to manual mode.
        """
        start_time = time.time()

        #self.__accept_connections()
        #self.__receive_messages()

        # ignore keeping the server at a constant tick rate if in manual mode, as user is responsible for calling update.
        if not self.manual_mode:
            self.__tick(start_time)

    def __server_loop(self) -> None:
        """
        Internal method that handles the server loop.
        """
        while not self.__stop_flag:
            self.update()

    def __tick(self, start_time: float) -> None:
        """
        Attempts to keep the server running at a constant tick rate.
        """
        elapsed_time = time.time() - start_time
        sleep_time = 1 / self.tick_rate - elapsed_time
        if sleep_time > 0:
            time.sleep(sleep_time)

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

    def set_connection_callback(self, callback) -> None:
        """
        Sets the callback to be invoked when a client connects to the server.
        """
        self.__on_connection_callback = callback

    def set_message_callback(self, callback) -> None:
        """
        Sets the callback to be invoked when a message is received from a client.
        """
        self.__on_message_callback = callback

    def set_disconnect_callback(self, callback) -> None:
        """
        Sets the callback to be invoked when a client disconnects from the server.
        """
        self.__on_disconnect_callback = callback

    def __on_connection(self, client: ClientConnection) -> None:
        """
        Internal method that handles the connection of a client.
        Will store the connection in a list and invoke event.
        """
        self.__clients.append(client)
        self.__on_connection_callback(client)

    def __on_message(self, message: NetworkMessage, client: ClientConnection) -> None:
        """
        Internal method that handles the message of a client.
        Will invoke event.
        """
        self.__on_message_callback(message, client)

    def __on_disconnect(self, client: ClientConnection) -> None:
        """
        Internal method that handles the disconnection of a client.
        Will remove the connection from the list and invoke event.
        """
        self.__clients.remove(client)
        self.__on_disconnect_callback(client)
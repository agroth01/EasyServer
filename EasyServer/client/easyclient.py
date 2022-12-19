import socket
import time

class EasyClient:
    def __init__(self, host, port) -> None:
        self.host = host
        self.port = port
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setblocking(0)

    def connect(self) -> None:
        """
        Connects to the server.
        """
        self.socket.connect((self.host, self.port))

    def send_message(self, message) -> None:
        """
        Sends a message to the server.
        """
        self.socket.send(message.encode())

    def read_message(self) -> str:
        """
        Reads a message from the server. Will return None
        if no message is available at the time of calling.
        """
        return self.socket.recv(1024).decode()

    def wait_for_message(self, timeout=0) -> str:
        """
        Reads a message from the server. 
        Will block thread until a message is received.
        Has optional timeout parameter before returning None.
        """
        start_time = time.time()
        while True:
            message = self.read_message()
            if message:
                return message
            else:
                if timeout == 0:
                    continue

                elapsed_time = time.time() - start_time
                if elapsed_time > timeout:
                    break
        return None
        
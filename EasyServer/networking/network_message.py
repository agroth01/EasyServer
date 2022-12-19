class NetworkMessage:
    def __init__(self) -> None:
        self.headers = {}
        self.body = None

    def add_header(self, name, value) -> None:
        """
        Adds a header to the message. Headers are key-value pairs that can be used to send additional information
        with and about the message.
        """
        self.headers[name] = value

    def set_body(self, body) -> None:
        """
        Sets the body of the message. The body is the actual content of the message.
        """
        self.body = body
class TypeSerializer:
    """
    A class that serializes and deserializes objects of a certain type.
    """  
    def __init__(self, type):
        self.type = type

    def serialize(self, obj):
        """
        Serializes an object of the type this serializer is for.
        """
        raise NotImplementedError

    def deserialize(self, obj):
        """
        Deserializes an object of the type this serializer is for.
        """
        raise NotImplementedError
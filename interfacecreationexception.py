class InterfaceCreationException(Exception):
    def __init__(self, message):
        super().__init__("Error adding interface to virtual machine", message)
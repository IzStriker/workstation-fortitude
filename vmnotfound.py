class VMNotFound(Exception):
    def __init__(self, name):
        self.message = f"Virtual machine {name} not found"
        super().__init__(self.message)
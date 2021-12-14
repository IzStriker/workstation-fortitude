class OptionNotFound(Exception):
    def __init__(self, option):
        self.message = f"option {option} not found"
        super().__init__(self.message)
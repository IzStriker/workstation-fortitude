class NoInterfacesRequired(Exception):
    def __init__(self):
        super().__init__("All required interfaces already exist")
class AppConfig:
    def __init__(self):
        self.apiType: str = None
        self.apiKey: str = None
        self.databaseDriver: str = None
        self.databaseName: str = None
        self.databaseAddress: str = None
        self.databasePort: int = None
        self.databaseLogin: str = None
        self.databasePassword: str = None

    def getApiKey(self):
        return self.apiKey

    def setApiKey(self, key):
        self.apiKey = key

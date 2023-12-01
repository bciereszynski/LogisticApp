class AppConfig:
    def __init__(self):
        self.apiKey: str = None
        self.databaseDriver: str = None
        self.databaseName: str = None
        self.databaseAddress: str = None
        self.databasePort: int = None
        self.databaseLogin: str = None
        self.databasePassword: str = None
        self.mailLogin: str = None
        self.mailPassword: str = None

    def getApiKey(self):
        return self.apiKey

    def setApiKey(self, key):
        self.apiKey = key

    def ConnectionString(self):
        return (self.databaseDriver + "://" + self.databaseLogin + ":" + self.databasePassword + "@" +
                self.databaseAddress + ":" + self.databasePort + "/" + self.databaseName)

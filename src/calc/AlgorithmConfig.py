class AlgorithmConfig:
    def __init__(self):
        self.MaxLocalLoops = 10
        self.TSP: bool = True
        self.Insert: bool = True
        self.Replace: bool = True
        self.Disrupt: bool = False
        self.DisruptPercent = 0.1
        self.MaxAlgLoops = 4

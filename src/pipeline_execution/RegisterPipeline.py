class RegisterPipeline:

    def __init__(self, stretapa: str):
        self.name = stretapa
        self.IF_ID = False
        self.ID_EX = False
        self.EX_MEM = False
        self.MEM_WB = False
        self.instruction = None

        if stretapa.upper() == "IF_ID":
            self.IF_ID = True
        elif stretapa.upper() == "ID_EX":
            self.ID_EX = True
        elif stretapa.upper() == "EX_MEM":
            self.EX_MEM = True
        elif stretapa.upper() == "MEM_WB":
            self.MEM_WB = True

    def __str__(self):
        return self.name + " " + self.instruction.str

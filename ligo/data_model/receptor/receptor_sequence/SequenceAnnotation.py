# quality: gold

class SequenceAnnotation:
    """
    Sequence Annotation class includes antigen-specific data (in experimental
    scenario) and implanted signals (in simulated scenario)
    """
    def __init__(self, implants: list = None, other: dict = None):
        self.implants = implants if implants is not None else []
        self.other = other if other is not None else {}

    def add_implant(self, implant):
        self.implants.append(implant)

    def __str__(self):
        return str([str(implant) for implant in self.implants])

    def __repr__(self):
        return f"SequenceAnnotation(implants={self.implants})"

"""
Custom defined exceptions.
"""

class TraceabilityError(Exception):
    """
    Exception raise if there are errors in communicating with traceability system.
    """

    def __init__(self, message="An error in communicating with the traceability system."):
        """
        Raise a traceability communication error.
        """
        self.message = message
        super().__init__(self.message)

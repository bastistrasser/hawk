class HawkException(Exception):
    """
    Generic exception thrown to indicate an error occurred in the 
    application
    """
    def __init__(self, message):
        """
        :param message: The message indicating what kind of error occurred
        """
        super().__init__(str(message))

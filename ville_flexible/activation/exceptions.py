class StrategyNotCoveringRequestedVolumeException(Exception):
    """Raised when a strategy fails to select assets covering the requested volume."""

    MESSAGE = "Selected strategy does not cover the requested volume."

    def __init__(self):
        super().__init__(self.MESSAGE)

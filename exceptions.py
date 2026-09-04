class AppError(Exception):
    """Base class for application exceptions."""
    pass

class InvalidCommandError(AppError):
    pass

class DataNotLoadedError(AppError):
    pass

class InvalidAttributeError(AppError):
    pass
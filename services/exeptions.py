class TaskNotFoundError(Exception):
    """Exception raised when a task is not found."""
    def __init__(self, message="Task not found"):
        self.message = message
        super().__init__(self.message)


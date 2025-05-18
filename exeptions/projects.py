class ProjectNotFoundError(Exception):
    """Exception raised when a task is not found."""

    def __init__(self, project_id: int):
        self.project_id = project_id
        super().__init__(f"Project with ID {project_id} not found")


class ProjectPermissionError(Exception):
    """Exception raised when a task is not found."""

    def __init__(self, project_id: int):
        self.project_id = project_id
        super().__init__(f"Project with ID {project_id} permission error")

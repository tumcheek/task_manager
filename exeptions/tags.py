class TagNotFoundError(Exception):
    """Exception raised when a tag is not found."""

    def __init__(self, tag_id: int):
        self.tag_id = tag_id
        super().__init__(f"Tag with ID {tag_id} not found")


class TagAlreadyExistsError(Exception):
    """Exception raised when a tag is already exists."""


class TagNotAssociatedError(Exception):
    def __init__(self, task_id, tag_id):
        self.tag_id = tag_id
        self.task_id = task_id
        super().__init__(
            f"Tag with ID {tag_id} is not associated with task with ID {task_id}"
        )

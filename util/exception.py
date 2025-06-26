class TaskManagerException(Exception):
    """base exception for the task manager """
    pass

class InvalidInputError(TaskManagerException):
    """Raised when the user input is invalid
    It should allow for chaining of the original exception (e.g., ValueError)"""
    def __init__(self, message="Invalid input provided.", original_exception=None):
        super().__init__(message)
        self.original_exception = original_exception

class ValidationError(TaskManagerException):
    """Raised when certain validation rules are failed"""
    def __init__(self, message="Validation failed.", field=None, value=None):
        super().__init__(message)
        self.field = field
        self.value = value

class TaskNotFoundException(TaskManagerException):
    """Raised when the requied task is not found"""
    def __init__(self, message="Task not found",task_id=None):
        super().__init__(message)
        self.task_id=task_id

class UserNotFoundException(TaskManagerException):
    """Raised when the requied user is not found"""
    def __init__(self, message="User not found",user_id=None):
        super().__init__(message)
        self.user_id=user_id

class DuplicateTaskException(TaskManagerException):
    """Raised when the task with the task id already exists"""
    def __init__(self, message="Task already exists",task_id=None):
        super().__init__(message)
        self.task_id=task_id

class DuplicateUserException(TaskManagerException):
    """Raised when another user with the same id exists"""
    def __init__(self, message="User already exists",user_id=None):
        super().__init__(message)
        self.user_id=user_id

class EmptyTaskListException(TaskManagerException):
    """Raised when task list is to be displayed but the list is empty"""
    def __init__(self, message="No Task"):
        super().__init__(message)
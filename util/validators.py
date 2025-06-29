from util.exception import ValidationError
from datetime import datetime

    
def validate_priority(priority):
    """Validates the priority level of a task.
        Args:
            priority (str): The priority to be validated. Expected values: "Low", "Medium", "High".
        Returns:
            str: The validated priority.
        Raises:
            ValidationError: If the priority is not one of the expected values.
        """
    if not priority:
         raise ValidationError("Priority can't be empty",field="priority",value=priority)
    priority = priority.strip().lower()
    valid_priorities = {
        "low": "Low",
        "medium": "Medium",
        "high": "High"
    }
    if priority not in valid_priorities:
        raise ValidationError("Invalid Priority", field="priority", value=priority)
    return valid_priorities[priority]
    
def validate_status(status):
    """Validates the status of a task.
    Args:
        status (str): The status to be validated. Expected values: "To Do", "In Progress", "Done".
    Returns:
        str: The validated status.
    Raises:
        ValidationError: If the status does not match any of the expected task statuses.
    """
    if not status:
         raise ValidationError("Status can't be empty",field="status",value=status)
    status = status.strip().lower()
    valid_statuses = {
        "to do": "To Do",
        "in progress": "In Progress",
        "done": "Done"
    }
    if status not in valid_statuses:
        raise ValidationError("Invalid Status", field="status", value=status)
    return valid_statuses[status]


def validate_title(title):
    """Ensures the title of task or name of user is not empty or just whitespace.
    Args:
        title (str): The title to be validated.
    Returns:
        str: The validated title.
    Raises:
        ValidationError: If the title is missing or not a valid non-empty string.
    """
    if not title or title.strip() == "":
        raise ValidationError("Title cannot be empty", field="title", value=title)
    if not isinstance(title,str):
        raise ValidationError("Should be a String",field="title",value=title)
    return True


def validate_due_date(due_date):
    """Validates the due date format for a task.
        Args:
            due_date (str): The due date to be validated in "dd-mm-yyyy" format.
        Returns:
            datetime.date: The parsed and validated due date.
        Raises:
            ValidationError: If the date is not in the correct format or not a valid date.
        """
    if not due_date:
        raise ValidationError("Due date cannot be empty", field="due_date", value=due_date)
    try:
        date = datetime.strptime(due_date, "%Y-%m-%d").date()
        today = datetime.today().date()
        if date < today:
            raise ValidationError("Due date cannot be in the past", field="due_date", value=due_date)
        return date
    except ValueError:
        raise ValidationError("Due date must be in yyyy-mm-dd format", field="due_date", value=due_date)
    



    
    


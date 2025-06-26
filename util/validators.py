from util.exception import ValidationError
from datetime import datetime

def validate_task_id(task_id):
    """Ensures that the task id is not empty and contains only numbers."""
    if not task_id:
        raise ValidationError("Task ID can't be empty",field="task_id",value=task_id)
    if not isinstance(task_id,int):
        raise ValidationError("Invalid Task ID",field="task_id",value=task_id)
    return True
    
def validate_user_id(user_id):
    """Ensures that the user id is not empty and contains only numbers."""
    if not user_id:
        raise ValidationError("User_id can't be empty")
    if not isinstance(user_id,int):
        raise ValidationError("Invalid User ID",field="user_id",value=user_id)
    return True
    
def validate_priority(priority):
    """Ensures that task priority is within accepted values.
       Checks: Must be "low", "medium", or "high" (case insensitive)"""
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
    """Purpose: Validates the task status value.
    Checks: Must be "To Do", "In Progress", or "Done" (case sensitive or can convert)"""
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
    """
    Ensures the title of task or name of user is not empty or just whitespace.
    """
    if not title or title.strip() == "":
        raise ValidationError("Title cannot be empty", field="title", value=title)
    if not isinstance(title,str):
        raise ValidationError("Should be a String",field="title",value=title)
    return True


def validate_due_date(due_date):
    """ Validates that the due date is in the format YYYY-MM-DD.
    Raises error if due date is :
    1)empty 
    2)is in wrong format 
    3)is date is before today  """
    if not due_date:
        raise ValidationError("Due date cannot be empty", field="due_date", value=due_date)
    try:
        date = datetime.strptime(due_date, "%d-%m-%Y").date()
        today = datetime.today().date()
        if date < today:
            raise ValidationError("Due date cannot be in the past", field="due_date", value=due_date)
        return date
    except ValueError:
        raise ValidationError("Due date must be in DD-MM-YYYY format", field="due_date", value=due_date)
    



    
    


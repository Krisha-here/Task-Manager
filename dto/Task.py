class Task:
    """Represents a Task object retrieved from the database."""

    def __init__(self, task_id, title, description, priority, due_date, status, assigned_to):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.status = status
        self.assigned_to = assigned_to  

    def update_status(self, new_status):
        """
        Updates the status of the task.
        """
        self.status = new_status

    def update_priority(self, new_priority):
        """
        Updates the priority of the task.
        """
        self.priority = new_priority

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "due_date": str(self.due_date),
            "status": self.status,
            "assigned_to": self.assigned_to
        }


    def display_info(self):
        """Displays the details of the task."""
        print("\n--- TASK ---")
        print(f"Task ID     : {self.task_id}")
        print(f"Title       : {self.title}")
        print(f"Description : {self.description}")
        print(f"Priority    : {self.priority}")
        print(f"Due Date    : {self.due_date}")
        print(f"Status      : {self.status}")
        if self.assigned_to:
            print(f"Assigned To : User ID:{self.assigned_to}")
        else:
            print("Assigned To : Not assigned")

    
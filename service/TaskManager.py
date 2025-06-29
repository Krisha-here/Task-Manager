from dto.Task import Task
from util.db import get_connection
from util.exception import (InvalidInputError,ValidationError,TaskNotFoundException,
                            UserNotFoundException,EmptyTaskListException)
from util.validators import validate_priority,validate_due_date,validate_status,validate_title


class TaskManager:
    def __init__(self):
        print("TaskManager initialized")
       
    def create_task(self,data):
        """Creates a new task using provided JSON data.

        Validates input fields (title, description, priority, due_date, status, assigned_to),
        inserts the task into the database, and returns a confirmation message.

        Expects:
            data (dict): Dictionary containing task details.
        Returns:
            dict: Confirmation message on successful task creation.
        Raises:
            InvalidInputError: If 'assigned_to' is not an integer.
            ValidationError: If required fields are missing or invalid.
        """
        print("Received Data:", data)
        title=data.get("title")
        description=data.get("description") 
        priority=data.get("priority")
        priority=validate_priority(priority)
        due_date=data.get("due_date")
        due_date=validate_due_date(due_date)
        status=data.get("status")
        assigned_to = data.get("assigned_to")
        if assigned_to is not None:
            try:
                assigned_to = int(assigned_to)
            except ValueError:
                raise InvalidInputError("Assigned_to must be an integer", field="assigned_to", value=assigned_to)
        status=validate_status(status)
        if not(validate_title(title)):
            raise ValidationError("One or more validation Failed")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Task(title, description, priority, due_date, status, assigned_to)VALUES (%s, %s, %s, %s, %s, %s)", (title, description, priority, due_date, status, assigned_to))
        conn.commit()
        print("Task inserted into DB")
        conn.close()

        return {"message": "Task created successfully"}
    
    def update_task_status(self, task_id, new_status):
        """Updates the status of a task with the provided task_id.
        Args:
            task_id (int): ID of the task to update.
            new_status (str): New status to set ('To Do', 'In Progress', 'Done').
        Returns:
            None
        Raises:
            Exception: If database operations fail.
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE Task SET status = %s WHERE task_id = %s", (new_status, task_id))
            conn.commit()
        except Exception as e:
            print("Error:", e)
        finally:
            cursor.close()
            conn.close()

    def update_task_priority(self, task_id, new_priority):
        """Updates the priority of a task with the provided task_id.
        Args:
            task_id (int): ID of the task to update.
            new_priority (str): New priority to set ('Low', 'Medium', 'High').
        Returns:
            None
        Raises:
            Exception: If database operations fail.
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE Task SET priority = %s WHERE task_id = %s", (new_priority, task_id))
            conn.commit()
        except Exception as e:
            print("Error:", e)
        finally:
            cursor.close()
            conn.close()


    def delete_task(self,task_id):
        """Deletes the task with the specified task_id from the database.
        Args:
            task_id (int): ID of the task to delete.
        Returns:
            dict: Confirmation message upon successful deletion.
        Raises:
            TaskNotFoundException: If the task does not exist in the database.
        """
        conn=get_connection()
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM Task WHERE task_id = %s",(task_id,))
        if not cursor.fetchone():
            conn.close()
            raise TaskNotFoundException(f"Task with ID {task_id} doesn't exists",task_id=task_id)
        cursor.execute("DELETE FROM Task WHERE task_id = %s",(task_id,))
        conn.commit()
        conn.close()
        return {"message": f"Task with ID {task_id} deleted successfully"}
            
    def get_task(self,task_id):
        """Retrieves the details of the task with the specified task_id.
        Args:
            task_id (int): ID of the task to retrieve.
        Returns:
            dict: Dictionary containing task details.
        Raises:
            TaskNotFoundException: If the task does not exist in the database.
        """
        conn=get_connection()
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM Task WHERE task_id = %s",(task_id,))
        row=cursor.fetchone()
        conn.close()
        if not row:
            raise TaskNotFoundException(f"Task with ID {task_id} doesn't exists",task_id=task_id)
        task=Task(*row)
        return task.to_dict()
        

    def list_all_tasks(self):
        """Retrieves all tasks from the database.
        Returns:
            dict: A dictionary containing a list of all tasks.
        Raises:
            EmptyTaskListException: If no tasks are found in the database.
        """
        conn=get_connection()
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM Task ")
        tasks=cursor.fetchall()
        conn.close()
        if not tasks:
            raise EmptyTaskListException("NO TASKS AVAILABLE")
        task_list=[]
        for row in tasks:
            task=Task(*row)
            task_list.append(task.to_dict())
        return {"tasks":task_list}

    def list_tasks_by_user(self,user_id):
        """Retrieves all tasks assigned to a specific user.
        Args:
            user_id (int): ID of the user whose tasks need to be retrieved.
        Returns:
            dict: A dictionary containing a list of tasks assigned to the user,
                  or a message if no tasks are assigned.
        Raises:
            UserNotFoundException: If the specified user does not exist.
        """
        conn=get_connection()
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM User WHERE user_id = %s",(user_id,))
        user=cursor.fetchone()
        if not user:
            conn.close()
            raise UserNotFoundException(f"User with ID {user_id} doesn't exists",user_id=user_id)
        cursor.execute("SELECT * FROM Task WHERE assigned_to = %s",(user_id,))
        tasks=cursor.fetchall()
        conn.close()
        if not tasks:
            return{"message":"No Task assigned to the user"}  
        task_list=[] 
        for row in tasks:
            task=Task(*row)
            task_list.append(task.to_dict())
        return {"tasks":task_list}

            

    def list_tasks_by_status(self, status):
        """Retrieves all tasks with the specified status.
        Args:
            status (str): The status to filter tasks by ('To Do', 'In Progress', 'Done').
        Returns:
            dict: A dictionary containing a list of tasks matching the status,
                  or a message if no tasks are found.
        Raises:
            ValidationError: If the status provided is invalid.
        """
        status = (validate_status(status)).strip() #Raises ValidationError incase of invalid status
        print(f"Validated status: '{status}'")
        conn=get_connection()
        print("Connected to:", conn.get_server_info())
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM Task WHERE status = %s",(status,))
        tasks=cursor.fetchall()
        conn.close()
        if not tasks:
            return{"error":"No tasks found with status"}
        else:    
            task_list=[] 
            for row in tasks:
                task=Task(*row)
                task_list.append(task.to_dict())
            return {"tasks":task_list}
            


    def create_user(self,data):
        """Creates a new user using provided JSON data.
        Validates the provided name and email, inserts the user into the database,
        and returns a confirmation message.
        Expects:
            data (dict): Dictionary containing user details ('name', 'email').
        Returns:
            dict: Confirmation message on successful user creation.
        Raises:
            ValidationError: If the provided name is invalid.
        """

        name=data.get("name")
        email=data.get("email")
        if not validate_title(name):
            raise ValidationError("One or more Validation Error")
        conn=get_connection()
        cursor=conn.cursor()
        cursor.execute("INSERT INTO User(name, email) VALUES(%s,%s)",(name,email))#creating new users
        conn.commit()
        conn.close()
        return{"message":"User created successfully"}

    def assign_task_to_user(self, task_id, user_id):
        """Assigns a task to a user in the database.
        Args:
            task_id (int): ID of the task to be assigned.
            user_id (int): ID of the user to whom the task will be assigned.
        Returns:
            dict: Confirmation message on successful assignment.
        Raises:
            TaskNotFoundException: If the specified task does not exist.
            UserNotFoundException: If the specified user does not exist.
        """
        conn=get_connection()
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM Task WHERE task_id = %s",(task_id,))
        if not cursor.fetchone():
            raise TaskNotFoundException(f"Task with ID {task_id} doesn't exists",task_id=task_id)
        cursor.execute("SELECT * FROM User WHERE user_id = %s",(user_id,))
        if not cursor.fetchone():
            raise UserNotFoundException(f"User with ID {user_id} doesn't exists",user_id=user_id)
        cursor.execute("UPDATE Task SET assigned_to = %s WHERE task_id = %s",(user_id,task_id))
        conn.commit()
        conn.close()
        return{"message":"Assigned successfully"}
        



from dto.Task import Task
from util.db import get_connection
from util.exception import (InvalidInputError,DuplicateTaskException,DuplicateUserException,ValidationError,TaskNotFoundException,
                            UserNotFoundException,EmptyTaskListException)
from util.validators import validate_task_id,validate_user_id,validate_priority,validate_due_date,validate_status,validate_title
from datetime import datetime

class TaskManager:
    def __init__(self):
        print("TaskManager initialized")
       
    def create_task(self,data):
        """Creates a new task from JSON data (Flask version).
         Validates and inserts into the database.
        Raises:
        - InvalidInputError
        - ValidationError
        - DuplicateTaskException
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
                raise ValidationError("Assigned_to must be an integer", field="assigned_to", value=assigned_to)
            validate_user_id(assigned_to)
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
        """
        Updates the status of a specific task.
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE tasks SET status = %s WHERE task_id = %s", (new_status, task_id))
            conn.commit()
        except Exception as e:
            print("Error:", e)
        finally:
            cursor.close()
            conn.close()

    def update_task_priority(self, task_id, new_priority):
        """
        Updates the priority of a specific task.
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE tasks SET priority = %s WHERE task_id = %s", (new_priority, task_id))
            conn.commit()
        except Exception as e:
            print("Error:", e)
        finally:
            cursor.close()
            conn.close()


    def delete_task(self,task_id):
        """Deletes the task with the given task_id.
        Raises TaskNotFoundException if the Task does not exist.
        Raises ValidationError if the Task ID is not valid"""
        validate_task_id(task_id) #raises ValidationError incase of invalid task id
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
        """Gets details of the task of specified task id
        Raises Validation error if task id is invalid
        Raises TaskNotFoundException if task is not found"""
        validate_task_id(task_id)
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
        """Gets details of the all task 
        Raises EmptyTaskListException if no tasks are found"""
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
        """Lists all tasks assigned to a User
        Raises UserNotFoundException if User doesn't exist"""
        validate_user_id(user_id)
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
        """Lists all the task with the given status
        Raises ValidationError if status is invalid"""
        status = validate_status(status) #Raises ValidationError incase of invalid status
        conn=get_connection()
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM Task WHERE status = %s",(status,))
        tasks=cursor.fetchall()
        conn.close()
        if not tasks:
            return{"message":"No tasks found with status"}
        else:    
            task_list=[] 
            for row in tasks:
                task=Task(*row)
                task_list.append(task.to_dict())
            return {"tasks":task_list}
            


    def create_user(self,data):
        """Creates new users.
        Validates user_id and name
        Raises ValidationError if validation fails
        Raises InvalidInputError if User ID id non numeric
        Raises DuplicateUserException if User ID already exists"""
        try:
            user_id=int(data.get("user_id"))
        except ValueError as e:
            raise InvalidInputError("User id must be integer",original_exception=e) from e
        else:
            name=data.get("name")
            email=data.get("email")
            if not (validate_user_id(user_id) and validate_title(name)):
                raise ValidationError("One or more Validation Error")
            conn=get_connection()
            cursor=conn.cursor()
            cursor.execute("SELECT * FROM User WHERE user_id = %s",(user_id,))#check for duplicate
            if cursor.fetchone():
                raise DuplicateUserException(f"User with ID {user_id} already exists")
            cursor.execute("INSERT INTO User(name, email) VALUES(%s,%s)",(name,email))#creating new users
            conn.commit()
            conn.close()
            return{"message":"User created successfully"}

    def assign_task_to_user(self, task_id, user_id):
        """Assigns the task to an user
        Checks if User ID and Task ID exists
        Raises Validation error if task_id or user_id is invalid
        Raises TaskNotFoundException if task id doesn't exist
        Raises UserNotFoundExcpetion if user id doesn't exist"""
        validate_task_id(task_id)
        validate_user_id(user_id)
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
        



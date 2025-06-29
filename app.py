from flask import Flask , request , jsonify
from service.TaskManager import TaskManager
from util.exception import ValidationError,InvalidInputError,TaskNotFoundException,EmptyTaskListException,UserNotFoundException
from flask_cors import CORS


app = Flask(__name__)
CORS(app)  # ← This line enables CORS

task_manager=TaskManager()

@app.route("/")
def home():
    return  "Task Management API is running"

@app.route('/tasks', methods=["POST"])
def create():
    """Creates a new task using the data provided in the request JSON.
    Expects:
        JSON:
            title (str): Title of the task.
            description (str): Description of the task.
            priority (str): Priority of the task ('Low', 'Medium', 'High').
            due_date (str): Due date of the task (YYYY-MM-DD).
            status (str): Status of the task ('To Do', 'In Progress', 'Done').
            assigned_to (int, optional): User ID to assign the task to.
    Returns:
        JSON: The created task details with task_id and provided data.
    Raises:
        InvalidInputError: If input validation fails.
        ValidationError: If required fields are missing or invalid.
    """
    try:
        data = request.json
        result = task_manager.create_task(data)
        return jsonify(result), 201
    except (InvalidInputError, ValidationError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error occurred: {str(e)}"}) , 500
    
    
@app.route('/tasks/<int:task_id>',methods=["DELETE"])
def delete(task_id):
    """Deletes a task based on the provided task_id.
    Args:
        task_id (int): The ID of the task to be deleted.
    Returns:
        JSON: Confirmation message on successful deletion.
    Raises:
        ValidationError: If task_id validation fails.
        TaskNotFoundException: If the task does not exist.
    """
    try:
        result=task_manager.delete_task(task_id)
        return jsonify(result),200
    except (ValidationError,TaskNotFoundException) as e:
        return jsonify({"error": str(e)}),400
    
@app.route("/tasks/<int:task_id>",methods=["GET"])
def get_task(task_id):
    """Retrieves the details of a specific task based on task_id.
    Args:
        task_id (int): The ID of the task to retrieve.
    Returns:
        JSON: Task details including task_id, title, description, etc.
    Raises:
        ValidationError: If task_id validation fails.
        TaskNotFoundException: If the task does not exist.
    """
    try:
        result=task_manager.get_task(task_id)
        return jsonify(result),200
    except (ValidationError,TaskNotFoundException) as e:
        return {"error": str(e)},400
    
@app.route("/tasks", methods=["GET"])
def get_all_task():
    """Retrieves all tasks stored in the database.
    Returns:
        JSON: A list of all tasks with their details.
    Raises:
        EmptyTaskListException: If no tasks are found in the database.
    """
    try:
        result = task_manager.list_all_tasks()
        return jsonify (result),200
    except EmptyTaskListException as e:
        return {"error": str(e)},400
    except Exception as e:
        return jsonify({"error": "Unexpected error occurred"}),500
    
@app.route("/users/<int:user_id>",methods=["GET"])
def get_task_by_user(user_id):
    """Retrieves all tasks assigned to a specific user.
    Args:
        user_id (int): The ID of the user whose tasks are to be retrieved.
    Returns:
        JSON: List of tasks assigned to the specified user.
    Raises:
        ValidationError: If user_id validation fails.
        UserNotFoundException: If the user does not exist.
    """
    try:
        result=task_manager.list_tasks_by_user(user_id)
        return jsonify(result),200
    except (ValidationError,UserNotFoundException) as e:
        return jsonify({"error": str(e)}),400

@app.route("/tasks/status/<string:status>", methods=["GET"])
def get_task_by_status(status):
    """Retrieves all tasks that match the specified status.
    Args:
        status (str): The status to filter tasks by ('To Do', 'In Progress', 'Done').
    Returns:
        JSON: List of tasks with the specified status.
    Raises:
        ValidationError: If the status value is invalid.
    """
    try:
        result=task_manager.list_tasks_by_status(status)
        return jsonify(result),200
    except ValidationError as e:
        return jsonify(f"Error: {str(e)}"),400

@app.route("/users", methods=["POST"])
def create_user():
    """Creates a new user using the data provided in the request JSON.
    Expects:
        JSON:
            name (str): The name of the user.
            email (str): The email address of the user.
    Returns:
        JSON: Details of the newly created user, including user_id.
    Raises:
        ValidationError: If required fields are missing or invalid.
        InvalidInputError: If input types are incorrect.
    """
    try:
        data = request.json
        result = task_manager.create_user(data)
        return jsonify(result),201
    except (ValidationError, InvalidInputError) as e:
        return jsonify({"error": str(e)}),400
    
@app.route("/users/<int:user_id>/tasks/<int:task_id>", methods=["POST"])
def assign(task_id,user_id):
    """Assigns an existing task to a specified user.
    Args:
        task_id (int): The ID of the task to assign.
        user_id (int): The ID of the user to assign the task to.
    Returns:
        JSON: Confirmation message upon successful assignment.
    Raises:
        ValidationError: If input validation fails.
        UserNotFoundException: If the user does not exist.
        TaskNotFoundException: If the task does not exist.
    """
    try:
        result=task_manager.assign_task_to_user(task_id,user_id)
        return jsonify(result),200
    except (ValidationError,UserNotFoundException,TaskNotFoundException) as e:
        return jsonify({"error": str(e)}),400

@app.route('/tasks/<int:task_id>/status', methods=['PUT'])
def update_status(task_id):
    """Updates the status of a specific task.
    Args:
        task_id (int): The ID of the task whose status is to be updated.
    Expects:
        JSON:
            status (str): The new status ('To Do', 'In Progress', 'Done').
    Returns:
        JSON: Confirmation message upon successful update.
    Raises:
        ValueError: If the provided status is invalid.
    """
    data = request.json

    try:
        new_status = data['status'].strip().title()
        if new_status not in ["To Do", "In Progress", "Done"]:
            raise ValueError("Invalid status.")
        task_manager.update_task_status(task_id, new_status)
        return jsonify({"message": "Status updated"}),200
    except Exception as e:
        return jsonify({"error": str(e)}),500

@app.route('/tasks/<int:task_id>/priority', methods=['PUT'])
def update_priority(task_id):
    """Updates the priority of a specific task.
    Args:
        task_id (int): The ID of the task whose priority is to be updated.
    Expects:
        JSON:
            priority (str): The new priority ('Low', 'Medium', 'High').
    Returns:
        JSON: Confirmation message upon successful update.
    Raises:
        ValueError: If the provided priority is invalid.
    """
    data = request.json
    print("Received data:", data, "Task ID:", task_id)
    try:
        new_priority = data['priority'].strip().capitalize()
        if new_priority not in ["Low", "Medium", "High"]:
            raise ValueError("Invalid priority.")
        task_manager.update_task_priority(task_id, new_priority)
        return jsonify({"message": "Priority updated"}),200
    except Exception as e:
        return jsonify({"error": str(e)}),500

    

if __name__ == "__main__":
    print("TaskManager initialized")
    app.run(debug=True)
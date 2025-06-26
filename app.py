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
    try:
        data = request.json
        print("Received JSON:", data)  
        result = task_manager.create_task(data)
        return jsonify(result), 201
    except (InvalidInputError, ValidationError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Unexpected error occurred: {str(e)}"}) , 500
    
    
@app.route('/tasks/<int:task_id>',methods=["DELETE"])
def delete(task_id):
    """Calls delete_task() to delete task from the database
       Handles ValidationError and TaskNotFoundException if function raises it"""
    try:
        result=task_manager.delete_task(task_id)
        return jsonify(result)
    except (ValidationError,TaskNotFoundException) as e:
        return jsonify({"error": str(e)})
    
@app.route("/tasks/<int:task_id>",methods=["GET"])
def get_task(task_id):
    """Retrieves a task from database based in task id
    Handles ValidationError and TaskNotFoundException if raised"""
    try:
        result=task_manager.get_task(task_id)
        return jsonify(result)
    except (ValidationError,TaskNotFoundException) as e:
        return {"error": str(e)}
    
@app.route("/tasks", methods=["GET"])
def get_all_task():
    """Retrieves all the task from database
    Handles EmptyTaskListException if raised"""
    try:
        result = task_manager.list_all_tasks()
        return jsonify (result)
    except EmptyTaskListException as e:
        return {"error": str(e)}
    except Exception as e:
        return jsonify({"error": "Unexpected error occurred"})
    
@app.route("/users/<int:user_id>",methods=["GET"])
def get_task_by_user(user_id):
    """Retrives all tasks assigned to an user
       Handles ValidationError and UserNotFoundException if raised"""
    try:
        result=task_manager.list_tasks_by_user(user_id)
        return jsonify(result)
    except (ValidationError,UserNotFoundException) as e:
        return jsonify({"error": str(e)})

@app.route("/tasks/status/<string:status>", methods=["GET"])
def get_task_by_status(status):
    """Retrives all tasks of specified status
       Handles ValidationError if raised"""
    try:
        result=task_manager.list_tasks_by_status(status)
        return jsonify(result)
    except ValidationError as e:
        return jsonify(f"Error: {str(e)}")

@app.route("/users", methods=["POST"])
def create_user():
    """Used to create new users
       Handles ValidationError, DuplicateUserException and InvalidInputError if raised """
    try:
        data = request.json
        result = task_manager.create_user(data)
        return jsonify(result)
    except (ValidationError, InvalidInputError) as e:
        return jsonify({"error": str(e)})
    
@app.route("/users/<int:user_id>/tasks/<int:task_id>", methods=["POST"])
def assign(task_id,user_id):
    """Assigns the task to user
   Handles ValidationError, UserNotFoundException, and TaskNotFoundException
   """
    try:
        result=task_manager.assign_task_to_user(task_id,user_id)
        return jsonify(result)
    except (ValidationError,UserNotFoundException,TaskNotFoundException) as e:
        return jsonify({"error": str(e)})

@app.route('/tasks/<int:task_id>/status', methods=['PUT'])
def update_status(task_id):
    data = request.json
    try:
        new_status = data['status'].strip().title()
        if new_status not in ["To Do", "In Progress", "Done"]:
            raise ValueError("Invalid status.")
        task_manager.update_task_status(task_id, new_status)
        return jsonify({"message": "Status updated"})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/tasks/<int:task_id>/priority', methods=['PUT'])
def update_priority(task_id):
    data = request.json
    try:
        new_priority = data['priority'].strip().capitalize()
        if new_priority not in ["Low", "Medium", "High"]:
            raise ValueError("Invalid priority.")
        task_manager.update_task_priority(task_id, new_priority)
        return jsonify({"message": "Priority updated"})
    except Exception as e:
        return jsonify({"error": str(e)})

    

if __name__ == "__main__":
    print("TaskManager initialized")
    app.run(debug=True)
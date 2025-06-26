from flask import Flask , request , jsonify
from service.TaskManager import TaskManager
from util.exception import ValidationError,InvalidInputError,DuplicateTaskException,DuplicateUserException,TaskNotFoundException,EmptyTaskListException,UserNotFoundException

app = Flask(__name__)
task_manager=TaskManager()

@app.route('/task/create',methods=["POST"])
def create():
    try:
        data=request.json
        result=task_manager.create_task(data)
        return jsonify(result)
    except (InvalidInputError, ValidationError, DuplicateTaskException) as e:
        return ({"error": str(e)})
    except Exception as e:
        return ({"error": "An unexpected error occurred"})
    
@app.route('/task/delete/<int:task_id>',methods=["DELETE"])
def delete(task_id):
    try:
        result=task_manager.delete_task(task_id)
        return result
    except (ValidationError,TaskNotFoundException) as e:
        return {"error": str(e)}
    
@app.route("/task/get/<int:task_id>",methods=["GET"])
def get_task(task_id):
    try:
        result=task_manager.get_task(task_id)
        return result
    except (ValidationError,TaskNotFoundException) as e:
        return {"error": str(e)}
    
@app.route("/task/get/all", methods=["GET"])
def get_all_task():
    try:
        result = task_manager.list_all_tasks()
        return result
    except EmptyTaskListException as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": "Unexpected error occurred"}
    
@app.route("/user/<int:user_id>/tasks")
def get_task_by_user(user_id):
    try:
        result=task_manager.list_tasks_by_user(user_id)
        return result
    except (ValidationError,UserNotFoundException) as e:
        return {"error": str(e)}

@app.route("/task/status/<string:status>", methods=["GET"])
def get_task_by_status(status):
    try:
        result=task_manager.list_tasks_by_status(status)
        return result
    except ValidationError as e:
        print(f"Error: {str(e)}")

@app.route("/user/create", methods=["POST"])
def create_user():
    try:
        data = request.json
        result = task_manager.create_user(data)
        return result
    except (ValidationError, DuplicateUserException, InvalidInputError) as e:
        return {"error": str(e)}
    
@app.route("/assign/<int:task_id>/to/<int:user_id>", methods=["POST"])
def assign(task_id,user_id):
    try:
        result=task_manager.assign_task_to_user(task_id,user_id)
        return result
    except (ValidationError,UserNotFoundException,TaskNotFoundException) as e:
        return {"error": str(e)}
    

if __name__ == "__main__":
    print("TaskManager initialized")
    app.run(debug=True)
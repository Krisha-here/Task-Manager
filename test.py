import requests

BASE_URL = "http://127.0.0.1:5000"

# 1. Create a User
user_data = {
    "user_id": 101,
    "name": "Aaryatha",
    "email": "aaryatha@example.com"
}
print("\n Creating User:")
response = requests.post(f"{BASE_URL}/user/create", json=user_data)
print("Status Code:", response.status_code)
print("Response:", response.json())

# 2. Create a Task
task_data = {
    "task_id": 201,
    "title": "Complete Internship Task",
    "description": "Implement Flask API endpoints for Task Manager",
    "priority": "High",
    "due_date": "28-06-2025",
    "status": "To Do"
}
print("\n Creating Task:")
response = requests.post(f"{BASE_URL}/task/create", json=task_data)
print("Status Code:", response.status_code)
print("Response:", response.json())

# 3. Assign Task to User
print("\n Assigning Task to User:")
response = requests.post(f"{BASE_URL}/assign/201/to/101")
print("Status Code:", response.status_code)
print("Response:", response.json())

# 4. Get Task by ID
print("\n Getting Task by ID:")
response = requests.get(f"{BASE_URL}/task/get/201")
print("Status Code:", response.status_code)
print("Response:", response.json())

# 5. Get All Tasks
print("\n Getting All Tasks:")
response = requests.get(f"{BASE_URL}/task/get/all")
print("Status Code:", response.status_code)
print("Response:", response.json())

# 6. Get Tasks by User
print("\n Getting Tasks by User ID:")
response = requests.get(f"{BASE_URL}/user/101/tasks")
print("Status Code:", response.status_code)
print("Response:", response.json())

# 7. Get Tasks by Status
print("\n Getting Tasks by Status:")
response = requests.get(f"{BASE_URL}/task/get/pending")
print("Status Code:", response.status_code)
print("Response:", response.json())

# 8. Delete Task
print("\n Deleting Task:")
response = requests.delete(f"{BASE_URL}/task/delete/201")
print("Status Code:", response.status_code)
print("Response:", response.json())


#  Task Manager System (Python + Flask + MySQL)

A Task Management System built using Python, Flask, and integrated with a MySQL database. The system allows users to create, update, delete, assign, and view tasks with full validation and exception handling.

---

##  Features

- Create and manage users
- Create, assign, and delete tasks
- View tasks by user or status
- Validations for dates, input types, and duplicates
- Integrated with **MySQL** database
- Clear exception handling & custom error messages
- **Now includes RESTful API using Flask**

---

##  Project Structure

```
Task_Manager_System/
│
├── main/
│   └── main.py               # CLI entry point (optional)
│
├── app.py                    # Flask app with REST API endpoints
│
├── dto/
│   ├── Task.py               # Task class definition with to_dict()
│   └── User.py               # User class (minimal usage)
│
├── service/
│   └── TaskManager.py        # All business logic + DB operations
│
├── util/
│   ├── db.py                 # Database connection setup
│   ├── exception.py          # Custom exceptions
│   └── validators.py         # Input/data validation logic
│
├── setup.sql                 # SQL schema to create necessary tables
├── test.py                   # Sample POST request testing
└── README.md                 # Project overview and instructions
```

---

##  Setup Instructions

### 1. Create and Activate Virtual Environment
```bash
python -m venv venv
.\venv\Scripts\activate   # On Windows
```

### 2. Install Dependencies
```bash
pip install flask mysql-connector-python requests
```

### 3. Set Up Database
In your MySQL client or PopSQL:
```sql
SOURCE setup.sql;
```

Or manually run the contents of `setup.sql`.

### 4. Configure DB Connection
Update `util/db.py` with your MySQL credentials:
```python
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="task_manager"
    )
```

---

##  Running the Flask API Server
```bash
python app.py
```
Server will start at:
```
http://127.0.0.1:5000
```

---



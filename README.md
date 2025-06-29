# Task Manager System (Python + Flask + MySQL)

A **Task Management System** built using **Python, Flask, and MySQL**, providing **RESTful API endpoints** and a **decoupled frontend** for creating, updating, deleting, assigning, and viewing tasks with **validation, structured exception handling, and modular architecture**.

---

## Features

Create, view, and manage **users**  
Create, assign, view, update, and delete **tasks**  
View tasks by **user** or **status**  
Integrated **validation** for input types, dates, and duplicate entries  
Uses **MySQL database** for persistent storage  
**RESTful API architecture with Flask** for decoupled frontend consumption  
Clean, layered architecture with DTOs, validators, and custom exceptions

---

## Project Structure

\`\`\`
Task_Manager_System/
│
├── app.py                    # Flask app with REST API endpoints
│
├── dto/                      # Data Transfer Objects
│   ├── Task.py
│   └── user.py
│
├── frontend/                 # Decoupled HTML/JS frontend
│   ├── index.html            # Acts as the home page of the frontend
│   ├── add_task.html
│   ├── get_all_task.html
│   ├── get_task.html
│   ├── delete_task.html
│   ├── get_task_by_user.html
│   ├── get_task_by_status.html
│   └── assign_task_to_user.html
│
├── service/                  # Business logic
│   └── TaskManager.py
│
├── util/                     # Utilities
│   ├── db.py
│   ├── exception.py
│   └── validators.py
│
├── setup.sql                 # SQL schema for database setup
├── requirements.txt          # Dependency list
└── README.md                 # Project documentation (this file)
\`\`\`

---

## ⚙️ Setup Instructions

### 1.Clone the Repository
\`\`\`bash
git clone <repo-url>
cd Task_Manager_System
\`\`\`

### 2.Create and Activate Virtual Environment
\`\`\`bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On Linux/macOS
source venv/bin/activate
\`\`\`

### 3.Install Dependencies
\`\`\`bash
pip install flask mysql-connector-python flask-cors requests
\`\`\`
*(Or run \`pip install -r requirements.txt\` if it is updated.)*

### 4.Set Up MySQL Database
Run the SQL script to create the required database and tables:
\`\`\`sql
SOURCE setup.sql;
\`\`\`
Or manually execute the contents of \`setup.sql\` in your MySQL client.

### 5.Configure Database Connection
In \`util/db.py\`, update with your MySQL credentials:
\`\`\`python
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="task_manager"
    )
\`\`\`

---

##  Running the Flask API Server
\`\`\`bash
python app.py
\`\`\`
The server will start at:
\`\`\`
http://127.0.0.1:5000
\`\`\`

You can now use **Postman** or your **frontend HTML pages** to interact with your REST APIs.

---

## 🖥️ Frontend Access

All HTML pages in the \`frontend/\` directory can be opened in your browser directly and will communicate with your Flask API using \`fetch\` for CRUD operations.

 **Note:** \`index.html\` acts as the **home page of your frontend** for navigating between different functionalities.

---

##  Contributing

Contributions, issue reports, and suggestions are welcome.

---


##  Contact

For queries or discussions:
\`\`\`
Aaryatha P R
aaryathaPr@gmail.com
\`\`\`


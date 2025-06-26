import mysql.connector

"""Database connection module for Task Manager."""

def get_connection():
    """Establishes a connection to the MySQL database."""
    return mysql.connector.connect(host="localhost",user="root",password="password@123",database="task_manager")

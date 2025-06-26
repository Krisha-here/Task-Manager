CREATE DATABASE task_manager;

USE task_manager;

CREATE TABLE User (
    user_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100)
);

CREATE TABLE Task (
    task_id INT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    priority VARCHAR(20) NOT NULL,
    due_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL,
    assigned_to INT,
    FOREIGN KEY (assigned_to) REFERENCES users(user_id) ON DELETE SET NULL
);
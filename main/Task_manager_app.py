from service.TaskManager import TaskManager
from util.exception import (TaskManagerException,TaskNotFoundException,UserNotFoundException,InvalidInputError,
                            ValidationError,DuplicateTaskException,DuplicateUserException,EmptyTaskListException)
                              
def main():
    tm=TaskManager()
    flag=True
    while flag:
        print("""
        1. Create Tasks
        2. Delete Task
        3. Get Task
        4. List all Tasks
        5. List Tasks by User
        6. List Tasks by Status
        7. Create user
        8. Assign Task to User
        9. Exit""")
        try:
            try:
                choice = int(input("Enter your choice: ").strip())
            except ValueError as ve:
                raise InvalidInputError("Expected a numeric input for menu choice.", original_exception=ve)

            if choice == 1:
                try:
                   print(tm.create_task())
                except (DuplicateTaskException, ValidationError) as e:
                    print(f"Error: {e}")

            elif choice == 2:
                try:
                    try:
                        task_id = int(input("Enter Task ID: ").strip())
                    except ValueError as ve:
                        raise InvalidInputError("Task id must be integer",original_exception=ve) from ve
                    print(tm.delete_task(task_id))
                except (TaskNotFoundException, ValidationError,InvalidInputError) as e:
                    print(f"Error: {e.args[0]}")
                    if isinstance(e, InvalidInputError) and e.original_exception:
                        print(f"Details: {e.original_exception}")

            elif choice == 3:
                try:
                    try:
                        task_id = int(input("Enter Task ID: ").strip())
                    except ValueError as ve:
                        raise InvalidInputError("Task id must be integer",original_exception=ve) from ve
                    print(tm.get_task(task_id))
                except (TaskNotFoundException,InvalidInputError) as e:
                    print(f"Error: {e.args[0]}")
                    if isinstance(e, InvalidInputError) and e.original_exception:
                        print(f"Details: {e.original_exception}")

            elif choice == 4:
                try:
                    print(tm.list_all_tasks())
                except EmptyTaskListException as e:
                    print(f"Error: {e}")

            elif choice == 5:
                try:
                    try:
                        user_id = int(input("Enter User ID: ").strip())
                    except ValueError as ve:
                        raise InvalidInputError("User id must be integer",original_exception=ve) from ve
                    print(tm.list_tasks_by_user(user_id))
                except (UserNotFoundException,InvalidInputError) as e:
                    print(f"Error: {e.args[0]}")
                    if isinstance(e, InvalidInputError) and e.original_exception:
                        print(f"Details: {e.original_exception}")

            elif choice == 6:
                try:
                    status = input("Enter status: ").strip()
                    print(tm.list_tasks_by_status(status))
                except ValidationError as e:
                    print(f"Error: {e}")

            elif choice == 7:
                try:
                    print(tm.create_user())
                except (DuplicateUserException, ValidationError,InvalidInputError) as e:
                    print(f"Error: {e.args[0]}")
                    if isinstance(e, InvalidInputError) and e.original_exception:
                        print(f"Details: {e.original_exception}")

            elif choice == 8:
                try:
                    try:
                        task_id = int(input("Enter Task ID: ").strip())
                        user_id = int(input("Enter User ID: ").strip())
                    except ValueError as ve:
                        raise InvalidInputError("Invalid input",original_exception=ve) from ve
                    print(tm.assign_task_to_user(task_id, user_id))
                except (TaskNotFoundException, UserNotFoundException,InvalidInputError) as e:
                    print(f"Error: {e.args[0]}")
                    if isinstance(e, InvalidInputError) and e.original_exception:
                        print(f"Details: {e.original_exception}")

            elif choice == 9:
                print("Exiting program.")
                break
            else:
                print("Invalid choice. Please select a number between 1 and 9.")

        except InvalidInputError as e:
            print(f"Error: {e}")
            if e.original_exception:
                print(f"Details: {e.original_exception}")

        except TaskManagerException as e:
            print(f"Application error: {e}")

        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
    


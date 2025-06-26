
class User:
    """Represents a user in the system."""

    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email

    def display_info(self):
        """Displays the details of the user."""
        print("\n--- USER ---")
        print(f"User ID : {self.user_id}")
        print(f"Name    : {self.name}")
        print(f"Email   : {self.email}")


        

            

    

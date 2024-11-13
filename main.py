import pymongo
import pymongo.errors
from cryptography.fernet import Fernet
import re
import password

class PasswordValidationError(Exception):
    def __init__(self, msg: str = "Password validation failed.") -> None:
        super().__init__(msg)

def validate_password(password: str):
    """
    Validates a password based on the following criteria:
    - Minimum length of 8 characters.
    - Contains at least one special character.
    - Contains both uppercase and lowercase letters.
    - Contains at least one digit.

    :param password: The password to validate.
    :raises PasswordValidationError: If any validation rule is violated.
    """
    # Check minimum length
    if len(password) < 8:
        raise PasswordValidationError(msg="Password cannot be less than 8 characters.")

    # Check for at least one special character
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise PasswordValidationError(msg="Password must contain at least one special character.")
    
    # Check for both uppercase and lowercase letters
    if not any(char.isupper() for char in password) or not any(char.islower() for char in password):
        raise PasswordValidationError(msg="Password must contain both uppercase and lowercase letters.")
    
    # Check for at least one digit
    if not any(char.isdigit() for char in password):
        raise PasswordValidationError(msg="Password must contain at least one digit.")

# Main application class
class PasswordManagerApp:

    def __init__(self) -> None:
        """
        Initializes the Password Manager App and connects to MongoDB.
        """
        try:
            client: pymongo.MongoClient = pymongo.MongoClient("localhost:27017")
            db = client['Password_Manager_App']
            self.collection = db["user"]
        except pymongo.errors.ConfigurationError:
            print("Invalid MongoDB connection string.")
        except pymongo.errors.ConnectionFailure:
            print("Failed to connect to the MongoDB server.")
        else:
            print("Database connected successfully.")

    def encrypt_password(self, password: str, key: bytes) -> bytes:
        """
        Encrypts a password using the provided key.

        :param password: The password to encrypt.
        :param key: The encryption key.
        :return: The encrypted password as bytes.
        """
        cipher_suite = Fernet(key)
        return cipher_suite.encrypt(password.encode())

    def decrypt_password(self, encrypted_password: bytes, key: bytes) -> str:
        """
        Decrypts an encrypted password using the provided key.

        :param encrypted_password: The encrypted password to decrypt.
        :param key: The encryption key.
        :return: The decrypted password as a string.
        """
        cipher_suite = Fernet(key)
        return cipher_suite.decrypt(encrypted_password).decode()

    def add_password(self):
        """
        Adds a new password entry after validating and encrypting the password.
        """
        try:
            domain = input("Enter a domain name: ").title()
            user_name = input("Enter a user name: ")
            get_user_pass = input("suggest a strong password (type 'y' or 'n'): ")
            if get_user_pass == 'n':
                user_password = input("Enter a password: ")
            elif get_user_pass == 'y':
                user_password = password.password
                print("your password is",user_password)
            
            # Validate password
            validate_password(user_password)

            # Generate encryption key and encrypt password
            key = Fernet.generate_key()
            encrypted_password = self.encrypt_password(password=user_password, key=key)

            # Insert the data into MongoDB
            insert_doc = {
                'domain': domain,
                'email': user_name,
                'password': encrypted_password,
                'key': key
            }
            self.collection.insert_one(insert_doc)
            print("Password added successfully.")
        except PasswordValidationError as e:
            print(f"Password validation error: {e}")
        except pymongo.errors.OperationFailure:
            print("Failed to insert the document into the database.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def view_passwords(self):
        """
        Retrieves and displays stored passwords after decryption.
        """
        try:
            all_docs = self.collection.find()
            for doc in all_docs:
                print(f"Domain: {doc['domain']}, Email: {doc['email']}")
                decrypted_password = self.decrypt_password(
                    encrypted_password=doc['password'], key=doc['key']
                )
                print(f"Password: {decrypted_password}")
        except pymongo.errors.PyMongoError:
            print("Error while fetching data from the database.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def update_details(self):
        """
        Updates user account details in the database.

        Provides options to update the following:
        1. Domain name
        2. User name (email)
        3. Password

        The method performs the following:
        - Prompts the user to select the type of detail to update.
        - Searches the database for the existing detail.
        - If the existing detail is found, prompts the user for new values and updates the database.
        - Handles cases where the provided detail does not exist in the database.

        :raises ValueError: If the user provides an invalid input.
        """
        option = int(input('''
                            1. Update domain name
                            2. Update user name (email)
                            3. Update password 
                            4. cancle
                            '''))
        match option:

            case 1:
                old_domain = input("Enter the domain name you want to update: ")
                find = self.collection.find_one({"domain": old_domain})
                if find is None:
                    print("The provided domain name does not exist.")
                    self.main()
                else:
                    new_domain = input("Enter the new domain name: ")
                    self.collection.update_one(
                        {"domain": old_domain},
                        {"$set": {"domain": new_domain}}
                    )
                    print(f"The domain name '{old_domain}' has been updated to '{new_domain}'.")
            
            case 2:
                old_user_name = input("Enter the user name you want to update: ")
                find = self.collection.find_one({"email": old_user_name})
                if find is None:
                    print("The provided user name does not exist.")
                    self.main()
                else:
                    new_user_name = input("Enter the new user name: ")
                    self.collection.update_one(
                        {"email": old_user_name},
                        {"$set": {"email": new_user_name}}
                    )
                    print(f"The user name '{old_user_name}' has been updated to '{new_user_name}'.")
            
            case 3:
                old_user_pass = input("Enter the password you want to update: ")
                find = self.collection.find_one({"password": old_user_pass})
                if find is None:
                    print("The provided password does not exist.")
                    self.main()
                else:
                    new_user_pass = input("Enter the new password: ")
                    self.collection.update_one(
                        {"password": old_user_pass},
                        {"$set": {"password": new_user_pass}}
                    )
                    print(f"The password has been updated successfully.")
            
            case 4:
                print("Operation canceled.")

            case _:
                print("Please choose a valid option.")
        
    def delete_details(self):
        """
        Deletes a record or multiple records from the database.

        Provides options for deleting:
        1. Records by domain name.
        2. Records by user name (email).
        3. Records by password.
        4. Delete all records.
        5. Cancel the operation.

        Prompts the user for confirmation before performing destructive operations.
        """
        option = int(input('''
                            1. Delete by domain name
                            2. Delete by user name (email)
                            3. Delete by password
                            4. Delete all records
                            5. Cancel
                            '''))
        match option:
            case 1:
                domain = input("Enter the domain name you want to delete: ")
                find = self.collection.find_one({"domain": domain})
                if find is None:
                    print("The provided domain name does not exist.")
                else:
                    self.collection.delete_one({"domain": domain})
                    print(f"Record with domain '{domain}' deleted successfully.")
                    
            case 2:
                user_name = input("Enter the user name (email) you want to delete: ")
                find = self.collection.find_one({"email": user_name})
                if find is None:
                    print("The provided user name does not exist.")
                else:
                    self.collection.delete_one({"email": user_name})
                    print(f"Record with user name '{user_name}' deleted successfully.")
                    
            case 3:
                user_password = input("Enter the password you want to delete: ")
                find = self.collection.find_one({"password": user_password})
                if find is None:
                    print("The provided password does not exist.")
                else:
                    self.collection.delete_one({"password": user_password})
                    print("Record with the specified password deleted successfully.")
                    
            case 4:
                confirm = input("Are you sure you want to delete ALL records? (yes/no): ")
                if confirm.lower() == 'yes':
                    result = self.collection.delete_many({})
                    print(f"All {result.deleted_count} records have been deleted.")
                else:
                    print("Operation canceled.")
                    
            case 5:
                print("Operation canceled.")
            
            case _:
                print("Invalid option. Please select a valid choice.")
    def search_details(self):
        """
        Allows the user to search for stored credentials by domain or email.
        Provides the option to view all stored records if no filter is applied.
        """
        try:
            option = int(input('''
            Choose your search criteria:
            1. Search by domain name
            2. Search by email (username)
            3. View all records
            4. Cancel
            '''))

            match option:
                case 1:
                    domain = input("Enter the domain name to search: ")
                    result = self.collection.find({"domain": {"$regex": domain, "$options": "i"}})
                    self._display_results(result)
                
                case 2:
                    email = input("Enter the email (username) to search: ")
                    result = self.collection.find({"email": {"$regex": email, "$options": "i"}})
                    self._display_results(result)

                case 3:
                    result = self.collection.find()
                    self._display_results(result)

                case 4:
                    print("Search operation canceled.")
                
                case _:
                    print("Invalid option. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def _display_results(self, results):
        """
        Displays search results from the database.
        
        :param results: Cursor object containing the search results.
        """
        found = False
        for doc in results:
            found = True
            print(f"\nDomain: {doc['domain']}")
            print(f"Email: {doc['email']}")
            decrypted_password = self.decrypt_password(
                encrypted_password=doc['password'], 
                key=doc['key']
            )
            print(f"Password: {decrypted_password}")
        if not found:
            print("No records found matching your query.")

    def main(self):
        """
        Main method to provide a CLI for managing passwords.
        """
        while True:
            print('''
                1. Add a password
                2. Update details
                3. Delete details
                4. View passwords
                5. search details
                6. Exit
            ''')
            try:
                user_choice = int(input("Enter your choice: "))
                match user_choice:
                    case 1:
                        self.add_password()
                    case 2:
                        self.update_details()
                    case 3:
                        self.delete_details()
                    case 4:
                        self.view_passwords()
                    case 5:
                        self.search_details()
                        # self._display_results()
                    case 6:
                        print("Exiting the application.")
                        break
                    case _:
                        print("Please choose a valid option.")
            except ValueError:
                print("Invalid input. Please enter a number.")
            except KeyboardInterrupt:
                print("\nExiting the application.")
                break

# Entry point of the application
if __name__ == "__main__":
    app = PasswordManagerApp()
    app.main()

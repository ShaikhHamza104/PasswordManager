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

    def main(self):
        """
        Main method to provide a CLI for managing passwords.
        """
        while True:
            print('''
                1. Add a password
                2. View passwords
                3. Exit
            ''')
            try:
                user_choice = int(input("Enter your choice: "))
                match user_choice:
                    case 1:
                        self.add_password()
                    case 2:
                        self.view_passwords()
                    case 3:
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

# Password Manager App

Welcome to the **Password Manager App**! This application helps users securely manage their passwords with encryption, validation, and password generation functionality.

## Features
- **Secure Password Storage**: Encrypts passwords before storing them in MongoDB.
- **Password Validation**: Ensures passwords meet security criteria such as length, special characters, uppercase/lowercase letters, and digits.
- **Password Generation**: Offers a feature to generate strong passwords.
- **MongoDB Integration**: Uses MongoDB to store user credentials securely.

## Installation

Follow these steps to get the project up and running on your local machine:

### Prerequisites
- **Python 3.x**
- **MongoDB** (running locally or remotely)

### Step 1: Clone the repository
Clone the repository to your local machine:
```bash
git clone https://github.com/ShaikhHamza104/PasswordManager
```

### Step 2: Install Dependencies
Navigate to the project directory and install required packages using pip:
```bash
cd PasswordManager
pip install -r requirements.txt
```

### Step 3: Run the Application
Run the Python script to start the application:
```bash
python main.py
```

### Usage

Once the application is running, you can:

1. **Add a password**:
    - Enter the domain name, username, and password.
    - You can choose to generate a strong password or provide your own.
    - The password will be validated, encrypted, and saved to MongoDB.

2. **View stored passwords**:
    - View the list of saved credentials with their domain and decrypted passwords.

### Main Menu
## 1. Add a password
## 2. View passwords
## 3. Exit


## Password Validation Criteria

- **Length**: Minimum 8 characters.
- **Special Character**: Must include at least one special character (e.g., `!@#$%^&*`).
- **Uppercase and Lowercase**: Must contain both uppercase and lowercase letters.
- **Digit**: Must include at least one digit.

## Project Structure

PasswordManager/
 ├── main.py # Main application logic and CLI interface 
 ├── password.py # Strong password generator 
 ├── requirements.txt # Required Python libraries 
 └── README.md # Project documentation


## Contributing

We welcome contributions to enhance the functionality and improve the code quality! Follow these steps to contribute:

### How to Contribute:
1. **Fork the repository**: Click the `Fork` button at the top-right corner of the project page.
2. **Clone your fork**:
    ```bash
    git clone https://github.com/your-username/PasswordManager.git
    ```
3. **Create a branch**:
    ```bash
    git checkout -b feature/your-feature-name
    ```
4. **Make changes**: Implement your improvements or bug fixes.
5. **Commit your changes**:
    ```bash
    git commit -m "Description of changes"
    ```
6. **Push to your fork**:
    ```bash
    git push origin feature/your-feature-name
    ```
7. **Create a pull request**: Open a pull request to merge your changes into the main repository.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Issues

If you encounter any issues, please feel free to open an issue on the [GitHub issues page](https://github.com/your-username/PasswordManager/issues).

## Contact

For any questions, feedback, or inquiries:
- **Your Name**: [kmohdhamza10@gmail,com](mailto:your-email@example.com)
- **GitHub**: [https://github.com/ShaikhHamza104](https://github.com/ShaikhHamza104)

---

### Thank you for using and contributing to this project!

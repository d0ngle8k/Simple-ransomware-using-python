#Import all necessary libraries
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

# Step 2: Deriving the encryption key from a simple password 
password = "hello"
salt = get_random_bytes(16)
key = password.encode().ljust(32, b'\0')[:32]

# Step 3: Function to encrypt a file
def encrypt_file(file_path, key):
    try:
        iv = get_random_bytes(16)  # Generate a random initialization vector
        cipher = AES.new(key, AES.MODE_CBC, iv)  # Create a new AES cipher
        with open(file_path, 'rb') as f:
            file_data = f.read()  # Read the file data
        encrypted_data = cipher.encrypt(pad(file_data, AES.block_size))  # Encrypt the data with padding
        with open(file_path + '.encrypted', 'wb') as f:
            f.write(salt + iv + encrypted_data)  # Write the salt, IV, and encrypted data to a new file
        os.remove(file_path)  # Remove the original file
        print('Successfully encrypted:', file_path)
    except Exception as e:
        print('Failed to encrypt:', file_path, 'Error:', e)
        
# Step 4: Creating Main Script
if __name__ == "__main__":
    # Hardcoded file path
    file_path = r"D:\test.docx"

    # Debugging: Print the file path to ensure it is correct
    print("Attempting to encrypt file at path:", file_path)

    if os.path.exists(file_path):
        print("File exists:", file_path)
        encrypt_file(file_path, key)
    else:
        print("The specified file does not exist.")
        print("Path:", os.path.abspath(file_path))
        directory, filename = os.path.split(file_path)
        print("Directory exists:", os.path.isdir(directory))
        print("File exists in directory:", os.path.isfile(file_path))
        
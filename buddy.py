import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

# --- DATABASE SETUP ---
DB_NAME = "study_buddy.db"


def init_sqlite_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS study_topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            topic TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """
    )
    conn.commit()
    conn.close()


# --- GUI APPLICATION CLASS ---
class SmartStudyBuddyApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Smart Study Buddy")
        self.root.geometry("650x500")

        # Input Frame
        input_frame = tk.LabelFrame(
            root, text=" Add / Update Topic ", padx=10, pady=10
        )
        input_frame.pack(fill="x", padx=15, pady=10)

        tk.Label(input_frame, text="Subject:").grid(
            row=0, column=0, sticky="w", padx=5, pady=5
        )
        self.subject_entry = tk.Entry(input_frame, width=25)
        self.subject_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Topic:").grid(
            row=0, column=2, sticky="w", padx=5, pady=5
        )
        self.topic_entry = tk.Entry(input_frame, width=25)
        self.topic_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(input_frame, text="Status:").grid(
            row=1, column=0, sticky="w", padx=5, pady=5
        )
        self.status_var = tk.StringVar(value="Pending")
        self.status_dropdown = ttk.Combobox(
            input_frame,
            textvariable=self.status_var,
            values=["Pending", "Completed"],
            state="readonly",
            width=22,
        )
        self.status_dropdown.grid(row=1, column=1, padx=5, pady=5)

        # Buttons Frame
        btn_frame = tk.Frame(root)
        btn_frame.pack(fill="x", padx=15, pady=5)

        tk.Button(
            btn_frame,
            text="Add Topic",
            bg="#4CAF50",
            fg="white",
            command=self.add_topic,
        ).pack(side="left", padx=5)
        tk.Button(
            btn_frame,
            text="Update Status",
            bg="#2196F3",
            fg="white",
            command=self.update_status,
        ).pack(side="left", padx=5)
        tk.Button(
            btn_frame,
            text="Delete Topic",
            bg="#f44336",
            fg="white",
            command=self.delete_topic,
        ).pack(side="left", padx=5)
        tk.Button(
            btn_frame,
            text="Clear Form",
            bg="#9E9E9E",
            fg="white",
            command=self.clear_entries,
        ).pack(side="left", padx=5)

        # Filter Options Frame
        filter_frame = tk.Frame(root)
        filter_frame.pack(fill="x", padx=15, pady=5)

        tk.Label(filter_frame, text="Filter View:").pack(side="left", padx=5)
        self.filter_var = tk.StringVar(value="All")
        filter_dropdown = ttk.Combobox(
            filter_frame,
            textvariable=self.filter_var,
            values=["All", "Pending", "Completed"],
            state="readonly",
            width=15,
        )
        filter_dropdown.pack(side="left", padx=5)
        filter_dropdown.bind("<<ComboboxSelected>>", lambda e: self.load_data())

        # Data Display Table (Treeview)
        tree_frame = tk.Frame(root)
        tree_frame.
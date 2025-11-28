import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from database import Database  # Importing the database module

class StudentConcernApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Concern Intake System - EVSU-OC")
        self.root.geometry("1000x600")
        
        # --- Initialize Database ---
        # This connects to 'concerns_db.sqlite' using the class from database.py
        self.db = Database('concerns_db.sqlite')

        # --- Variables ---
        self.concern_id_var = tk.StringVar()
        self.student_name_var = tk.StringVar()
        self.student_id_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Pending")
        self.search_var = tk.StringVar()

        # --- GUI Layout ---
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self.root, bg="#800000", pady=10)
        header_frame.pack(fill=tk.X)
        lbl_title = tk.Label(header_frame, text="EVSU-OC Student Concern Intake System", font=("Arial", 20, "bold"), bg="#800000", fg="white")
        lbl_title.pack()

        # Main Content Area
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Left Side: Entry Form ---
        form_frame = tk.LabelFrame(main_frame, text="Concern Entry", font=("Arial", 12, "bold"), padx=10, pady=10)
        form_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)

        # Student ID
        tk.Label(form_frame, text="Student ID:").grid(row=0, column=0, sticky="w", pady=5)
        tk.Entry(form_frame, textvariable=self.student_id_var, width=30).grid(row=0, column=1, pady=5)

        # Student Name
        tk.Label(form_frame, text="Student Name:").grid(row=1, column=0, sticky="w", pady=5)
        tk.Entry(form_frame, textvariable=self.student_name_var, width=30).grid(row=1, column=1, pady=5)

        # Category
        tk.Label(form_frame, text="Category:").grid(row=2, column=0, sticky="w", pady=5)
        categories = ["Academics", "Finance", "Behavior", "Facilities", "Other"]
        combo_cat = ttk.Combobox(form_frame, textvariable=self.category_var, values=categories, state="readonly", width=27)
        combo_cat.grid(row=2, column=1, pady=5)
        combo_cat.current(0)

        # Concern Details
        tk.Label(form_frame, text="Details:").grid(row=3, column=0, sticky="nw", pady=5)
        self.txt_details = tk.Text(form_frame, width=22, height=8)
        self.txt_details.grid(row=3, column=1, pady=5)

        # Status
        tk.Label(form_frame, text="Status:").grid(row=4, column=0, sticky="w", pady=5)
        status_opts = ["Pending", "In Progress", "Resolved", "Closed"]
        combo_status = ttk.Combobox(form_frame, textvariable=self.status_var, values=status_opts, state="readonly", width=27)
        combo_status.grid(row=4, column=1, pady=5)

        # Buttons Frame
        btn_frame = tk.Frame(form_frame, pady=10)
        btn_frame.grid(row=5, column=0, columnspan=2)

        tk.Button(btn_frame, text="Add Record", command=self.add_record, bg="#4CAF50", fg="white", width=12).grid(row=0, column=0, padx=2, pady=2)
        tk.Button(btn_frame, text="Update", command=self.update_record, bg="#2196F3", fg="white", width=12).grid(row=0, column=1, padx=2, pady=2)
        tk.Button(btn_frame, text="Delete", command=self.delete_record, bg="#f44336", fg="white", width=12).grid(row=1, column=0, padx=2, pady=2)
        tk.Button(btn_frame, text="Clear", command=self.clear_form, bg="#FF9800", fg="white", width=12).grid(row=1, column=1, padx=2, pady=2)

        # --- Right Side: Data List ---
        list_frame = tk.LabelFrame(main_frame, text="Records Database", font=("Arial", 12, "bold"), padx=10, pady=10)
        list_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

        # Search Bar
        search_frame = tk.Frame(list_frame)
        search_frame.pack(fill=tk.X, pady=5)
        tk.Label(search_frame, text="Search by Name/ID:").pack(side=tk.LEFT)
        tk.Entry(search_frame, textvariable=self.search_var).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        tk.Button(search_frame, text="Search", command=self.search_data).pack(side=tk.LEFT)
        tk.Button(search_frame, text="Show All", command=self.load_data).pack(side=tk.LEFT, padx=5)

        # Treeview (Table)
        columns = ("ID", "Student ID", "Name", "Category", "Date", "Status")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Student ID", text="Student ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Date", text="Date Filed")
        self.tree.heading("Status", text="Status")

        self.tree.column("ID", width=30)
        self.tree.column("Student ID", width=80)
        self.tree.column("Name", width=150)
        self.tree.column("Category", width=100)
        self.tree.column("Date", width=100)
        self.tree.column("Status", width=80)

        self.tree.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<ButtonRelease-1>", self.get_cursor)

    # --- Backend Functions ---

    def add_record(self):
        if self.student_id_var.get() == "" or self.student_name_var.get() == "":
            messagebox.showwarning("Input Error", "Student ID and Name are required.")
            return

        try:
            date_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            details = self.txt_details.get("1.0", tk.END).strip()
            
            # Call database module
            self.db.insert(self.student_id_var.get(),
                           self.student_name_var.get(),
                           self.category_var.get(),
                           details,
                           date_now,
                           self.status_var.get())
            
            self.load_data()
            self.clear_form()
            messagebox.showinfo("Success", "Record Added Successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_data(self):
        self.tree.delete(*self.tree.get_children())
        rows = self.db.fetch_all() # Call database module
        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def search_data(self):
        search_term = self.search_var.get()
        self.tree.delete(*self.tree.get_children())
        rows = self.db.search(search_term) # Call database module
        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def get_cursor(self, event):
        cursor_row = self.tree.focus()
        contents = self.tree.item(cursor_row)
        row = contents['values']
        
        if row:
            self.concern_id_var.set(row[0])
            self.student_id_var.set(row[1])
            self.student_name_var.set(row[2])
            self.category_var.set(row[3])
            self.status_var.set(row[5])
            
            # Fetch details from DB module
            details_row = self.db.fetch_details(row[0])
            self.txt_details.delete("1.0", tk.END)
            if details_row:
                self.txt_details.insert(tk.END, details_row[0])

    def update_record(self):
        if not self.concern_id_var.get():
            messagebox.showwarning("Selection Error", "Please select a record to update.")
            return

        try:
            details = self.txt_details.get("1.0", tk.END).strip()
            # Call database module
            self.db.update(self.concern_id_var.get(),
                           self.student_id_var.get(),
                           self.student_name_var.get(),
                           self.category_var.get(),
                           details,
                           self.status_var.get())
            
            self.load_data()
            messagebox.showinfo("Success", "Record Updated Successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_record(self):
        if not self.concern_id_var.get():
            messagebox.showwarning("Selection Error", "Please select a record to delete.")
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?")
        if confirm:
            try:
                # Call database module
                self.db.delete(self.concern_id_var.get())
                self.load_data()
                self.clear_form()
                messagebox.showinfo("Success", "Record Deleted Successfully")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def clear_form(self):
        self.concern_id_var.set("")
        self.student_id_var.set("")
        self.student_name_var.set("")
        self.category_var.set("Academics")
        self.status_var.set("Pending")
        self.txt_details.delete("1.0", tk.END)
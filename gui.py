import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import os
from database import Database  # Importing the database module

class StudentConcernApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Concern Intake System - EVSU-OC")
        self.root.geometry("1200x800") # Enlarged window size
        
        # --- Initialize Database ---
        self.db = Database('concerns_db.sqlite')

        # --- Variables ---
        self.concern_id_var = tk.StringVar()
        self.student_name_var = tk.StringVar()
        self.student_id_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Pending")
        self.search_var = tk.StringVar()
        
        # --- Load Assets ---
        self.logo_image = None
        try:
            # Construct path relative to the script
            img_path = os.path.join(os.path.dirname(__file__), "image", "logo.png")
            if os.path.exists(img_path):
                raw_img = tk.PhotoImage(file=img_path)
                # Subsample to resize (shrink) the image if it's too big. 
                # (5, 5) reduces it to 1/5th size. Adjust if your logo is too small/big.
                self.logo_image = raw_img.subsample(5, 5) 
        except Exception as e:
            print(f"Warning: Could not load logo. {e}")

        # --- GUI Layout ---
        self.configure_styles()
        self.create_widgets()
        self.load_data()

    def configure_styles(self):
        """Sets up custom styles for fonts and table appearance."""
        style = ttk.Style()
        style.theme_use('clam') # Use a cleaner theme
        
        # Configure Treeview (Table) Styles
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#d9d9d9")
        style.configure("Treeview", font=("Arial", 11), rowheight=30) # Taller rows for readability
        style.map("Treeview", background=[('selected', '#800000')]) # Maroon selection color

    def create_widgets(self):
        # --- Header Section ---
        header_frame = tk.Frame(self.root, bg="#800000", pady=15)
        header_frame.pack(fill=tk.X)

        # Inner frame to center the content (Logo + Text)
        header_inner = tk.Frame(header_frame, bg="#800000")
        header_inner.pack()

        # Logo
        if self.logo_image:
            lbl_logo = tk.Label(header_inner, image=self.logo_image, bg="#800000")
            lbl_logo.pack(side=tk.LEFT, padx=15)

        # Title Text
        title_text = "EVSU-OC Student Concern Intake System"
        lbl_title = tk.Label(header_inner, text=title_text, font=("Arial", 26, "bold"), bg="#800000", fg="white")
        lbl_title.pack(side=tk.LEFT)

        # --- Main Content Area ---
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Left Side: Entry Form ---
        # Increased font size for the LabelFrame
        form_frame = tk.LabelFrame(main_frame, text="Concern Entry Details", font=("Arial", 14, "bold"), padx=15, pady=15, fg="#800000")
        form_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))

        # Standard font for labels and entries
        lbl_font = ("Arial", 12)
        entry_font = ("Arial", 12)

        # Student ID
        tk.Label(form_frame, text="Student ID:", font=lbl_font).grid(row=0, column=0, sticky="w", pady=8)
        tk.Entry(form_frame, textvariable=self.student_id_var, font=entry_font, width=35).grid(row=0, column=1, pady=8)

        # Student Name
        tk.Label(form_frame, text="Student Name:", font=lbl_font).grid(row=1, column=0, sticky="w", pady=8)
        tk.Entry(form_frame, textvariable=self.student_name_var, font=entry_font, width=35).grid(row=1, column=1, pady=8)

        # Category
        tk.Label(form_frame, text="Category:", font=lbl_font).grid(row=2, column=0, sticky="w", pady=8)
        categories = ["Academics", "Finance", "Behavior", "Facilities", "Other"]
        combo_cat = ttk.Combobox(form_frame, textvariable=self.category_var, values=categories, state="readonly", width=33, font=entry_font)
        combo_cat.grid(row=2, column=1, pady=8)
        combo_cat.current(0)

        # Concern Details
        tk.Label(form_frame, text="Details:", font=lbl_font).grid(row=3, column=0, sticky="nw", pady=8)
        self.txt_details = tk.Text(form_frame, width=35, height=10, font=("Arial", 11))
        self.txt_details.grid(row=3, column=1, pady=8)

        # Status
        tk.Label(form_frame, text="Status:", font=lbl_font).grid(row=4, column=0, sticky="w", pady=8)
        status_opts = ["Pending", "In Progress", "Resolved", "Closed"]
        combo_status = ttk.Combobox(form_frame, textvariable=self.status_var, values=status_opts, state="readonly", width=33, font=entry_font)
        combo_status.grid(row=4, column=1, pady=8)

        # Buttons Frame
        btn_frame = tk.Frame(form_frame, pady=20)
        btn_frame.grid(row=5, column=0, columnspan=2)

        # Common button configuration
        btn_config = {"font": ("Arial", 11, "bold"), "width": 14, "pady": 5}

        tk.Button(btn_frame, text="Add Record", command=self.add_record, bg="#4CAF50", fg="white", **btn_config).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Update", command=self.update_record, bg="#2196F3", fg="white", **btn_config).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="Delete", command=self.delete_record, bg="#f44336", fg="white", **btn_config).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Clear", command=self.clear_form, bg="#FF9800", fg="white", **btn_config).grid(row=1, column=1, padx=5, pady=5)


        # --- Right Side: Data List ---
        list_frame = tk.LabelFrame(main_frame, text="Records Database", font=("Arial", 14, "bold"), padx=15, pady=15, fg="#800000")
        list_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Search Bar
        search_frame = tk.Frame(list_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(search_frame, text="Search by Name/ID:", font=("Arial", 12)).pack(side=tk.LEFT)
        tk.Entry(search_frame, textvariable=self.search_var, font=("Arial", 12)).pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        tk.Button(search_frame, text="Search", command=self.search_data, font=("Arial", 10, "bold"), bg="#ddd").pack(side=tk.LEFT)
        tk.Button(search_frame, text="Show All", command=self.load_data, font=("Arial", 10, "bold"), bg="#ddd").pack(side=tk.LEFT, padx=5)

        # Treeview (Table)
        columns = ("ID", "Student ID", "Name", "Category", "Date", "Status")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        # Define Headings
        self.tree.heading("ID", text="ID")
        self.tree.heading("Student ID", text="Student ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Date", text="Date Filed")
        self.tree.heading("Status", text="Status")

        # Define Columns Width - Enlarged
        self.tree.column("ID", width=40, anchor="center")
        self.tree.column("Student ID", width=100, anchor="center")
        self.tree.column("Name", width=180)
        self.tree.column("Category", width=120, anchor="center")
        self.tree.column("Date", width=120, anchor="center")
        self.tree.column("Status", width=100, anchor="center")

        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind Click Event
        self.tree.bind("<ButtonRelease-1>", self.get_cursor)

    # --- Backend Functions ---

    def add_record(self):
        if self.student_id_var.get() == "" or self.student_name_var.get() == "":
            messagebox.showwarning("Input Error", "Student ID and Name are required.")
            return

        try:
            date_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            details = self.txt_details.get("1.0", tk.END).strip()
            
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
        rows = self.db.fetch_all()
        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def search_data(self):
        search_term = self.search_var.get()
        self.tree.delete(*self.tree.get_children())
        rows = self.db.search(search_term)
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
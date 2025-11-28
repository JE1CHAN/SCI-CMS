import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
import datetime
import os
from database import Database

class StudentConcernApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Concern Intake System - EVSU-OC")
        self.root.geometry("1200x800") 
        
        # --- Initialize Database ---
        self.db = Database('concerns_db.sqlite')

        # --- Variables ---
        self.concern_id_var = tk.StringVar()
        self.student_name_var = tk.StringVar()
        self.student_id_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Pending")
        self.search_var = tk.StringVar()
        self.is_anonymous_var = tk.BooleanVar(value=False)
        self.user_role = None # 'student' or 'admin'
        
        # --- Load Assets ---
        self.logo_image = None
        self.load_assets()

        # --- Styles ---
        self.configure_styles()

        # --- Start with Login Screen ---
        self.show_login_screen()

    def load_assets(self):
        try:
            img_path = os.path.join(os.path.dirname(__file__), "image", "logo.png")
            if os.path.exists(img_path):
                raw_img = tk.PhotoImage(file=img_path)
                self.logo_image = raw_img.subsample(5, 5) 
        except Exception as e:
            print(f"Warning: Could not load logo. {e}")

    def configure_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#d9d9d9")
        style.configure("Treeview", font=("Arial", 11), rowheight=30)
        style.map("Treeview", background=[('selected', '#800000')])

    def clear_window(self):
        """Removes all widgets from the root window."""
        for widget in self.root.winfo_children():
            widget.destroy()

    # ==========================================
    #               SCREENS
    # ==========================================

    def show_login_screen(self):
        self.clear_window()
        self.user_role = None
        self.root.geometry("600x600") # Slightly taller for vertical logo

        # Main Container
        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.pack(fill=tk.BOTH, expand=True)

        # Header/Logo Area
        header_frame = tk.Frame(frame, bg="#800000", pady=30)
        header_frame.pack(fill=tk.X)
        
        if self.logo_image:
            tk.Label(header_frame, image=self.logo_image, bg="#800000").pack(side=tk.TOP, pady=(0, 10))
        
        tk.Label(header_frame, text="Welcome to EVSU-OC\nConcern Monitoring System", 
                 font=("Arial", 18, "bold"), bg="#800000", fg="white").pack(side=tk.TOP)

        # Buttons Area
        btn_frame = tk.Frame(frame, bg="#f0f0f0", pady=40)
        btn_frame.pack()

        tk.Label(btn_frame, text="Please select your role:", font=("Arial", 14), bg="#f0f0f0").pack(pady=(0, 20))

        btn_student = tk.Button(btn_frame, text="I am a Student", font=("Arial", 14, "bold"), 
                                bg="#4CAF50", fg="white", width=20, height=2,
                                command=self.show_student_dashboard)
        btn_student.pack(pady=10)

        btn_admin = tk.Button(btn_frame, text="I am an Admin", font=("Arial", 14, "bold"), 
                              bg="#2196F3", fg="white", width=20, height=2,
                              command=self.request_admin_login)
        btn_admin.pack(pady=10)

    def request_admin_login(self):
        login_win = Toplevel(self.root)
        login_win.title("Admin Login")
        login_win.geometry("350x250")
        login_win.configure(bg="#f0f0f0")
        login_win.grab_set()

        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 175
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 125
        login_win.geometry(f"+{x}+{y}")

        tk.Label(login_win, text="Admin Authentication", font=("Arial", 14, "bold"), bg="#f0f0f0", pady=15).pack()

        frame = tk.Frame(login_win, bg="#f0f0f0")
        frame.pack(pady=10)

        tk.Label(frame, text="Username:", font=("Arial", 10), bg="#f0f0f0").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        user_entry = tk.Entry(frame, font=("Arial", 10))
        user_entry.grid(row=0, column=1, padx=5, pady=5)
        user_entry.focus()

        tk.Label(frame, text="Password:", font=("Arial", 10), bg="#f0f0f0").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        pass_entry = tk.Entry(frame, font=("Arial", 10), show="*")
        pass_entry.grid(row=1, column=1, padx=5, pady=5)

        def attempt_login(event=None):
            username = user_entry.get()
            password = pass_entry.get()
            
            if username == "admin" and password == "admin123":
                login_win.destroy()
                self.show_admin_dashboard()
            else:
                messagebox.showerror("Login Failed", "Invalid Username or Password", parent=login_win)
                pass_entry.delete(0, tk.END)

        login_win.bind('<Return>', attempt_login)
        
        tk.Button(login_win, text="Login", command=attempt_login, 
                  bg="#2196F3", fg="white", font=("Arial", 10, "bold"), width=15).pack(pady=15)

    def show_student_dashboard(self):
        self.clear_window()
        self.user_role = 'student'
        self.root.geometry("800x800")
        
        # Standard Layout for Student: Header Top, Form Center
        self.create_header(self.root, show_logout=True)
        
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.create_form(main_frame)

    def show_admin_dashboard(self):
        self.clear_window()
        self.user_role = 'admin'
        self.root.geometry("1200x800")
        
        # --- NEW LAYOUT: Left Sidebar (Form) | Right Content (Header + DB) ---
        
        # Main container
        main_container = tk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True)

        # LEFT: Sidebar for Form (Full Height)
        left_sidebar = tk.Frame(main_container, bg="#f0f0f0", padx=10, pady=10)
        left_sidebar.pack(side=tk.LEFT, fill=tk.Y)
        
        # RIGHT: Content Area
        right_content = tk.Frame(main_container)
        right_content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # 1. Place Header at the TOP of the Right Content
        self.create_header(right_content, show_logout=True)
        
        # 2. Place Form in the Left Sidebar
        self.create_form(left_sidebar)
        
        # 3. Place Database in the Right Content (below Header)
        # Add padding to separate it from header
        db_container = tk.Frame(right_content, padx=10, pady=10)
        db_container.pack(fill=tk.BOTH, expand=True)
        self.create_database_view(db_container)
        
        # Load initial data
        self.load_data()

    # ==========================================
    #           WIDGET GENERATORS
    # ==========================================

    def create_header(self, parent, show_logout=False):
        """Creates the header with Logo ABOVE Title."""
        header_frame = tk.Frame(parent, bg="#800000", pady=15)
        header_frame.pack(fill=tk.X, side=tk.TOP)

        # Content container centered
        content_frame = tk.Frame(header_frame, bg="#800000")
        content_frame.pack(fill=tk.X, padx=20)

        # Logout Button (Placed first so it can float right, or use grid/place)
        # Using a frame to manage the centered text vs right-aligned button is cleaner
        
        if show_logout:
            logout_btn = tk.Button(header_frame, text="Back / Logout", font=("Arial", 10, "bold"), 
                                   bg="#f44336", fg="white", command=self.confirm_logout)
            # Place absolute top-right of header frame to avoid messing up centering
            logout_btn.place(relx=0.98, rely=0.1, anchor="ne")

        # Logo (Top)
        if self.logo_image:
            tk.Label(content_frame, image=self.logo_image, bg="#800000").pack(side=tk.TOP, pady=(0, 5))

        title_text = "EVSU-OC Student Concern Intake System"
        if self.user_role == 'admin':
            title_text += " (ADMIN)"
        
        # Title (Bottom)
        tk.Label(content_frame, text=title_text, font=("Arial", 22, "bold"), bg="#800000", fg="white").pack(side=tk.TOP)


    def confirm_logout(self):
        if messagebox.askyesno("Confirm Logout", "Are you sure you want to log out?"):
            self.show_login_screen()

    def create_form(self, parent):
        # Determine layout based on role
        if self.user_role == 'student':
            side = tk.TOP
            fill = tk.NONE
            title = "Submit Your Concern"
        else:
            # For admin, this is inside a sidebar, so just pack top
            side = tk.TOP
            fill = tk.BOTH # Fill width of sidebar
            title = "Concern Entry Details"

        form_frame = tk.LabelFrame(parent, text=title, font=("Arial", 14, "bold"), padx=15, pady=15, fg="#800000")
        form_frame.pack(side=side, fill=fill, expand=True if self.user_role=='admin' else False)

        lbl_font = ("Arial", 12)
        entry_font = ("Arial", 12)
        
        # Anonymous Checkbox
        chk_anonymous = tk.Checkbutton(form_frame, text="Remain Anonymous", variable=self.is_anonymous_var, 
                                       onvalue=True, offvalue=False, command=self.toggle_anonymity, font=("Arial", 11, "italic"))
        chk_anonymous.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

        # Inputs
        tk.Label(form_frame, text="Student ID:", font=lbl_font).grid(row=1, column=0, sticky="w", pady=8)
        self.entry_id = tk.Entry(form_frame, textvariable=self.student_id_var, font=entry_font, width=35)
        self.entry_id.grid(row=1, column=1, pady=8)

        tk.Label(form_frame, text="Student Name:", font=lbl_font).grid(row=2, column=0, sticky="w", pady=8)
        self.entry_name = tk.Entry(form_frame, textvariable=self.student_name_var, font=entry_font, width=35)
        self.entry_name.grid(row=2, column=1, pady=8)

        tk.Label(form_frame, text="Category:", font=lbl_font).grid(row=3, column=0, sticky="w", pady=8)
        categories = ["Academics", "Finance", "Behavior", "Facilities", "Other"]
        combo_cat = ttk.Combobox(form_frame, textvariable=self.category_var, values=categories, state="readonly", width=33, font=entry_font)
        combo_cat.grid(row=3, column=1, pady=8)
        combo_cat.current(0)

        tk.Label(form_frame, text="Details:", font=lbl_font).grid(row=4, column=0, sticky="nw", pady=8)
        self.txt_details = tk.Text(form_frame, width=35, height=15, font=("Arial", 11)) # Taller text box for sidebar
        self.txt_details.grid(row=4, column=1, pady=8)

        # Status - Only visible for Admin
        row_idx = 5
        if self.user_role == 'admin':
            tk.Label(form_frame, text="Status:", font=lbl_font).grid(row=row_idx, column=0, sticky="w", pady=8)
            status_opts = ["Pending", "In Progress", "Resolved", "Closed"]
            combo_status = ttk.Combobox(form_frame, textvariable=self.status_var, values=status_opts, state="readonly", width=33, font=entry_font)
            combo_status.grid(row=row_idx, column=1, pady=8)
            row_idx += 1

        # Buttons
        btn_frame = tk.Frame(form_frame, pady=20)
        btn_frame.grid(row=row_idx, column=0, columnspan=2)
        btn_config = {"font": ("Arial", 11, "bold"), "width": 14, "pady": 5}

        if self.user_role == 'student':
            tk.Button(btn_frame, text="Send Concern", command=self.add_record, bg="#4CAF50", fg="white", **btn_config).pack()
        else:
            # Admin Buttons - Grid Layout
            tk.Button(btn_frame, text="Add Record", command=self.add_record, bg="#4CAF50", fg="white", **btn_config).grid(row=0, column=0, padx=5, pady=5)
            tk.Button(btn_frame, text="Update", command=self.update_record, bg="#2196F3", fg="white", **btn_config).grid(row=0, column=1, padx=5, pady=5)
            tk.Button(btn_frame, text="Delete", command=self.delete_record, bg="#f44336", fg="white", **btn_config).grid(row=1, column=0, padx=5, pady=5)
            tk.Button(btn_frame, text="Clear", command=self.clear_form, bg="#FF9800", fg="white", **btn_config).grid(row=1, column=1, padx=5, pady=5)

    def create_database_view(self, parent):
        list_frame = tk.LabelFrame(parent, text="Records Database", font=("Arial", 14, "bold"), padx=15, pady=15, fg="#800000")
        list_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Search Bar
        search_frame = tk.Frame(list_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(search_frame, text="Search by Name/ID:", font=("Arial", 12)).pack(side=tk.LEFT)
        tk.Entry(search_frame, textvariable=self.search_var, font=("Arial", 12)).pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        tk.Button(search_frame, text="Search", command=self.search_data, font=("Arial", 10, "bold"), bg="#ddd").pack(side=tk.LEFT)
        tk.Button(search_frame, text="Show All", command=self.load_data, font=("Arial", 10, "bold"), bg="#ddd").pack(side=tk.LEFT, padx=5)

        # Treeview
        columns = ("ID", "Student ID", "Name", "Category", "Date", "Status")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Student ID", text="Student ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Date", text="Date Filed")
        self.tree.heading("Status", text="Status")

        self.tree.column("ID", width=40, anchor="center")
        self.tree.column("Student ID", width=100, anchor="center")
        self.tree.column("Name", width=180)
        self.tree.column("Category", width=120, anchor="center")
        self.tree.column("Date", width=120, anchor="center")
        self.tree.column("Status", width=100, anchor="center")

        self.tree.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bindings
        self.tree.bind("<ButtonRelease-1>", self.get_cursor)
        self.tree.bind("<Double-1>", self.open_detail_window) 

        # Extra Button for Expanding
        tk.Button(list_frame, text="Expand Selected Concern (New Window)", command=self.open_detail_window_btn, 
                  bg="#607D8B", fg="white", font=("Arial", 10, "bold"), pady=5).pack(fill=tk.X, pady=5)

    # ==========================================
    #             LOGIC & BACKEND
    # ==========================================

    def toggle_anonymity(self):
        if self.is_anonymous_var.get():
            self.student_name_var.set("Anonymous")
            self.student_id_var.set("N/A")
            self.entry_name.config(state='disabled')
            self.entry_id.config(state='disabled')
        else:
            self.student_name_var.set("")
            self.student_id_var.set("")
            self.entry_name.config(state='normal')
            self.entry_id.config(state='normal')

    def add_record(self):
        if not self.is_anonymous_var.get():
            if self.student_id_var.get() == "" or self.student_name_var.get() == "":
                messagebox.showwarning("Input Error", "Student ID and Name are required unless Anonymous.")
                return

        try:
            date_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            details = self.txt_details.get("1.0", tk.END).strip()
            anon_val = 1 if self.is_anonymous_var.get() else 0
            
            # If student, force status to "Pending"
            current_status = "Pending" if self.user_role == 'student' else self.status_var.get()

            self.db.insert(self.student_id_var.get(),
                           self.student_name_var.get(),
                           self.category_var.get(),
                           details,
                           date_now,
                           current_status,
                           anon_val)
            
            if self.user_role == 'admin':
                self.load_data()
                self.clear_form()
            else:
                self.clear_form()
                
            messagebox.showinfo("Success", "Concern Submitted Successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_data(self):
        if self.user_role != 'admin': return
        self.tree.delete(*self.tree.get_children())
        rows = self.db.fetch_all()
        for row in rows:
            display_row = list(row[:6])
            is_anon = row[6]
            if is_anon == 1:
                display_row[1] = "N/A"
                display_row[2] = "Anonymous"
            self.tree.insert("", tk.END, values=display_row)

    def search_data(self):
        if self.user_role != 'admin': return
        search_term = self.search_var.get()
        self.tree.delete(*self.tree.get_children())
        rows = self.db.search(search_term)
        for row in rows:
            display_row = list(row[:6])
            is_anon = row[6]
            if is_anon == 1:
                display_row[1] = "N/A"
                display_row[2] = "Anonymous"
            self.tree.insert("", tk.END, values=display_row)

    def get_cursor(self, event):
        if self.user_role != 'admin': return
        cursor_row = self.tree.focus()
        contents = self.tree.item(cursor_row)
        row = contents['values']
        
        if row:
            record_id = row[0]
            details_row = self.db.fetch_details(record_id)
            if details_row:
                self.concern_id_var.set(record_id)
                self.student_id_var.set(row[1])
                self.student_name_var.set(row[2])
                self.category_var.set(row[3])
                self.status_var.set(row[5])
                
                self.txt_details.delete("1.0", tk.END)
                self.txt_details.insert(tk.END, details_row[0])

                is_anon = details_row[1]
                self.is_anonymous_var.set(True if is_anon == 1 else False)
                
                # Update text fields visual state
                if is_anon == 1:
                    self.entry_name.config(state='disabled')
                    self.entry_id.config(state='disabled')
                else:
                    self.entry_name.config(state='normal')
                    self.entry_id.config(state='normal')

    def update_record(self):
        if not self.concern_id_var.get():
            messagebox.showwarning("Selection Error", "Please select a record to update.")
            return

        try:
            details = self.txt_details.get("1.0", tk.END).strip()
            anon_val = 1 if self.is_anonymous_var.get() else 0

            self.db.update(self.concern_id_var.get(),
                           self.student_id_var.get(),
                           self.student_name_var.get(),
                           self.category_var.get(),
                           details,
                           self.status_var.get(),
                           anon_val)
            
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
        self.is_anonymous_var.set(False)
        self.toggle_anonymity()

    def open_detail_window_btn(self):
        if not self.concern_id_var.get():
             messagebox.showwarning("No Selection", "Please select a concern from the list first.")
             return
        self.open_detail_window(None)

    def open_detail_window(self, event):
        cursor_row = self.tree.focus()
        contents = self.tree.item(cursor_row)
        row = contents['values']
        
        if not row: return

        record_id = row[0]
        details_row = self.db.fetch_details(record_id) 
        full_details_text = details_row[0] if details_row else ""

        top = Toplevel(self.root)
        top.title(f"Concern Details - ID #{row[0]}")
        top.geometry("600x500")
        top.configure(bg="#f0f0f0")

        tk.Label(top, text="Full Concern Details", font=("Arial", 16, "bold"), bg="#800000", fg="white", pady=10).pack(fill=tk.X)

        info_frame = tk.Frame(top, padx=20, pady=20, bg="#f0f0f0")
        info_frame.pack(fill=tk.BOTH, expand=True)

        def add_info(label, value):
            container = tk.Frame(info_frame, bg="#f0f0f0")
            container.pack(fill=tk.X, pady=5)
            tk.Label(container, text=label, font=("Arial", 12, "bold"), width=15, anchor="w", bg="#f0f0f0").pack(side=tk.LEFT)
            tk.Label(container, text=value, font=("Arial", 12), anchor="w", bg="#f0f0f0", wraplength=350, justify="left").pack(side=tk.LEFT)

        add_info("Student Name:", row[2])
        add_info("Student ID:", row[1])
        add_info("Category:", row[3])
        add_info("Date Filed:", row[4])
        add_info("Current Status:", row[5])

        tk.Label(info_frame, text="Description/Concern:", font=("Arial", 12, "bold"), bg="#f0f0f0", anchor="w").pack(fill=tk.X, pady=(15, 5))
        
        txt_display = tk.Text(info_frame, height=10, font=("Arial", 11), wrap=tk.WORD, bg="white")
        txt_display.insert(tk.END, full_details_text)
        txt_display.config(state="disabled")
        txt_display.pack(fill=tk.BOTH, expand=True)

        tk.Button(top, text="Close Window", command=top.destroy, bg="#f44336", fg="white", font=("Arial", 10, "bold")).pack(pady=10)
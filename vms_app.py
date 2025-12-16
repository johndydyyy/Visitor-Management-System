import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import hashlib

# ==========================================
# CONFIGURATION & THEME
# ==========================================
class Theme:
    """Centralized Theme Configuration"""
    # Colors (Dark Modern Tech Theme)
    BG_PRIMARY = "#1e1e2e"    # Dark Blue/Grey Background
    BG_SECONDARY = "#252b48"  # Slightly lighter container
    BG_TERTIARY = "#3e4c6e"   # Inputs/Cards
    
    ACCENT = "#00d2ff"        # Cyan/Electric Blue
    ACCENT_HOVER = "#3a86ff"  # Darker Blue
    
    TEXT_MAIN = "#ffffff"     # White
    TEXT_MUTED = "#a0a0a0"    # Grey text
    
    SUCCESS = "#2ecc71"       # Green
    ERROR = "#ef476f"         # Red/Pink
    WARNING = "#f1c40f"       # Yellow

    # Fonts
    FONT_HEADER = ("Segoe UI", 24, "bold")
    FONT_SUBHEADER = ("Segoe UI", 16, "bold")
    FONT_NORMAL = ("Segoe UI", 11)
    FONT_BOLD = ("Segoe UI", 11, "bold")
    FONT_SMALL = ("Segoe UI", 9)

# ==========================================
# DATABASE MANAGER
# ==========================================
class DatabaseManager:
    """Handles all database interactions"""
    DB_NAME = "vms.db"

    @staticmethod
    def init_db():
        try:
            conn = sqlite3.connect(DatabaseManager.DB_NAME)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS visitors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fullname TEXT NOT NULL,
                    email TEXT,
                    phone TEXT,
                    address TEXT,
                    meeting_with TEXT,
                    department TEXT,
                    purpose TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            conn.close()
        except Exception as e:
            messagebox.showerror("Database Error", f"Init failed: {e}")

    @staticmethod
    def add_visitor(data):
        conn = sqlite3.connect(DatabaseManager.DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO visitors (fullname, email, phone, address, meeting_with, department, purpose)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (data['fullname'], data['email'], data['phone'], data['address'], 
              data['meeting_with'], data['department'], data['purpose']))
        conn.commit()
        conn.close()

    @staticmethod
    def update_visitor(visitor_id, data):
        conn = sqlite3.connect(DatabaseManager.DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE visitors 
            SET fullname=?, email=?, phone=?, address=?, meeting_with=?, department=?, purpose=?
            WHERE id=?
        """, (data['fullname'], data['email'], data['phone'], data['address'], 
              data['meeting_with'], data['department'], data['purpose'], visitor_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_visitor(visitor_id):
        conn = sqlite3.connect(DatabaseManager.DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM visitors WHERE id = ?", (visitor_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def get_visitors(filters=None):
        conn = sqlite3.connect(DatabaseManager.DB_NAME)
        cursor = conn.cursor()
        
        query = "SELECT id, fullname, email, phone, created_at, meeting_with, department FROM visitors"
        params = []
        
        if filters and filters.get('from') and filters.get('to'):
             # Assumes input format YYYY-MM-DD; adds time for full day coverage
            query += " WHERE created_at BETWEEN ? AND ?"
            params = [f"{filters['from']} 00:00:00", f"{filters['to']} 23:59:59"]
            
        query += " ORDER BY created_at DESC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return rows
    
    @staticmethod
    def get_visitor_by_id(visitor_id):
        conn = sqlite3.connect(DatabaseManager.DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM visitors WHERE id = ?", (visitor_id,))
        row = cursor.fetchone()
        conn.close()
        return row

    @staticmethod
    def get_stats():
        conn = sqlite3.connect(DatabaseManager.DB_NAME)
        cursor = conn.cursor()
        
        today = datetime.now().strftime("%Y-%m-%d")
        
        cursor.execute("SELECT COUNT(*) FROM visitors")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM visitors WHERE date(created_at) = date('now', 'localtime')")
        today_count = cursor.fetchone()[0]
        
        conn.close()
        return {"total": total, "today": today_count}

# ==========================================
# UI COMPONENTS
# ==========================================
class StyledButton(tk.Button):
    def __init__(self, parent, text, command, bg=Theme.ACCENT, fg=Theme.TEXT_MAIN, width=15):
        super().__init__(
            parent, 
            text=text, 
            command=command,
            bg=bg,
            fg=fg,
            font=Theme.FONT_BOLD,
            relief=tk.FLAT,
            activebackground=Theme.ACCENT_HOVER,
            activeforeground=fg,
            cursor="hand2",
            width=width,
            pady=8
        )
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.default_bg = bg
        
    def on_enter(self, e):
        self['bg'] = Theme.ACCENT_HOVER
        
    def on_leave(self, e):
        self['bg'] = self.default_bg

class StyledEntry(tk.Entry):
    def __init__(self, parent, width=30, show=None):
        super().__init__(
            parent,
            font=Theme.FONT_NORMAL,
            bg=Theme.BG_TERTIARY,
            fg=Theme.TEXT_MAIN,
            insertbackground="white", # cursor color
            relief=tk.FLAT,
            width=width,
            show=show,
            bd=5
        )

# ==========================================
# APPLICATION CLASS
# ==========================================
class VMSApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Visitor Management System")
        self.root.geometry("1200x800")
        self.root.configure(bg=Theme.BG_PRIMARY)
        
        # Initialize
        DatabaseManager.init_db()
        self.current_user = None
        
        # Styles for Treeview
        self.setup_ttk_styles()
        
        # Start
        self.show_login()

    def setup_ttk_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        # Treeview Header
        style.configure(
            "Treeview.Heading", 
            background=Theme.BG_TERTIARY, 
            foreground="white", 
            font=Theme.FONT_BOLD,
            relief="flat"
        )
        style.map("Treeview.Heading", background=[('active', Theme.BG_SECONDARY)])
        
        # Treeview Body
        style.configure(
            "Treeview",
            background=Theme.BG_SECONDARY,
            foreground="white",
            fieldbackground=Theme.BG_SECONDARY,
            font=Theme.FONT_NORMAL,
            rowheight=35
        )
        style.map("Treeview", background=[("selected", Theme.ACCENT)])

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ================= LOGIN =================
    def show_login(self):
        self.clear_window()
        
        # Split layout: Left (Brand/Art), Right (Login Form)
        container = tk.Frame(self.root, bg=Theme.BG_PRIMARY)
        container.pack(fill=tk.BOTH, expand=True)

        # Content Frame (Centered)
        center_frame = tk.Frame(container, bg=Theme.BG_SECONDARY, padx=40, pady=40)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Logo/Title
        tk.Label(
            center_frame, 
            text="VMS ADMIN", 
            font=("Segoe UI", 32, "bold"), 
            bg=Theme.BG_SECONDARY, 
            fg=Theme.ACCENT
        ).pack(pady=(0, 10))
        
        tk.Label(
            center_frame, 
            text="Sign in to continue", 
            font=Theme.FONT_NORMAL, 
            bg=Theme.BG_SECONDARY, 
            fg=Theme.TEXT_MUTED
        ).pack(pady=(0, 30))

        # Username
        tk.Label(center_frame, text="Username", font=Theme.FONT_SMALL, bg=Theme.BG_SECONDARY, fg=Theme.TEXT_MUTED).pack(anchor="w")
        self.login_user = StyledEntry(center_frame)
        self.login_user.pack(pady=(5, 15))
        
        # Password
        tk.Label(center_frame, text="Password", font=Theme.FONT_SMALL, bg=Theme.BG_SECONDARY, fg=Theme.TEXT_MUTED).pack(anchor="w")
        self.login_pass = StyledEntry(center_frame, show="*")
        self.login_pass.pack(pady=(5, 25))
        
        # Login Button
        StyledButton(center_frame, text="LOGIN", command=self.handle_login, width=30).pack()

        # Bind enter key
        self.root.bind('<Return>', lambda e: self.handle_login())

    def handle_login(self):
        u = self.login_user.get()
        p = self.login_pass.get()
        
        if u == "admin" and p == "admin123":
            self.current_user = "admin"
            self.root.unbind('<Return>')
            self.show_dashboard()
        else:
            messagebox.showerror("Access Denied", "Invalid Credentials")

    # ================= LAYOUT HELPERS =================
    def create_sidebar(self, active_item):
        sidebar = tk.Frame(self.root, bg=Theme.BG_SECONDARY, width=250)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)
        
        # Brand
        tk.Label(
            sidebar, 
            text="VMS SYSTEM", 
            font=("Segoe UI", 18, "bold"), 
            bg=Theme.BG_SECONDARY, 
            fg="white"
        ).pack(pady=40)
        
        # Menu Items
        menu_items = [
            ("Dashboard", self.show_dashboard),
            ("New Visitor", self.show_new_visitor),
            ("Manage Visitors", self.show_manage_visitors),
        ]
        
        for text, cmd in menu_items:
            is_active = (text == active_item)
            fg_color = Theme.ACCENT if is_active else Theme.TEXT_MAIN
            bg_color = "#2f3650" if is_active else Theme.BG_SECONDARY
            font = Theme.FONT_BOLD if is_active else Theme.FONT_NORMAL
            
            btn = tk.Button(
                sidebar,
                text=f"  {text}",
                bg=bg_color,
                fg=fg_color,
                font=font,
                relief=tk.FLAT,
                anchor="w",
                padx=20,
                pady=12,
                command=cmd,
                cursor="hand2",
                activebackground="#2f3650",
                activeforeground="white"
            )
            btn.pack(fill=tk.X, pady=2)

        # Logout at bottom
        tk.Button(
            sidebar, 
            text="Logout", 
            bg=Theme.ERROR, 
            fg="white", 
            font=Theme.FONT_BOLD,
            relief=tk.FLAT, 
            command=self.show_login
        ).pack(side=tk.BOTTOM, fill=tk.X, pady=20, padx=20)

        return sidebar

    def create_main_area(self):
        main = tk.Frame(self.root, bg=Theme.BG_PRIMARY)
        main.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        return main

    # ================= DASHBOARD =================
    def show_dashboard(self):
        self.clear_window()
        self.create_sidebar("Dashboard")
        main = self.create_main_area()
        
        # Header
        tk.Label(main, text="Dashboard Overview", font=Theme.FONT_HEADER, bg=Theme.BG_PRIMARY, fg="white").pack(anchor="w", padx=40, pady=40)
        
        # Stats Grid
        stats_frame = tk.Frame(main, bg=Theme.BG_PRIMARY)
        stats_frame.pack(fill=tk.X, padx=40)
        
        stats = DatabaseManager.get_stats()
        
        self.create_stat_card(stats_frame, "Total Visitors", str(stats['total']), Theme.ACCENT).pack(side=tk.LEFT, padx=(0, 20), expand=True, fill=tk.X)
        self.create_stat_card(stats_frame, "Visitors Today", str(stats['today']), Theme.SUCCESS).pack(side=tk.LEFT, padx=(0, 20), expand=True, fill=tk.X)
        self.create_stat_card(stats_frame, "Active Now", "2", Theme.WARNING).pack(side=tk.LEFT, expand=True, fill=tk.X) # Mock data for now

    def create_stat_card(self, parent, title, value, color):
        card = tk.Frame(parent, bg=Theme.BG_SECONDARY, padx=20, pady=20)
        
        # Color Strip
        tk.Frame(card, bg=color, height=80, width=5).pack(side=tk.LEFT, fill=tk.Y)
        
        content = tk.Frame(card, bg=Theme.BG_SECONDARY, padx=10)
        content.pack(side=tk.LEFT)
        
        tk.Label(content, text=title, font=Theme.FONT_NORMAL, bg=Theme.BG_SECONDARY, fg=Theme.TEXT_MUTED).pack(anchor="w")
        tk.Label(content, text=value, font=("Segoe UI", 28, "bold"), bg=Theme.BG_SECONDARY, fg="white").pack(anchor="w")
        
        return card

    # ================= ADD/EDIT VISITOR =================
    def show_new_visitor(self, existing_data=None):
        self.clear_window()
        page_title = "Edit Visitor" if existing_data else "New Visitor"
        self.create_sidebar("New Visitor" if not existing_data else "")
        main = self.create_main_area()
        
        # Scrollable Frame
        canvas = tk.Canvas(main, bg=Theme.BG_PRIMARY, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=Theme.BG_PRIMARY)
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        canvas.pack(side="left", fill="both", expand=True, padx=40, pady=20)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Header
        tk.Label(scrollable_frame, text=page_title, font=Theme.FONT_HEADER, bg=Theme.BG_PRIMARY, fg="white").pack(anchor="w", pady=(20, 30))

        # Form Container
        form = tk.Frame(scrollable_frame, bg=Theme.BG_SECONDARY, padx=30, pady=30)
        form.pack(fill=tk.BOTH, expand=True)

        # Fields Storage
        self.form_fields = {}
        
        # Layout Input Fields (Grid)
        fields = [
            ("Full Name", "fullname"),
            ("Email Address", "email"),
            ("Phone Number", "phone"),
            ("Department", "department"),
            ("Meeting With", "meeting_with"),
        ]
        
        for i, (label, key) in enumerate(fields):
            tk.Label(form, text=label, font=Theme.FONT_BOLD, bg=Theme.BG_SECONDARY, fg="white").grid(row=i, column=0, sticky="w", pady=(10, 5))
            entry = StyledEntry(form, width=40)
            entry.grid(row=i, column=1, sticky="w", pady=(0, 15), padx=(0, 20))
            self.form_fields[key] = entry

        # Text Areas for Address & Purpose
        tk.Label(form, text="Address", font=Theme.FONT_BOLD, bg=Theme.BG_SECONDARY, fg="white").grid(row=0, column=2, sticky="w", pady=(10, 5))
        self.addr_text = tk.Text(form, height=4, width=35, bg=Theme.BG_TERTIARY, fg="white", font=Theme.FONT_NORMAL, relief=tk.FLAT, insertbackground="white")
        self.addr_text.grid(row=0, column=3, rowspan=2, sticky="nw", pady=(0, 15))
        
        tk.Label(form, text="Purpose", font=Theme.FONT_BOLD, bg=Theme.BG_SECONDARY, fg="white").grid(row=2, column=2, sticky="w", pady=(10, 5))
        self.purp_text = tk.Text(form, height=4, width=35, bg=Theme.BG_TERTIARY, fg="white", font=Theme.FONT_NORMAL, relief=tk.FLAT, insertbackground="white")
        self.purp_text.grid(row=2, column=3, rowspan=2, sticky="nw", pady=(0, 15))

        # Buttons
        btn_text = "UPDATE" if existing_data else "SUBMIT"
        cmd = lambda: self.save_visitor(existing_data[0] if existing_data else None)
        
        btn_frame = tk.Frame(form, bg=Theme.BG_SECONDARY)
        btn_frame.grid(row=6, column=0, columnspan=4, pady=30, sticky="e")
        
        StyledButton(btn_frame, text=btn_text, command=cmd, bg=Theme.SUCCESS).pack(side=tk.RIGHT)
        if existing_data:
             StyledButton(btn_frame, text="CANCEL", command=self.show_manage_visitors, bg=Theme.ERROR).pack(side=tk.RIGHT, padx=10)

        # Pre-fill if editing
        if existing_data:
            # existing_data = (id, fullname, email, phone, address, meeting_with, department, purpose, created_at)
            # CAREFUL: DatabaseManager.get_visitor_by_id returns specific order.
            # ID=0, Name=1, Email=2, Phone=3, Addr=4, Meet=5, Dept=6, Purp=7, Time=8
            
            self.form_fields['fullname'].insert(0, existing_data[1])
            self.form_fields['email'].insert(0, existing_data[2])
            self.form_fields['phone'].insert(0, existing_data[3])
            self.addr_text.insert("1.0", existing_data[4])
            self.form_fields['meeting_with'].insert(0, existing_data[5])
            self.form_fields['department'].insert(0, existing_data[6])
            self.purp_text.insert("1.0", existing_data[7])

    def save_visitor(self, visitor_id=None):
        data = {
            'fullname': self.form_fields['fullname'].get().strip(),
            'email': self.form_fields['email'].get().strip(),
            'phone': self.form_fields['phone'].get().strip(),
            'department': self.form_fields['department'].get().strip(),
            'meeting_with': self.form_fields['meeting_with'].get().strip(),
            'address': self.addr_text.get("1.0", tk.END).strip(),
            'purpose': self.purp_text.get("1.0", tk.END).strip(),
        }
        
        # Basic Validation
        if not data['fullname'] or not data['phone']:
            messagebox.showwarning("Missing Data", "Full Name and Phone are required.")
            return

        if visitor_id:
            DatabaseManager.update_visitor(visitor_id, data)
            messagebox.showinfo("Success", "Visitor Updated Successfully")
            self.show_manage_visitors()
        else:
            DatabaseManager.add_visitor(data)
            messagebox.showinfo("Success", "Visitor Added Successfully")
            # Clear form
            self.show_new_visitor()

    # ================= MANAGE VISITORS =================
    def show_manage_visitors(self):
        self.clear_window()
        self.create_sidebar("Manage Visitors")
        main = self.create_main_area()
        
        # Header
        top_frame = tk.Frame(main, bg=Theme.BG_PRIMARY)
        top_frame.pack(fill=tk.X, padx=40, pady=40)
        
        tk.Label(top_frame, text="Manage Visitors", font=Theme.FONT_HEADER, bg=Theme.BG_PRIMARY, fg="white").pack(side=tk.LEFT)
        
        # Filter Bar
        filter_frame = tk.Frame(main, bg=Theme.BG_PRIMARY)
        filter_frame.pack(fill=tk.X, padx=40, pady=(0, 20))
        
        tk.Label(filter_frame, text="From:", bg=Theme.BG_PRIMARY, fg="white").pack(side=tk.LEFT)
        self.date_from = StyledEntry(filter_frame, width=15)
        self.date_from.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_from.pack(side=tk.LEFT, padx=10)
        
        tk.Label(filter_frame, text="To:", bg=Theme.BG_PRIMARY, fg="white").pack(side=tk.LEFT)
        self.date_to = StyledEntry(filter_frame, width=15)
        self.date_to.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_to.pack(side=tk.LEFT, padx=10)
        
        StyledButton(filter_frame, text="Filter", width=10, command=self.load_table_data).pack(side=tk.LEFT, padx=10)

        # Action Buttons
        StyledButton(filter_frame, text="Delete Selected", width=15, bg=Theme.ERROR, command=self.delete_selected).pack(side=tk.RIGHT)
        StyledButton(filter_frame, text="Edit Selected", width=15, bg=Theme.WARNING, command=self.edit_selected).pack(side=tk.RIGHT, padx=10)

        # Table
        table_frame = tk.Frame(main, bg=Theme.BG_SECONDARY)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=(0, 40))
        
        columns = ("id", "name", "email", "phone", "date", "dept")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # Config Columns
        cols_config = [
            ("id", "ID", 50),
            ("name", "Full Name", 150),
            ("email", "Email", 200),
            ("phone", "Phone", 120),
            ("date", "Date Time", 150),
            ("dept", "Department", 100)
        ]
        
        for col, text, width in cols_config:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width)

        # Scrollbar
        sb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=sb.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.load_table_data()

    def load_table_data(self):
        # Clear
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        filters = {
            'from': self.date_from.get(),
            'to': self.date_to.get()
        }
        
        try:
            rows = DatabaseManager.get_visitors(filters)
            for row in rows:
                # row: id, fullname, email, phone, created_at, meeting_with, department
                # tree expects: id, name, email, phone, date, dept
                self.tree.insert("", tk.END, values=(row[0], row[1], row[2], row[3], row[4], row[6]))
        except Exception:
            # Fallback if date is invalid, load all
            rows = DatabaseManager.get_visitors()
            for row in rows:
                self.tree.insert("", tk.END, values=(row[0], row[1], row[2], row[3], row[4], row[6]))

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "No visitor selected")
            return
            
        if messagebox.askyesno("Confirm", "Delete selected visitor?"):
            visitor_id = self.tree.item(selected[0])['values'][0]
            DatabaseManager.delete_visitor(visitor_id)
            self.load_table_data()
            messagebox.showinfo("Success", "Visitor deleted")

    def edit_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "No visitor selected")
            return
            
        visitor_id = self.tree.item(selected[0])['values'][0]
        data = DatabaseManager.get_visitor_by_id(visitor_id)
        if data:
            self.show_new_visitor(data)

if __name__ == "__main__":
    root = tk.Tk()
    app = VMSApplication(root)
    root.mainloop()

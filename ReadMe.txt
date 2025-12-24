#  Visitor Management System (VMS)

A modern, user-friendly desktop application designed to streamline visitor tracking. Built with **Python** and **Tkinter**, this system offers a professional "plug-and-play" experience for managing guests, contractors, and clients without the need for complex server configurations.

---

##  Features

* **Secure Authentication:** Built-in login system using `hashlib` for secure credential handling.
* **Full CRUD Operations:** Add, view, edit, and delete visitor records with ease.
* **Modern UI:** A sleek, responsive dark-themed interface designed for low eye strain during long shifts.
* **Data Persistence:** Uses **SQLite3**, creating a local `vms.db` file automatically—no database setup required.
* **Reporting:** Built-in statistics and reporting tools to track visitor traffic and patterns.

---

##  Getting Started

### Prerequisites
- **Python 3.6 or higher**
- **Tkinter** (usually bundled with Python)
- **SQLite3** (standard Python library)

### Installation
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/johndydyyy/Visitor-Management-System.git](https://github.com/johndydyyy/Visitor-Management-System.git)
   cd Visitor-Management-System
2. Verify Dependencies:Run the following command to ensure your environment is ready:Bashpython -c "import tkinter; import sqlite3; import datetime; import hashlib; print('All required modules are installed!')"
3. Running the AppExecute the main application script:Bashpython vms_app.py
4. Default CredentialsFieldValueUsernameadminPasswordadmin123Note: For security, please change the default password immediately after your first login.

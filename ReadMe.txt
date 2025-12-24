# Visitor Management System (VMS)
=============================
This Visitor Management System (VMS) is a lightweight, local-first desktop solution designed to streamline how organizations track guests, contractors, and clients. By leveraging Python’s Tkinter for the interface and SQLite for data storage, it offers a professional "plug-and-play" experience without the need for complex server configurations.

![Image](https://github.com/johndydyyy/Visitor-Management-System/blob/e6a6e89eb4b8dee96441472a9060f44519cb2796/Screenshot%202025-12-24%20191620.png)

A modern, user-friendly desktop application for managing visitors, built with Python and Tkinter.

Prerequisites
------------
- Python 3.6 or higher
- Tkinter (usually comes with Python)
- SQLite3 (included in Python standard library)

Installation
------------
1. Make sure you have Python installed on your system.
2. Verify the required Python modules are installed by running:
   ```
   python -c "import tkinter; import sqlite3; import datetime; import hashlib; print('All required modules are installed!')"
   ```
   If you see any errors, install the missing packages using pip.

Running the Application
----------------------
1. Open a terminal/command prompt
2. Navigate to the directory containing vms_app.py
3. Run the application with Python:
   ```
   python vms_app.py
   ```

Features
--------
- User authentication
- Add, edit, and delete visitor records
- View visitor statistics and reports
- Modern, responsive UI with dark theme
- Data persistence using SQLite database

Default Login Credentials
-----------------------
- Username: admin
- Password: admin123

Note: Please change the default password after first login for security.

Database
--------
- The application uses SQLite and will automatically create a 'vms.db' file in the same directory.
- No additional database setup is required.

Troubleshooting
--------------
- If you encounter any issues, ensure all required Python modules are installed.
- Make sure you have write permissions in the application directory.
- The application requires a display to run (it's a GUI application).

![Image](https://github.com/johndydyyy/Visitor-Management-System/blob/e6a6e89eb4b8dee96441472a9060f44519cb2796/Screenshot%202025-12-24%20191634.png)
![Image](https://github.com/johndydyyy/Visitor-Management-System/blob/e6a6e89eb4b8dee96441472a9060f44519cb2796/Screenshot%202025-12-24%20191652.png)
![Image](https://github.com/johndydyyy/Visitor-Management-System/blob/e6a6e89eb4b8dee96441472a9060f44519cb2796/Screenshot%202025-12-24%20191704.png)





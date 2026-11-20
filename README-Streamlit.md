# AquaFlow — Streamlit Application

This folder contains a Streamlit interface for the existing AquaFlow Smart Water Issue Monitoring and Management System.

## Features

### Building Captain
- Secure login with the existing password-hash verification
- View water status by building
- Submit a water complaint with an optional image
- View personal complaint history and progress updates
- Read announcements
- View system reports

### Administrator
- Secure login with role verification
- View system reports
- View complaints and update their status
- View complaint image attachments
- Update water status for buildings
- Publish announcements

## Important database requirement

The Streamlit application uses the same MySQL database as the Tkinter application:

- Database: `smart_water_db`
- Tables used: `Users`, `Buildings`, `Water_Status`, `Complaints`, `Complaint_Updates`, `Announcements`

The database and its tables must already exist. This project ZIP did not include a SQL database export or schema file, so the app does not create or alter tables automatically.

## 1. Install Python packages

Open a terminal in this project folder and run:

```bash
python -m pip install -r requirements-streamlit.txt
```

## 2. Configure MySQL credentials

The app reads credentials from environment variables. In PowerShell, set them for the current terminal session:

```powershell
$env:DB_HOST="localhost"
$env:DB_USER="root"
$env:DB_PASSWORD="YOUR_MYSQL_PASSWORD"
$env:DB_NAME="smart_water_db"
$env:DB_PORT="3306"
```

Replace `YOUR_MYSQL_PASSWORD` with your actual MySQL password. Do not commit passwords to GitHub.

Alternatively, Streamlit secrets can be configured in `.streamlit/secrets.toml`:

```toml
[mysql]
host = "localhost"
user = "root"
password = "YOUR_MYSQL_PASSWORD"
database = "smart_water_db"
port = 3306
```

Keep `secrets.toml` private and add it to `.gitignore` before pushing to GitHub.

## 3. Run the Streamlit application

```bash
python -m streamlit run streamlit_app.py
```

Streamlit will show a local address in the terminal, usually `http://localhost:8501`.

## 4. Login

Use the existing user IDs and passwords stored in your `Users` table. Select the matching role:
- Building Captain
- Admin

The app uses the password hash format and verification method from the existing Tkinter application.

## Notes and limitations to verify

1. The original application stores complaint image paths in MySQL. The Streamlit version saves uploaded images into an `uploads` folder and stores the resulting path. Keep this folder with the app when using local storage.
2. For deployment on another computer or a cloud host, local image paths may not be accessible. A shared storage service or storing image data in the database would be needed for that deployment.
3. The `Water_Status` update feature expects one existing row for each building, matching the original Tkinter implementation.
4. Test the app against a backup or test copy of the database before using it with important records.

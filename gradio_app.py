
import os
import hashlib
import hmac
import shutil
import uuid
from pathlib import Path

import gradio as gr
import mysql.connector


# ============================================================
# 1. APPLICATION SETTINGS
# ============================================================

APP_TITLE = "AquaFlow - Smart Water Management"

NAVY = "#123B5D"
DARK_BLUE = "#154C79"
OCEAN_BLUE = "#2471A3"
AQUA = "#48CAE4"
LIGHT_BLUE = "#D6EAF8"
PALE_BLUE = "#EDF6FC"
WHITE = "#FFFFFF"
TEXT = "#263B4D"
MUTED = "#718096"
BORDER = "#C8DCE9"

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


# ============================================================
# 2. DATABASE CONNECTION
# ============================================================

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "smart_water_db"),
        port=int(os.getenv("DB_PORT", "3306"))
    )


def run_query(query, params=None, fetch="all"):
    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute(query, params or ())

        if fetch == "one":
            result = cursor.fetchone()
        else:
            result = cursor.fetchall()

        cursor.close()
        return result

    finally:
        connection.close()


def run_change(query, params=None):
    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute(query, params or ())
        connection.commit()
        return cursor.rowcount

    except Exception:
        connection.rollback()
        raise

    finally:
        if cursor:
            cursor.close()
        connection.close()


def to_table(rows):
    return [list(row) for row in rows] if rows else []


# ============================================================
# 3. PASSWORD VERIFICATION
# ============================================================

def verify_password(password, stored_hash):
    try:
        salt, saved_hash = stored_hash.split("$")

        calculated_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            bytes.fromhex(salt),
            600000
        ).hex()

        return hmac.compare_digest(
            calculated_hash,
            saved_hash
        )

    except (ValueError, AttributeError, TypeError):
        return False


# ============================================================
# 4. AUTHENTICATION
# ============================================================

def authenticate(login_id, password, selected_role):

    account = run_query(
        """
        SELECT user_id, full_name, password_hash, role
        FROM Users
        WHERE login_id = %s
        """,
        (login_id,),
        fetch="one"
    )

    if not account:
        return None, "User ID does not exist."

    user_id, full_name, stored_hash, database_role = account

    if not verify_password(password, stored_hash):
        return None, "Incorrect password."

    expected_role = (
        "Captain"
        if selected_role == "Building Captain"
        else "Admin"
    )

    if database_role != expected_role:
        return None, "Selected role does not match your account."

    return {
        "user_id": user_id,
        "full_name": full_name,
        "role": database_role
    }, None


def login_action(login_id, password, role):

    if not login_id or not password:
        return (
            None,
            "Please enter your User ID and password.",
            gr.update(visible=True),
            gr.update(visible=False),
            "",
            gr.update(visible=False),
            gr.update(visible=False)
        )

    try:
        user, error = authenticate(
            login_id.strip(),
            password,
            role
        )

        if error:
            return (
                None,
                error,
                gr.update(visible=True),
                gr.update(visible=False),
                "",
                gr.update(visible=False),
                gr.update(visible=False)
            )

        is_captain = user["role"] == "Captain"

        welcome_message = (
            f"**Welcome, {user['full_name']}!** "
            f"| {'BUILDING CAPTAIN' if is_captain else 'ADMINISTRATOR'}"
        )

        return (
            user,
            "Login successful.",
            gr.update(visible=False),
            gr.update(visible=True),
            welcome_message,
            gr.update(visible=is_captain),
            gr.update(visible=not is_captain)
        )

    except Exception as error:
        return (
            None,
            f"Login error: {error}",
            gr.update(visible=True),
            gr.update(visible=False),
            "",
            gr.update(visible=False),
            gr.update(visible=False)
        )


def logout_action():

    return (
        None,
        gr.update(visible=True),
        gr.update(visible=False),
        "You have been logged out.",
        gr.update(visible=False),
        gr.update(visible=False)
    )


# ============================================================
# 5. COMMON DATABASE FUNCTIONS
# ============================================================

def get_buildings():

    rows = run_query(
        """
        SELECT building_name
        FROM Buildings
        ORDER BY building_id
        """
    )

    return [row[0] for row in rows]


def get_water_status():

    return run_query(
        """
        SELECT
            Buildings.building_name,
            Water_Status.status,
            Water_Status.remarks,
            Water_Status.updated_at
        FROM Buildings
        LEFT JOIN Water_Status
            ON Buildings.building_id = Water_Status.building_id
        ORDER BY Buildings.building_id
        """
    )


def get_announcements():

    return run_query(
        """
        SELECT title, message, created_at
        FROM Announcements
        ORDER BY created_at DESC
        """
    )


def get_all_complaints():

    return run_query(
        """
        SELECT
            Complaints.complaint_id,
            Users.full_name,
            Buildings.building_name,
            Complaints.issue_type,
            Complaints.description,
            Complaints.created_at,
            Complaints.status
        FROM Complaints
        INNER JOIN Users
            ON Complaints.user_id = Users.user_id
        INNER JOIN Buildings
            ON Complaints.building_id = Buildings.building_id
        ORDER BY Complaints.created_at DESC
        """
    )


def get_captain_complaints(user_id):

    return run_query(
        """
        SELECT
            Complaints.complaint_id,
            Buildings.building_name,
            Complaints.issue_type,
            Complaints.description,
            Complaints.created_at,
            Complaints.status
        FROM Complaints
        INNER JOIN Buildings
            ON Complaints.building_id = Buildings.building_id
        WHERE Complaints.user_id = %s
        ORDER BY Complaints.created_at DESC
        """,
        (user_id,)
    )


def format_water_table(rows):

    result = []

    for row in rows:
        result.append([
            row[0],
            row[1] or "Not Updated",
            row[2] or "No remarks",
            str(row[3]) if row[3] else "Not Available"
        ])

    return result


# ============================================================
# 6. WATER STATUS
# ============================================================

def water_status_action():

    try:
        return (
            format_water_table(get_water_status()),
            "Water status loaded successfully."
        )

    except Exception as error:
        return [], f"Unable to load water status: {error}"


# ============================================================
# 7. CAPTAIN - SUBMIT COMPLAINT
# ============================================================

def submit_complaint_action(
    user,
    building,
    issue,
    description,
    photo
):

    if not user or user.get("role") != "Captain":
        return "Please log in using a Building Captain account."

    if not building or not issue or not description or not description.strip():
        return "Please complete all required fields."

    try:

        building_row = run_query(
            """
            SELECT building_id
            FROM Buildings
            WHERE building_name = %s
            """,
            (building,),
            fetch="one"
        )

        if not building_row:
            return "Selected building was not found."

        photo_path = None

        if photo:

            source = Path(photo)

            if not source.is_file():
                return "The selected picture could not be found."

            extension = source.suffix.lower()

            filename = (
                f"{user['user_id']}_{uuid.uuid4().hex}{extension}"
            )

            destination = UPLOAD_DIR / filename

            shutil.copy2(source, destination)

            photo_path = str(destination.resolve())

        run_change(
            """
            INSERT INTO Complaints
            (
                user_id,
                building_id,
                issue_type,
                description,
                photo_path
            )
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                user["user_id"],
                building_row[0],
                issue,
                description.strip(),
                photo_path
            )
        )

        return "Complaint submitted successfully!"

    except Exception as error:
        return f"Unable to submit complaint: {error}"


# ============================================================
# 8. CAPTAIN - ALL COMPLAINTS
# ============================================================

def captain_all_complaints(user):

    if not user or user.get("role") != "Captain":
        return [], "Please log in again."

    try:

        rows = run_query(
            """
            SELECT
                Complaints.complaint_id,
                Buildings.building_name,
                Complaints.issue_type,
                Complaints.description,
                Complaints.created_at,
                Complaints.status
            FROM Complaints
            INNER JOIN Buildings
                ON Complaints.building_id = Buildings.building_id
            ORDER BY Complaints.created_at DESC
            """
        )

        return to_table(rows), "Complaints loaded successfully."

    except Exception as error:
        return [], f"Error: {error}"


# ============================================================
# 9. CAPTAIN - COMPLAINT HISTORY
# ============================================================

def captain_history_action(user):

    if not user or user.get("role") != "Captain":
        return [], gr.update(choices=[], value=None), "Please log in again."

    try:

        rows = get_captain_complaints(user["user_id"])

        choices = [str(row[0]) for row in rows]

        return (
            to_table(rows),
            gr.update(choices=choices, value=None),
            f"Loaded {len(rows)} complaint(s)."
        )

    except Exception as error:

        return (
            [],
            gr.update(choices=[], value=None),
            f"Error: {error}"
        )


def captain_updates_action(complaint_id, user):

    if not user or user.get("role") != "Captain":
        return [], "Please log in again."

    if not complaint_id:
        return [], "Please select a complaint ID."

    try:

        own_complaint = run_query(
            """
            SELECT complaint_id
            FROM Complaints
            WHERE complaint_id = %s AND user_id = %s
            """,
            (int(complaint_id), user["user_id"]),
            fetch="one"
        )

        if not own_complaint:
            return [], "This complaint does not belong to your account."

        rows = run_query(
            """
            SELECT
                Complaint_Updates.status,
                Complaint_Updates.remarks,
                Users.full_name,
                Complaint_Updates.updated_at
            FROM Complaint_Updates
            INNER JOIN Users
                ON Complaint_Updates.updated_by = Users.user_id
            WHERE Complaint_Updates.complaint_id = %s
            ORDER BY Complaint_Updates.updated_at DESC
            """,
            (int(complaint_id),)
        )

        if not rows:
            return [], "No progress updates have been recorded yet."

        return to_table(rows), "Complaint updates loaded."

    except Exception as error:
        return [], f"Error: {error}"


# ============================================================
# 10. ANNOUNCEMENTS
# ============================================================

def announcement_table_action():

    try:

        rows = get_announcements()

        result = [
            [row[0], row[1], str(row[2]) if row[2] else ""]
            for row in rows
        ]

        return result, "Announcements loaded."

    except Exception as error:
        return [], f"Error: {error}"


# ============================================================
# 11. ADMIN - COMPLAINT MANAGEMENT
# ============================================================

def admin_complaints_action(user):

    if not user or user.get("role") != "Admin":
        return [], gr.update(choices=[], value=None), "Administrator access required."

    try:

        rows = get_all_complaints()

        choices = [str(row[0]) for row in rows]

        return (
            to_table(rows),
            gr.update(choices=choices, value=None),
            f"Loaded {len(rows)} complaint(s)."
        )

    except Exception as error:

        return (
            [],
            gr.update(choices=[], value=None),
            f"Error: {error}"
        )


def admin_update_complaint(user, complaint_id, status, remarks):

    if not user or user.get("role") != "Admin":
        return "Administrator access is required."

    if not complaint_id:
        return "Please select a complaint."

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE Complaints
            SET status = %s
            WHERE complaint_id = %s
            """,
            (status, int(complaint_id))
        )

        if cursor.rowcount == 0:
            connection.rollback()
            return "Complaint ID was not found."

        cursor.execute(
            """
            INSERT INTO Complaint_Updates
            (
                complaint_id,
                updated_by,
                status,
                remarks
            )
            VALUES (%s, %s, %s, %s)
            """,
            (
                int(complaint_id),
                user["user_id"],
                status,
                (remarks or "").strip()
            )
        )

        connection.commit()

        return "Complaint updated successfully!"

    except Exception as error:

        if connection:
            connection.rollback()

        return f"Unable to update complaint: {error}"

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


def admin_picture_action(complaint_id, user):

    if not user or user.get("role") != "Admin":
        return None, "Administrator access is required."

    if not complaint_id:
        return None, "Please select a complaint."

    try:

        result = run_query(
            """
            SELECT photo_path
            FROM Complaints
            WHERE complaint_id = %s
            """,
            (int(complaint_id),),
            fetch="one"
        )

        if not result or not result[0]:
            return None, "This complaint has no attached picture."

        photo_path = result[0]

        if not os.path.isfile(photo_path):
            return None, "Attached picture could not be found."

        return photo_path, "Attached picture loaded."

    except Exception as error:
        return None, f"Error: {error}"


# ============================================================
# 12. ADMIN - UPDATE WATER STATUS
# ============================================================

def admin_update_water(user, building, status, remarks):

    if not user or user.get("role") != "Admin":
        return "Administrator access is required."

    if not building or not status:
        return "Please select a building and water status."

    try:

        building_row = run_query(
            """
            SELECT building_id
            FROM Buildings
            WHERE building_name = %s
            """,
            (building,),
            fetch="one"
        )

        if not building_row:
            return "Selected building was not found."

        building_id = building_row[0]

        connection = get_connection()
        cursor = connection.cursor()

        try:

            cursor.execute(
                """
                UPDATE Water_Status
                SET
                    status = %s,
                    remarks = %s,
                    updated_by = %s
                WHERE building_id = %s
                """,
                (
                    status,
                    (remarks or "").strip(),
                    user["user_id"],
                    building_id
                )
            )

            if cursor.rowcount == 0:

                cursor.execute(
                    """
                    INSERT INTO Water_Status
                    (
                        building_id,
                        status,
                        remarks,
                        updated_by
                    )
                    VALUES (%s, %s, %s, %s)
                    """,
                    (
                        building_id,
                        status,
                        (remarks or "").strip(),
                        user["user_id"]
                    )
                )

            connection.commit()

            return "Water status updated successfully!"

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()

    except Exception as error:
        return f"Unable to update water status: {error}"


# ============================================================
# 13. ADMIN - ANNOUNCEMENTS
# ============================================================

def admin_publish_announcement(user, title, message):

    if not user or user.get("role") != "Admin":
        return "Administrator access is required."

    if not title or not title.strip():
        return "Please enter an announcement title."

    if not message or not message.strip():
        return "Please enter an announcement message."

    try:

        run_change(
            """
            INSERT INTO Announcements
            (title, message, created_by)
            VALUES (%s, %s, %s)
            """,
            (
                title.strip(),
                message.strip(),
                user["user_id"]
            )
        )

        return "Announcement published successfully!"

    except Exception as error:
        return f"Unable to publish announcement: {error}"


# ============================================================
# 14. REPORTS
# ============================================================

def reports_action(user):

    if not user or user.get("role") not in ("Admin", "Captain"):
        return (
            0, 0, 0, 0,
            0, 0, 0,
            [],
            "Please log in again."
        )

    try:

        complaint_data = run_query(
            """
            SELECT
                COUNT(*),
                COUNT(CASE WHEN status = 'Pending' THEN 1 END),
                COUNT(CASE WHEN status = 'In Progress' THEN 1 END),
                COUNT(CASE WHEN status = 'Resolved' THEN 1 END)
            FROM Complaints
            """,
            fetch="one"
        )

        water_data = run_query(
            """
            SELECT
                COUNT(CASE WHEN status = 'Available' THEN 1 END),
                COUNT(CASE WHEN status = 'Low Supply' THEN 1 END),
                COUNT(CASE WHEN status = 'No Water' THEN 1 END)
            FROM Water_Status
            """,
            fetch="one"
        )

        buildings = get_water_status()

        return (
            complaint_data[0] or 0,
            complaint_data[1] or 0,
            complaint_data[2] or 0,
            complaint_data[3] or 0,
            water_data[0] or 0,
            water_data[1] or 0,
            water_data[2] or 0,
            format_water_table(buildings),
            "Reports refreshed successfully."
        )

    except Exception as error:

        return (
            0, 0, 0, 0,
            0, 0, 0,
            [],
            f"Unable to load reports: {error}"
        )


# ============================================================
# 15. NAVIGATION
# ============================================================

def change_captain_page(page):

    pages = [
        "Dashboard",
        "Water Status",
        "Submit Complaint",
        "All Complaints",
        "Complaint History",
        "Announcements",
        "Management Reports"
    ]

    return [
        gr.update(visible=(page == name))
        for name in pages
    ]


def change_admin_page(page):

    pages = [
        "Dashboard",
        "Manage Complaints",
        "Update Water Status",
        "Manage Announcements",
        "View Reports"
    ]

    return [
        gr.update(visible=(page == name))
        for name in pages
    ]


# ============================================================
# 16. BUILDING OPTIONS
# ============================================================

def initial_buildings():

    try:

        options = get_buildings()
        selected = options[0] if options else None

        return (
            gr.update(choices=options, value=selected),
            gr.update(choices=options, value=selected)
        )

    except Exception:

        return (
            gr.update(choices=[], value=None),
            gr.update(choices=[], value=None)
        )


# ============================================================
# 17. DESIGN - CSS
# ============================================================

CSS = """
html, body, .gradio-container {
    background: #EDF6FC !important;
    color: #263B4D !important;
    font-family: Arial, sans-serif !important;
}

.gradio-container {
    max-width: 100% !important;
    width: 100% !important;
    padding: 16px !important;
}

footer {
    display: none !important;
}

#application {
    width: 100% !important;
    max-width: 100% !important;
}

h1, h2, h3, h4 {
    color: #123B5D !important;
}

p {
    color: #526579 !important;
}

/* Login */

.login-panel {
    background: #FFFFFF !important;
    border: 1px solid #C8DCE9 !important;
    border-radius: 10px !important;
    padding: 25px !important;
    box-shadow: 0 3px 12px rgba(18,59,93,0.07) !important;
}

/* Header */

#top-header {
    background: #FFFFFF !important;
    border: 1px solid #C8DCE9 !important;
    border-radius: 10px !important;
    padding: 12px 20px !important;
    margin-bottom: 15px !important;
}

/* Sidebar */

.sidebar {
    background: #123B5D !important;
    border-radius: 10px !important;
    padding: 18px 12px !important;
    min-height: 690px !important;
    max-width: 245px !important;
}

.sidebar h1,
.sidebar h2,
.sidebar h3,
.sidebar p,
.sidebar label,
.sidebar span {
    color: #FFFFFF !important;
}

.sidebar-brand {
    text-align: center !important;
    padding: 10px 5px 22px !important;
    border-bottom: 1px solid #36546C !important;
    margin-bottom: 18px !important;
}

.sidebar-brand h2 {
    color: #FFFFFF !important;
    font-size: 25px !important;
}

.sidebar-brand p {
    color: #48CAE4 !important;
    font-size: 10px !important;
    letter-spacing: 1.5px !important;
}

/* Navigation */

#captain-navigation,
#admin-navigation {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

#captain-navigation label,
#admin-navigation label {
    background: transparent !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 7px !important;
    padding: 12px 10px !important;
    margin: 4px 0 !important;
    cursor: pointer !important;
}

#captain-navigation label span,
#admin-navigation label span {
    color: #FFFFFF !important;
}

#captain-navigation label:hover,
#admin-navigation label:hover {
    background: #154C79 !important;
}

#captain-navigation label:has(input:checked),
#admin-navigation label:has(input:checked) {
    background: #2471A3 !important;
    border-left: 4px solid #48CAE4 !important;
}

/* Content */

.content-area {
    min-width: 0 !important;
    padding: 5px 8px 20px 18px !important;
    background: transparent !important;
}

/* Page panels */

.page-panel {
    background: #FFFFFF !important;
    border: 1px solid #C8DCE9 !important;
    border-radius: 10px !important;
    padding: 24px !important;
    min-height: 580px !important;
    box-shadow: 0 2px 8px rgba(18,59,93,0.05) !important;
}

/* Dashboard cards */

.dashboard-card {
    background: #EDF6FC !important;
    border: 1px solid #C8DCE9 !important;
    border-left: 4px solid #2471A3 !important;
    border-radius: 8px !important;
    padding: 18px !important;
    min-height: 115px !important;
    margin-bottom: 10px !important;
}

.dashboard-card h3 {
    color: #123B5D !important;
    font-size: 16px !important;
}

.dashboard-card p {
    color: #526579 !important;
    font-size: 13px !important;
    line-height: 1.6 !important;
}

/* Inputs */

.gradio-container input,
.gradio-container textarea,
.gradio-container select {
    background: #FFFFFF !important;
    color: #263B4D !important;
    -webkit-text-fill-color: #263B4D !important;
    border: 1px solid #C8DCE9 !important;
    border-radius: 6px !important;
    opacity: 1 !important;
}

.gradio-container input::placeholder,
.gradio-container textarea::placeholder {
    color: #8494A4 !important;
    -webkit-text-fill-color: #8494A4 !important;
    opacity: 1 !important;
}

/* Buttons */

.gradio-container button {
    border-radius: 7px !important;
    font-weight: 600 !important;
}

.gradio-container button.primary {
    background: #2471A3 !important;
    color: #FFFFFF !important;
    border: none !important;
}

.gradio-container button.primary:hover {
    background: #154C79 !important;
}

.gradio-container button.stop {
    background: #D9534F !important;
    color: #FFFFFF !important;
}

/* Tables */

.gradio-container table {
    width: 100% !important;
    border-collapse: collapse !important;
}

.gradio-container table th {
    background: #D6EAF8 !important;
    color: #123B5D !important;
    padding: 12px !important;
}

.gradio-container table td {
    background: #FFFFFF !important;
    color: #263B4D !important;
    padding: 10px !important;
    border-bottom: 1px solid #E2EDF4 !important;
}

/* Responsive */

@media (max-width: 850px) {
    .gradio-container {
        padding: 8px !important;
    }

    .sidebar {
        max-width: 100% !important;
        min-height: auto !important;
    }

    .content-area {
        padding: 10px 0 !important;
    }

    .page-panel {
        padding: 14px !important;
    }
}
"""


# ============================================================
# 18. MAIN GRADIO APPLICATION
# ============================================================

with gr.Blocks(title=APP_TITLE, css=CSS) as demo:

    user_state = gr.State(None)

    # --------------------------------------------------------
    # LOGIN SCREEN
    # --------------------------------------------------------

    with gr.Group(visible=True) as login_group:

        gr.HTML("""
        <div style="text-align:center;padding:18px;margin-bottom:12px">
            <h1 style="color:#123B5D;font-size:32px;margin:0">
                💧 AquaFlow
            </h1>
            <p style="color:#718096;font-size:12px;letter-spacing:2px">
                SMART WATER ISSUE MONITORING AND MANAGEMENT SYSTEM
            </p>
        </div>
        """)

        with gr.Row(equal_height=True):

            with gr.Column(scale=5, min_width=300):

                gr.HTML("""
                <div style="
                    min-height:520px;
                    background:linear-gradient(145deg,#123B5D,#154C79,#2471A3);
                    color:white;
                    text-align:center;
                    padding:65px 25px;
                    border-radius:10px;
                ">
                    <div style="font-size:75px">💧</div>
                    <h1 style="color:white;font-size:36px">AquaFlow</h1>
                    <p style="color:#48CAE4;font-size:11px;
                    font-weight:bold;letter-spacing:2px">
                        SMART WATER MANAGEMENT
                    </p>
                    <hr style="border-color:#42647D;margin:30px">
                    <h2 style="color:white">Every Drop Matters</h2>
                    <p style="color:#D8F4FC;line-height:2">
                        Monitor Water Availability<br>
                        Report Water Issues<br>
                        Track Maintenance Progress
                    </p>
                    <p style="margin-top:45px;color:#BDEBFA">
                        Smarter monitoring for a better future.
                    </p>
                </div>
                """)

            with gr.Column(scale=5, min_width=300):

                with gr.Group(elem_classes=["login-panel"]):

                    gr.Markdown("## Welcome Back!")

                    gr.Markdown(
                        "Sign in to continue to your AquaFlow account."
                    )

                    login_id = gr.Textbox(
                        label="USER ID",
                        placeholder="Enter your user ID"
                    )

                    login_password = gr.Textbox(
                        label="PASSWORD",
                        type="password",
                        placeholder="Enter your password"
                    )

                    login_role = gr.Dropdown(
                        choices=["Building Captain", "Admin"],
                        value="Building Captain",
                        label="LOGIN AS"
                    )

                    login_button = gr.Button(
                        "SIGN IN",
                        variant="primary"
                    )

                    login_message = gr.Markdown()

                gr.HTML("""
                <p style="text-align:center;color:#718096;
                font-size:11px;margin-top:18px">
                    AQUAFLOW | SMART WATER ISSUE MONITORING
                </p>
                """)

    # --------------------------------------------------------
    # MAIN APPLICATION
    # --------------------------------------------------------

    with gr.Group(visible=False, elem_id="application") as app_group:

        with gr.Row(elem_id="top-header", equal_height=True):

            welcome = gr.Markdown("**Welcome to AquaFlow**")

            logout_button = gr.Button(
                "LOG OUT",
                variant="stop",
                scale=0,
                min_width=120
            )

        # ====================================================
        # CAPTAIN INTERFACE
        # ====================================================

        with gr.Group(visible=False) as captain_group:

            with gr.Row(equal_height=False):

                with gr.Column(
                    scale=0,
                    min_width=245,
                    elem_classes=["sidebar"]
                ):

                    gr.HTML("""
                    <div class="sidebar-brand">
                        <div style="font-size:42px">💧</div>
                        <h2>AquaFlow</h2>
                        <p>BUILDING CAPTAIN</p>
                    </div>
                    """)

                    captain_nav = gr.Radio(
                        choices=[
                            "Dashboard",
                            "Water Status",
                            "Submit Complaint",
                            "All Complaints",
                            "Complaint History",
                            "Announcements",
                            "Management Reports"
                        ],
                        value="Dashboard",
                        show_label=False,
                        container=False,
                        elem_id="captain-navigation"
                    )

                with gr.Column(
                    scale=1,
                    min_width=400,
                    elem_classes=["content-area"]
                ):

                    # CAPTAIN DASHBOARD

                    with gr.Group(
                        visible=True,
                        elem_classes=["page-panel"]
                    ) as cap_home:

                        gr.Markdown("## Building Captain Dashboard")

                        gr.Markdown(
                            "Monitor water supply and manage water-related issues."
                        )

                        gr.HTML("""
                        <div style="
                            background:#D6EAF8;
                            border:1px solid #C8DCE9;
                            border-radius:8px;
                            padding:22px;
                            margin:12px 0 20px">
                            <h2 style="color:#123B5D">
                                Welcome to AquaFlow!
                            </h2>
                            <p style="color:#526579;line-height:1.8">
                                Use the navigation menu to check water
                                availability, report water problems and
                                follow the progress of your complaints.
                            </p>
                        </div>
                        """)

                        with gr.Row():

                            gr.HTML("""
                            <div class="dashboard-card">
                                <h3>01. Water Status</h3>
                                <p>Check water availability across buildings.</p>
                            </div>
                            """)

                            gr.HTML("""
                            <div class="dashboard-card">
                                <h3>02. Submit Complaint</h3>
                                <p>Report water-related problems.</p>
                            </div>
                            """)

                        with gr.Row():

                            gr.HTML("""
                            <div class="dashboard-card">
                                <h3>03. All Complaints</h3>
                                <p>Review submitted complaints.</p>
                            </div>
                            """)

                            gr.HTML("""
                            <div class="dashboard-card">
                                <h3>04. Complaint History</h3>
                                <p>Follow Admin updates.</p>
                            </div>
                            """)

                        with gr.Row():

                            gr.HTML("""
                            <div class="dashboard-card">
                                <h3>05. Announcements</h3>
                                <p>Read college announcements.</p>
                            </div>
                            """)

                            gr.HTML("""
                            <div class="dashboard-card">
                                <h3>06. Management Reports</h3>
                                <p>View water management reports.</p>
                            </div>
                            """)

                    # CAPTAIN WATER STATUS

                    with gr.Group(
                        visible=False,
                        elem_classes=["page-panel"]
                    ) as cap_water_page:

                        gr.Markdown("## Water Status")

                        gr.Markdown(
                            "View the latest water supply status for all buildings."
                        )

                        captain_water_btn = gr.Button(
                            "REFRESH WATER STATUS",
                            variant="primary"
                        )

                        captain_water_table = gr.Dataframe(
                            headers=[
                                "Building",
                                "Water Status",
                                "Remarks",
                                "Last Updated"
                            ],
                            interactive=False,
                            wrap=True
                        )

                        captain_water_msg = gr.Markdown()

                    # CAPTAIN SUBMIT COMPLAINT

                    with gr.Group(
                        visible=False,
                        elem_classes=["page-panel"]
                    ) as cap_submit_page:

                        gr.Markdown("## Submit Water Complaint")

                        gr.Markdown(
                            "Provide the details of the water-related problem."
                        )

                        cap_building = gr.Dropdown(
                            choices=[],
                            label="Select Building"
                        )

                        cap_issue = gr.Dropdown(
                            choices=[
                                "No Water",
                                "Low Water Pressure",
                                "Water Leakage",
                                "Dirty Water",
                                "Other"
                            ],
                            value="No Water",
                            label="Issue Type"
                        )

                        cap_description = gr.Textbox(
                            lines=5,
                            label="Describe the Problem",
                            placeholder="Explain the water issue..."
                        )

                        cap_photo = gr.File(
                            label="Attach Picture (Optional)",
                            file_types=[".png", ".jpg", ".jpeg", ".gif", ".bmp"],
                            type="filepath"
                        )

                        cap_submit = gr.Button(
                            "SUBMIT COMPLAINT",
                            variant="primary"
                        )

                        cap_submit_msg = gr.Markdown()

                    # CAPTAIN ALL COMPLAINTS

                    with gr.Group(
                        visible=False,
                        elem_classes=["page-panel"]
                    ) as cap_all_page:

                        gr.Markdown("## All Complaints")

                        gr.Markdown(
                            "View complaints submitted in the system."
                        )

                        all_cap_btn = gr.Button(
                            "REFRESH COMPLAINTS",
                            variant="primary"
                        )

                        all_cap_table = gr.Dataframe(
                            headers=[
                                "ID",
                                "Building",
                                "Issue",
                                "Description",
                                "Date",
                                "Status"
                            ],
                            interactive=False,
                            wrap=True
                        )

                        all_cap_msg = gr.Markdown()

                    # CAPTAIN HISTORY

                    with gr.Group(
                        visible=False,
                        elem_classes=["page-panel"]
                    ) as cap_history_page:

                        gr.Markdown("## Complaint History")

                        cap_history_btn = gr.Button(
                            "LOAD MY COMPLAINT HISTORY",
                            variant="primary"
                        )

                        cap_history_table = gr.Dataframe(
                            headers=[
                                "Complaint ID",
                                "Building",
                                "Issue",
                                "Description",
                                "Date",
                                "Status"
                            ],
                            interactive=False,
                            wrap=True
                        )

                        cap_history_msg = gr.Markdown()

                        gr.Markdown("### View Complaint Updates")

                        cap_update_id = gr.Dropdown(
                            choices=[],
                            label="Select Complaint ID"
                        )

                        cap_updates_btn = gr.Button(
                            "VIEW COMPLAINT UPDATES",
                            variant="primary"
                        )

                        cap_updates_table = gr.Dataframe(
                            headers=[
                                "Status",
                                "Remarks",
                                "Updated By",
                                "Updated At"
                            ],
                            interactive=False,
                            wrap=True
                        )

                        cap_updates_msg = gr.Markdown()

                    # CAPTAIN ANNOUNCEMENTS

                    with gr.Group(
                        visible=False,
                        elem_classes=["page-panel"]
                    ) as cap_ann_page:

                        gr.Markdown("## College Announcements")

                        cap_announcement_btn = gr.Button(
                            "REFRESH ANNOUNCEMENTS",
                            variant="primary"
                        )

                        cap_announcement_table = gr.Dataframe(
                            headers=["Title", "Message", "Published"],
                            interactive=False,
                            wrap=True
                        )

                        cap_announcement_msg = gr.Markdown()

                    # CAPTAIN REPORTS

                    with gr.Group(
                        visible=False,
                        elem_classes=["page-panel"]
                    ) as cap_reports_page:

                        gr.Markdown("## Management Reports")

                        report_btn_cap = gr.Button(
                            "REFRESH REPORTS",
                            variant="primary"
                        )

                        with gr.Row():
                            cap_total = gr.Number(
                                label="Total Complaints",
                                interactive=False
                            )
                            cap_pending = gr.Number(
                                label="Pending",
                                interactive=False
                            )

                        with gr.Row():
                            cap_progress = gr.Number(
                                label="In Progress",
                                interactive=False
                            )
                            cap_resolved = gr.Number(
                                label="Resolved",
                                interactive=False
                            )

                        with gr.Row():
                            cap_available = gr.Number(
                                label="Available",
                                interactive=False
                            )
                            cap_low = gr.Number(
                                label="Low Supply",
                                interactive=False
                            )
                            cap_none = gr.Number(
                                label="No Water",
                                interactive=False
                            )

                        gr.Markdown("### Building Water Status")

                        cap_report_table = gr.Dataframe(
                            headers=[
                                "Building",
                                "Status",
                                "Remarks",
                                "Updated"
                            ],
                            interactive=False,
                            wrap=True
                        )

                        cap_report_msg = gr.Markdown()

        # ====================================================
        # ADMIN INTERFACE
        # ====================================================

        with gr.Group(visible=False) as admin_group:

            with gr.Row(equal_height=False):

                with gr.Column(
                    scale=0,
                    min_width=245,
                    elem_classes=["sidebar"]
                ):

                    gr.HTML("""
                    <div class="sidebar-brand">
                        <div style="font-size:42px">💧</div>
                        <h2>AquaFlow</h2>
                        <p>ADMINISTRATOR</p>
                    </div>
                    """)

                    admin_nav = gr.Radio(
                        choices=[
                            "Dashboard",
                            "Manage Complaints",
                            "Update Water Status",
                            "Manage Announcements",
                            "View Reports"
                        ],
                        value="Dashboard",
                        show_label=False,
                        container=False,
                        elem_id="admin-navigation"
                    )

                with gr.Column(
                    scale=1,
                    min_width=400,
                    elem_classes=["content-area"]
                ):

                    # ADMIN DASHBOARD

                    with gr.Group(
                        visible=True,
                        elem_classes=["page-panel"]
                    ) as adm_home:

                        gr.Markdown("## Administrator Dashboard")

                        gr.Markdown(
                            "Manage water complaints, water supply and announcements."
                        )

                        gr.HTML("""
                        <div style="
                            background:#D6EAF8;
                            border:1px solid #C8DCE9;
                            border-radius:8px;
                            padding:22px;
                            margin:12px 0 20px">
                            <h2 style="color:#123B5D">
                                Welcome to AquaFlow!
                            </h2>
                            <p style="color:#526579;line-height:1.8">
                                Use the navigation menu to manage complaints,
                                update water availability, publish announcements
                                and monitor system reports.
                            </p>
                        </div>
                        """)

                        with gr.Row():

                            gr.HTML("""
                            <div class="dashboard-card">
                                <h3>01. Manage Complaints</h3>
                                <p>Review complaints and update repair progress.</p>
                            </div>
                            """)

                            gr.HTML("""
                            <div class="dashboard-card">
                                <h3>02. Update Water Status</h3>
                                <p>Update the supply status for each building.</p>
                            </div>
                            """)

                        with gr.Row():

                            gr.HTML("""
                            <div class="dashboard-card">
                                <h3>03. Manage Announcements</h3>
                                <p>Publish important notices and updates.</p>
                            </div>
                            """)

                            gr.HTML("""
                            <div class="dashboard-card">
                                <h3>04. View Reports</h3>
                                <p>Check complaint statistics and water status.</p>
                            </div>
                            """)

                    # ADMIN MANAGE COMPLAINTS

                    with gr.Group(
                        visible=False,
                        elem_classes=["page-panel"]
                    ) as adm_complaints_page:

                        gr.Markdown("## Manage Water Complaints")

                        admin_refresh_complaints = gr.Button(
                            "REFRESH COMPLAINTS",
                            variant="primary"
                        )

                        admin_complaint_table = gr.Dataframe(
                            headers=[
                                "ID",
                                "Reported By",
                                "Building",
                                "Issue",
                                "Description",
                                "Date",
                                "Status"
                            ],
                            interactive=False,
                            wrap=True
                        )

                        admin_complaint_msg = gr.Markdown()

                        gr.Markdown("### Update Selected Complaint")

                        admin_complaint_id = gr.Dropdown(
                            choices=[],
                            label="Select Complaint ID"
                        )

                        admin_status = gr.Dropdown(
                            choices=["Pending", "In Progress", "Resolved"],
                            value="Pending",
                            label="New Status"
                        )

                        admin_remarks = gr.Textbox(
                            lines=3,
                            label="Repair Remarks"
                        )

                        admin_save_complaint = gr.Button(
                            "SAVE UPDATE",
                            variant="primary"
                        )

                        admin_save_complaint_msg = gr.Markdown()

                        gr.Markdown("### Attached Complaint Picture")

                        admin_picture_btn = gr.Button(
                            "VIEW ATTACHED PICTURE",
                            variant="primary"
                        )

                        admin_picture = gr.Image(
                            label="Complaint Picture",
                            interactive=False
                        )

                        admin_picture_msg = gr.Markdown()

                    # ADMIN WATER STATUS

                    with gr.Group(
                        visible=False,
                        elem_classes=["page-panel"]
                    ) as adm_water_page:

                        gr.Markdown("## Update Water Status")

                        admin_building = gr.Dropdown(
                            choices=[],
                            label="Select Building"
                        )

                        admin_water_status = gr.Dropdown(
                            choices=["Available", "Low Supply", "No Water"],
                            value="Available",
                            label="Water Status"
                        )

                        admin_water_remarks = gr.Textbox(
                            lines=4,
                            label="Remarks"
                        )

                        admin_save_water = gr.Button(
                            "SAVE WATER STATUS",
                            variant="primary"
                        )

                        admin_save_water_msg = gr.Markdown()

                        gr.Markdown("### Current Water Status")

                        admin_water_refresh = gr.Button(
                            "REFRESH CURRENT STATUS",
                            variant="primary"
                        )

                        admin_water_table = gr.Dataframe(
                            headers=[
                                "Building",
                                "Water Status",
                                "Remarks",
                                "Last Updated"
                            ],
                            interactive=False,
                            wrap=True
                        )

                        admin_water_refresh_msg = gr.Markdown()

                    # ADMIN ANNOUNCEMENTS

                    with gr.Group(
                        visible=False,
                        elem_classes=["page-panel"]
                    ) as adm_ann_page:

                        gr.Markdown("## Manage Announcements")

                        gr.Markdown("### Create New Announcement")

                        ann_title = gr.Textbox(
                            label="Announcement Title"
                        )

                        ann_message = gr.Textbox(
                            lines=4,
                            label="Announcement Message"
                        )

                        ann_publish = gr.Button(
                            "PUBLISH ANNOUNCEMENT",
                            variant="primary"
                        )

                        ann_publish_msg = gr.Markdown()

                        gr.Markdown("### Published Announcements")

                        admin_ann_refresh = gr.Button(
                            "REFRESH PUBLISHED ANNOUNCEMENTS",
                            variant="primary"
                        )

                        admin_ann_table = gr.Dataframe(
                            headers=["Title", "Message", "Published"],
                            interactive=False,
                            wrap=True
                        )

                        admin_ann_refresh_msg = gr.Markdown()

                    # ADMIN REPORTS

                    with gr.Group(
                        visible=False,
                        elem_classes=["page-panel"]
                    ) as adm_reports_page:

                        gr.Markdown("## Smart Water System Reports")

                        admin_report_btn = gr.Button(
                            "REFRESH REPORTS",
                            variant="primary"
                        )

                        with gr.Row():
                            adm_total = gr.Number(
                                label="Total Complaints",
                                interactive=False
                            )
                            adm_pending = gr.Number(
                                label="Pending",
                                interactive=False
                            )

                        with gr.Row():
                            adm_progress = gr.Number(
                                label="In Progress",
                                interactive=False
                            )
                            adm_resolved = gr.Number(
                                label="Resolved",
                                interactive=False
                            )

                        with gr.Row():
                            adm_available = gr.Number(
                                label="Available",
                                interactive=False
                            )
                            adm_low = gr.Number(
                                label="Low Supply",
                                interactive=False
                            )
                            adm_none = gr.Number(
                                label="No Water",
                                interactive=False
                            )

                        gr.Markdown("### Building Water Status")

                        adm_report_table = gr.Dataframe(
                            headers=[
                                "Building",
                                "Status",
                                "Remarks",
                                "Updated"
                            ],
                            interactive=False,
                            wrap=True
                        )

                        adm_report_msg = gr.Markdown()

    # ========================================================
    # 19. LOGIN AND LOGOUT EVENTS
    # ========================================================

    login_button.click(
        fn=login_action,
        inputs=[login_id, login_password, login_role],
        outputs=[
            user_state,
            login_message,
            login_group,
            app_group,
            welcome,
            captain_group,
            admin_group
        ]
    )

    logout_button.click(
        fn=logout_action,
        inputs=None,
        outputs=[
            user_state,
            login_group,
            app_group,
            login_message,
            captain_group,
            admin_group
        ]
    )

    # ========================================================
    # 20. CAPTAIN NAVIGATION
    # ========================================================

    captain_nav.change(
        fn=change_captain_page,
        inputs=captain_nav,
        outputs=[
            cap_home,
            cap_water_page,
            cap_submit_page,
            cap_all_page,
            cap_history_page,
            cap_ann_page,
            cap_reports_page
        ]
    )

    # ========================================================
    # 21. ADMIN NAVIGATION
    # ========================================================

    admin_nav.change(
        fn=change_admin_page,
        inputs=admin_nav,
        outputs=[
            adm_home,
            adm_complaints_page,
            adm_water_page,
            adm_ann_page,
            adm_reports_page
        ]
    )

    # ========================================================
    # 22. CAPTAIN EVENTS
    # ========================================================

    captain_water_btn.click(
        fn=water_status_action,
        inputs=None,
        outputs=[
            captain_water_table,
            captain_water_msg
        ]
    )

    cap_submit.click(
        fn=submit_complaint_action,
        inputs=[
            user_state,
            cap_building,
            cap_issue,
            cap_description,
            cap_photo
        ],
        outputs=cap_submit_msg
    )

    all_cap_btn.click(
        fn=captain_all_complaints,
        inputs=user_state,
        outputs=[
            all_cap_table,
            all_cap_msg
        ]
    )

    cap_history_btn.click(
        fn=captain_history_action,
        inputs=user_state,
        outputs=[
            cap_history_table,
            cap_update_id,
            cap_history_msg
        ]
    )

    cap_updates_btn.click(
        fn=captain_updates_action,
        inputs=[
            cap_update_id,
            user_state
        ],
        outputs=[
            cap_updates_table,
            cap_updates_msg
        ]
    )

    cap_announcement_btn.click(
        fn=announcement_table_action,
        inputs=None,
        outputs=[
            cap_announcement_table,
            cap_announcement_msg
        ]
    )

    report_btn_cap.click(
        fn=reports_action,
        inputs=user_state,
        outputs=[
            cap_total,
            cap_pending,
            cap_progress,
            cap_resolved,
            cap_available,
            cap_low,
            cap_none,
            cap_report_table,
            cap_report_msg
        ]
    )

    # ========================================================
    # 23. ADMIN EVENTS
    # ========================================================

    admin_refresh_complaints.click(
        fn=admin_complaints_action,
        inputs=user_state,
        outputs=[
            admin_complaint_table,
            admin_complaint_id,
            admin_complaint_msg
        ]
    )

    admin_save_complaint.click(
        fn=admin_update_complaint,
        inputs=[
            user_state,
            admin_complaint_id,
            admin_status,
            admin_remarks
        ],
        outputs=admin_save_complaint_msg
    )

    admin_picture_btn.click(
        fn=admin_picture_action,
        inputs=[
            admin_complaint_id,
            user_state
        ],
        outputs=[
            admin_picture,
            admin_picture_msg
        ]
    )

    admin_save_water.click(
        fn=admin_update_water,
        inputs=[
            user_state,
            admin_building,
            admin_water_status,
            admin_water_remarks
        ],
        outputs=admin_save_water_msg
    )

    admin_water_refresh.click(
        fn=water_status_action,
        inputs=None,
        outputs=[
            admin_water_table,
            admin_water_refresh_msg
        ]
    )

    ann_publish.click(
        fn=admin_publish_announcement,
        inputs=[
            user_state,
            ann_title,
            ann_message
        ],
        outputs=ann_publish_msg
    )

    admin_ann_refresh.click(
        fn=announcement_table_action,
        inputs=None,
        outputs=[
            admin_ann_table,
            admin_ann_refresh_msg
        ]
    )

    admin_report_btn.click(
        fn=reports_action,
        inputs=user_state,
        outputs=[
            adm_total,
            adm_pending,
            adm_progress,
            adm_resolved,
            adm_available,
            adm_low,
            adm_none,
            adm_report_table,
            adm_report_msg
        ]
    )

    # ========================================================
    # 24. LOAD BUILDING OPTIONS
    # ========================================================

    demo.load(
        fn=initial_buildings,
        inputs=None,
        outputs=[
            cap_building,
            admin_building
        ]
    )


# ============================================================
# 25. RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    demo.launch(
        theme=gr.themes.Soft(
            primary_hue="blue",
            secondary_hue="cyan",
            neutral_hue="slate"
        ),
        inbrowser=True
    )

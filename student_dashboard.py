
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import sys

from database import create_connection


# ==========================================
# AQUAFLOW DESIGN SETTINGS
# ==========================================

NAVY = "#123B5D"
DARK_BLUE = "#154C79"
OCEAN_BLUE = "#2471A3"
AQUA = "#48CAE4"
LIGHT_BLUE = "#D6EAF8"
PALE_BLUE = "#EDF6FC"
BACKGROUND = "#F3F8FC"
WHITE = "#FFFFFF"
TEXT = "#263B50"
MUTED = "#718096"
GREEN = "#229954"
RED = "#C0392B"
ORANGE = "#D68910"


# ==========================================
# STYLE
# ==========================================

def setup_style():

    style = ttk.Style()

    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure(
        "Treeview",
        background=WHITE,
        foreground=TEXT,
        fieldbackground=WHITE,
        rowheight=35,
        font=("Arial", 10),
        borderwidth=0
    )

    style.configure(
        "Treeview.Heading",
        background=NAVY,
        foreground=WHITE,
        font=("Arial", 10, "bold"),
        padding=10,
        relief="flat"
    )

    style.map(
        "Treeview",
        background=[("selected", LIGHT_BLUE)],
        foreground=[("selected", NAVY)]
    )

    style.configure(
        "TCombobox",
        padding=7,
        font=("Arial", 10)
    )

    style.map(
        "TCombobox",
        fieldbackground=[("readonly", WHITE)],
        selectbackground=[("readonly", WHITE)],
        selectforeground=[("readonly", TEXT)]
    )


def make_button(parent, text, command, color=OCEAN_BLUE):

    button = tk.Button(
        parent,
        text=text,
        command=command,
        font=("Arial", 10, "bold"),
        bg=color,
        fg=WHITE,
        activebackground=DARK_BLUE,
        activeforeground=WHITE,
        relief="flat",
        bd=0,
        padx=16,
        pady=10,
        cursor="hand2"
    )

    button.bind(
        "<Enter>",
        lambda event: button.config(bg=DARK_BLUE)
    )

    button.bind(
        "<Leave>",
        lambda event: button.config(bg=color)
    )

    return button


def make_table(parent, columns, headings, widths):

    frame = tk.Frame(parent, bg=WHITE)

    frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=12
    )

    table = ttk.Treeview(
        frame,
        columns=columns,
        show="headings"
    )

    for column in columns:

        table.heading(
            column,
            text=headings[column]
        )

        table.column(
            column,
            width=widths[column],
            minwidth=70
        )

    vertical = ttk.Scrollbar(
        frame,
        orient="vertical",
        command=table.yview
    )

    horizontal = ttk.Scrollbar(
        frame,
        orient="horizontal",
        command=table.xview
    )

    table.configure(
        yscrollcommand=vertical.set,
        xscrollcommand=horizontal.set
    )

    table.grid(row=0, column=0, sticky="nsew")
    vertical.grid(row=0, column=1, sticky="ns")
    horizontal.grid(row=1, column=0, sticky="ew")

    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    return table


# ==========================================
# CAPTAIN DASHBOARD
# ==========================================

def open_captain_dashboard(full_name, user_id):

    dashboard = tk.Tk()

    dashboard.title("AquaFlow | Building Captain Dashboard")
    dashboard.geometry("1250x800")
    dashboard.minsize(950, 650)
    dashboard.configure(bg=BACKGROUND)

    setup_style()

    # ======================================
    # MAIN LAYOUT
    # ======================================

    sidebar = tk.Frame(
        dashboard,
        bg=NAVY,
        width=250
    )

    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    main_area = tk.Frame(
        dashboard,
        bg=BACKGROUND
    )

    main_area.pack(
        side="left",
        fill="both",
        expand=True
    )

    # ======================================
    # SIDEBAR BRANDING
    # ======================================

    tk.Label(
        sidebar,
        text="AquaFlow",
        font=("Arial", 26, "bold"),
        bg=NAVY,
        fg=WHITE
    ).pack(anchor="w", padx=25, pady=(32, 2))

    tk.Label(
        sidebar,
        text="SMART WATER MANAGEMENT",
        font=("Arial", 8, "bold"),
        bg=NAVY,
        fg="#A9D6F5"
    ).pack(anchor="w", padx=27, pady=(0, 25))

    tk.Frame(
        sidebar,
        bg="#426784",
        height=1
    ).pack(fill="x", padx=20, pady=5)

    tk.Label(
        sidebar,
        text="CAPTAIN MENU",
        font=("Arial", 9, "bold"),
        bg=NAVY,
        fg="#A9D6F5"
    ).pack(anchor="w", padx=25, pady=(20, 12))

    # ======================================
    # TOP BAR
    # ======================================

    topbar = tk.Frame(
        main_area,
        bg=WHITE,
        height=75
    )

    topbar.pack(fill="x")
    topbar.pack_propagate(False)

    tk.Label(
        topbar,
        text=f"Welcome, {full_name}!",
        font=("Arial", 19, "bold"),
        bg=WHITE,
        fg=NAVY
    ).pack(side="left", padx=28, pady=18)

    tk.Label(
        topbar,
        text="BUILDING CAPTAIN",
        font=("Arial", 9, "bold"),
        bg=WHITE,
        fg=OCEAN_BLUE
    ).pack(side="right", padx=28)

    # ======================================
    # PAGE TITLE AREA
    # ======================================

    title_area = tk.Frame(
        main_area,
        bg=BACKGROUND
    )

    title_area.pack(
        fill="x",
        padx=28,
        pady=(22, 8)
    )

    page_title = tk.Label(
        title_area,
        text="Dashboard Overview",
        font=("Arial", 21, "bold"),
        bg=BACKGROUND,
        fg=NAVY
    )

    page_title.pack(anchor="w")

    page_subtitle = tk.Label(
        title_area,
        text="Monitor water supply and manage water-related issues.",
        font=("Arial", 10),
        bg=BACKGROUND,
        fg=MUTED
    )

    page_subtitle.pack(anchor="w", pady=(4, 0))

    # ======================================
    # PAGE CONTENT AREA
    # ======================================

    content_holder = tk.Frame(
        main_area,
        bg=BACKGROUND
    )

    content_holder.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=5
    )

    current_page = {"name": "Dashboard"}
    animation_job = {"id": None}
    page_number = {"value": 0}
    navigation_buttons = {}

    # ======================================
    # PAGE HEADER
    # ======================================

    def section_label(parent, text):

        tk.Label(
            parent,
            text=text,
            font=("Arial", 12, "bold"),
            bg=BACKGROUND,
            fg=NAVY
        ).pack(anchor="w", padx=20, pady=(12, 0))

    # ======================================
    # 1. DASHBOARD HOME
    # ======================================

    def dashboard_home(parent):

        intro = tk.Frame(
            parent,
            bg=WHITE,
            padx=25,
            pady=22,
            highlightbackground="#DCE8F1",
            highlightthickness=1
        )

        intro.pack(fill="x", padx=12, pady=12)

        tk.Label(
            intro,
            text="Welcome to AquaFlow!",
            font=("Arial", 20, "bold"),
            bg=WHITE,
            fg=NAVY
        ).pack(anchor="w")

        tk.Label(
            intro,
            text=(
                "Use the menu to monitor water availability, "
                "report problems and follow maintenance progress."
            ),
            font=("Arial", 10),
            bg=WHITE,
            fg=MUTED,
            wraplength=750,
            justify="left"
        ).pack(anchor="w", pady=(8, 0))

        features = [

            (
                "01",
                "View Water Status",
                "Check water availability across all 12 buildings.",
                "Water Status",
                OCEAN_BLUE
            ),

            (
                "02",
                "Submit Water Complaint",
                "Report water leakage, low pressure or other problems.",
                "Submit Complaint",
                "#168A9B"
            ),

            (
                "03",
                "View All Complaints",
                "Review submitted complaints and attached pictures.",
                "All Complaints",
                "#3976A8"
            ),

            (
                "04",
                "Complaint History",
                "Follow Admin updates and repair progress.",
                "Complaint History",
                "#5277A5"
            ),

            (
                "05",
                "Announcements",
                "Read the latest college announcements.",
                "Announcements",
                "#287C83"
            ),

            (
                "06",
                "Management Reports",
                "View complaint statistics and water reports.",
                "Management Reports",
                "#245A83"
            )
        ]

        cards_frame = tk.Frame(
            parent,
            bg=BACKGROUND
        )

        cards_frame.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=5
        )

        for index, feature in enumerate(features):

            number, title, description, destination, accent = feature

            row = index // 2
            column = index % 2

            card = tk.Frame(
                cards_frame,
                bg=WHITE,
                padx=18,
                pady=15,
                highlightbackground="#DCE8F1",
                highlightthickness=1,
                cursor="hand2"
            )

            card.grid(
                row=row,
                column=column,
                padx=8,
                pady=8,
                sticky="nsew"
            )

            number_label = tk.Label(
                card,
                text=number,
                font=("Arial", 10, "bold"),
                bg=accent,
                fg=WHITE,
                padx=10,
                pady=5,
                cursor="hand2"
            )

            number_label.pack(anchor="w")

            title_label = tk.Label(
                card,
                text=title,
                font=("Arial", 12, "bold"),
                bg=WHITE,
                fg=NAVY,
                cursor="hand2"
            )

            title_label.pack(anchor="w", pady=(9, 4))

            description_label = tk.Label(
                card,
                text=description,
                font=("Arial", 9),
                bg=WHITE,
                fg=MUTED,
                wraplength=330,
                justify="left",
                cursor="hand2"
            )

            description_label.pack(anchor="w", pady=(0, 8))

            open_button = make_button(
                card,
                "OPEN",
                lambda name=destination: navigate(name),
                accent
            )

            open_button.pack(anchor="w")

            def open_card(event, name=destination):
                navigate(name)

            for clickable in (
                card,
                number_label,
                title_label,
                description_label
            ):

                clickable.bind(
                    "<Button-1>",
                    open_card
                )

            def card_enter(event, widget=card):
                widget.config(highlightbackground=AQUA)

            def card_leave(event, widget=card):
                widget.config(highlightbackground="#DCE8F1")

            card.bind("<Enter>", card_enter)
            card.bind("<Leave>", card_leave)

            for child in (
                number_label,
                title_label,
                description_label
            ):

                child.bind("<Enter>", card_enter)
                child.bind("<Leave>", card_leave)

        for column in range(2):

            cards_frame.grid_columnconfigure(
                column,
                weight=1
            )

        for row in range(3):

            cards_frame.grid_rowconfigure(
                row,
                weight=1
            )

    # ======================================
    # 2. VIEW WATER STATUS
    # ======================================

    def water_status_page(parent):

        connection = create_connection()

        if connection is None:

            messagebox.showerror(
                "Error",
                "Database connection failed.",
                parent=dashboard
            )

            return

        try:

            cursor = connection.cursor()

            # LEFT JOIN displays every building,
            # even when no water status exists.

            cursor.execute("""
                SELECT
                    Buildings.building_name,
                    Water_Status.status,
                    Water_Status.remarks
                FROM Buildings
                LEFT JOIN Water_Status
                    ON Buildings.building_id =
                       Water_Status.building_id
                ORDER BY Buildings.building_id
            """)

            buildings = cursor.fetchall()

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error),
                parent=dashboard
            )

            return

        finally:
            connection.close()

        info = tk.Frame(
            parent,
            bg=WHITE,
            padx=18,
            pady=14
        )

        info.pack(fill="x", padx=12, pady=10)

        tk.Label(
            info,
            text=f"{len(buildings)} Buildings",
            font=("Arial", 14, "bold"),
            bg=WHITE,
            fg=OCEAN_BLUE
        ).pack(anchor="w")

        tk.Label(
            info,
            text="Current water supply information",
            font=("Arial", 9),
            bg=WHITE,
            fg=MUTED
        ).pack(anchor="w", pady=(3, 0))

        table = make_table(
            parent,
            ("building", "status", "remarks"),
            {
                "building": "Building Name",
                "status": "Water Status",
                "remarks": "Remarks"
            },
            {
                "building": 230,
                "status": 180,
                "remarks": 450
            }
        )

        for building in buildings:

            table.insert(
                "",
                "end",
                values=(
                    building[0],
                    building[1] if building[1] else "Not Updated",
                    building[2] if building[2] else "No remarks"
                )
            )

        make_button(
            parent,
            "REFRESH WATER STATUS",
            lambda: navigate("Water Status")
        ).pack(pady=8)

    # ======================================
    # 3. SUBMIT COMPLAINT
    # ======================================

    def submit_complaint_page(parent):

        form_frame = tk.Frame(
            parent,
            bg=WHITE,
            padx=25,
            pady=18,
            highlightbackground="#D9E6F0",
            highlightthickness=1
        )

        form_frame.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=10
        )

        connection = create_connection()

        if connection is None:

            messagebox.showerror(
                "Error",
                "Database connection failed.",
                parent=dashboard
            )

            return

        try:

            cursor = connection.cursor()

            cursor.execute("""
                SELECT building_name
                FROM Buildings
                ORDER BY building_id
            """)

            buildings = [row[0] for row in cursor.fetchall()]

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error),
                parent=dashboard
            )

            return

        finally:
            connection.close()

        def field_label(text):

            tk.Label(
                form_frame,
                text=text,
                font=("Arial", 10, "bold"),
                bg=WHITE,
                fg=TEXT
            ).pack(anchor="w", pady=(8, 4))

        field_label("Select Building")

        building_box = ttk.Combobox(
            form_frame,
            values=buildings,
            state="readonly",
            font=("Arial", 10)
        )

        building_box.pack(fill="x", ipady=4)

        field_label("Issue Type")

        issue_box = ttk.Combobox(
            form_frame,
            values=[
                "No Water",
                "Low Water Pressure",
                "Water Leakage",
                "Dirty Water",
                "Other"
            ],
            state="readonly",
            font=("Arial", 10)
        )

        issue_box.pack(fill="x", ipady=4)

        field_label("Describe the Problem")

        description_frame = tk.Frame(
            form_frame,
            bg=WHITE
        )

        description_frame.pack(
            fill="both",
            expand=True,
            pady=5
        )

        description_entry = tk.Text(
            description_frame,
            height=5,
            font=("Arial", 10),
            wrap="word",
            bg="#F8FBFD",
            fg=TEXT,
            relief="solid",
            bd=1,
            padx=10,
            pady=8
        )

        description_entry.pack(
            side="left",
            fill="both",
            expand=True
        )

        description_scrollbar = ttk.Scrollbar(
            description_frame,
            orient="vertical",
            command=description_entry.yview
        )

        description_scrollbar.pack(side="right", fill="y")

        description_entry.configure(
            yscrollcommand=description_scrollbar.set
        )

        field_label("Attach Picture (Optional)")

        selected_photo = {"path": ""}

        photo_frame = tk.Frame(
            form_frame,
            bg=PALE_BLUE,
            padx=10,
            pady=10
        )

        photo_frame.pack(fill="x", pady=5)

        photo_label = tk.Label(
            photo_frame,
            text="No picture selected",
            font=("Arial", 9),
            bg=PALE_BLUE,
            fg=MUTED
        )

        photo_label.pack(side="left", padx=5)

        def choose_picture():

            file_path = filedialog.askopenfilename(
                parent=dashboard,
                title="Select Complaint Picture",
                filetypes=[
                    ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
                    ("All files", "*.*")
                ]
            )

            if file_path:

                selected_photo["path"] = file_path

                photo_label.config(
                    text=os.path.basename(file_path),
                    fg=OCEAN_BLUE
                )

        def remove_picture():

            selected_photo["path"] = ""

            photo_label.config(
                text="No picture selected",
                fg=MUTED
            )

        make_button(
            photo_frame,
            "CHOOSE PICTURE",
            choose_picture,
            LIGHT_BLUE
        ).pack(side="left", padx=5)

        tk.Button(
            photo_frame,
            text="REMOVE",
            command=remove_picture,
            font=("Arial", 9, "bold"),
            bg="#FCE4E4",
            fg=RED,
            relief="flat",
            padx=12,
            pady=8,
            cursor="hand2"
        ).pack(side="left", padx=5)

        def save_complaint():

            selected_building = building_box.get()
            selected_issue = issue_box.get()

            description = description_entry.get(
                "1.0",
                "end-1c"
            ).strip()

            photo_path = selected_photo["path"] or None

            if not selected_building or not selected_issue or not description:

                messagebox.showwarning(
                    "Missing Information",
                    "Please complete all required fields.",
                    parent=dashboard
                )

                return

            db_connection = create_connection()

            if db_connection is None:

                messagebox.showerror(
                    "Error",
                    "Database connection failed.",
                    parent=dashboard
                )

                return

            try:

                db_cursor = db_connection.cursor()

                db_cursor.execute(
                    """
                    SELECT building_id
                    FROM Buildings
                    WHERE building_name = %s
                    """,
                    (selected_building,)
                )

                building = db_cursor.fetchone()

                if building is None:

                    messagebox.showerror(
                        "Error",
                        "Selected building was not found.",
                        parent=dashboard
                    )

                    return

                db_cursor.execute(
                    """
                    INSERT INTO Complaints
                    (user_id, building_id, issue_type,
                     description, photo_path)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        user_id,
                        building[0],
                        selected_issue,
                        description,
                        photo_path
                    )
                )

                db_connection.commit()

                messagebox.showinfo(
                    "Success",
                    "Your water complaint has been submitted!",
                    parent=dashboard
                )

                navigate("All Complaints")

            except Exception as error:

                db_connection.rollback()

                messagebox.showerror(
                    "Error",
                    str(error),
                    parent=dashboard
                )

            finally:
                db_connection.close()

        make_button(
            form_frame,
            "SUBMIT COMPLAINT",
            save_complaint
        ).pack(fill="x", pady=(12, 0))

    # ======================================
    # 4. VIEW ALL COMPLAINTS
    # ======================================

    def all_complaints_page(parent):

        connection = create_connection()

        if connection is None:

            messagebox.showerror(
                "Error",
                "Could not connect to the database.",
                parent=dashboard
            )

            return

        try:

            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    Complaints.complaint_id,
                    Buildings.building_name,
                    Complaints.issue_type,
                    Complaints.description,
                    Complaints.created_at,
                    Complaints.status
                FROM Complaints
                INNER JOIN Buildings
                    ON Complaints.building_id =
                       Buildings.building_id
                ORDER BY Complaints.created_at DESC
            """)

            complaints = cursor.fetchall()

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error),
                parent=dashboard
            )

            return

        finally:
            connection.close()

        table = make_table(
            parent,
            ("id", "building", "issue", "description", "date", "status"),
            {
                "id": "Complaint ID",
                "building": "Building",
                "issue": "Issue Type",
                "description": "Description",
                "date": "Submitted Date",
                "status": "Status"
            },
            {
                "id": 90,
                "building": 150,
                "issue": 150,
                "description": 300,
                "date": 160,
                "status": 120
            }
        )

        for complaint in complaints:

            table.insert("", "end", values=complaint)

        def view_attached_picture():

            selected = table.selection()

            if not selected:

                messagebox.showwarning(
                    "Select Complaint",
                    "Please select a complaint first.",
                    parent=dashboard
                )

                return

            values = table.item(selected[0], "values")
            complaint_id = values[0]

            picture_connection = create_connection()

            if picture_connection is None:

                messagebox.showerror(
                    "Error",
                    "Database connection failed.",
                    parent=dashboard
                )

                return

            try:

                picture_cursor = picture_connection.cursor()

                picture_cursor.execute(
                    """
                    SELECT photo_path
                    FROM Complaints
                    WHERE complaint_id = %s
                    """,
                    (complaint_id,)
                )

                result = picture_cursor.fetchone()

                if result is None or not result[0]:

                    messagebox.showinfo(
                        "No Picture",
                        "No picture was attached to this complaint.",
                        parent=dashboard
                    )

                    return

                photo_path = result[0]

                if not os.path.isfile(photo_path):

                    messagebox.showerror(
                        "Picture Not Found",
                        "The attached picture could not be found. "
                        "It may have been moved or deleted.",
                        parent=dashboard
                    )

                    return

                try:
                    os.startfile(photo_path)

                except Exception as error:

                    messagebox.showerror(
                        "Unable to Open Picture",
                        str(error),
                        parent=dashboard
                    )

            except Exception as error:

                messagebox.showerror(
                    "Picture Error",
                    str(error),
                    parent=dashboard
                )

            finally:
                picture_connection.close()

        make_button(
            parent,
            "VIEW ATTACHED PICTURE",
            view_attached_picture
        ).pack(pady=10)

        if not complaints:

            tk.Label(
                parent,
                text="There are currently no water complaints.",
                font=("Arial", 11),
                bg=BACKGROUND,
                fg=MUTED
            ).pack(pady=15)

    # ======================================
    # 5. COMPLAINT HISTORY
    # ======================================

    def complaint_history_page(parent):

        connection = create_connection()

        if connection is None:

            messagebox.showerror(
                "Error",
                "Database connection failed.",
                parent=dashboard
            )

            return

        try:

            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    Complaints.complaint_id,
                    Buildings.building_name,
                    Complaints.issue_type,
                    Complaints.description,
                    Complaints.status
                FROM Complaints
                INNER JOIN Buildings
                    ON Complaints.building_id =
                       Buildings.building_id
                ORDER BY Complaints.created_at DESC
            """)

            complaints = cursor.fetchall()

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error),
                parent=dashboard
            )

            return

        finally:
            connection.close()

        section_label(parent, "ALL COMPLAINTS")

        complaint_table = make_table(
            parent,
            ("id", "building", "issue", "description", "status"),
            {
                "id": "Complaint ID",
                "building": "Building",
                "issue": "Issue Type",
                "description": "Description",
                "status": "Current Status"
            },
            {
                "id": 80,
                "building": 140,
                "issue": 140,
                "description": 350,
                "status": 130
            }
        )

        for complaint in complaints:

            complaint_table.insert("", "end", values=complaint)

        section_label(parent, "ADMIN UPDATES AND REPAIR REMARKS")

        history_table = make_table(
            parent,
            ("status", "remarks", "updated_by", "date"),
            {
                "status": "Status",
                "remarks": "Repair Remarks",
                "updated_by": "Updated By",
                "date": "Update Date"
            },
            {
                "status": 120,
                "remarks": 350,
                "updated_by": 150,
                "date": 180
            }
        )

        def load_history():

            selected = complaint_table.selection()

            if not selected:

                messagebox.showwarning(
                    "Select Complaint",
                    "Please select a complaint first.",
                    parent=dashboard
                )

                return

            values = complaint_table.item(
                selected[0],
                "values"
            )

            complaint_id = values[0]

            for item in history_table.get_children():
                history_table.delete(item)

            history_connection = create_connection()

            if history_connection is None:

                messagebox.showerror(
                    "Error",
                    "Database connection failed.",
                    parent=dashboard
                )

                return

            try:

                history_cursor = history_connection.cursor()

                history_cursor.execute("""
                    SELECT
                        Complaint_Updates.status,
                        Complaint_Updates.remarks,
                        Users.full_name,
                        Complaint_Updates.updated_at
                    FROM Complaint_Updates
                    INNER JOIN Users
                        ON Complaint_Updates.updated_by =
                           Users.user_id
                    WHERE Complaint_Updates.complaint_id = %s
                    ORDER BY Complaint_Updates.updated_at DESC
                """, (complaint_id,))

                updates = history_cursor.fetchall()

                for update in updates:

                    status, remarks, updated_by, updated_at = update

                    history_table.insert(
                        "",
                        "end",
                        values=(
                            status,
                            remarks if remarks else "No remarks provided",
                            updated_by,
                            updated_at
                        )
                    )

                if not updates:

                    messagebox.showinfo(
                        "No History",
                        "No Admin updates have been recorded yet.",
                        parent=dashboard
                    )

            except Exception as error:

                messagebox.showerror(
                    "History Error",
                    str(error),
                    parent=dashboard
                )

            finally:
                history_connection.close()

        make_button(
            parent,
            "VIEW SELECTED COMPLAINT HISTORY",
            load_history
        ).pack(pady=10)

    # ======================================
    # 6. ANNOUNCEMENTS
    # ======================================

    def announcements_page(parent):

        table = make_table(
            parent,
            ("title", "message", "date"),
            {
                "title": "Announcement Title",
                "message": "Message",
                "date": "Published Date"
            },
            {
                "title": 220,
                "message": 450,
                "date": 180
            }
        )

        connection = create_connection()

        if connection is None:

            messagebox.showerror(
                "Error",
                "Database connection failed.",
                parent=dashboard
            )

            return

        try:

            cursor = connection.cursor()

            cursor.execute("""
                SELECT title, message, created_at
                FROM Announcements
                ORDER BY created_at DESC
            """)

            announcements = cursor.fetchall()

            for announcement in announcements:

                table.insert("", "end", values=announcement)

            if not announcements:

                tk.Label(
                    parent,
                    text="There are currently no announcements.",
                    font=("Arial", 11),
                    bg=BACKGROUND,
                    fg=MUTED
                ).pack(pady=15)

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error),
                parent=dashboard
            )

        finally:
            connection.close()

    # ======================================
    # 7. MANAGEMENT REPORTS
    # ======================================

    def reports_page(parent):

        summary_frame = tk.Frame(
            parent,
            bg=BACKGROUND
        )

        summary_frame.pack(
            fill="x",
            padx=10,
            pady=5
        )

        section_label(parent, "WATER STATUS OF ALL BUILDINGS")

        table = make_table(
            parent,
            ("building", "status", "remarks", "updated"),
            {
                "building": "Building",
                "status": "Water Status",
                "remarks": "Remarks",
                "updated": "Last Updated"
            },
            {
                "building": 180,
                "status": 140,
                "remarks": 350,
                "updated": 170
            }
        )

        def load_reports():

            connection = create_connection()

            if connection is None:

                messagebox.showerror(
                    "Error",
                    "Database connection failed.",
                    parent=dashboard
                )

                return

            try:

                cursor = connection.cursor()

                for widget in summary_frame.winfo_children():
                    widget.destroy()

                for item in table.get_children():
                    table.delete(item)

                cursor.execute("""
                    SELECT status, COUNT(*)
                    FROM Complaints
                    GROUP BY status
                """)

                complaint_counts = dict(cursor.fetchall())

                total = sum(complaint_counts.values())

                pending = complaint_counts.get("Pending", 0)
                in_progress = complaint_counts.get("In Progress", 0)
                resolved = complaint_counts.get("Resolved", 0)

                cursor.execute("""
                    SELECT COUNT(*)
                    FROM Buildings
                """)

                total_buildings = cursor.fetchone()[0]

                cursor.execute("""
                    SELECT status, COUNT(*)
                    FROM Water_Status
                    GROUP BY status
                """)

                water_counts = dict(cursor.fetchall())

                summaries = [
                    ("Total Complaints", total, NAVY),
                    ("Pending", pending, ORANGE),
                    ("In Progress", in_progress, OCEAN_BLUE),
                    ("Resolved", resolved, GREEN),
                    ("Total Buildings", total_buildings, NAVY),
                    ("Available", water_counts.get("Available", 0), GREEN),
                    ("Low Supply", water_counts.get("Low Supply", 0), ORANGE),
                    ("No Water", water_counts.get("No Water", 0), RED)
                ]

                for index, (title, number, color) in enumerate(summaries):

                    card = tk.Frame(
                        summary_frame,
                        bg=WHITE,
                        padx=10,
                        pady=10,
                        highlightbackground="#D9E6F0",
                        highlightthickness=1
                    )

                    card.grid(
                        row=index // 4,
                        column=index % 4,
                        padx=5,
                        pady=5,
                        sticky="nsew"
                    )

                    tk.Label(
                        card,
                        text=title,
                        font=("Arial", 9, "bold"),
                        bg=WHITE,
                        fg=MUTED
                    ).pack()

                    tk.Label(
                        card,
                        text=str(number),
                        font=("Arial", 21, "bold"),
                        bg=WHITE,
                        fg=color
                    ).pack(pady=(4, 0))

                for column in range(4):

                    summary_frame.grid_columnconfigure(
                        column,
                        weight=1
                    )

                # LEFT JOIN ensures all buildings are included.

                cursor.execute("""
                    SELECT
                        Buildings.building_name,
                        Water_Status.status,
                        Water_Status.remarks,
                        Water_Status.updated_at
                    FROM Buildings
                    LEFT JOIN Water_Status
                        ON Buildings.building_id =
                           Water_Status.building_id
                    ORDER BY Buildings.building_id
                """)

                buildings = cursor.fetchall()

                for building_name, status, remarks, updated in buildings:

                    table.insert(
                        "",
                        "end",
                        values=(
                            building_name,
                            status if status else "Not Updated",
                            remarks if remarks else "No remarks",
                            updated if updated else "Not Available"
                        )
                    )

            except Exception as error:

                messagebox.showerror(
                    "Report Error",
                    str(error),
                    parent=dashboard
                )

            finally:
                connection.close()

        make_button(
            parent,
            "REFRESH REPORTS",
            load_reports
        ).pack(pady=10)

        load_reports()

    # ======================================
    # NAVIGATION
    # ======================================

    pages = {
        "Dashboard": (
            "Dashboard Overview",
            "Monitor water supply and manage water-related issues.",
            dashboard_home
        ),

        "Water Status": (
            "Water Status",
            "Check the current water supply condition across all 12 buildings.",
            water_status_page
        ),

        "Submit Complaint": (
            "Submit Water Complaint",
            "Report a water-related problem to the college administration.",
            submit_complaint_page
        ),

        "All Complaints": (
            "All Water Complaints",
            "Review submitted complaints and attached pictures.",
            all_complaints_page
        ),

        "Complaint History": (
            "Complaint Progress History",
            "Follow Admin updates and repair progress.",
            complaint_history_page
        ),

        "Announcements": (
            "College Announcements",
            "Read the latest college announcements.",
            announcements_page
        ),

        "Management Reports": (
            "Water Management Reports",
            "View complaint statistics and building water reports.",
            reports_page
        )
    }

    # ======================================
    # UPDATE SIDEBAR STYLE
    # ======================================

    def update_navigation_style(name):

        for button_name, button in navigation_buttons.items():

            if button_name == name:

                button.config(
                    bg=OCEAN_BLUE,
                    fg=WHITE
                )

            else:

                button.config(
                    bg=NAVY,
                    fg=WHITE
                )

    # ======================================
    # PAGE NAVIGATION AND ANIMATION
    # ======================================

    def show_page(name):

        if name not in pages:
            return

        if animation_job["id"] is not None:

            try:
                dashboard.after_cancel(animation_job["id"])

            except tk.TclError:
                pass

            animation_job["id"] = None

        page_number["value"] += 1
        this_page = page_number["value"]

        title, subtitle, page_function = pages[name]

        current_page["name"] = name

        page_title.config(text=title)
        page_subtitle.config(text=subtitle)

        update_navigation_style(name)

        for widget in content_holder.winfo_children():
            widget.destroy()

        page = tk.Frame(
            content_holder,
            bg=BACKGROUND
        )

        page.place(
            relx=0.04,
            rely=0,
            relwidth=1,
            relheight=1
        )

        try:

            page_function(page)

        except Exception as error:

            messagebox.showerror(
                "Page Error",
                str(error),
                parent=dashboard
            )

        def slide(step=0):

            if this_page != page_number["value"]:
                return

            if not page.winfo_exists():
                return

            progress = min(step / 8, 1)

            position = 0.04 * (1 - progress)

            page.place_configure(relx=position)

            if step < 8:

                animation_job["id"] = dashboard.after(
                    15,
                    lambda: slide(step + 1)
                )

            else:

                page.place_configure(relx=0)

                animation_job["id"] = None

        slide()

    def navigate(name):
        show_page(name)

    # ======================================
    # SIDEBAR NAVIGATION BUTTONS
    # ======================================

    sidebar_items = [
        ("Dashboard", "Dashboard"),
        ("Water Status", "Water Status"),
        ("Submit Complaint", "Submit Complaint"),
        ("All Complaints", "All Complaints"),
        ("Complaint History", "Complaint History"),
        ("Announcements", "Announcements"),
        ("Management Reports", "Management Reports")
    ]

    for label, page_name in sidebar_items:

        button = tk.Button(
            sidebar,
            text="   " + label,
            command=lambda name=page_name: navigate(name),
            font=("Arial", 10, "bold"),
            bg=NAVY,
            fg=WHITE,
            activebackground=DARK_BLUE,
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            anchor="w",
            padx=18,
            pady=13,
            cursor="hand2"
        )

        button.pack(
            fill="x",
            padx=12,
            pady=2
        )

        navigation_buttons[page_name] = button

        button.bind(
            "<Enter>",
            lambda event, b=button, n=page_name:
                b.config(bg=DARK_BLUE)
                if current_page["name"] != n else None
        )

        button.bind(
            "<Leave>",
            lambda event, b=button, n=page_name:
                b.config(bg=NAVY)
                if current_page["name"] != n else None
        )

    # ======================================
    # LOGOUT
    # ======================================

    def logout():

        confirm = messagebox.askyesno(
            "Confirm Logout",
            "Are you sure you want to logout?",
            parent=dashboard
        )

        if confirm:

            main_file = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "main.py"
            )

            os.execl(
                sys.executable,
                sys.executable,
                main_file
            )

    tk.Frame(
        sidebar,
        bg="#426784",
        height=1
    ).pack(fill="x", padx=20, pady=(20, 12))

    logout_button = tk.Button(
        sidebar,
        text="   Logout",
        command=logout,
        font=("Arial", 10, "bold"),
        bg=RED,
        fg=WHITE,
        activebackground="#922B21",
        activeforeground=WHITE,
        relief="flat",
        bd=0,
        anchor="w",
        padx=18,
        pady=12,
        cursor="hand2"
    )

    logout_button.pack(
        side="bottom",
        fill="x",
        padx=12,
        pady=20
    )

    # ======================================
    # FOOTER
    # ======================================

    tk.Label(
        main_area,
        text="AquaFlow | Smart Water Issue Monitoring and Management System",
        font=("Arial", 8),
        bg=BACKGROUND,
        fg=MUTED
    ).pack(pady=(0, 10))

    # ======================================
    # START DASHBOARD
    # ======================================

    navigate("Dashboard")

    dashboard.mainloop()


if __name__ == "__main__":

    print("Run main.py to open the AquaFlow login screen.")

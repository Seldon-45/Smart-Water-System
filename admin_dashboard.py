
import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys

from database import create_connection


# ==================================================
# AQUAFLOW THEME
# ==================================================

NAVY = "#12304A"
DARK_BLUE = "#174A6E"
OCEAN_BLUE = "#168AAD"
LIGHT_BLUE = "#EAF5FB"
PALE_BLUE = "#F4F9FC"
WHITE = "#FFFFFF"
TEXT = "#263B4D"
MUTED = "#718096"
GREEN = "#15966B"
RED = "#D9534F"
ORANGE = "#D99A24"
PURPLE = "#6C63A8"
BORDER = "#D8E6EF"


# ==================================================
# REUSABLE DESIGN FUNCTIONS
# ==================================================

def setup_style():

    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "Aqua.TCombobox",
        padding=7,
        fieldbackground=WHITE,
        background=WHITE,
        foreground=TEXT
    )

    style.configure(
        "Aqua.Treeview",
        background=WHITE,
        foreground=TEXT,
        rowheight=36,
        fieldbackground=WHITE,
        borderwidth=0,
        font=("Arial", 10)
    )

    style.configure(
        "Aqua.Treeview.Heading",
        background=NAVY,
        foreground=WHITE,
        font=("Arial", 10, "bold"),
        padding=10,
        relief="flat"
    )

    style.map(
        "Aqua.Treeview",
        background=[("selected", "#D5ECF8")],
        foreground=[("selected", NAVY)]
    )


def create_table(parent, columns, headings, widths, height=10):

    frame = tk.Frame(parent, bg=WHITE)

    table = ttk.Treeview(
        frame,
        columns=columns,
        show="headings",
        height=height,
        style="Aqua.Treeview"
    )

    for column, heading, width in zip(columns, headings, widths):

        table.heading(column, text=heading)

        table.column(
            column,
            width=width,
            minwidth=60,
            anchor="w"
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

    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)

    return frame, table


def action_button(parent, text, command, color=OCEAN_BLUE):

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


def create_card(parent, title, value="0", accent=OCEAN_BLUE):

    card = tk.Frame(
        parent,
        bg=WHITE,
        padx=18,
        pady=16,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    tk.Frame(
        card,
        bg=accent,
        height=5
    ).pack(fill="x", pady=(0, 12))

    tk.Label(
        card,
        text=title,
        font=("Arial", 10, "bold"),
        bg=WHITE,
        fg=MUTED
    ).pack(anchor="w")

    value_label = tk.Label(
        card,
        text=value,
        font=("Arial", 25, "bold"),
        bg=WHITE,
        fg=accent
    )

    value_label.pack(anchor="w", pady=(7, 0))

    return card, value_label


# ==================================================
# MAIN ADMIN DASHBOARD
# ==================================================

def open_admin_dashboard(full_name, user_id):

    root = tk.Tk()

    setup_style()

    root.title("Admin Dashboard - AquaFlow")
    root.geometry("1250x800")
    root.minsize(950, 650)
    root.configure(bg=LIGHT_BLUE)
    root.resizable(True, True)

    # ==================================================
    # MAIN LAYOUT
    # ==================================================

    main_frame = tk.Frame(root, bg=LIGHT_BLUE)
    main_frame.pack(fill="both", expand=True)

    # ==================================================
    # SIDEBAR
    # ==================================================

    sidebar = tk.Frame(
        main_frame,
        bg=NAVY,
        width=245
    )

    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    tk.Label(
        sidebar,
        text="AquaFlow",
        font=("Arial", 25, "bold"),
        bg=NAVY,
        fg=WHITE
    ).pack(anchor="w", padx=25, pady=(30, 0))

    tk.Label(
        sidebar,
        text="ADMINISTRATION PANEL",
        font=("Arial", 9, "bold"),
        bg=NAVY,
        fg="#9ACDE6"
    ).pack(anchor="w", padx=27, pady=(3, 30))

    tk.Frame(
        sidebar,
        bg="#42647D",
        height=1
    ).pack(fill="x", padx=20, pady=(0, 18))

    tk.Label(
        sidebar,
        text="MAIN MENU",
        font=("Arial", 9, "bold"),
        bg=NAVY,
        fg="#9ACDE6"
    ).pack(anchor="w", padx=25, pady=(0, 10))

    # ==================================================
    # RIGHT SIDE
    # ==================================================

    right_frame = tk.Frame(main_frame, bg=LIGHT_BLUE)

    right_frame.pack(
        side="left",
        fill="both",
        expand=True
    )

    # ==================================================
    # FIXED TOP BAR
    # ==================================================

    top_bar = tk.Frame(
        right_frame,
        bg=WHITE,
        padx=25,
        pady=17,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    top_bar.pack(fill="x")

    page_title_label = tk.Label(
        top_bar,
        text="Admin Dashboard",
        font=("Arial", 20, "bold"),
        bg=WHITE,
        fg=NAVY
    )

    page_title_label.pack(side="left")

    tk.Label(
        top_bar,
        text=f"Welcome, {full_name}",
        font=("Arial", 10, "bold"),
        bg=WHITE,
        fg=OCEAN_BLUE
    ).pack(side="right")

    # ==================================================
    # SCROLLABLE CONTENT AREA
    # ==================================================

    content_container = tk.Frame(
        right_frame,
        bg=LIGHT_BLUE
    )

    content_container.pack(
        fill="both",
        expand=True
    )

    content_canvas = tk.Canvas(
        content_container,
        bg=LIGHT_BLUE,
        highlightthickness=0
    )

    content_scrollbar = ttk.Scrollbar(
        content_container,
        orient="vertical",
        command=content_canvas.yview
    )

    content_frame = tk.Frame(
        content_canvas,
        bg=LIGHT_BLUE,
        padx=25,
        pady=22
    )

    content_window = content_canvas.create_window(
        (0, 0),
        window=content_frame,
        anchor="nw"
    )

    def update_scroll_region(event=None):

        content_canvas.configure(
            scrollregion=content_canvas.bbox("all")
        )

    def resize_content(event):

        content_canvas.itemconfigure(
            content_window,
            width=event.width
        )

    content_frame.bind(
        "<Configure>",
        update_scroll_region
    )

    content_canvas.bind(
        "<Configure>",
        resize_content
    )

    content_canvas.configure(
        yscrollcommand=content_scrollbar.set
    )

    content_canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    content_scrollbar.pack(
        side="right",
        fill="y"
    )

    # Mouse wheel scrolling.
    # Bind only while the pointer is over the content area.

    def scroll_content(event):

        if event.delta:
            content_canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )

    def enable_mousewheel(event):

        content_canvas.bind_all(
            "<MouseWheel>",
            scroll_content
        )

    def disable_mousewheel(event):

        content_canvas.unbind_all("<MouseWheel>")

    content_canvas.bind(
        "<Enter>",
        enable_mousewheel
    )

    content_canvas.bind(
        "<Leave>",
        disable_mousewheel
    )

    # ==================================================
    # PAGE NAVIGATION
    # ==================================================

    sidebar_buttons = {}

    current_page = {
        "name": "Dashboard"
    }

    def clear_page():

        for widget in content_frame.winfo_children():
            widget.destroy()

    def page_header(title, subtitle):

        tk.Label(
            content_frame,
            text=title,
            font=("Arial", 22, "bold"),
            bg=LIGHT_BLUE,
            fg=NAVY
        ).pack(anchor="w")

        tk.Label(
            content_frame,
            text=subtitle,
            font=("Arial", 10),
            bg=LIGHT_BLUE,
            fg=MUTED
        ).pack(anchor="w", pady=(5, 18))

    def highlight_sidebar(selected):

        for name, button in sidebar_buttons.items():

            if name == selected:

                button.config(
                    bg=OCEAN_BLUE,
                    fg=WHITE
                )

            else:

                button.config(
                    bg=NAVY,
                    fg=WHITE
                )

    def show_page(name):

        clear_page()

        content_canvas.yview_moveto(0)

        current_page["name"] = name

        page_title_label.config(
            text=name
        )

        highlight_sidebar(name)

        if name == "Dashboard":
            dashboard_home()

        elif name == "Manage Complaints":
            complaints_page()

        elif name == "Update Water Status":
            water_status_page()

        elif name == "Manage Announcements":
            announcements_page()

        elif name == "View Reports":
            reports_page()

        content_frame.update_idletasks()

        content_canvas.configure(
            scrollregion=content_canvas.bbox("all")
        )

    def sidebar_button(name):

        button = tk.Button(
            sidebar,
            text="   " + name,
            command=lambda: show_page(name),
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
            padx=10,
            pady=3
        )

        button.bind(
            "<Enter>",
            lambda event: (
                button.config(bg=DARK_BLUE)
                if current_page["name"] != name
                else None
            )
        )

        button.bind(
            "<Leave>",
            lambda event: (
                button.config(bg=NAVY)
                if current_page["name"] != name
                else None
            )
        )

        sidebar_buttons[name] = button

    # ==================================================
    # 1. DASHBOARD HOME
    # ==================================================

    def dashboard_home():

        page_header(
            "Welcome to AquaFlow",
            "Manage water complaints, update supply information "
            "and monitor system activity."
        )

        cards_frame = tk.Frame(
            content_frame,
            bg=LIGHT_BLUE
        )

        cards_frame.pack(
            fill="both",
            expand=True
        )

        feature_cards = [
            (
                "01",
                "Manage Complaints",
                "Review submitted complaints, view attached pictures "
                "and update repair progress.",
                "OPEN COMPLAINTS",
                "Manage Complaints",
                OCEAN_BLUE
            ),
            (
                "02",
                "Update Water Status",
                "Update water availability and remarks for all "
                "12 college buildings.",
                "UPDATE STATUS",
                "Update Water Status",
                GREEN
            ),
            (
                "03",
                "Manage Announcements",
                "Publish important notices and water supply "
                "announcements.",
                "MANAGE NOTICES",
                "Manage Announcements",
                PURPLE
            ),
            (
                "04",
                "View System Reports",
                "Check complaint statistics and the water status "
                "of each building.",
                "VIEW REPORTS",
                "View Reports",
                ORANGE
            )
        ]

        for index, item in enumerate(feature_cards):

            number, title, description, button_text, destination, accent = item

            row = index // 2
            column = index % 2

            card = tk.Frame(
                cards_frame,
                bg=WHITE,
                padx=20,
                pady=18,
                highlightbackground=BORDER,
                highlightthickness=1,
                cursor="hand2"
            )

            card.grid(
                row=row,
                column=column,
                sticky="nsew",
                padx=9,
                pady=9
            )

            number_label = tk.Label(
                card,
                text=number,
                font=("Arial", 13, "bold"),
                bg=LIGHT_BLUE,
                fg=accent,
                padx=10,
                pady=5,
                cursor="hand2"
            )

            number_label.pack(anchor="w")

            title_label = tk.Label(
                card,
                text=title,
                font=("Arial", 15, "bold"),
                bg=WHITE,
                fg=NAVY,
                cursor="hand2"
            )

            title_label.pack(
                anchor="w",
                pady=(12, 7)
            )

            description_label = tk.Label(
                card,
                text=description,
                font=("Arial", 10),
                bg=WHITE,
                fg=MUTED,
                wraplength=350,
                justify="left",
                cursor="hand2"
            )

            description_label.pack(
                anchor="w",
                pady=(0, 15)
            )

            def open_feature(page_name=destination):
                show_page(page_name)

            open_button = action_button(
                card,
                button_text,
                open_feature,
                color=accent
            )

            open_button.pack(anchor="w")

            # Make the complete card clickable.

            for widget in (
                card,
                number_label,
                title_label,
                description_label
            ):

                widget.bind(
                    "<Button-1>",
                    lambda event, page=destination: show_page(page)
                )

                widget.bind(
                    "<Enter>",
                    lambda event, target=card: target.config(
                        highlightbackground=OCEAN_BLUE
                    )
                )

                widget.bind(
                    "<Leave>",
                    lambda event, target=card: target.config(
                        highlightbackground=BORDER
                    )
                )

        cards_frame.columnconfigure(0, weight=1)
        cards_frame.columnconfigure(1, weight=1)

        cards_frame.rowconfigure(0, weight=1)
        cards_frame.rowconfigure(1, weight=1)

    # ==================================================
    # 2. MANAGE COMPLAINTS
    # ==================================================

    def complaints_page():

        page_header(
            "Manage Water Complaints",
            "Review reports, check attached pictures and update repair progress."
        )

        filter_card = tk.Frame(
            content_frame,
            bg=WHITE,
            padx=15,
            pady=13,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        filter_card.pack(
            fill="x",
            pady=(0, 12)
        )

        tk.Label(
            filter_card,
            text="SEARCH AND FILTER COMPLAINTS",
            font=("Arial", 12, "bold"),
            bg=WHITE,
            fg=NAVY
        ).grid(
            row=0,
            column=0,
            columnspan=5,
            sticky="w",
            pady=(0, 10)
        )

        tk.Label(
            filter_card,
            text="Search ID / Building:",
            bg=WHITE,
            fg=TEXT
        ).grid(
            row=1,
            column=0,
            padx=5,
            pady=5,
            sticky="w"
        )

        search_entry = tk.Entry(
            filter_card,
            font=("Arial", 10),
            width=19,
            relief="solid",
            bd=1
        )

        search_entry.grid(
            row=1,
            column=1,
            padx=5,
            pady=5
        )

        tk.Label(
            filter_card,
            text="Status:",
            bg=WHITE,
            fg=TEXT
        ).grid(
            row=1,
            column=2,
            padx=5,
            pady=5
        )

        status_filter = ttk.Combobox(
            filter_card,
            values=["All", "Pending", "In Progress", "Resolved"],
            state="readonly",
            width=14,
            style="Aqua.TCombobox"
        )

        status_filter.grid(
            row=1,
            column=3,
            padx=5,
            pady=5
        )

        status_filter.set("All")

        tk.Label(
            filter_card,
            text="Issue:",
            bg=WHITE,
            fg=TEXT
        ).grid(
            row=2,
            column=0,
            padx=5,
            pady=5,
            sticky="w"
        )

        issue_filter = ttk.Combobox(
            filter_card,
            values=[
                "All",
                "No Water",
                "Low Water Pressure",
                "Water Leakage",
                "Dirty Water",
                "Other"
            ],
            state="readonly",
            width=18,
            style="Aqua.TCombobox"
        )

        issue_filter.grid(
            row=2,
            column=1,
            padx=5,
            pady=5
        )

        issue_filter.set("All")

        table_card = tk.Frame(
            content_frame,
            bg=WHITE,
            padx=12,
            pady=12,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        table_card.pack(
            fill="both",
            expand=True,
            pady=5
        )

        tk.Label(
            table_card,
            text="ALL SUBMITTED COMPLAINTS",
            font=("Arial", 12, "bold"),
            bg=WHITE,
            fg=NAVY
        ).pack(
            anchor="w",
            pady=(0, 10)
        )

        columns = (
            "ID",
            "Captain",
            "Building",
            "Issue",
            "Description",
            "Date",
            "Status"
        )

        table_frame, table = create_table(
            table_card,
            columns,
            columns,
            (60, 120, 140, 140, 230, 145, 105),
            height=8
        )

        table_frame.pack(
            fill="both",
            expand=True
        )

        all_complaints = []

        count_label = tk.Label(
            table_card,
            text="Showing 0 complaint(s)",
            font=("Arial", 10, "bold"),
            bg=WHITE,
            fg=OCEAN_BLUE
        )

        count_label.pack(
            anchor="w",
            pady=(7, 0)
        )

        def display_complaints():

            for item in table.get_children():
                table.delete(item)

            search_text = search_entry.get().strip().lower()
            selected_status = status_filter.get()
            selected_issue = issue_filter.get()

            displayed_count = 0

            for complaint in all_complaints:

                complaint_id = str(complaint[0])
                building_name = str(complaint[2]).lower()
                issue_type = complaint[3]
                status = complaint[6]

                if search_text:

                    if (
                        search_text not in complaint_id.lower()
                        and search_text not in building_name
                    ):
                        continue

                if selected_status != "All" and status != selected_status:
                    continue

                if selected_issue != "All" and issue_type != selected_issue:
                    continue

                table.insert(
                    "",
                    "end",
                    values=complaint
                )

                displayed_count += 1

            count_label.config(
                text=f"Showing {displayed_count} complaint(s)"
            )

        def load_complaints():

            all_complaints.clear()

            connection = create_connection()

            if connection is None:
                messagebox.showerror(
                    "Error",
                    "Database connection failed.",
                    parent=root
                )
                return

            try:
                cursor = connection.cursor()

                cursor.execute("""
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
                """)

                all_complaints.extend(cursor.fetchall())

                display_complaints()

            except Exception as error:

                messagebox.showerror(
                    "Error",
                    str(error),
                    parent=root
                )

            finally:
                connection.close()

        def reset_filters():

            search_entry.delete(0, tk.END)
            status_filter.set("All")
            issue_filter.set("All")

            display_complaints()

        action_button(
            filter_card,
            "SEARCH",
            display_complaints
        ).grid(
            row=1,
            column=4,
            padx=6
        )

        action_button(
            filter_card,
            "RESET",
            reset_filters,
            color=MUTED
        ).grid(
            row=2,
            column=3,
            padx=5
        )

        action_button(
            filter_card,
            "REFRESH",
            load_complaints,
            color=GREEN
        ).grid(
            row=2,
            column=4,
            padx=5
        )

        update_card = tk.Frame(
            content_frame,
            bg=WHITE,
            padx=15,
            pady=12,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        update_card.pack(
            fill="x",
            pady=(10, 0)
        )

        tk.Label(
            update_card,
            text="UPDATE SELECTED COMPLAINT",
            font=("Arial", 12, "bold"),
            bg=WHITE,
            fg=NAVY
        ).pack(
            anchor="w",
            pady=(0, 8)
        )

        controls = tk.Frame(
            update_card,
            bg=WHITE
        )

        controls.pack(fill="x")

        status_area = tk.Frame(
            controls,
            bg=WHITE
        )

        status_area.pack(
            side="left",
            padx=(0, 20)
        )

        tk.Label(
            status_area,
            text="New Status:",
            bg=WHITE,
            fg=TEXT,
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

        status_box = ttk.Combobox(
            status_area,
            values=["Pending", "In Progress", "Resolved"],
            state="readonly",
            width=18,
            style="Aqua.TCombobox"
        )

        status_box.pack(pady=5)
        status_box.set("Pending")

        remarks_area = tk.Frame(
            controls,
            bg=WHITE
        )

        remarks_area.pack(
            side="left",
            fill="both",
            expand=True
        )

        tk.Label(
            remarks_area,
            text="Repair Remarks:",
            bg=WHITE,
            fg=TEXT,
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

        remarks_entry = tk.Text(
            remarks_area,
            height=3,
            font=("Arial", 10),
            wrap="word",
            relief="solid",
            bd=1
        )

        remarks_entry.pack(
            fill="both",
            expand=True,
            pady=5
        )

        def view_attached_picture():

            selected_item = table.selection()

            if not selected_item:

                messagebox.showwarning(
                    "No Selection",
                    "Please select a complaint first.",
                    parent=root
                )

                return

            complaint = table.item(
                selected_item[0],
                "values"
            )

            complaint_id = complaint[0]

            connection = create_connection()

            if connection is None:

                messagebox.showerror(
                    "Error",
                    "Database connection failed.",
                    parent=root
                )

                return

            try:
                cursor = connection.cursor()

                cursor.execute("""
                    SELECT photo_path
                    FROM Complaints
                    WHERE complaint_id = %s
                """, (complaint_id,))

                result = cursor.fetchone()

                if result is None or not result[0]:

                    messagebox.showinfo(
                        "No Picture",
                        "This complaint has no attached picture.",
                        parent=root
                    )

                    return

                photo_path = result[0]

                if not os.path.isfile(photo_path):

                    messagebox.showerror(
                        "Picture Not Found",
                        "The attached picture could not be found.",
                        parent=root
                    )

                    return

                if hasattr(os, "startfile"):
                    os.startfile(photo_path)
                else:
                    messagebox.showinfo(
                        "Picture Location",
                        photo_path,
                        parent=root
                    )

            except Exception as error:

                messagebox.showerror(
                    "Error",
                    str(error),
                    parent=root
                )

            finally:
                connection.close()

        def update_complaint():

            selected_item = table.selection()

            if not selected_item:

                messagebox.showwarning(
                    "No Selection",
                    "Please select a complaint first.",
                    parent=root
                )

                return

            complaint = table.item(
                selected_item[0],
                "values"
            )

            complaint_id = complaint[0]

            new_status = status_box.get()

            remarks = remarks_entry.get(
                "1.0",
                tk.END
            ).strip()

            if not new_status:

                messagebox.showwarning(
                    "Missing Status",
                    "Please select a complaint status.",
                    parent=root
                )

                return

            connection = create_connection()

            if connection is None:

                messagebox.showerror(
                    "Error",
                    "Database connection failed.",
                    parent=root
                )

                return

            try:
                cursor = connection.cursor()

                cursor.execute("""
                    UPDATE Complaints
                    SET status = %s
                    WHERE complaint_id = %s
                """, (
                    new_status,
                    complaint_id
                ))

                cursor.execute("""
                    INSERT INTO Complaint_Updates
                    (complaint_id, updated_by, status, remarks)
                    VALUES (%s, %s, %s, %s)
                """, (
                    complaint_id,
                    user_id,
                    new_status,
                    remarks
                ))

                connection.commit()

                messagebox.showinfo(
                    "Success",
                    "Complaint updated successfully!",
                    parent=root
                )

                remarks_entry.delete(
                    "1.0",
                    tk.END
                )

                status_box.set("Pending")

                load_complaints()

            except Exception as error:

                connection.rollback()

                messagebox.showerror(
                    "Error",
                    str(error),
                    parent=root
                )

            finally:
                connection.close()

        action_button(
            update_card,
            "VIEW ATTACHED PICTURE",
            view_attached_picture,
            color=GREEN
        ).pack(
            side="left",
            padx=(0, 8),
            pady=(10, 0)
        )

        action_button(
            update_card,
            "SAVE UPDATE",
            update_complaint
        ).pack(
            side="left",
            pady=(10, 0)
        )

        load_complaints()

    # ==================================================
    # 3. UPDATE WATER STATUS
    # ==================================================

    def water_status_page():

        page_header(
            "Update Water Status",
            "Update the current water supply condition for any of the 12 buildings."
        )

        form_frame = tk.Frame(
            content_frame,
            bg=WHITE,
            padx=25,
            pady=22,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        form_frame.pack(
            fill="both",
            expand=True
        )

        tk.Label(
            form_frame,
            text="BUILDING INFORMATION",
            font=("Arial", 13, "bold"),
            bg=WHITE,
            fg=NAVY
        ).pack(
            anchor="w",
            pady=(0, 18)
        )

        tk.Label(
            form_frame,
            text="Select Building:",
            font=("Arial", 10, "bold"),
            bg=WHITE,
            fg=TEXT
        ).pack(anchor="w")

        building_box = ttk.Combobox(
            form_frame,
            state="readonly",
            font=("Arial", 11),
            style="Aqua.TCombobox"
        )

        building_box.pack(
            fill="x",
            pady=(7, 18)
        )

        tk.Label(
            form_frame,
            text="Select Water Status:",
            font=("Arial", 10, "bold"),
            bg=WHITE,
            fg=TEXT
        ).pack(anchor="w")

        status_box = ttk.Combobox(
            form_frame,
            values=["Available", "Low Supply", "No Water"],
            state="readonly",
            font=("Arial", 11),
            style="Aqua.TCombobox"
        )

        status_box.pack(
            fill="x",
            pady=(7, 18)
        )

        tk.Label(
            form_frame,
            text="Remarks:",
            font=("Arial", 10, "bold"),
            bg=WHITE,
            fg=TEXT
        ).pack(anchor="w")

        remarks_entry = tk.Text(
            form_frame,
            height=8,
            font=("Arial", 11),
            wrap="word",
            relief="solid",
            bd=1
        )

        remarks_entry.pack(
            fill="both",
            expand=True,
            pady=7
        )

        connection = create_connection()

        if connection is None:

            messagebox.showerror(
                "Error",
                "Database connection failed.",
                parent=root
            )

            return

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT building_name
                FROM Buildings
                ORDER BY building_id
            """)

            buildings = cursor.fetchall()

            building_box["values"] = [
                building[0] for building in buildings
            ]

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error),
                parent=root
            )

        finally:
            connection.close()

        def save_water_status():

            building = building_box.get()
            status = status_box.get()

            remarks = remarks_entry.get(
                "1.0",
                tk.END
            ).strip()

            if not building or not status:

                messagebox.showwarning(
                    "Missing Information",
                    "Please select a building and water status.",
                    parent=root
                )

                return

            connection = create_connection()

            if connection is None:

                messagebox.showerror(
                    "Error",
                    "Database connection failed.",
                    parent=root
                )

                return

            try:
                cursor = connection.cursor()

                cursor.execute("""
                    SELECT building_id
                    FROM Buildings
                    WHERE building_name = %s
                """, (building,))

                result = cursor.fetchone()

                if result is None:

                    messagebox.showerror(
                        "Error",
                        "Building not found.",
                        parent=root
                    )

                    return

                building_id = result[0]

                cursor.execute("""
                    UPDATE Water_Status
                    SET status = %s,
                        remarks = %s,
                        updated_by = %s
                    WHERE building_id = %s
                """, (
                    status,
                    remarks,
                    user_id,
                    building_id
                ))

                if cursor.rowcount == 0:

                    raise Exception(
                        "No water status record was found for this building."
                    )

                connection.commit()

                messagebox.showinfo(
                    "Success",
                    "Water status updated successfully!",
                    parent=root
                )

                building_box.set("")
                status_box.set("")

                remarks_entry.delete(
                    "1.0",
                    tk.END
                )

            except Exception as error:

                connection.rollback()

                messagebox.showerror(
                    "Error",
                    str(error),
                    parent=root
                )

            finally:
                connection.close()

        action_button(
            form_frame,
            "SAVE WATER STATUS",
            save_water_status,
            color=GREEN
        ).pack(
            anchor="e",
            pady=(12, 0)
        )

    # ==================================================
    # 4. MANAGE ANNOUNCEMENTS
    # ==================================================

    def announcements_page():

        page_header(
            "Manage Announcements",
            "Publish important water supply notices and college updates."
        )

        form_frame = tk.Frame(
            content_frame,
            bg=WHITE,
            padx=20,
            pady=17,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        form_frame.pack(
            fill="x",
            pady=(0, 15)
        )

        tk.Label(
            form_frame,
            text="CREATE NEW ANNOUNCEMENT",
            font=("Arial", 13, "bold"),
            bg=WHITE,
            fg=NAVY
        ).pack(
            anchor="w",
            pady=(0, 12)
        )

        tk.Label(
            form_frame,
            text="Announcement Title:",
            font=("Arial", 10, "bold"),
            bg=WHITE,
            fg=TEXT
        ).pack(anchor="w")

        title_entry = tk.Entry(
            form_frame,
            font=("Arial", 11),
            relief="solid",
            bd=1
        )

        title_entry.pack(
            fill="x",
            pady=(6, 12)
        )

        tk.Label(
            form_frame,
            text="Announcement Message:",
            font=("Arial", 10, "bold"),
            bg=WHITE,
            fg=TEXT
        ).pack(anchor="w")

        message_text = tk.Text(
            form_frame,
            height=4,
            font=("Arial", 11),
            wrap="word",
            relief="solid",
            bd=1
        )

        message_text.pack(
            fill="x",
            pady=6
        )

        table_card = tk.Frame(
            content_frame,
            bg=WHITE,
            padx=15,
            pady=13,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        table_card.pack(
            fill="both",
            expand=True
        )

        tk.Label(
            table_card,
            text="PUBLISHED ANNOUNCEMENTS",
            font=("Arial", 13, "bold"),
            bg=WHITE,
            fg=NAVY
        ).pack(
            anchor="w",
            pady=(0, 10)
        )

        columns = (
            "ID",
            "Title",
            "Message",
            "Date"
        )

        table_frame, announcement_table = create_table(
            table_card,
            columns,
            columns,
            (60, 180, 400, 150),
            height=8
        )

        table_frame.pack(
            fill="both",
            expand=True
        )

        def load_announcements():

            for item in announcement_table.get_children():
                announcement_table.delete(item)

            connection = create_connection()

            if connection is None:

                messagebox.showerror(
                    "Error",
                    "Database connection failed.",
                    parent=root
                )

                return

            try:
                cursor = connection.cursor()

                cursor.execute("""
                    SELECT
                        announcement_id,
                        title,
                        message,
                        created_at
                    FROM Announcements
                    ORDER BY created_at DESC
                """)

                for announcement in cursor.fetchall():

                    announcement_table.insert(
                        "",
                        "end",
                        values=announcement
                    )

            except Exception as error:

                messagebox.showerror(
                    "Error",
                    str(error),
                    parent=root
                )

            finally:
                connection.close()

        def publish_announcement():

            title = title_entry.get().strip()

            message = message_text.get(
                "1.0",
                tk.END
            ).strip()

            if not title or not message:

                messagebox.showwarning(
                    "Missing Information",
                    "Please enter both the title and message.",
                    parent=root
                )

                return

            connection = create_connection()

            if connection is None:

                messagebox.showerror(
                    "Error",
                    "Database connection failed.",
                    parent=root
                )

                return

            try:
                cursor = connection.cursor()

                cursor.execute("""
                    INSERT INTO Announcements
                    (title, message, created_by)
                    VALUES (%s, %s, %s)
                """, (
                    title,
                    message,
                    user_id
                ))

                connection.commit()

                messagebox.showinfo(
                    "Success",
                    "Announcement published successfully!",
                    parent=root
                )

                title_entry.delete(0, tk.END)

                message_text.delete(
                    "1.0",
                    tk.END
                )

                load_announcements()

            except Exception as error:

                connection.rollback()

                messagebox.showerror(
                    "Error",
                    str(error),
                    parent=root
                )

            finally:
                connection.close()

        action_button(
            form_frame,
            "PUBLISH ANNOUNCEMENT",
            publish_announcement,
            color=GREEN
        ).pack(
            anchor="e",
            pady=(8, 0)
        )

        load_announcements()

    # ==================================================
    # 5. VIEW SYSTEM REPORTS
    # ==================================================

    def reports_page():

        page_header(
            "Smart Water System Reports",
            "Monitor complaint progress and the water supply condition of all buildings."
        )

        # ---------------- COMPLAINT SUMMARY ----------------

        tk.Label(
            content_frame,
            text="COMPLAINT SUMMARY",
            font=("Arial", 13, "bold"),
            bg=LIGHT_BLUE,
            fg=NAVY
        ).pack(
            anchor="w",
            pady=(0, 8)
        )

        complaint_frame = tk.Frame(
            content_frame,
            bg=LIGHT_BLUE
        )

        complaint_frame.pack(
            fill="x",
            pady=(0, 15)
        )

        complaint_labels = {}

        summary_items = [
            ("Total Complaints", "total", OCEAN_BLUE),
            ("Pending", "pending", RED),
            ("In Progress", "progress", ORANGE),
            ("Resolved", "resolved", GREEN)
        ]

        for title, key, accent in summary_items:

            card, value_label = create_card(
                complaint_frame,
                title,
                "0",
                accent
            )

            card.pack(
                side="left",
                expand=True,
                fill="both",
                padx=5
            )

            complaint_labels[key] = value_label

        # ---------------- WATER SUMMARY ----------------

        tk.Label(
            content_frame,
            text="WATER STATUS SUMMARY",
            font=("Arial", 13, "bold"),
            bg=LIGHT_BLUE,
            fg=NAVY
        ).pack(
            anchor="w",
            pady=(0, 8)
        )

        water_frame = tk.Frame(
            content_frame,
            bg=LIGHT_BLUE
        )

        water_frame.pack(
            fill="x",
            pady=(0, 15)
        )

        water_labels = {}

        water_items = [
            ("Available", "available", GREEN),
            ("Low Supply", "low", ORANGE),
            ("No Water", "none", RED)
        ]

        for title, key, accent in water_items:

            card, value_label = create_card(
                water_frame,
                title,
                "0",
                accent
            )

            card.pack(
                side="left",
                expand=True,
                fill="both",
                padx=5
            )

            water_labels[key] = value_label

        # ---------------- BUILDING STATUS TABLE ----------------

        table_card = tk.Frame(
            content_frame,
            bg=WHITE,
            padx=18,
            pady=18,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        table_card.pack(
            fill="both",
            expand=True,
            pady=(5, 10)
        )

        tk.Label(
            table_card,
            text="WATER STATUS OF EACH BUILDING",
            font=("Arial", 15, "bold"),
            bg=WHITE,
            fg=NAVY
        ).pack(
            anchor="w",
            pady=(0, 14)
        )

        columns = (
            "building",
            "status",
            "remarks",
            "updated"
        )

        table_frame, table = create_table(
            table_card,
            columns,
            (
                "Building Name",
                "Water Status",
                "Remarks",
                "Last Updated"
            ),
            (200, 160, 380, 190),
            height=12
        )

        table_frame.pack(
            fill="both",
            expand=True
        )

        def load_reports():

            for item in table.get_children():
                table.delete(item)

            connection = create_connection()

            if connection is None:

                messagebox.showerror(
                    "Error",
                    "Database connection failed.",
                    parent=root
                )

                return

            try:
                cursor = connection.cursor()

                # Complaint statistics

                cursor.execute("""
                    SELECT
                        COUNT(*),
                        COUNT(CASE WHEN status = 'Pending' THEN 1 END),
                        COUNT(CASE WHEN status = 'In Progress' THEN 1 END),
                        COUNT(CASE WHEN status = 'Resolved' THEN 1 END)
                    FROM Complaints
                """)

                complaint_data = cursor.fetchone()

                total, pending, progress, resolved = complaint_data

                complaint_labels["total"].config(
                    text=str(total)
                )

                complaint_labels["pending"].config(
                    text=str(pending)
                )

                complaint_labels["progress"].config(
                    text=str(progress)
                )

                complaint_labels["resolved"].config(
                    text=str(resolved)
                )

                # Water statistics

                cursor.execute("""
                    SELECT
                        COUNT(CASE WHEN status = 'Available' THEN 1 END),
                        COUNT(CASE WHEN status = 'Low Supply' THEN 1 END),
                        COUNT(CASE WHEN status = 'No Water' THEN 1 END)
                    FROM Water_Status
                """)

                water_data = cursor.fetchone()

                available, low, no_water = water_data

                water_labels["available"].config(
                    text=str(available)
                )

                water_labels["low"].config(
                    text=str(low)
                )

                water_labels["none"].config(
                    text=str(no_water)
                )

                # All 12 building statuses

                cursor.execute("""
                    SELECT
                        Buildings.building_name,
                        Water_Status.status,
                        Water_Status.remarks,
                        Water_Status.updated_at
                    FROM Buildings
                    LEFT JOIN Water_Status
                        ON Buildings.building_id = Water_Status.building_id
                    ORDER BY Buildings.building_id
                """)

                buildings = cursor.fetchall()

                for building in buildings:

                    building_name, status, remarks, updated = building

                    table.insert(
                        "",
                        "end",
                        values=(
                            building_name,
                            status if status else "Not Set",
                            remarks if remarks else "No remarks",
                            updated if updated else "Not available"
                        )
                    )

            except Exception as error:

                messagebox.showerror(
                    "Report Error",
                    str(error),
                    parent=root
                )

            finally:
                connection.close()

        action_button(
            content_frame,
            "REFRESH REPORTS",
            load_reports,
            color=GREEN
        ).pack(
            anchor="e",
            pady=(10, 0)
        )

        load_reports()

    # ==================================================
    # SIDEBAR NAVIGATION
    # ==================================================

    sidebar_button("Dashboard")
    sidebar_button("Manage Complaints")
    sidebar_button("Update Water Status")
    sidebar_button("Manage Announcements")
    sidebar_button("View Reports")

    # ==================================================
    # LOGOUT
    # ==================================================

    tk.Frame(
        sidebar,
        bg="#42647D",
        height=1
    ).pack(
        fill="x",
        padx=20,
        pady=(25, 15)
    )

    def logout():

        confirm = messagebox.askyesno(
            "Confirm Logout",
            "Are you sure you want to logout?",
            parent=root
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

    sidebar_button("Logout")

    sidebar_buttons["Logout"].config(
        command=logout
    )

    tk.Label(
        sidebar,
        text="AquaFlow Water Management",
        font=("Arial", 8),
        bg=NAVY,
        fg="#9ACDE6"
    ).pack(
        side="bottom",
        pady=18
    )

    # ==================================================
    # OPEN DASHBOARD
    # ==================================================

    show_page("Dashboard")

    root.mainloop()

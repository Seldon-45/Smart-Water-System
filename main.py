
import tkinter as tk
from tkinter import ttk, messagebox
import hashlib
import hmac
import math
import random

from database import create_connection
from student_dashboard import open_captain_dashboard
from admin_dashboard import open_admin_dashboard


# ==========================================
# 1. COLOUR THEME
# ==========================================

NAVY = "#102B46"
DARK_BLUE = "#123D5A"
OCEAN = "#168AAD"
AQUA = "#48CAE4"
LIGHT_BLUE = "#EAF6FC"
WHITE = "#FFFFFF"
TEXT_GREY = "#718096"


# ==========================================
# 2. PASSWORD VERIFICATION
# ==========================================

def verify_password(password, stored_hash):
    try:
        salt, saved_hash = stored_hash.split("$")

        calculated_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode(),
            bytes.fromhex(salt),
            600000
        ).hex()

        return hmac.compare_digest(calculated_hash, saved_hash)

    except (ValueError, AttributeError):
        return False


# ==========================================
# 3. LOGIN FUNCTION
# ==========================================

def login():

    login_id = user_entry.get().strip()
    password = password_entry.get()
    selected_role = role_box.get()

    if not login_id or not password or not selected_role:
        messagebox.showwarning(
            "Missing Information",
            "Please fill in all fields."
        )
        return

    connection = create_connection()

    if connection is None:
        messagebox.showerror(
            "Connection Error",
            "Could not connect to the database."
        )
        return

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT user_id, full_name, password_hash, role
            FROM Users
            WHERE login_id = %s
            """,
            (login_id,)
        )

        account = cursor.fetchone()

        if account is None:
            messagebox.showerror(
                "Login Failed",
                "User ID does not exist."
            )
            return

        account_user_id, full_name, stored_hash, database_role = account

        if not verify_password(password, stored_hash):
            messagebox.showerror(
                "Login Failed",
                "Incorrect password."
            )
            return

        expected_role = (
            "Captain"
            if selected_role == "Building Captain"
            else "Admin"
        )

        if database_role != expected_role:
            messagebox.showerror(
                "Login Failed",
                "The selected role does not match your account."
            )
            return

        connection.close()
        connection = None

        root.destroy()

        if database_role == "Captain":
            open_captain_dashboard(full_name, account_user_id)

        elif database_role == "Admin":
            open_admin_dashboard(full_name, account_user_id)

    except Exception as error:
        messagebox.showerror("Error", str(error))

    finally:
        if connection is not None:
            connection.close()


# ==========================================
# 4. CLEAR LOGIN FIELDS
# ==========================================

def clear_fields():

    user_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

    role_box.set("Building Captain")

    user_entry.focus_set()


# ==========================================
# 5. SHOW / HIDE PASSWORD
# ==========================================

def toggle_password():

    if show_password_var.get():
        password_entry.configure(show="")
    else:
        password_entry.configure(show="*")


# ==========================================
# 6. MAIN WINDOW
# ==========================================

root = tk.Tk()

root.title("AquaFlow | Smart Water Management System")
root.geometry("1050x680")
root.minsize(900, 620)
root.configure(bg="#F3F8FC")


# ==========================================
# 7. LEFT WATER PANEL
# ==========================================

water_canvas = tk.Canvas(
    root,
    width=430,
    bg=NAVY,
    highlightthickness=0
)

water_canvas.pack(
    side="left",
    fill="y"
)


# Background decorative circles

water_canvas.create_oval(
    -130, 30, 230, 390,
    outline="#174B68",
    width=2
)

water_canvas.create_oval(
    220, 100, 550, 430,
    outline="#174B68",
    width=2
)

water_canvas.create_oval(
    -150, 360, 180, 690,
    outline="#174B68",
    width=2
)


# Brand name

water_canvas.create_text(
    35, 55,
    text="AquaFlow",
    anchor="w",
    font=("Arial", 29, "bold"),
    fill=WHITE
)

water_canvas.create_text(
    37, 95,
    text="SMART WATER MANAGEMENT",
    anchor="w",
    font=("Arial", 9, "bold"),
    fill=AQUA
)


# Main water drop

water_canvas.create_text(
    215, 240,
    text="💧",
    font=("Arial", 90),
    fill=WHITE
)


# Main message

water_canvas.create_text(
    215, 350,
    text="Every Drop Matters",
    font=("Arial", 22, "bold"),
    fill=WHITE
)

water_canvas.create_text(
    215, 388,
    text="Smarter monitoring for a better future.",
    font=("Arial", 10),
    fill="#C5E8F5"
)


# Feature messages

water_canvas.create_text(
    215, 455,
    text="●  Monitor Water Availability",
    font=("Arial", 11, "bold"),
    fill="#D8F4FC"
)

water_canvas.create_text(
    215, 490,
    text="●  Report Water Issues",
    font=("Arial", 11, "bold"),
    fill="#D8F4FC"
)

water_canvas.create_text(
    215, 525,
    text="●  Track Maintenance Progress",
    font=("Arial", 11, "bold"),
    fill="#D8F4FC"
)


# ==========================================
# 8. FLOATING BUBBLES
# ==========================================

bubbles = []

for i in range(18):

    x = random.randint(20, 400)
    y = random.randint(50, 650)
    size = random.randint(3, 9)
    speed = random.uniform(0.5, 1.5)

    bubble = water_canvas.create_oval(
        x, y,
        x + size, y + size,
        outline="#72DDF2",
        width=1
    )

    bubbles.append({
        "id": bubble,
        "x": x,
        "y": y,
        "size": size,
        "speed": speed
    })


# ==========================================
# 9. FALLING WATER DROPLETS
# ==========================================

droplets = []

for i in range(10):

    x = random.randint(20, 400)
    y = random.randint(-400, 650)
    speed = random.uniform(2, 4)

    drop = water_canvas.create_oval(
        x, y,
        x + 5, y + 11,
        fill=AQUA,
        outline=""
    )

    droplets.append({
        "id": drop,
        "x": x,
        "y": y,
        "speed": speed
    })


# ==========================================
# 10. ANIMATED WATER WAVES
# ==========================================

wave1 = water_canvas.create_polygon(
    0, 550, 430, 550, 430, 680, 0, 680,
    fill="#168AAD",
    outline=""
)

wave2 = water_canvas.create_polygon(
    0, 590, 430, 590, 430, 680, 0, 680,
    fill="#48CAE4",
    outline=""
)


animation_time = 0


def animate_water():

    global animation_time

    animation_time += 0.12

    width = water_canvas.winfo_width()
    height = water_canvas.winfo_height()

    if width < 10:
        width = 430

    # First wave

    points1 = [0, height]

    for x in range(0, width + 10, 10):

        y = (
            height - 105
            + math.sin(x * 0.018 + animation_time) * 13
        )

        points1.extend([x, y])

    points1.extend([width, height])

    water_canvas.coords(wave1, *points1)

    # Second wave

    points2 = [0, height]

    for x in range(0, width + 10, 10):

        y = (
            height - 72
            + math.sin(x * 0.018 + animation_time + 2) * 11
        )

        points2.extend([x, y])

    points2.extend([width, height])

    water_canvas.coords(wave2, *points2)

    # Floating bubbles

    for bubble in bubbles:

        bubble["y"] -= bubble["speed"]

        if bubble["y"] < -15:
            bubble["y"] = height + random.randint(10, 100)
            bubble["x"] = random.randint(10, width - 15)

        x = bubble["x"]
        y = bubble["y"]
        size = bubble["size"]

        water_canvas.coords(
            bubble["id"],
            x, y,
            x + size, y + size
        )

    # Falling droplets

    for drop in droplets:

        drop["y"] += drop["speed"]

        if drop["y"] > height:
            drop["y"] = random.randint(-150, -20)
            drop["x"] = random.randint(15, width - 15)

        x = drop["x"]
        y = drop["y"]

        water_canvas.coords(
            drop["id"],
            x, y,
            x + 5, y + 11
        )

    root.after(35, animate_water)


# ==========================================
# 11. RIGHT LOGIN SECTION
# ==========================================

right_frame = tk.Frame(
    root,
    bg="#F3F8FC"
)

right_frame.pack(
    side="right",
    fill="both",
    expand=True
)


# Login card

login_frame = tk.Frame(
    right_frame,
    bg=WHITE,
    padx=48,
    pady=35,
    highlightbackground="#DCEAF2",
    highlightthickness=1
)

login_frame.place(
    relx=0.5,
    rely=0.47,
    anchor="center"
)


# Small accent line

accent = tk.Frame(
    login_frame,
    bg=AQUA,
    height=5,
    width=65
)

accent.pack(anchor="w", pady=(0, 18))


# Heading

tk.Label(
    login_frame,
    text="Welcome Back!",
    font=("Arial", 27, "bold"),
    bg=WHITE,
    fg=NAVY
).pack(anchor="w", pady=(0, 5))


tk.Label(
    login_frame,
    text="Sign in to continue to your account.",
    font=("Arial", 10),
    bg=WHITE,
    fg=TEXT_GREY
).pack(anchor="w", pady=(0, 27))


# Security label

tk.Label(
    login_frame,
    text="  SECURE ACCOUNT ACCESS  ",
    font=("Arial", 8, "bold"),
    bg="#E6F7FC",
    fg=OCEAN,
    pady=6
).pack(anchor="w", pady=(0, 22))


# ==========================================
# 12. USER ID FIELD
# ==========================================

tk.Label(
    login_frame,
    text="USER ID",
    font=("Arial", 9, "bold"),
    bg=WHITE,
    fg=DARK_BLUE
).pack(anchor="w")


user_entry = tk.Entry(
    login_frame,
    font=("Arial", 12),
    width=34,
    bg="#F5F9FC",
    fg=NAVY,
    relief="flat",
    highlightthickness=1,
    highlightbackground="#DCEAF2",
    highlightcolor=OCEAN,
    insertbackground=NAVY
)

user_entry.pack(
    pady=(8, 19),
    ipady=11
)


# ==========================================
# 13. PASSWORD FIELD
# ==========================================

tk.Label(
    login_frame,
    text="PASSWORD",
    font=("Arial", 9, "bold"),
    bg=WHITE,
    fg=DARK_BLUE
).pack(anchor="w")


password_entry = tk.Entry(
    login_frame,
    font=("Arial", 12),
    width=34,
    show="*",
    bg="#F5F9FC",
    fg=NAVY,
    relief="flat",
    highlightthickness=1,
    highlightbackground="#DCEAF2",
    highlightcolor=OCEAN,
    insertbackground=NAVY
)

password_entry.pack(
    pady=(8, 8),
    ipady=11
)


# Show password option

show_password_var = tk.BooleanVar(value=False)

show_password_check = tk.Checkbutton(
    login_frame,
    text="Show password",
    variable=show_password_var,
    command=toggle_password,
    font=("Arial", 9),
    bg=WHITE,
    fg=TEXT_GREY,
    activebackground=WHITE,
    activeforeground=OCEAN,
    selectcolor=WHITE,
    cursor="hand2"
)

show_password_check.pack(
    anchor="w",
    pady=(0, 18)
)


# ==========================================
# 14. ROLE SELECTION
# ==========================================

tk.Label(
    login_frame,
    text="LOGIN AS",
    font=("Arial", 9, "bold"),
    bg=WHITE,
    fg=DARK_BLUE
).pack(anchor="w")


style = ttk.Style()

style.theme_use("clam")

style.configure(
    "Aqua.TCombobox",
    fieldbackground="#F5F9FC",
    background="#F5F9FC",
    foreground=NAVY,
    bordercolor="#DCEAF2",
    padding=10,
    font=("Arial", 11)
)

style.map(
    "Aqua.TCombobox",
    fieldbackground=[("readonly", "#F5F9FC")],
    selectbackground=[("readonly", "#F5F9FC")],
    selectforeground=[("readonly", NAVY)]
)


role_box = ttk.Combobox(
    login_frame,
    values=["Admin", "Building Captain"],
    state="readonly",
    font=("Arial", 11),
    width=31,
    style="Aqua.TCombobox"
)

role_box.pack(
    pady=(8, 24),
    ipady=5
)

role_box.set("Building Captain")


# ==========================================
# 15. BUTTON HOVER EFFECTS
# ==========================================

def login_hover(event):
    login_button.configure(bg="#126F91")


def login_leave(event):
    login_button.configure(bg=OCEAN)


def clear_hover(event):
    clear_button.configure(bg="#E0F1F8")


def clear_leave(event):
    clear_button.configure(bg="#F0F7FA")


# ==========================================
# 16. BUTTONS
# ==========================================

button_frame = tk.Frame(
    login_frame,
    bg=WHITE
)

button_frame.pack(fill="x")


login_button = tk.Button(
    button_frame,
    text="SIGN IN  →",
    font=("Arial", 11, "bold"),
    bg=OCEAN,
    fg=WHITE,
    activebackground="#126F91",
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2",
    width=22,
    pady=12,
    command=login
)

login_button.pack(
    side="left",
    fill="x",
    expand=True,
    padx=(0, 8)
)

login_button.bind("<Enter>", login_hover)
login_button.bind("<Leave>", login_leave)


clear_button = tk.Button(
    button_frame,
    text="CLEAR",
    font=("Arial", 10, "bold"),
    bg="#F0F7FA",
    fg=DARK_BLUE,
    activebackground="#E0F1F8",
    activeforeground=NAVY,
    relief="flat",
    cursor="hand2",
    width=9,
    pady=12,
    command=clear_fields
)

clear_button.pack(side="right")

clear_button.bind("<Enter>", clear_hover)
clear_button.bind("<Leave>", clear_leave)


# Press Enter to log in

root.bind("<Return>", lambda event: login())


# ==========================================
# 17. FOOTER
# ==========================================

tk.Label(
    right_frame,
    text="SMART WATER ISSUE MONITORING & MANAGEMENT SYSTEM",
    font=("Arial", 8, "bold"),
    bg="#F3F8FC",
    fg="#8297A8"
).pack(
    side="bottom",
    pady=15
)


# ==========================================
# 18. START APPLICATION
# ==========================================

root.after(100, animate_water)

user_entry.focus_set()

root.mainloop()

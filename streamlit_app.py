
import os
import hashlib
import hmac
from pathlib import Path

import mysql.connector
import streamlit as st
import streamlit.components.v1 as components

# =========================================================
# AQUAFLOW - SMART WATER ISSUE MONITORING SYSTEM
# Streamlit Version
# =========================================================

st.set_page_config(
    page_title="AquaFlow | Smart Water Management",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded",
)

NAVY = "#102B46"
OCEAN = "#168AAD"
AQUA = "#48CAE4"

# =========================================================
# CUSTOM DESIGN AND CSS
# =========================================================

st.markdown(
    f"""
    <style>
      .stApp {{
          background: #F3F8FC;
      }}

      [data-testid="stHeader"] {{
          background: transparent;
      }}

      .block-container {{
          padding: 1.2rem 2rem 2rem 2rem;
          max-width: 1500px;
      }}

      [data-testid="stSidebar"] {{
          background: {NAVY};
      }}

      [data-testid="stSidebar"] * {{
          color: white !important;
      }}

      .brand {{
          color: {NAVY};
          font-size: 2.15rem;
          font-weight: 800;
      }}

      .subbrand {{
          color: {OCEAN};
          font-size: .82rem;
          font-weight: 700;
          letter-spacing: 1px;
      }}

      div[data-testid="stMetric"] {{
          background: white;
          padding: 14px;
          border-radius: 10px;
          border: 1px solid #DCE8F1;
      }}

      .stButton > button {{
          border-radius: 5px;
          font-weight: 700;
          min-height: 2.8rem;
      }}

      /* LOGIN WATER PANEL */

      .login-water-panel {{
          position: relative;
          overflow: hidden;
          min-height: 650px;
          height: 78vh;
          border-radius: 3px;
          padding: 36px 32px;
          color: white;
          background: linear-gradient(
              160deg,
              #102B46 0%,
              #123D5A 58%,
              #168AAD 100%
          );
      }}

      .login-water-panel:before,
      .login-water-panel:after {{
          content: "";
          position: absolute;
          border: 2px solid rgba(72,202,228,.12);
          border-radius: 50%;
          width: 350px;
          height: 350px;
          pointer-events: none;
      }}

      .login-water-panel:before {{
          top: 90px;
          left: -145px;
      }}

      .login-water-panel:after {{
          top: 160px;
          right: -205px;
          width: 330px;
          height: 330px;
      }}

      .water-brand {{
          position: relative;
          z-index: 2;
          font-size: 2rem;
          font-weight: 800;
      }}

      .water-tag {{
          position: relative;
          z-index: 2;
          color: #48CAE4;
          font-size: .72rem;
          font-weight: 800;
          letter-spacing: 1.5px;
      }}

      .water-center {{
          position: relative;
          z-index: 2;
          text-align: center;
          margin-top: 100px;
      }}

      .water-drop {{
          font-size: 5.8rem;
          line-height: 1.1;
          filter: drop-shadow(0 8px 12px rgba(0,0,0,.15));
      }}

      .water-title {{
          color: white;
          font-size: 1.55rem;
          font-weight: 800;
          margin-top: 18px;
      }}

      .water-copy {{
          color: #C5E8F5;
          font-size: .88rem;
          margin-top: 8px;
      }}

      .water-features {{
          position: relative;
          z-index: 2;
          margin: 42px auto 0;
          width: fit-content;
          color: #D8F4FC;
          font-size: .9rem;
          font-weight: 700;
          line-height: 2.7;
      }}

      .water-features div {{
          white-space: nowrap;
      }}

      /* ANIMATED BUBBLES */

      .bubble {{
          position: absolute;
          bottom: -20px;
          width: 8px;
          height: 8px;
          border: 1px solid #72DDF2;
          border-radius: 50%;
          opacity: .65;
          animation: rise 8s linear infinite;
      }}

      .bubble.b1 {{
          left: 12%;
          animation-delay: 0s;
      }}

      .bubble.b2 {{
          left: 30%;
          width: 5px;
          height: 5px;
          animation-delay: 2s;
          animation-duration: 10s;
      }}

      .bubble.b3 {{
          left: 67%;
          width: 10px;
          height: 10px;
          animation-delay: 1s;
          animation-duration: 9s;
      }}

      .bubble.b4 {{
          left: 85%;
          width: 6px;
          height: 6px;
          animation-delay: 4s;
      }}

      @keyframes rise {{
          from {{
              transform: translateY(0);
              opacity: .1;
          }}
          20% {{
              opacity: .7;
          }}
          to {{
              transform: translateY(-650px);
              opacity: 0;
          }}
      }}

      /* ANIMATED WATER WAVES */

      .wave-wrap {{
          position: absolute;
          bottom: 0;
          left: 0;
          width: 200%;
          height: 90px;
      }}

      .wave {{
          position: absolute;
          bottom: -30px;
          width: 200%;
          height: 105px;
          border-radius: 43%;
          background: rgba(22,138,173,.6);
          animation: waveMove 9s linear infinite;
      }}

      .wave.two {{
          bottom: -43px;
          background: rgba(72,202,228,.5);
          animation-duration: 12s;
          animation-direction: reverse;
      }}

      @keyframes waveMove {{
          from {{
              transform: translateX(0) rotate(0deg);
          }}
          to {{
              transform: translateX(-25%) rotate(4deg);
          }}
      }}

      /* LOGIN FORM */

      .login-heading {{
          color: #102B46;
          font-size: 2rem;
          font-weight: 800;
          margin-bottom: 0;
      }}

      .login-subheading {{
          color: #718096;
          margin-top: 3px;
          margin-bottom: 22px;
      }}

      .secure-label {{
          display: inline-block;
          padding: 6px 10px;
          background: #E6F7FC;
          color: #168AAD;
          font-size: .72rem;
          font-weight: 800;
          letter-spacing: .5px;
          margin: 8px 0 20px 0;
      }}

      .login-footer {{
          color: #8297A8;
          font-size: .67rem;
          font-weight: 800;
          letter-spacing: .5px;
          text-align: center;
          margin-top: 30px;
      }}

      @media(max-width: 850px) {{
          .login-water-panel {{
              min-height: 420px;
              height: auto;
          }}

          .water-center {{
              margin-top: 45px;
          }}

          .water-features {{
              margin-top: 20px;
          }}
      }}


      /* BUILDING CAPTAIN DASHBOARD - MATCH TKINTER DESIGN */
      [data-testid="stSidebar"] {{
          background: #153F5F !important;
          min-width: 250px;
          max-width: 250px;
      }}
      [data-testid="stSidebar"] > div:first-child {{
          background: #153F5F !important;
      }}
      [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
      [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1,
      [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2,
      [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3 {{
          color: #FFFFFF !important;
      }}
      .af-sidebar-brand {{
          color: #FFFFFF;
          font-size: 2rem;
          font-weight: 800;
          padding: 20px 8px 0 8px;
          line-height: 1.2;
      }}
      .af-sidebar-tag {{
          color: #B9DDF0;
          font-size: .68rem;
          font-weight: 700;
          padding: 5px 10px 25px 10px;
          border-bottom: 1px solid rgba(255,255,255,.2);
          letter-spacing: .2px;
      }}
      .af-menu-label {{
          color: #B9DDF0;
          font-size: .72rem;
          font-weight: 700;
          padding: 18px 8px 10px 8px;
      }}
      [data-testid="stSidebar"] [data-testid="stRadio"] label {{
          color: #FFFFFF !important;
          font-weight: 650 !important;
          padding: 7px 9px !important;
      }}
      [data-testid="stSidebar"] [data-testid="stRadio"] > label {{
          display: none;
      }}
      [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] {{
          gap: 5px;
      }}
      [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] label {{
          border-radius: 0 !important;
      }}
      [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) {{
          background: #2877A6 !important;
      }}
      [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] label p {{
          color: white !important;
      }}
      [data-testid="stSidebar"] .stButton > button {{
          background: #C6382B !important;
          color: white !important;
          border: 0 !important;
          border-radius: 0 !important;
          font-weight: 700;
          margin-top: 20px;
      }}
      .af-topbar {{
          background: #FFFFFF;
          margin: -1.2rem -2rem 1.5rem -2rem;
          padding: 18px 30px;
          min-height: 76px;
          display: flex;
          align-items: center;
          justify-content: space-between;
          border-bottom: 1px solid #E4EDF4;
      }}
      .af-topbar-welcome {{
          color: #123D63;
          font-size: 1.55rem;
          font-weight: 750;
      }}
      .af-topbar-role {{
          color: #12649A;
          font-size: .72rem;
          font-weight: 750;
          text-align: right;
      }}
      .af-dashboard-title {{
          color: #153F67;
          font-size: 1.75rem;
          font-weight: 750;
          margin: 4px 0 2px 0;
      }}
      .af-dashboard-subtitle {{
          color: #7189A0;
          font-size: .86rem;
          margin-bottom: 25px;
      }}
      .af-welcome-panel {{
          background: #FFFFFF;
          border: 1px solid #D6E4EF;
          padding: 22px 24px;
          margin-bottom: 24px;
      }}
      .af-welcome-title {{
          color: #153F67;
          font-size: 1.65rem;
          font-weight: 750;
          margin-bottom: 8px;
      }}
      .af-welcome-copy {{
          color: #7189A0;
          font-size: .85rem;
      }}
      .af-dashboard-card {{
          background: #FFFFFF;
          border: 1px solid #D6E4EF;
          min-height: 96px;
          padding: 15px 18px;
          margin-bottom: 16px;
      }}
      .af-card-number {{
          display: inline-block;
          color: #FFFFFF;
          background: #2877A6;
          font-size: .82rem;
          font-weight: 750;
          padding: 6px 12px;
          margin-bottom: 8px;
      }}
      .af-card-number.teal {{ background: #168C9B; }}
      .af-card-number.blue {{ background: #477DB5; }}
      .af-card-number.green {{ background: #27858C; }}
      .af-card-title {{
          color: #153F67;
          font-size: 1rem;
          font-weight: 700;
      }}
      .af-dashboard-footer {{
          color: #8297A8;
          font-size: .68rem;
          text-align: center;
          margin-top: 4px;
          padding-bottom: 5px;
      }}
      @media(max-width: 800px) {{
          [data-testid="stSidebar"] {{ min-width: 210px; max-width: 210px; }}
          .af-topbar {{ margin-left: -1rem; margin-right: -1rem; padding: 15px; }}
      }}

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_db_config():

    try:
        secrets = st.secrets.get("mysql", {})
    except Exception:
        secrets = {}

    return {
        "host": secrets.get(
            "host",
            os.getenv("DB_HOST", "localhost")
        ),
        "user": secrets.get(
            "user",
            os.getenv("DB_USER", "root")
        ),
        # Set DB_PASSWORD in PowerShell before starting Streamlit.
        # Streamlit secrets take priority when configured.
        "password": secrets.get(
            "password",
            os.getenv("DB_PASSWORD", "")
        ),
        "database": secrets.get(
            "database",
            os.getenv("DB_NAME", "smart_water_db")
        ),
        "port": int(
            secrets.get(
                "port",
                os.getenv("DB_PORT", "3306")
            )
        ),
    }


def get_connection():
    return mysql.connector.connect(**get_db_config())


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

    try:
        cursor = connection.cursor()
        cursor.execute(query, params or ())

        connection.commit()

        affected = cursor.rowcount

        cursor.close()

        return affected

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


# =========================================================
# AUTHENTICATION
# =========================================================

def verify_password(password, stored_hash):

    try:
        salt, saved_hash = stored_hash.split("$")

        calculated_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            bytes.fromhex(salt),
            600000,
        ).hex()

        return hmac.compare_digest(
            calculated_hash,
            saved_hash
        )

    except (
        ValueError,
        AttributeError,
        TypeError
    ):
        return False


def authenticate(login_id, password, selected_role):

    account = run_query(
        """
        SELECT user_id, full_name, password_hash, role
        FROM Users
        WHERE login_id = %s
        """,
        (login_id,),
        fetch="one",
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
        return None, "The selected role does not match your account."

    return {
        "user_id": user_id,
        "full_name": full_name,
        "role": database_role,
    }, None


def logout():

    for key in (
        "authenticated",
        "user_id",
        "full_name",
        "role",
        "page"
    ):
        st.session_state.pop(key, None)

    st.rerun()


# =========================================================
# SHARED DATA FUNCTIONS
# =========================================================

def load_water_status():

    return run_query(
        """
        SELECT Buildings.building_name,
               Water_Status.status,
               Water_Status.remarks,
               Water_Status.updated_at

        FROM Buildings

        LEFT JOIN Water_Status
        ON Buildings.building_id = Water_Status.building_id

        ORDER BY Buildings.building_id
        """
    )


def load_announcements():

    return run_query(
        """
        SELECT title, message, created_at
        FROM Announcements
        ORDER BY created_at DESC
        """
    )


def load_complaints(for_user=False):

    if for_user:

        return run_query(
            """
            SELECT Complaints.complaint_id,
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
            (st.session_state.user_id,),
        )

    return run_query(
        """
        SELECT Complaints.complaint_id,
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


# =========================================================
# COMMON HEADER
# =========================================================

def show_header(title, description=""):

    st.markdown(
        '<div class="brand">💧 AquaFlow</div>'
        '<div class="subbrand">'
        'SMART WATER ISSUE MONITORING & MANAGEMENT'
        '</div>',
        unsafe_allow_html=True
    )

    st.title(title)

    if description:
        st.caption(description)


# =========================================================
# LOGIN SCREEN
# =========================================================

def clear_login_fields():

    st.session_state["login_user_id"] = ""
    st.session_state["login_password"] = ""
    st.session_state["login_role"] = "Building Captain"
    st.session_state["login_show_password"] = False


def show_login():

    left_panel, right_panel = st.columns(
        [0.9, 1.1],
        gap="large"
    )

    # LEFT WATER PANEL

    with left_panel:

        components.html(
            """
            <!DOCTYPE html>
            <html>
            <head>
            <style>
                * { box-sizing: border-box; }
                html, body {
                    margin: 0;
                    padding: 0;
                    width: 100%;
                    height: 100%;
                    overflow: hidden;
                    font-family: Arial, sans-serif;
                }
                .login-water-panel {
                    position: relative;
                    overflow: hidden;
                    width: 100%;
                    height: 650px;
                    border-radius: 3px;
                    padding: 36px 32px;
                    color: white;
                    background: linear-gradient(160deg, #102B46 0%, #123D5A 58%, #168AAD 100%);
                }
                .login-water-panel:before,
                .login-water-panel:after {
                    content: "";
                    position: absolute;
                    border: 2px solid rgba(72,202,228,.16);
                    border-radius: 50%;
                    width: 350px;
                    height: 350px;
                    pointer-events: none;
                }
                .login-water-panel:before { top: 90px; left: -145px; }
                .login-water-panel:after {
                    top: 160px;
                    right: -205px;
                    width: 330px;
                    height: 330px;
                }
                .water-brand {
                    position: relative;
                    z-index: 2;
                    font-size: 2rem;
                    font-weight: 800;
                }
                .water-tag {
                    position: relative;
                    z-index: 2;
                    color: #48CAE4;
                    font-size: .72rem;
                    font-weight: 800;
                    letter-spacing: 1.5px;
                    margin-top: 4px;
                }
                .water-center {
                    position: relative;
                    z-index: 2;
                    text-align: center;
                    margin-top: 90px;
                }
                .water-drop {
                    font-size: 5.8rem;
                    line-height: 1.1;
                    filter: drop-shadow(0 8px 12px rgba(0,0,0,.15));
                    animation: dropFloat 3s ease-in-out infinite;
                }
                .water-title {
                    color: white;
                    font-size: 1.55rem;
                    font-weight: 800;
                    margin-top: 18px;
                }
                .water-copy {
                    color: #C5E8F5;
                    font-size: .88rem;
                    margin-top: 8px;
                }
                .water-features {
                    position: relative;
                    z-index: 2;
                    margin: 42px auto 0;
                    width: fit-content;
                    color: #D8F4FC;
                    font-size: .9rem;
                    font-weight: 700;
                    line-height: 2.7;
                }
                .water-features div { white-space: nowrap; }
                .bubble {
                    position: absolute;
                    bottom: -20px;
                    width: 8px;
                    height: 8px;
                    border: 1px solid #72DDF2;
                    border-radius: 50%;
                    opacity: .65;
                    animation: rise 8s linear infinite;
                    z-index: 1;
                }
                .bubble.b1 { left: 12%; animation-delay: 0s; }
                .bubble.b2 { left: 30%; width: 5px; height: 5px; animation-delay: 2s; animation-duration: 10s; }
                .bubble.b3 { left: 67%; width: 10px; height: 10px; animation-delay: 1s; animation-duration: 9s; }
                .bubble.b4 { left: 85%; width: 6px; height: 6px; animation-delay: 4s; }
                @keyframes rise {
                    from { transform: translateY(0); opacity: .1; }
                    20% { opacity: .7; }
                    to { transform: translateY(-650px); opacity: 0; }
                }
                @keyframes dropFloat {
                    0%, 100% { transform: translateY(0); }
                    50% { transform: translateY(-10px); }
                }
                .wave-wrap {
                    position: absolute;
                    bottom: 0;
                    left: 0;
                    width: 200%;
                    height: 90px;
                    z-index: 1;
                }
                .wave {
                    position: absolute;
                    bottom: -30px;
                    width: 200%;
                    height: 105px;
                    border-radius: 43%;
                    background: rgba(22,138,173,.6);
                    animation: waveMove 9s linear infinite;
                }
                .wave.two {
                    bottom: -43px;
                    background: rgba(72,202,228,.5);
                    animation-duration: 12s;
                    animation-direction: reverse;
                }
                @keyframes waveMove {
                    from { transform: translateX(0) rotate(0deg); }
                    to { transform: translateX(-25%) rotate(4deg); }
                }
            </style>
            </head>
            <body>
                <div class="login-water-panel">
                    <div class="water-brand">💧 AquaFlow</div>
                    <div class="water-tag">SMART WATER MANAGEMENT</div>
                    <div class="water-center">
                        <div class="water-drop">💧</div>
                        <div class="water-title">Every Drop Matters</div>
                        <div class="water-copy">Smarter monitoring for a better future.</div>
                    </div>
                    <div class="water-features">
                        <div>● &nbsp; Monitor Water Availability</div>
                        <div>● &nbsp; Report Water Issues</div>
                        <div>● &nbsp; Track Maintenance Progress</div>
                    </div>
                    <span class="bubble b1"></span>
                    <span class="bubble b2"></span>
                    <span class="bubble b3"></span>
                    <span class="bubble b4"></span>
                    <div class="wave-wrap">
                        <div class="wave"></div>
                        <div class="wave two"></div>
                    </div>
                </div>
            </body>
            </html>
            """,
            height=650,
            scrolling=False
        )

    # RIGHT LOGIN FORM

    with right_panel:

        st.markdown(
            '<div style="height:55px"></div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="login-heading">Welcome Back!</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="login-subheading">'
            'Sign in to continue to your account.'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="secure-label">'
            'SECURE ACCOUNT ACCESS'
            '</div>',
            unsafe_allow_html=True
        )

        st.text_input(
            "USER ID",
            key="login_user_id",
            placeholder="Enter your user ID"
        )

        show_password = st.checkbox(
            "Show password",
            key="login_show_password"
        )

        st.text_input(
            "PASSWORD",
            type="default" if show_password else "password",
            key="login_password",
            placeholder="Enter your password"
        )

        st.selectbox(
            "LOGIN AS",
            ["Admin", "Building Captain"],
            index=1,
            key="login_role"
        )

        sign_col, clear_col = st.columns([2.2, 1])

        with sign_col:

            sign_in = st.button(
                "SIGN IN  →",
                type="primary",
                use_container_width=True
            )

        with clear_col:

            st.button(
                "CLEAR",
                use_container_width=True,
                on_click=clear_login_fields
            )

        st.markdown(
            '<div class="login-footer">'
            'SMART WATER ISSUE MONITORING & MANAGEMENT SYSTEM'
            '</div>',
            unsafe_allow_html=True
        )

        if sign_in:

            login_id = st.session_state.get(
                "login_user_id", ""
            ).strip()

            password = st.session_state.get(
                "login_password", ""
            )

            role = st.session_state.get(
                "login_role",
                "Building Captain"
            )

            if not login_id or not password or not role:

                st.warning("Please fill in all fields.")

            else:

                try:

                    user, error = authenticate(
                        login_id,
                        password,
                        role
                    )

                    if error:

                        st.error(error)

                    else:

                        st.session_state.authenticated = True
                        st.session_state.user_id = user["user_id"]
                        st.session_state.full_name = user["full_name"]
                        st.session_state.role = user["role"]
                        st.session_state.page = "Dashboard"

                        st.rerun()

                except mysql.connector.Error as error:

                    st.error(
                        f"Database connection error: {error}"
                    )

                except Exception as error:

                    st.error(
                        f"Unable to sign in: {error}"
                    )


# =========================================================
# SYSTEM REPORTS
# =========================================================

def reports_page():

    show_header(
        "System Reports",
        "Overview of complaints and water supply across all buildings."
    )

    complaint_stats = run_query(
        """
        SELECT COUNT(*),

               COUNT(
                   CASE WHEN status = 'Pending'
                   THEN 1 END
               ),

               COUNT(
                   CASE WHEN status = 'In Progress'
                   THEN 1 END
               ),

               COUNT(
                   CASE WHEN status = 'Resolved'
                   THEN 1 END
               )

        FROM Complaints
        """,
        fetch="one"
    )

    water_stats = run_query(
        """
        SELECT

            COUNT(
                CASE WHEN status = 'Available'
                THEN 1 END
            ),

            COUNT(
                CASE WHEN status = 'Low Supply'
                THEN 1 END
            ),

            COUNT(
                CASE WHEN status = 'No Water'
                THEN 1 END
            )

        FROM Water_Status
        """,
        fetch="one"
    )

    c1, c2, c3, c4 = st.columns(4)

    for col, label, value in zip(
        (c1, c2, c3, c4),
        (
            "Total complaints",
            "Pending",
            "In progress",
            "Resolved"
        ),
        complaint_stats
    ):

        col.metric(label, value or 0)

    st.subheader("Water supply summary")

    w1, w2, w3 = st.columns(3)

    for col, label, value in zip(
        (w1, w2, w3),
        ("Available", "Low supply", "No water"),
        water_stats
    ):

        col.metric(label, value or 0)

    st.subheader("Water status by building")

    rows = load_water_status()

    st.dataframe(
        rows,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# BUILDING CAPTAIN DASHBOARD
# =========================================================

def captain_home():

    # Header styled to match the original Tkinter Building Captain window.
    captain_name = st.session_state.full_name
    st.markdown(
        f"""
        <div class="af-topbar">
            <div class="af-topbar-welcome">Welcome, {captain_name}!</div>
            <div class="af-topbar-role">BUILDING CAPTAIN</div>
        </div>
        <div class="af-dashboard-title">Dashboard Overview</div>
        <div class="af-dashboard-subtitle">
            Monitor water supply and manage water-related issues.
        </div>
        <div class="af-welcome-panel">
            <div class="af-welcome-title">Welcome to AquaFlow!</div>
            <div class="af-welcome-copy">
                Use the menu to monitor water availability, report problems and follow maintenance progress.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Six dashboard shortcuts, arranged like the Tkinter dashboard.
    cards = [
        ("01", "View Water Status", "", "Water Status"),
        ("02", "Submit Water Complaint", "teal", "Submit Complaint"),
        ("03", "View All Complaints", "blue", "All Complaints"),
        ("04", "Complaint History", "blue", "Complaint History"),
        ("05", "Announcements", "green", "Announcements"),
        ("06", "Management Reports", "", "Management Reports"),
    ]

    left, right = st.columns(2, gap="medium")
    for index, (number, title, colour, page_name) in enumerate(cards):
        target = left if index % 2 == 0 else right
        with target:
            st.markdown(
                f"""
                <div class="af-dashboard-card">
                    <span class="af-card-number {colour}">{number}</span>
                    <div class="af-card-title">{title}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown(
        '<div class="af-dashboard-footer">'
        'AquaFlow | Smart Water Issue Monitoring and Management System'
        '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# ADMIN DASHBOARD
# =========================================================

def admin_home():

    # Administrator dashboard styled to match the Tkinter dashboard.
    admin_name = st.session_state.full_name

    st.markdown(
        f"""
        <div class="af-topbar">
            <div class="af-topbar-welcome">Welcome, {admin_name}!</div>
            <div class="af-topbar-role">ADMINISTRATOR</div>
        </div>
        <div class="af-dashboard-title">Dashboard Overview</div>
        <div class="af-dashboard-subtitle">
            Monitor water supply, manage complaints and oversee water-related activities.
        </div>
        <div class="af-welcome-panel">
            <div class="af-welcome-title">Welcome to AquaFlow!</div>
            <div class="af-welcome-copy">
                Use the menu to manage complaints, update water status, publish announcements and review management reports.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Four administrator shortcuts matching the same card style.
    cards = [
        ("01", "Manage Complaints", "", "Manage Complaints"),
        ("02", "Update Water Status", "teal", "Update Water Status"),
        ("03", "Manage Announcements", "blue", "Manage Announcements"),
        ("04", "View Management Reports", "green", "View Reports"),
    ]

    left, right = st.columns(2, gap="medium")
    for index, (number, title, colour, page_name) in enumerate(cards):
        target = left if index % 2 == 0 else right
        with target:
            st.markdown(
                f"""
                <div class="af-dashboard-card">
                    <span class="af-card-number {colour}">{number}</span>
                    <div class="af-card-title">{title}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown(
        '<div class="af-dashboard-footer">'
        'AquaFlow | Smart Water Issue Monitoring and Management System'
        '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# BUILDING CAPTAIN FEATURES
# =========================================================

def captain_water_status():

    show_header(
        "Water Status",
        "Check the current water supply condition in each building."
    )

    rows = load_water_status()

    st.dataframe(
        rows,
        use_container_width=True,
        hide_index=True
    )

    if st.button("Refresh water status"):

        st.rerun()


def submit_complaint():

    show_header(
        "Submit Water Complaint",
        "Report a water-related issue in your building."
    )

    buildings = run_query(
        """
        SELECT building_name
        FROM Buildings
        ORDER BY building_id
        """
    )

    building_names = [
        row[0] for row in buildings
    ]

    if not building_names:

        st.warning(
            "No buildings are available in the database."
        )

        return

    with st.form(
        "complaint_form",
        clear_on_submit=True
    ):

        building = st.selectbox(
            "Select building",
            building_names
        )

        issue = st.selectbox(
            "Issue type",
            [
                "No Water",
                "Low Water Pressure",
                "Water Leakage",
                "Dirty Water",
                "Other"
            ]
        )

        description = st.text_area(
            "Describe the problem"
        )

        photo = st.file_uploader(
            "Attach picture (optional)",
            type=[
                "png",
                "jpg",
                "jpeg",
                "gif",
                "bmp"
            ]
        )

        submitted = st.form_submit_button(
            "SUBMIT COMPLAINT",
            use_container_width=True
        )

    if submitted:

        if not description.strip():

            st.warning(
                "Please describe the problem before submitting."
            )

            return

        photo_path = None

        if photo is not None:

            upload_dir = Path("uploads")

            upload_dir.mkdir(exist_ok=True)

            safe_name = Path(
                photo.name
            ).name.replace(" ", "_")

            saved_file = (
                upload_dir /
                f"{st.session_state.user_id}_{safe_name}"
            )

            saved_file.write_bytes(
                photo.getbuffer()
            )

            photo_path = str(saved_file)

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

            st.error(
                "Selected building was not found."
            )

            return

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
                st.session_state.user_id,
                building_row[0],
                issue,
                description.strip(),
                photo_path
            )
        )

        st.success(
            "Your water complaint has been submitted."
        )

        st.rerun()


def all_complaints_page():

    show_header(
        "All Complaints",
        "View water complaints submitted across all buildings."
    )

    rows = run_query(
        """
        SELECT Complaints.complaint_id,
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

    if rows:

        st.dataframe(
            rows,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "There are currently no water complaints."
        )


def captain_complaints():

    show_header(
        "Complaint History",
        "Track the progress of the complaints you submitted."
    )

    rows = load_complaints(for_user=True)

    if rows:

        st.dataframe(
            rows,
            use_container_width=True,
            hide_index=True
        )

        complaint_ids = [
            row[0] for row in rows
        ]

        selected_id = st.selectbox(
            "View update history for complaint",
            complaint_ids
        )

        updates = run_query(
            """
            SELECT Complaint_Updates.status,
                   Complaint_Updates.remarks,
                   Users.full_name,
                   Complaint_Updates.updated_at

            FROM Complaint_Updates

            INNER JOIN Users
            ON Complaint_Updates.updated_by = Users.user_id

            WHERE Complaint_Updates.complaint_id = %s

            ORDER BY Complaint_Updates.updated_at DESC
            """,
            (selected_id,)
        )

        st.subheader("Complaint updates")

        if updates:

            st.dataframe(
                updates,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No progress updates have been recorded yet."
            )

    else:

        st.info(
            "You have not submitted any complaints yet."
        )


def announcements_page():

    show_header(
        "Announcements",
        "Important water supply notices and college updates."
    )

    rows = load_announcements()

    if rows:

        for title, message, created in rows:

            with st.container(border=True):

                st.subheader(title)

                st.write(message)

                st.caption(str(created))

    else:

        st.info(
            "There are currently no announcements."
        )


# =========================================================
# ADMIN FEATURES
# =========================================================

def admin_complaints():

    show_header(
        "Manage Complaints",
        "Review reported issues and update their progress."
    )

    rows = load_complaints(for_user=False)

    if not rows:

        st.info(
            "There are currently no water complaints."
        )

        return

    st.dataframe(
        rows,
        use_container_width=True,
        hide_index=True
    )

    ids = [
        row[0] for row in rows
    ]

    selected_id = st.selectbox(
        "Select complaint ID to update",
        ids
    )

    selected = next(
        row for row in rows
        if row[0] == selected_id
    )

    photo_result = run_query(
        """
        SELECT photo_path
        FROM Complaints
        WHERE complaint_id = %s
        """,
        (selected_id,),
        fetch="one"
    )

    if (
        photo_result
        and photo_result[0]
        and Path(photo_result[0]).is_file()
    ):

        st.image(
            photo_result[0],
            caption=f"Attachment for complaint #{selected_id}",
            width=350
        )

    elif photo_result and photo_result[0]:

        st.warning(
            "The stored image path is not available on this computer."
        )

    st.write(
        f"**Reported by:** {selected[1]}"
    )

    st.write(
        f"**Building:** {selected[2]}  |  **Issue:** {selected[3]}"
    )

    st.write(
        f"**Description:** {selected[4]}"
    )

    with st.form("update_complaint_form"):

        new_status = st.selectbox(
            "New status",
            [
                "Pending",
                "In Progress",
                "Resolved"
            ],
            index=(
                ["Pending", "In Progress", "Resolved"].index(selected[6])
                if selected[6] in [
                    "Pending",
                    "In Progress",
                    "Resolved"
                ]
                else 0
            )
        )

        remarks = st.text_area(
            "Update remarks"
        )

        save = st.form_submit_button(
            "SAVE UPDATE"
        )

    if save:

        connection = get_connection()

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                UPDATE Complaints
                SET status = %s
                WHERE complaint_id = %s
                """,
                (new_status, selected_id)
            )

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
                    selected_id,
                    st.session_state.user_id,
                    new_status,
                    remarks.strip()
                )
            )

            connection.commit()

            st.success(
                "Complaint updated successfully."
            )

            st.rerun()

        except Exception:

            connection.rollback()

            raise

        finally:

            connection.close()


def admin_water_status():

    show_header(
        "Update Water Status",
        "Update the current water supply condition for a building."
    )

    buildings = run_query(
        """
        SELECT building_name
        FROM Buildings
        ORDER BY building_id
        """
    )

    names = [
        row[0] for row in buildings
    ]

    if not names:

        st.warning(
            "No buildings are available."
        )

        return

    with st.form("water_status_form"):

        building = st.selectbox(
            "Select building",
            names
        )

        status = st.selectbox(
            "Water status",
            [
                "Available",
                "Low Supply",
                "No Water"
            ]
        )

        remarks = st.text_area(
            "Remarks"
        )

        save = st.form_submit_button(
            "SAVE WATER STATUS"
        )

    if save:

        building_row = run_query(
            """
            SELECT building_id
            FROM Buildings
            WHERE building_name = %s
            """,
            (building,),
            fetch="one"
        )

        affected = run_change(
            """
            UPDATE Water_Status

            SET status = %s,
                remarks = %s,
                updated_by = %s

            WHERE building_id = %s
            """,
            (
                status,
                remarks.strip(),
                st.session_state.user_id,
                building_row[0]
            )
        )

        if affected == 0:

            st.error(
                "No water status record exists for this building. "
                "Check the Water_Status table."
            )

        else:

            st.success(
                "Water status updated successfully."
            )

            st.rerun()

    st.subheader(
        "Current status of all buildings"
    )

    st.dataframe(
        load_water_status(),
        use_container_width=True,
        hide_index=True
    )


def admin_announcements():

    show_header(
        "Manage Announcements",
        "Publish notices for building captains and other users."
    )

    with st.form(
        "announcement_form",
        clear_on_submit=True
    ):

        title = st.text_input(
            "Announcement title"
        )

        message = st.text_area(
            "Announcement message"
        )

        publish = st.form_submit_button(
            "PUBLISH ANNOUNCEMENT"
        )

    if publish:

        if not title.strip() or not message.strip():

            st.warning(
                "Please enter both the title and message."
            )

        else:

            run_change(
                """
                INSERT INTO Announcements
                    (title, message, created_by)

                VALUES (%s, %s, %s)
                """,
                (
                    title.strip(),
                    message.strip(),
                    st.session_state.user_id
                )
            )

            st.success(
                "Announcement published successfully."
            )

            st.rerun()

    st.subheader(
        "Published announcements"
    )

    rows = run_query(
        """
        SELECT announcement_id,
               title,
               message,
               created_at

        FROM Announcements

        ORDER BY created_at DESC
        """
    )

    st.dataframe(
        rows,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# MAIN APPLICATION
# =========================================================

def main():

    if not st.session_state.get("authenticated"):

        show_login()

        return

    role = st.session_state.role

    name = st.session_state.full_name

    # SIDEBAR NAVIGATION

    with st.sidebar:

        menu_label = "ADMIN MENU" if role == "Admin" else "CAPTAIN MENU"
        st.markdown(
            '<div class="af-sidebar-brand">AquaFlow</div>'
            '<div class="af-sidebar-tag">SMART WATER MANAGEMENT</div>'
            f'<div class="af-menu-label">{menu_label}</div>',
            unsafe_allow_html=True
        )

        # ADMIN NAVIGATION

        if role == "Admin":

            pages = {

                "Dashboard": admin_home,

                "Manage Complaints": admin_complaints,

                "Update Water Status": admin_water_status,

                "Manage Announcements": admin_announcements,

                "View Reports": reports_page,

            }

        # BUILDING CAPTAIN NAVIGATION

        else:

            pages = {

                "Dashboard": captain_home,

                "Water Status": captain_water_status,

                "Submit Complaint": submit_complaint,

                "All Complaints": all_complaints_page,

                "Complaint History": captain_complaints,

                "Announcements": announcements_page,

                "Management Reports": reports_page,

            }

        selected_page = st.radio(
            "Navigation",
            list(pages.keys())
        )

        st.divider()

        if st.button(
            "Log out",
            use_container_width=True
        ):

            logout()

    # DISPLAY SELECTED PAGE

    try:

        pages[selected_page]()

    except mysql.connector.Error as error:

        st.error(
            f"Database error: {error}"
        )

        st.info(
            "Check that MySQL is running, the smart_water_db database "
            "exists, and the connection settings are correct."
        )

    except Exception as error:

        st.error(
            f"Something went wrong: {error}"
        )


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    main()

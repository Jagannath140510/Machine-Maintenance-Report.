import streamlit as st
import libsql_client
import hashlib
import datetime
import pandas as pd

st.set_page_config(page_title="মেইনটেন্যান্স ম্যানেজার", page_icon="⚙️", layout="wide")

# ------------------- কাস্টম CSS ও HTML থিম ইনজেকশন -------------------
def apply_custom_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }
        .main > div {
            padding-top: 1rem;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0a1929 0%, #132f4c 100%);
            padding-top: 2rem;
        }
        [data-testid="stSidebar"] * {
            color: #e6f1ff !important;
        }
        [data-testid="stSidebar"] .stSelectbox label,
        [data-testid="stSidebar"] .stNumberInput label {
            color: #88b4d9 !important;
            font-weight: 600;
        }
        [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] {
            background-color: #1e3a5f;
            border-radius: 8px;
            border: 1px solid #2b4f7a;
        }
        [data-testid="stSidebar"] .stButton button {
            background: #00b4d8 !important;
            color: #000 !important;
            font-weight: 700;
            border-radius: 20px;
            border: none;
            transition: 0.3s;
        }
        [data-testid="stSidebar"] .stButton button:hover {
            background: #48cae4 !important;
            transform: scale(1.02);
        }
        .sidebar-title {
            font-size: 1.8rem;
            font-weight: 700;
            color: #00b4d8 !important;
            text-align: center;
            border-bottom: 2px solid #00b4d8;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        .sidebar-user {
            background: #1e3a5f;
            padding: 10px;
            border-radius: 30px;
            text-align: center;
            margin-bottom: 20px;
            border: 1px solid #2b4f7a;
            font-size: 0.9rem;
        }

        [data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 15px 10px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
            transition: 0.2s;
        }
        [data-testid="stMetric"]:hover {
            transform: translateY(-5px);
            border-color: #00b4d8;
        }
        [data-testid="stMetric"] label {
            color: #88b4d9 !important;
            font-weight: 600;
            font-size: 1rem !important;
        }
        [data-testid="stMetric"] div[data-testid="stMetricValue"] {
            color: #ffffff !important;
            font-size: 2.2rem !important;
            font-weight: 700;
        }

        .custom-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(5px);
            border-left: 5px solid #00b4d8;
            border-radius: 12px;
            padding: 15px 20px;
            margin-bottom: 15px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: #e6f1ff;
        }
        .custom-card strong {
            color: #48cae4;
        }

        .streamlit-expanderHeader {
            background: rgba(0, 180, 216, 0.15) !important;
            border-radius: 10px !important;
            border: 1px solid #1e3a5f !important;
            color: #e6f1ff !important;
        }
        .streamlit-expanderContent {
            background: rgba(10, 25, 41, 0.8) !important;
            border-radius: 0 0 10px 10px !important;
            border: 1px solid #1e3a5f !important;
            border-top: none !important;
            color: #cbd5e1 !important;
        }

        .badge-red {
            background: #ef4444;
            color: white;
            padding: 4px 12px;
            border-radius: 30px;
            font-weight: 700;
            font-size: 0.8rem;
            display: inline-block;
        }
        .badge-green {
            background: #22c55e;
            color: black;
            padding: 4px 12px;
            border-radius: 30px;
            font-weight: 700;
            font-size: 0.8rem;
            display: inline-block;
        }
        .badge-yellow {
            background: #f59e0b;
            color: black;
            padding: 4px 12px;
            border-radius: 30px;
            font-weight: 700;
            font-size: 0.8rem;
            display: inline-block;
        }

        .login-container {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 90vh;
            background: radial-gradient(circle at 30% 30%, #0a1929, #020617);
        }
        .login-box {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(20px);
            padding: 40px 50px;
            border-radius: 40px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 25px 50px -12px rgba(0,0,0,0.8);
            width: 100%;
            max-width: 420px;
            text-align: center;
        }
        .login-box h1 {
            color: #00b4d8;
            font-size: 2.5rem;
            font-weight: 800;
            margin-bottom: 5px;
        }
        .login-box .sub {
            color: #88b4d9;
            margin-bottom: 30px;
            font-weight: 400;
        }
        .login-box .stTextInput input {
            background: #1e293b !important;
            border: 1px solid #334155 !important;
            border-radius: 30px !important;
            padding: 12px 20px !important;
            color: white !important;
        }
        .login-box .stButton button {
            background: #00b4d8 !important;
            color: #000 !important;
            font-weight: 700;
            border-radius: 40px;
            padding: 10px 40px;
            width: 100%;
            border: none;
            transition: 0.3s;
        }
        .login-box .stButton button:hover {
            background: #48cae4 !important;
            transform: scale(1.02);
        }

        .stDataFrame {
            background: transparent !important;
        }
        .stDataFrame table {
            background: rgba(10, 25, 41, 0.6) !important;
            border-radius: 12px;
            color: #e6f1ff !important;
        }
        .stDataFrame thead tr th {
            background: #1e3a5f !important;
            color: #00b4d8 !important;
        }

        .app-header {
            font-size: 2rem;
            font-weight: 700;
            background: linear-gradient(to right, #00b4d8, #90e0ef);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }
        .app-subheader {
            color: #94a3b8;
            border-bottom: 1px solid #1e293b;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }

        .stTextInput input, .stTextArea textarea, .stNumberInput input {
            background: #1e293b !important;
            border: 1px solid #334155 !important;
            border-radius: 12px !important;
            color: white !important;
        }
        .stSelectbox div[data-baseweb="select"] {
            background: #1e293b !important;
            border-radius: 12px !important;
        }
    </style>
    """, unsafe_allow_html=True)


# ------------------- Turso ডাটাবেস কানেকশন র‍্যাপার -------------------
# sqlite3.Row-এর আচরণ নকল করে, যাতে বাকি কোড অপরিবর্তিত থাকে
class TursoRow(dict):
    def __getitem__(self, key):
        return dict.__getitem__(self, key)


class TursoResult:
    def __init__(self, result_set):
        columns = result_set.columns
        self._rows = [TursoRow(zip(columns, row)) for row in result_set.rows]

    def fetchall(self):
        return self._rows

    def fetchone(self):
        return self._rows[0] if self._rows else None


class TursoConnection:
    def __init__(self, url, auth_token):
        self.client = libsql_client.create_client_sync(url=url, auth_token=auth_token)

    def execute(self, sql, params=None):
        result = self.client.execute(sql, params or [])
        return TursoResult(result)

    def commit(self):
        pass  # libsql প্রতিটা execute-এ auto-commit করে

    def close(self):
        self.client.close()


def get_db_connection():
    return TursoConnection(
        st.secrets["TURSO_DATABASE_URL"],
        st.secrets["TURSO_AUTH_TOKEN"]
    )


def init_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS machines (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    location TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS parts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    machine_id INTEGER,
                    part_name TEXT NOT NULL,
                    install_date TEXT,
                    FOREIGN KEY (machine_id) REFERENCES machines (id))''')
    conn.execute('''CREATE TABLE IF NOT EXISTS maintenance_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    part_id INTEGER,
                    runtime_hours REAL,
                    failure_type TEXT,
                    symptoms_text TEXT,
                    solution_text TEXT,
                    downtime_mins INTEGER,
                    created_by TEXT,
                    created_at TEXT,
                    FOREIGN KEY (part_id) REFERENCES parts (id))''')
    hashed_pw = hashlib.sha256('admin123'.encode()).hexdigest()
    conn.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ['admin', hashed_pw])
    conn.close()


def login_user(username, password):
    hashed = hashlib.sha256(password.encode()).hexdigest()
    conn = get_db_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?", [username, hashed]
    ).fetchone()
    conn.close()
    return user is not None


def init_session_state():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = ""


# ------------------- লগইন পেজ -------------------
def login_page():
    apply_custom_css()
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown("""
        <div class="login-box">
            <h1>⚙️ মেইনটেন্যান্স</h1>
            <div class="sub">লগইন করে চালিয়ে যান</div>
        </div>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1, 2, 1])
    with col:
        username = st.text_input("ইউজারনেম", key="login_user")
        password = st.text_input("পাসওয়ার্ড", type="password", key="login_pass")
        if st.button("🔓 লগইন করুন"):
            if login_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("❌ ভুল ইউজারনেম বা পাসওয়ার্ড।")
    st.markdown('</div>', unsafe_allow_html=True)


# ------------------- মূল অ্যাপ -------------------
def main_app():
    apply_custom_css()
    st.sidebar.markdown('<div class="sidebar-title">⚙️ মেইনটেন্যান্স</div>', unsafe_allow_html=True)
    st.sidebar.markdown(f'<div class="sidebar-user">👤 {st.session_state.username}</div>', unsafe_allow_html=True)

    menu = ["📊 ড্যাশবোর্ড", "🏗️ মেশিন/পার্ট ম্যানেজ", "📝 নতুন লগ এন্ট্রি", "🔍 ট্রাবলশুটিং", "🔮 প্রেডিকশন"]
    choice = st.sidebar.selectbox("মেনু নির্বাচন করুন", menu)

    if st.sidebar.button("🚪 লগআউট"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

    # ------------------- ড্যাশবোর্ড -------------------
    if choice == "📊 ড্যাশবোর্ড":
        st.markdown('<div class="app-header">📈 ড্যাশবোর্ড</div>', unsafe_allow_html=True)
        st.markdown('<div class="app-subheader">সামগ্রিক মেইনটেন্যান্স অবস্থা</div>', unsafe_allow_html=True)

        conn = get_db_connection()
        total_machines = conn.execute("SELECT COUNT(*) as c FROM machines").fetchone()['c']
        total_parts = conn.execute("SELECT COUNT(*) as c FROM parts").fetchone()['c']
        total_logs = conn.execute("SELECT COUNT(*) as c FROM maintenance_logs").fetchone()['c']

        col1, col2, col3 = st.columns(3)
        col1.metric("🏭 মোট মেশিন", total_machines)
        col2.metric("🔩 মোট পার্টস", total_parts)
        col3.metric("📋 মোট লগ", total_logs)

        st.markdown("---")
        st.subheader("🕐 সাম্প্রতিক লগ")
        recent = conn.execute('''
            SELECT l.*, p.part_name, m.name as machine_name
            FROM maintenance_logs l
            JOIN parts p ON l.part_id = p.id
            JOIN machines m ON p.machine_id = m.id
            ORDER BY l.created_at DESC LIMIT 5
        ''').fetchall()

        if recent:
            for row in recent:
                card_html = f"""
                <div class="custom-card">
                    <strong>{row['machine_name']}</strong> → {row['part_name']} <br>
                    <span style="color:#fbbf24;">⚠️ লক্ষণ:</span> {row['symptoms_text'][:80]}... <br>
                    <span style="color:#34d399;">✅ সমাধান:</span> {row['solution_text'][:60]}... <br>
                    <span style="font-size:0.8rem; color:#64748b;">📅 {row['created_at']} | 👤 {row['created_by']}</span>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
        else:
            st.warning("কোনো লগ এখনো যোগ করা হয়নি।")
        conn.close()

    # ------------------- মেশিন/পার্ট ম্যানেজ -------------------
    elif choice == "🏗️ মেশিন/পার্ট ম্যানেজ":
        st.markdown('<div class="app-header">🏗️ মেশিন ও পার্টস</div>', unsafe_allow_html=True)
        conn = get_db_connection()

        with st.expander("➕ নতুন মেশিন যোগ করুন", expanded=True):
            with st.form("add_machine"):
                m_name = st.text_input("মেশিনের নাম")
                m_loc = st.text_input("লোকেশন")
                submit_m = st.form_submit_button("যোগ করুন")
                if submit_m and m_name:
                    conn.execute("INSERT INTO machines (name, location) VALUES (?, ?)", [m_name, m_loc])
                    conn.commit()
                    st.success("✅ মেশিন যোগ হয়েছে!", icon="🎉")
                    st.rerun()

        machines = conn.execute("SELECT * FROM machines").fetchall()
        if machines:
            machine_options = {f"{m['name']} ({m['location']})": m['id'] for m in machines}
            selected_machine_label = st.selectbox("পার্ট যোগ করতে মেশিন নির্বাচন করুন", list(machine_options.keys()))
            selected_machine_id = machine_options[selected_machine_label]

            with st.form("add_part"):
                p_name = st.text_input("পার্টের নাম")
                install_dt = st.date_input("ইনস্টল তারিখ", datetime.date.today())
                submit_p = st.form_submit_button("পার্ট যোগ করুন")
                if submit_p and p_name:
                    conn.execute(
                        "INSERT INTO parts (machine_id, part_name, install_date) VALUES (?, ?, ?)",
                        [selected_machine_id, p_name, install_dt.isoformat()]
                    )
                    conn.commit()
                    st.success("✅ পার্ট যোগ হয়েছে!", icon="⚙️")
                    st.rerun()
        else:
            st.warning("দয়া করে প্রথমে একটি মেশিন যোগ করুন।")
        conn.close()

    # ------------------- নতুন লগ -------------------
    elif choice == "📝 নতুন লগ এন্ট্রি":
        st.markdown('<div class="app-header">📝 ব্রেকডাউন রিপোর্ট</div>', unsafe_allow_html=True)
        conn = get_db_connection()
        machines = conn.execute("SELECT * FROM machines").fetchall()

        if not machines:
            st.warning("প্রথমে মেশিন যোগ করুন!")
            conn.close()
            return

        machine_options = {m['name']: m['id'] for m in machines}
        selected_machine_id = st.selectbox(
            "মেশিন নির্বাচন", list(machine_options.values()),
            format_func=lambda x: [m['name'] for m in machines if m['id'] == x][0]
        )

        parts = conn.execute("SELECT * FROM parts WHERE machine_id = ?", [selected_machine_id]).fetchall()
        if not parts:
            st.warning("এই মেশিনে কোনো পার্ট নেই। আগে পার্ট যোগ করুন।")
            conn.close()
            return

        part_options = {p['part_name']: p['id'] for p in parts}
        selected_part_id = st.selectbox(
            "কোন পার্ট?", list(part_options.values()),
            format_func=lambda x: [p['part_name'] for p in parts if p['id'] == x][0]
        )

        with st.form("log_form"):
            runtime = st.number_input("বর্তমান রান টাইম (ঘন্টায়)", min_value=0.0, step=0.5)
            failure_type = st.selectbox("ফেইলিউর টাইপ", ["মেকানিক্যাল", "ইলেকট্রিক্যাল", "সফটওয়্যার", "মানবিক ত্রুটি", "অন্যান্য"])
            symptoms = st.text_area("সমস্যার বিবরণ (লক্ষণ) লিখুন", height=100)
            solution = st.text_area("কীভাবে সমাধান করলেন?", height=100)
            downtime = st.number_input("ডাউনটাইম (মিনিট)", min_value=0, step=1)
            submitted = st.form_submit_button("📥 লগ সংরক্ষণ করুন")

            if submitted:
                if symptoms and solution:
                    now = datetime.datetime.now().isoformat()
                    conn.execute('''INSERT INTO maintenance_logs
                                 (part_id, runtime_hours, failure_type, symptoms_text, solution_text, downtime_mins, created_by, created_at)
                                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                                 [selected_part_id, runtime, failure_type, symptoms, solution, downtime, st.session_state.username, now])
                    conn.commit()
                    st.success("✅ লগ সফলভাবে সংরক্ষিত হয়েছে!", icon="🎉")
                    st.balloons()
                    conn.close()
                    st.rerun()
                else:
                    st.error("লক্ষণ এবং সমাধান দুইটি অবশ্যই পূরণ করতে হবে।")
        conn.close()

    # ------------------- ট্রাবলশুটিং -------------------
    elif choice == "🔍 ট্রাবলশুটিং":
        st.markdown('<div class="app-header">🔍 ট্রাবলশুটিং সার্চ</div>', unsafe_allow_html=True)
        st.markdown('<div class="app-subheader">আগের সমাধান ডাটাবেসে খুঁজুন</div>', unsafe_allow_html=True)

        search_query = st.text_input("আপনার সমস্যা টাইপ করুন (যেমন: 'মোটর গরম হচ্ছে')")
        if search_query:
            conn = get_db_connection()
            query = f"%{search_query}%"
            results = conn.execute('''
                SELECT l.*, p.part_name, m.name as machine_name
                FROM maintenance_logs l
                JOIN parts p ON l.part_id = p.id
                JOIN machines m ON p.machine_id = m.id
                WHERE l.symptoms_text LIKE ? OR l.solution_text LIKE ?
                ORDER BY l.created_at DESC
            ''', [query, query]).fetchall()
            conn.close()

            if results:
                st.success(f"🔎 {len(results)} টি অনুরূপ সমাধান পাওয়া গেছে:")
                for row in results:
                    with st.expander(f"🛠️ {row['machine_name']} → {row['part_name']}"):
                        st.write(f"**⚠️ লক্ষণ:** {row['symptoms_text']}")
                        st.write(f"**✅ সমাধান:** {row['solution_text']}")
                        st.write(f"**⏱️ ডাউনটাইম:** {row['downtime_mins']} মিনিট")
                        st.caption(f"📅 {row['created_at']} | 👤 {row['created_by']}")
            else:
                st.warning("❌ মিলে যায়নি। আপনি কি নতুন লগ হিসেবে এটি সংরক্ষণ করতে চান?")

    # ------------------- প্রেডিকশন -------------------
    elif choice == "🔮 প্রেডিকশন":
        st.markdown('<div class="app-header">🔮 প্রেডিকটিভ অ্যানালাইসিস</div>', unsafe_allow_html=True)
        st.markdown('<div class="app-subheader">MTBF (গড় ফেইলিউর সময়) ভিত্তিক প্রেডিকশন</div>', unsafe_allow_html=True)

        conn = get_db_connection()
        parts = conn.execute("SELECT * FROM parts").fetchall()

        if not parts:
            st.warning("কোনো পার্ট নেই।")
            conn.close()
            return

        data_list = []
        for part in parts:
            logs = conn.execute(
                "SELECT * FROM maintenance_logs WHERE part_id = ? ORDER BY created_at ASC",
                [part['id']]
            ).fetchall()

            runtimes = [log['runtime_hours'] for log in logs if log['runtime_hours'] and log['runtime_hours'] > 0]

            if len(runtimes) < 2:
                data_list.append({
                    "পার্ট": part['part_name'],
                    "গড় ব্যবধান (ঘন্টা)": "N/A",
                    "বর্তমান রান (ঘন্টা)": runtimes[-1] if runtimes else "N/A",
                    "পরবর্তী ফেইলিউর সম্ভাবনা (আনুমানিক ঘন্টা)": "N/A",
                    "স্ট্যাটাস": "⚠️ ডেটা অপ্রতুল",
                    "সুপারিশ": "কমপক্ষে ২টি লগ দরকার",
                    "_badge_class": "badge-yellow"
                })
                continue

            gaps = [runtimes[i] - runtimes[i - 1] for i in range(1, len(runtimes)) if runtimes[i] > runtimes[i - 1]]

            if not gaps:
                data_list.append({
                    "পার্ট": part['part_name'],
                    "গড় ব্যবধান (ঘন্টা)": "N/A",
                    "বর্তমান রান (ঘন্টা)": runtimes[-1],
                    "পরবর্তী ফেইলিউর সম্ভাবনা (আনুমানিক ঘন্টা)": "N/A",
                    "স্ট্যাটাস": "⚠️ ডেটা অস্পষ্ট",
                    "সুপারিশ": "রানটাইম সঠিকভাবে এন্ট্রি করুন",
                    "_badge_class": "badge-yellow"
                })
                continue

            avg_gap = sum(gaps) / len(gaps)
            current_run = runtimes[-1]
            predicted_next_failure = current_run + avg_gap
            usage_ratio = current_run / avg_gap if avg_gap > 0 else 0

            if usage_ratio >= 0.9:
                status = "🔴 জরুরি"
                badge_class = "badge-red"
                recommendation = "শীঘ্রই মেইনটেন্যান্স করুন"
            elif usage_ratio >= 0.7:
                status = "🟡 সতর্কতা"
                badge_class = "badge-yellow"
                recommendation = "মেইনটেন্যান্স শিডিউল করুন"
            else:
                status = "🟢 স্বাভাবিক"
                badge_class = "badge-green"
                recommendation = "নিয়মিত মনিটর করুন"

            data_list.append({
                "পার্ট": part['part_name'],
                "গড় ব্যবধান (ঘন্টা)": round(avg_gap, 1),
                "বর্তমান রান (ঘন্টা)": current_run,
                "পরবর্তী ফেইলিউর সম্ভাবনা (আনুমানিক ঘন্টা)": round(predicted_next_failure, 1),
                "স্ট্যাটাস": status,
                "সুপারিশ": recommendation,
                "_badge_class": badge_class
            })

        conn.close()

        df = pd.DataFrame(data_list)
        display_df = df.drop(columns=["_badge_class"]) if "_badge_class" in df.columns else df
        st.dataframe(display_df, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.subheader("🎯 বিস্তারিত কার্ড ভিউ")

        for item in data_list:
            badge_class = item.get("_badge_class", "badge-yellow")
            card_html = f"""
            <div class="custom-card">
                <strong>🔩 {item['পার্ট']}</strong>
                <span class="{badge_class}" style="float:right;">{item['স্ট্যাটাস']}</span>
                <br><br>
                📊 গড় ব্যবধান: <strong>{item.get('গড় ব্যবধান (ঘন্টা)', 'N/A')}</strong> ঘন্টা <br>
                ⏱️ বর্তমান রান: <strong>{item.get('বর্তমান রান (ঘন্টা)', 'N/A')}</strong> ঘন্টা <br>
                🔮 আনুমানিক পরবর্তী ফেইলিউর: <strong>{item.get('পরবর্তী ফেইলিউর সম্ভাবনা (আনুমানিক ঘন্টা)', 'N/A')}</strong> ঘন্টা <br>
                💡 সুপারিশ: {item['সুপারিশ']}
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)


# ------------------- এন্ট্রি পয়েন্ট -------------------
def main():
    init_session_state()
    init_db()

    if not st.session_state.logged_in:
        login_page()
    else:
        main_app()


if __name__ == "__main__":
    main()

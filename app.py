import json
import random
import string
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="VaultBank",
    page_icon="🏦",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
}

/* Background */
.stApp {
    background: #0a0a0f;
    color: #e8e4dc;
}

/* Hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }

/* Hero banner */
.hero {
    background: linear-gradient(135deg, #0d1117 0%, #161b27 50%, #0d1117 100%);
    border: 1px solid #1e2a3a;
    border-radius: 16px;
    padding: 2.5rem 2rem 2rem 2rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 180px; height: 180px;
    background: radial-gradient(circle, rgba(99,179,237,0.12) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-size: 2.4rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: #f0ece4;
    margin: 0 0 0.3rem 0;
    line-height: 1.1;
}
.hero-accent { color: #63b3ed; }
.hero-sub {
    font-family: 'DM Mono', monospace;
    font-size: 0.78rem;
    color: #4a5568;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}

/* Card */
.card {
    background: #111118;
    border: 1px solid #1a1f2e;
    border-radius: 12px;
    padding: 1.8rem;
    margin-bottom: 1.2rem;
}

/* Section label */
.section-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #63b3ed;
    margin-bottom: 1rem;
}

/* Balance chip */
.balance-chip {
    display: inline-block;
    background: linear-gradient(90deg, #1a2535, #162032);
    border: 1px solid #2d4a6e;
    border-radius: 8px;
    padding: 0.5rem 1.2rem;
    font-family: 'DM Mono', monospace;
    font-size: 1.5rem;
    font-weight: 500;
    color: #63b3ed;
    letter-spacing: 0.04em;
}

/* Account number chip */
.acc-chip {
    display: inline-block;
    background: #0f1520;
    border: 1px dashed #2d3748;
    border-radius: 6px;
    padding: 0.35rem 0.9rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.82rem;
    color: #718096;
    letter-spacing: 0.08em;
    margin-bottom: 0.5rem;
}

/* Status messages */
.msg-success {
    background: #0f2015;
    border-left: 3px solid #48bb78;
    border-radius: 6px;
    padding: 0.8rem 1rem;
    color: #68d391;
    font-size: 0.9rem;
    margin: 0.8rem 0;
}
.msg-error {
    background: #1a0f0f;
    border-left: 3px solid #fc8181;
    border-radius: 6px;
    padding: 0.8rem 1rem;
    color: #feb2b2;
    font-size: 0.9rem;
    margin: 0.8rem 0;
}
.msg-info {
    background: #0f1a2a;
    border-left: 3px solid #63b3ed;
    border-radius: 6px;
    padding: 0.8rem 1rem;
    color: #90cdf4;
    font-size: 0.9rem;
    margin: 0.8rem 0;
}

/* Streamlit widget overrides */
div[data-testid="stSelectbox"] label,
div[data-testid="stTextInput"] label,
div[data-testid="stNumberInput"] label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.1em !important;
    color: #718096 !important;
    text-transform: uppercase !important;
}

div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input {
    background: #0d1117 !important;
    border: 1px solid #1e2a3a !important;
    border-radius: 8px !important;
    color: #e8e4dc !important;
    font-family: 'DM Mono', monospace !important;
}

div[data-testid="stTextInput"] input:focus,
div[data-testid="stNumberInput"] input:focus {
    border-color: #63b3ed !important;
    box-shadow: 0 0 0 2px rgba(99,179,237,0.15) !important;
}

div[data-testid="stSelectbox"] > div > div {
    background: #0d1117 !important;
    border: 1px solid #1e2a3a !important;
    border-radius: 8px !important;
    color: #e8e4dc !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #2b4d7a, #1a3355) !important;
    color: #e8f4fd !important;
    border: 1px solid #3a6494 !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
    padding: 0.55rem 1.4rem !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #3a6494, #2b4d7a) !important;
    border-color: #63b3ed !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(99,179,237,0.2) !important;
}

/* Divider */
hr { border-color: #1a1f2e !important; }

/* Detail row */
.detail-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.65rem 0;
    border-bottom: 1px solid #1a1f2e;
    font-size: 0.9rem;
}
.detail-key {
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    color: #4a5568;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.detail-val { color: #cbd5e0; font-weight: 500; }
</style>
""", unsafe_allow_html=True)

DATABASE = "database.json"

def load_data():
    if Path(DATABASE).exists():
        with open(DATABASE) as f:
            return json.loads(f.read())
    return []

def save_data(data):
    with open(DATABASE, 'w') as f:
        f.write(json.dumps(data))

def generate_account():
    alpha = random.choices(string.ascii_letters, k=8)
    num = random.choices(string.digits, k=4)
    acc = alpha + num
    random.shuffle(acc)
    return "".join(acc)

def find_user(data, accno, pin):
    results = [u for u in data if u['AccountNo.'] == accno and u['pin'] == pin]
    return results[0] if results else None

st.markdown("""
<div class="hero">
    <p class="hero-sub">● Secure Digital Banking</p>
    <h1 class="hero-title">Vault<span class="hero-accent">Bank</span></h1>
    <p style="color:#4a5568;font-size:0.88rem;margin:0.5rem 0 0 0;font-family:'DM Mono',monospace;">
        Manage accounts · Deposits · Withdrawals
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown('<p class="section-label">Select Operation</p>', unsafe_allow_html=True)
operation = st.selectbox(
    "operation",
    ["Create Account", "Deposit Money", "Withdraw Money",
     "View Account Details", "Update Details", "Delete Account"],
    label_visibility="collapsed"
)

st.markdown("---")

data = load_data()

if operation == "Create Account":
    st.markdown('<p class="section-label">New Account</p>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
    with col2:
        age = st.number_input("Age", min_value=0, max_value=120, step=1)
        pin = st.text_input("4-Digit PIN", type="password", max_chars=4)

    if st.button("Create Account →"):
        if not name or not email or not pin:
            st.markdown('<div class="msg-error">⚠ Please fill in all fields.</div>', unsafe_allow_html=True)
        elif age < 12:
            st.markdown('<div class="msg-error">⚠ Minimum age to open an account is 12 years.</div>', unsafe_allow_html=True)
        elif not pin.isdigit() or len(pin) != 4:
            st.markdown('<div class="msg-error">⚠ PIN must be exactly 4 digits.</div>', unsafe_allow_html=True)
        else:
            acc_no = generate_account()
            new_user = {
                "name": name, "age": int(age), "email": email,
                "AccountNo.": acc_no, "pin": int(pin), "balance": 0
            }
            data.append(new_user)
            save_data(data)
            st.markdown(f"""
            <div class="msg-success">✓ Account created successfully!</div>
            <div class="card" style="margin-top:1rem;">
                <p class="section-label">Your Account Details</p>
                <div class="detail-row"><span class="detail-key">Name</span><span class="detail-val">{name}</span></div>
                <div class="detail-row"><span class="detail-key">Email</span><span class="detail-val">{email}</span></div>
                <div class="detail-row"><span class="detail-key">Age</span><span class="detail-val">{age}</span></div>
                <div class="detail-row" style="border:none;">
                    <span class="detail-key">Account No.</span>
                    <span class="acc-chip">{acc_no}</span>
                </div>
            </div>
            <div class="msg-info">🔐 Save your account number and PIN — you'll need them for all transactions.</div>
            """, unsafe_allow_html=True)

elif operation == "Deposit Money":
    st.markdown('<p class="section-label">Deposit</p>', unsafe_allow_html=True)
    accno = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password", max_chars=4)
    amount = st.number_input("Amount to Deposit (₹)", min_value=1, step=100)

    if st.button("Deposit →"):
        user = find_user(data, accno, int(pin) if pin.isdigit() else -1)
        if not user:
            st.markdown('<div class="msg-error">⚠ Invalid account number or PIN.</div>', unsafe_allow_html=True)
        else:
            user['balance'] += int(amount)
            save_data(data)
            st.markdown(f"""
            <div class="msg-success">✓ ₹{amount:,} deposited successfully.</div>
            <div class="card" style="margin-top:1rem;">
                <p class="section-label">Updated Balance</p>
                <span class="balance-chip">₹ {user['balance']:,}</span>
            </div>
            """, unsafe_allow_html=True)


elif operation == "Withdraw Money":
    st.markdown('<p class="section-label">Withdrawal</p>', unsafe_allow_html=True)
    accno = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password", max_chars=4)
    amount = st.number_input("Amount to Withdraw (₹)", min_value=1, step=100)

    if st.button("Withdraw →"):
        user = find_user(data, accno, int(pin) if pin.isdigit() else -1)
        if not user:
            st.markdown('<div class="msg-error">⚠ Invalid account number or PIN.</div>', unsafe_allow_html=True)
        elif int(amount) > user['balance']:
            st.markdown(f'<div class="msg-error">⚠ Insufficient balance. Available: ₹{user["balance"]:,}</div>', unsafe_allow_html=True)
        else:
            user['balance'] -= int(amount)
            save_data(data)
            st.markdown(f"""
            <div class="msg-success">✓ ₹{amount:,} withdrawn successfully.</div>
            <div class="card" style="margin-top:1rem;">
                <p class="section-label">Remaining Balance</p>
                <span class="balance-chip">₹ {user['balance']:,}</span>
            </div>
            """, unsafe_allow_html=True)
            
elif operation == "View Account Details":
    st.markdown('<p class="section-label">Account Details</p>', unsafe_allow_html=True)
    accno = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password", max_chars=4)

    if st.button("View Details →"):
        user = find_user(data, accno, int(pin) if pin.isdigit() else -1)
        if not user:
            st.markdown('<div class="msg-error">⚠ Invalid account number or PIN.</div>', unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="card">
                <p class="section-label">Account Summary</p>
                <div class="detail-row"><span class="detail-key">Name</span><span class="detail-val">{user['name']}</span></div>
                <div class="detail-row"><span class="detail-key">Age</span><span class="detail-val">{user['age']}</span></div>
                <div class="detail-row"><span class="detail-key">Email</span><span class="detail-val">{user['email']}</span></div>
                <div class="detail-row"><span class="detail-key">Account No.</span><span class="acc-chip">{user['AccountNo.']}</span></div>
                <div class="detail-row" style="border:none;"><span class="detail-key">Balance</span>
                    <span class="balance-chip">₹ {user['balance']:,}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

elif operation == "Update Details":
    st.markdown('<p class="section-label">Update Account</p>', unsafe_allow_html=True)
    accno = st.text_input("Account Number")
    pin = st.text_input("Current PIN", type="password", max_chars=4)

    if accno and pin:
        user = find_user(data, accno, int(pin) if pin.isdigit() else -1)
        if user:
            st.markdown('<div class="msg-info">ℹ Leave fields blank to keep current values.</div>', unsafe_allow_html=True)
            new_name = st.text_input("New Name", placeholder=user['name'])
            new_email = st.text_input("New Email", placeholder=user['email'])
            new_pin = st.text_input("New PIN", type="password", max_chars=4, placeholder="Leave blank to keep")

            if st.button("Update →"):
                if new_name: user['name'] = new_name
                if new_email: user['email'] = new_email
                if new_pin:
                    if new_pin.isdigit() and len(new_pin) == 4:
                        user['pin'] = int(new_pin)
                    else:
                        st.markdown('<div class="msg-error">⚠ New PIN must be 4 digits.</div>', unsafe_allow_html=True)
                        st.stop()
                save_data(data)
                st.markdown('<div class="msg-success">✓ Account updated successfully.</div>', unsafe_allow_html=True)
        else:
            if len(pin) == 4:
                st.markdown('<div class="msg-error">⚠ Invalid account number or PIN.</div>', unsafe_allow_html=True)


elif operation == "Delete Account":
    st.markdown('<p class="section-label">Delete Account</p>', unsafe_allow_html=True)
    st.markdown('<div class="msg-error">⚠ This action is permanent and cannot be undone.</div>', unsafe_allow_html=True)
    accno = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password", max_chars=4)
    confirm = st.checkbox("I understand this will permanently delete my account")

    if st.button("Delete Account →"):
        user = find_user(data, accno, int(pin) if pin.isdigit() else -1)
        if not user:
            st.markdown('<div class="msg-error">⚠ Invalid account number or PIN.</div>', unsafe_allow_html=True)
        elif not confirm:
            st.markdown('<div class="msg-error">⚠ Please check the confirmation box to proceed.</div>', unsafe_allow_html=True)
        else:
            data.remove(user)
            save_data(data)
            st.markdown('<div class="msg-success">✓ Account deleted successfully.</div>', unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center;margin-top:3rem;padding-top:1.5rem;border-top:1px solid #1a1f2e;">
    <p style="font-family:'DM Mono',monospace;font-size:0.7rem;color:#2d3748;letter-spacing:0.1em;">
        VAULTBANK · SECURE · PRIVATE · RELIABLE
    </p>
</div>
""", unsafe_allow_html=True)

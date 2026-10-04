import streamlit as st

# ১. পেজ কনফিগারেশন ও ব্রাউজার ট্যাবে নাম এবং ইউনিক স্পার্কল আইকন সেটআপ
st.set_page_config(
    page_title="Meizu",
    page_icon="🌟",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ২. প্রিমিয়াম ও ফিউচারস্টিক ডিজাইন দেওয়ার জন্য কাস্টম CSS স্টাইল
st.markdown(
    """
    <style>
    /* ব্যাকগ্রাউন্ড ও টেক্সট স্টাইল */
    .stApp {
        background-color: #0d1117;
        color: #e6edf3;
    }
    /* হেডিং ডিজাইন */
    h1 {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #58a6ff;
        text-align: center;
        letter-spacing: 1px;
    }
    /* পাসওয়ার্ড ইনপুট বক্স ডিজাইন */
    .stTextInput input {
        background-color: #161b22;
        color: #ffffff;
        border: 1px solid #30363d;
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ৩. পাসওয়ার্ড প্রটেকশন লজিক (পাসওয়ার্ড: sp281018)
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        "<h2 style='text-align: center; color: #58a6ff;'>🔒 Meizu Security Portal</h2>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align: center; color: #8b949e;'>Enter your security key to access the assistant.</p>",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        password = st.text_input(
            "Password", type="password", label_visibility="collapsed"
        )
        if st.button("Unlock Meizu", use_container_width=True):
            if password == "sp281018":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("ভুল পাসওয়ার্ড! আবার চেষ্টা করুন।")
    st.stop()

# ৪. মূল অ্যাপ ইন্টারফেস (পাসওয়ার্ড দেওয়ার পর যা দেখা যাবে)
st.markdown("<h1>🌟 Meizu</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; color: #8b949e;'>ফিউচারস্টিক পার্সোনাল এআই অ্যাসিস্ট্যান্ট</p>",
    unsafe_allow_html=True,
)
st.divider()

# চ্যাট ইন্টারফেস বা অ্যাসিস্ট্যান্টের মূল অংশ
st.chat_message("assistant", avatar="🌟").write(
    "হ্যালো বস! আমি **Meizu**। আপনার জব, ফুড ইন্ডাস্ট্রি প্রফেশনাল গাইডলাইন, মাইক্রোসফট এক্সেল, এবং অটোমেশন কাজের জন্য প্রস্তুত। বলুন আজ কী করতে হবে?"
)

# ইউজারের চ্যাট ইনপুট
user_prompt = st.chat_input("আপনার কমান্ড বা প্রশ্ন এখানে লিখুন...")
if user_prompt:
    st.chat_message("user").write(user_prompt)
    st.chat_message("assistant", avatar="🌟").write(
        f"আপনার কমান্ডটি গ্রহণ করা হয়েছে: '{user_prompt}'। এটি প্রসেস করা হচ্ছে..."
    )

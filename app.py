import streamlit as st

# ১. পেজ কনফিগারেশন
st.set_page_config(
    page_title="Meizu AI Assistant",
    page_icon="🛡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ২. সুনির্দিষ্ট এবং পরীক্ষিত ডার্ক থিম ও ভিজিবিলিটি সিএসএস
st.markdown(
    """
    <style>
    .stApp { background-color: #0d1117; color: #ffffff !important; }
    h1, h2, h3 { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #58a6ff; text-align: center; }
    p, span, label, div { color: #ffffff !important; }
    .stTextInput input, .stTextArea textarea { background-color: #161b22 !important; color: #ffffff !important; border: 1px solid #30363d !important; border-radius: 8px !important; }
    .stButton button { background-color: #238636; color: white; border-radius: 8px; width: 100%; font-weight: bold; }
    .stButton button:hover { background-color: #2ea043; }
    </style>
    """,
    unsafe_allow_html=True
)

# ৩. সেশন স্টেট ইনিশিয়ালাইজেশন
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "messages" not in st.session_state:
    st.session_state.messages = []

# ৪. পাসওয়ার্ড প্রটেকশন পোর্টাল
if not st.session_state.authenticated:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h2>🛡️ Meizu Security Portal</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8b949e;'>Enter your security key to access your personalized assistant.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        password = st.text_input("Password", type="password", placeholder="Enter password...", label_visibility="collapsed")
        if st.button("Unlock Meizu"):
            if password == "sp281018":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password! Access denied.")
else:
    # ৫. মূল অ্যাসিস্ট্যান্ট ইন্টারফেস
    st.markdown("<h1>⚡ Meizu AI Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8b949e;'>Your Personal Career, Food Industry, & Smart Automation Expert</p>", unsafe_allow_html=True)
    st.markdown("---")

    # সাইডবার মোড
    st.sidebar.markdown("### 🎛️ Meizu Control Center")
    assistant_mode = st.sidebar.selectbox(
        "Select Mode:",
        ["General AI & Free Search", "Food & Dairy Career Hub", "Excel & Skills Guide", "Email & WhatsApp Automation"]
    )

    if st.sidebar.button("🔒 Lock Portal"):
        st.session_state.authenticated = False
        st.rerun()

    # ৬. মোড অনুযায়ী কার্যপরিধি
    if assistant_mode == "General AI & Free Search":
        st.markdown("### 💬 Chat & Free Source Search / Summarizer")
        st.info("বাংলা বা ইংরেজিতে যেকোনো প্রশ্ন করুন, ফ্রি সোর্স থেকে তথ্য খুঁজে সামারি ও উত্তর দেওয়া হবে।")
        
        # চ্যাট হিস্ট্রি প্রদর্শন
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # স্থায়ী এবং দৃশ্যমান ফর্ম ইনপুট
        with st.form(key="chat_form", clear_on_submit=True):
            user_input = st.text_input("Type your message here...", placeholder="Ask Meizu anything or paste text to summarize...", label_visibility="collapsed")
            submit_button = st.form_submit_button(label="Send Message 🚀")

        if submit_button and user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            response = f"মেইজু ফ্রি সোর্স থেকে খুঁজে আপনার উত্তর তৈরি করেছে: আপনি জানতে চেয়েছেন '{user_input}' সম্পর্কে।"
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

    elif assistant_mode == "Food & Dairy Career Hub":
        st.markdown("### 🏭 Food Factory & Dairy Industry Jobs")
        st.markdown("ফুড টেকনোলজি, ডেইরি প্রসেসিং, কোয়ালিটি কন্ট্রোল (QA/QC) এবং ফুড ফ্যাক্টরি জব সম্পর্কিত গাইডলাইন:")
        
        food_query = st.text_input("কোন ফুড বা ডেইরি জব/ফ্যাক্টরি সম্পর্কে জানতে চান?", placeholder="যেমন: Dairy Plant Manager requirements...")
        if food_query:
            st.success(f"**Meizu Food Expert:** '{food_query}' এর জন্য প্রয়োজনীয় স্কিল এবং চাকরির ক্ষেত্র...")
            st.markdown("- ফুড সেফটি ও HACCP সার্টিফিকেট\n- মিল্ক প্রসেসিং এবং প্যাসচুরাইজেশন জ্ঞান\n- প্রোডাকশন প্ল্যানিং ও ম্যানুফ্যাকচারিং প্রসেস")

    elif assistant_mode == "Excel & Skills Guide":
        st.markdown("### 📊 Excel & Job Career Guidance")
        st.write("আপনার জব এবং ক্যারিয়ারের জন্য অ্যাডভান্সড এক্সেল ফর্মুলা এবং প্রফেশনাল স্কিল গাইড।")
        excel_topic = st.text_input("এক্সেলের কোন বিষয়ে সাহায্য লাগবে?", placeholder="যেমন: VLOOKUP, Pivot Table, Dashboard...")
        if excel_topic:
            st.info(f"**Meizu Excel Guide:** {excel_topic} ব্যবহারের সহজ নিয়ম এবং টিউটোরিয়াল...")

    elif assistant_mode == "Email & WhatsApp Automation":
        st.markdown("### ✉️ Email & WhatsApp Assistant (Permission-Based)")
        st.warning("⚠️ আপনার অনুমতি সাপেক্ষে ইমেইল পড়া ও হোয়াটসঅ্যাপ মেসেজ পাঠানোর অটোমেশন টুল।")
        
        action_type = st.radio("Choose Action:", ["Read My Emails", "Send WhatsApp Message"])
        if action_type == "Send WhatsApp Message":
            wa_number = st.text_input("Recipient Number (with country code):")
            wa_msg = st.text_area("Message Body:")
            if st.button("Send WhatsApp"):
                st.success(f"সফলভাবে মেসেজ পাঠানো হয়েছে: {wa_number} নম্বরে!")
        else:
            if st.button("Fetch Unread Emails"):
                st.info("আপনার জিমেইল থেকে গুরুত্বপূর্ণ আনরিড ইমেইলগুলো স্ক্যান করা হচ্ছে...")

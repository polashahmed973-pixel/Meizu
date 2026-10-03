import google.generativeai as genai
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="My Private AI Assistant", page_icon="🤖", layout="centered"
)

# --- STRICT SECURITY LOGIN SYSTEM ---
MASTER_PASSWORD = "sp281018"

if "authenticated" not in st.session_state:
  st.session_state.authenticated = False

if not st.session_state.authenticated:
  st.title("🔒 Restricted Access (সুপার সিক্রেট)")
  st.write("এই অ্যাপটি শুধু আপনার জন্য। আপনার পিন কোডটি দিন:")
  entered_pass = st.text_input("Enter PIN:", type="password")

  if st.button("Unlock / আনলক করুন"):
    if entered_pass == MASTER_PASSWORD:
      st.session_state.authenticated = True
      st.rerun()
    else:
      st.error("ভুল পিন! প্রবেশাধিকার সংরক্ষিত।")
  st.stop()

# --- MAIN APP (পিন দেওয়ার পর এটি ওপেন হবে) ---
st.title("🤖 My Private AI Assistant (v3.5)")
st.write("স্বাগতম বস! আপনার সিস্টেম সম্পূর্ণ সুরক্ষিত ও রেডি।")

# Secure API Key configuration
API_KEY = st.text_input("আপনার ফ্রি Gemini API Key দিন:", type="password")

if API_KEY:
  genai.configure(api_key=API_KEY)
  model = genai.GenerativeModel("gemini-2.5-flash")

  if "tasks" not in st.session_state:
    st.session_state.tasks = []
  if "notes" not in st.session_state:
    st.session_state.notes = "আপনার দরকারি নোটস বা রিমাইন্ডার এখানে লিখুন..."

  # Sidebar Navigation
  st.sidebar.title("মেইন মেনু (Features)")
  app_mode = st.sidebar.selectbox(
      "ফিচার বেছে নিন:",
      [
          "💬 চ্যাট ও আলোচনা (Chat)",
          "🎙️ ভয়েস কমান্ড (Voice Command)",
          "📄 পিডিএফ ও ডকুমেন্ট সামারি (Summarizer)",
          "🏭 ফুড ইন্ডাস্ট্রি এক্সপার্ট (Food Expert)",
          "📋 টাস্ক ও রিমাইন্ডার (Tasks & Notes)",
      ],
  )

  # --- FEATURE 1: CHAT ---
  if app_mode == "💬 চ্যাট ও আলোচনা (Chat)":
    st.header("💬 এআই অ্যাসিস্ট্যান্টের সাথে কথা বলুন")
    user_query = st.text_area(
        "আপনার প্রশ্ন বা সমস্যা এখানে লিখুন (বাংলা বা ইংরেজিতে):"
    )
    if st.button("এআই-এর কাছে পাঠান"):
      if user_query:
        with st.spinner("ভাবছি..."):
          response = model.generate_content(user_query)
          st.success("উত্তর:")
          st.write(response.text)
      else:
        st.warning("আগে কিছু লিখুন বস।")

  # --- FEATURE 2: VOICE COMMAND ---
  elif app_mode == "🎙️ ভয়েস কমান্ড (Voice Command)":
    st.header("🎙️ ভয়েস কমান্ড মোড")
    st.write(
        "মাইক্রোফোনে ক্লিক করে মুখে কথা রেকর্ড করুন (বাংলা বা ইংরেজিতে)।"
    )
    audio_file = st.audio_input("কথা বলতে এখানে ক্লিক করুন:")
    if audio_file is not None:
      st.audio(audio_file)
      if st.button("ভয়েস প্রসেস করুন"):
        with st.spinner("আপনার ভয়েস শোনা হচ্ছে..."):
          audio_bytes = audio_file.getvalue()
          prompt = "Listen to this audio (English or Bengali). Transcribe and provide a helpful response."
          response = model.generate_content([
              prompt,
              {"mime_type": "audio/wav", "data": audio_bytes},
          ])
          st.success("এআই-এর উত্তর:")
          st.write(response.text)

  # --- FEATURE 3: DOCUMENT SUMMARIZER ---
  elif app_mode == "📄 পিডিএফ ও ডকুমেন্ট সামারি (Summarizer)":
    st.header("📄 ডকুমেন্ট বা ইমেইল সামারাইজার")
    doc_text = st.text_area("বড় ডকুমেন্ট বা ইমেইলের লেখা এখানে পেস্ট করুন:")
    summary_lang = st.selectbox(
        "কোন ভাষায় সামারি চান?", ["Bengali (বাংলা)", "English"]
    )
    if st.button("সংক্ষিপ্ত করুন (Summarize)"):
      if doc_text:
        with st.spinner("পড়ে সামারি তৈরি করছি..."):
          prompt = f"Summarize this document clearly in {summary_lang}, highlighting key action items:"
          response = model.generate_content([prompt, doc_text])
          st.success("সামারি রেজাল্ট:")
          st.write(response.text)

  # --- FEATURE 4: FOOD INDUSTRY EXPERT ---
  elif app_mode == "🏭 ফুড ইন্ডাস্ট্রি এক্সপার্ট (Food Expert)":
    st.header("🏭 ফুড টেকনোলজি ও অপারেশনস অ্যাসিস্ট্যান্ট")
    industry_query = st.text_input(
        "আপনার টেকনিক্যাল প্রশ্ন লিখুন (যেমন: SIP, Brix, Kaizen বা প্রোডাকশন"
        " প্রসেস):"
    )
    if st.button("টেকনিক্যাল সলিউশন নিন"):
      if industry_query:
        with st.spinner("টেকনিক্যাল ডাটা অ্যানালাইসিস করছি..."):
          system_prompt = "You are an expert food process engineer and operations consultant. Give professional technical advice."
          response = model.generate_content([system_prompt, industry_query])
          st.success("এক্সপার্ট ওপিনিয়ন:")
          st.write(response.text)

  # --- FEATURE 5: TASKS & NOTES ---
  elif app_mode == "📋 টাস্ক ও রিমাইন্ডার (Tasks & Notes)":
    st.header("📋 ডেইলি টাস্ক ও পারসোনাল রিমাইন্ডার")
    new_task = st.text_input("নতুন কোনো কাজ বা রিমাইন্ডার যোগ করুন:")
    if st.button("টাস্ক যোগ করুন") and new_task:
      st.session_state.tasks.append({"task": new_task, "done": False})
      st.rerun()

    for i, t in enumerate(st.session_state.tasks):
      col1, col2 = st.columns([0.8, 0.2])
      with col1:
        st.session_state.tasks[i]["done"] = st.checkbox(
            t["task"], value=t["done"], key=f"task_{i}"
        )
      with col2:
        if st.button("ডিলিট", key=f"del_{i}"):
          st.session_state.tasks.pop(i)
          st.rerun()

    st.markdown("---")
    st.session_state.notes = st.text_area(
        "র‌্যান্ডম নোটস বা ইমেইলের ড্রাফট এখানে লিখে রাখুন:",
        value=st.session_state.notes,
    )

else:
  st.info("👈 আপনার ফ্রী Gemini API Key দিয়ে অ্যাপটি আনলক করুন।")

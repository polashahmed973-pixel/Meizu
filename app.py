import streamlit as st
from google import genai

# পেজ কনফিগারেশন
st.set_page_config(
    page_title="Meizu AI Assistant",
    page_icon="🤖",
    layout="centered"
)

# ১. সিকিউরিটি পাসওয়ার্ড চেক (আপনার দেওয়া পাসওয়ার্ড: sp281018)
def check_password():
    def password_entered():
        # স্ট্রিমলিট সিক্রেটস থেকে পাসওয়ার্ড চেক করবে, না থাকলে আপনার দেওয়া পাসওয়ার্ড ডিফল্ট ধরবে
        correct_password = st.secrets.get("APP_PASSWORD", "sp281018")
        if st.session_state["password"] == correct_password:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.markdown("### 🔐 Meizu সিকিউরিটি লক")
        st.text_input("আপনার গোপন পাসওয়ার্ড দিন:", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.markdown("### 🔐 Meizu সিকিউরিটি লক")
        st.text_input("আপনার গোপন পাসওয়ার্ড দিন:", type="password", on_change=password_entered, key="password")
        st.error("😕 পাসওয়ার্ড ভুল হয়েছে! সঠিক পাসওয়ার্ড দিন (sp281018)")
        return False
    else:
        return True

# পাসওয়ার্ড সঠিক হলে মূল অ্যাপ রান করবে
if check_password():
    st.title("🤖 Meizu AI Assistant")
    st.markdown("##### আপনার পার্সোনাল জব, ফুড ইন্ডাস্ট্রি, স্কিল ডেভেলপমেন্ট ও অটোমেশন অ্যাসিস্ট্যান্ট")

    if "GEMINI_API_KEY" in st.secrets:
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
        
        # চ্যাট হিস্ট্রি ধরে রাখার জন্য
        if "messages" not in st.session_state:
            st.session_state.messages = []
            # সিস্টেম প্রম্পট বা নির্দেশিকা সেট করা
            st.session_state.messages.append({
                "role": "assistant", 
                "content": "হ্যালো বস! আমি Meizu। আপনার জব, ফুড ইন্ডাস্ট্রি প্রফেশনাল গাইডলাইন, মাইক্রোসফট এক্সেল এবং স্কিল ডেভেলপমেন্টে সাহায্য করার জন্য আমি পুরোপুরি প্রস্তুত। এছাড়া WhatsApp-এ মেসেজ পাঠানো/পড়া, কল করা বা ক্যালেন্ডার রিমাইন্ডার সেট করার মতো যেকোনো পার্সোনাল কাজের ক্ষেত্রে আমি সবসময় আপনার পারমিশন নিয়ে কাজ করব। বলুন আজ কী করতে হবে?"
            })

        # আগের চ্যাটগুলো স্ক্রিনে দেখানোর জন্য
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # নিচে ফিক্সড চ্যাট ইনপুট বক্স
        if prompt := st.chat_input("আপনার কমান্ড বা প্রশ্ন এখানে লিখুন..."):
            # ইউজারের মেসেজ যোগ করা
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # এআই-এর জন্য প্রফেশনাল কনটেক্সট বা সিস্টেম ইন্সট্রাকশন
            system_instruction = (
                "You are 'Meizu', a highly secure, personalized AI assistant built exclusively for your owner. "
                "You specialize in your owner's job, food industry expertise, Microsoft Excel learning, and skill development. "
                "CRITICAL RULES: "
                "1. For any personal or sensitive actions like reading/sending WhatsApp messages, checking emails, setting calendar reminders, or making calls, "
                "you MUST ask for explicit permission first before proceeding. "
                "2. When the user asks to send or read WhatsApp messages, manage calls, or handle calendar tasks, acknowledge the request, verify the details, ask for confirmation/permission, and guide them accordingly."
            )

            # জেমিনির কাছ থেকে উত্তর আনা
            try:
                # ফুল চ্যাট কনটেক্সটসহ রিকোয়েস্ট পাঠানো
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=f"{system_instruction}\n\nUser Query: {prompt}",
                )
                ai_response = response.text
                
                # এআই-এর উত্তর যোগ করা
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                with st.chat_message("assistant"):
                    st.markdown(ai_response)
                    
            except Exception as e:
                error_msg = f"ত্রুটি দেখা দিয়েছে: {e}"
                st.error(error_msg)
    else:
        st.warning("দয়া করে স্ট্রিমলিট সিক্রেটসে 'GEMINI_API_KEY' যুক্ত করুন।")

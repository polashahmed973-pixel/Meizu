import streamlit as st
import google.generativeai as genai

# Page Configuration
st.set_page_config(
    page_title="Meizu AI Assistant",
    page_icon="🤖",
    layout="centered"
)

# App Title & Interface
st.title("🤖 Meizu AI Assistant")
st.write("আপনার পার্সোনাল এআই অ্যাসিস্ট্যান্টে স্বাগতম!")

# API Key Configuration
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    # Simple chat input
    user_prompt = st.text_input("আপনার প্রশ্ন এখানে লিখুন...")
    if user_prompt:
        try:
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(user_prompt)
            st.write("### উত্তর:")
            st.write(response.text)
        except Exception as e:
            st.error(e)
else:
    st.warning("অনুগ্রহ করে Streamlit Secrets-এ আপনার GEMINI_API_KEY কনফিগার করুন।")

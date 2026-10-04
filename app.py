import streamlit as st
from google import genai

st.title("🤖 Meizu AI Assistant")
st.write("আপনার পার্সোনাল এআই অ্যাসিস্ট্যান্টে স্বাগতম!")

if "GEMINI_API_KEY" in st.secrets:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
    
    user_prompt = st.text_input("আপনার প্রশ্ন এখানে লিখুন...")
    if user_prompt:
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=user_prompt,
            )
            st.write("### উত্তর:")
            st.write(response.text)
        except Exception as e:
            st.error(f"ত্রুটি দেখা দিয়েছে: {e}")
else:
    st.warning("দয়া করে স্ট্রিমলিট সিক্রেটসে 'GEMINI_API_KEY' যুক্ত করুন।")

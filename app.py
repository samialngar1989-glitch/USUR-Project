import streamlit as st
import whisper
from deep_translator import GoogleTranslator
import os

st.set_page_config(page_title="نظام USUR للترجمة", page_icon="💠")

st.title("💠 نظام USUR: تحويل وترجمة الوسائط")

@st.cache_resource
def load_model():
    return whisper.load_model("base")

model = load_model()

uploaded_file = st.file_uploader("ارفع ملف صوت أو فيديو", type=["mp3", "wav", "m4a", "mp4", "amr", "opus"])

if uploaded_file is not None:
    with open("temp_file", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success("✅ تم رفع الملف")

    if st.button("🎙️ استخراج النص والترجمة"):
        with st.spinner("جاري المعالجة..."):
            # استخراج النص
            result = model.transcribe("temp_file")
            text = result['text']
            st.session_state['text'] = text
            
            # الترجمة للعربية تلقائياً
            translated = GoogleTranslator(source='auto', target='ar').translate(text)
            st.session_state['translated'] = translated

    if 'text' in st.session_state:
        st.subheader("النص الأصلي:")
        st.write(st.session_state['text'])
        
        st.subheader("الترجمة العربية:")
        st.write(st.session_state['translated'])

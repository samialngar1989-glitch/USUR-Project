import streamlit as st
import whisper
import os

st.set_page_config(page_title="USUR Lite", page_icon="💠")
st.title("💠 نظام USUR (النسخة المستقرة)")

@st.cache_resource
def load_model():
    # استخدام أصغر موديل لضمان استقرار السيرفر ومنع توقفه
    return whisper.load_model("tiny")

model = load_model()

uploaded_file = st.file_uploader("ارفع ملف الصوت (AMR, MP3, WAV)", type=["mp3", "wav", "m4a", "amr", "opus"])

if uploaded_file is not None:
    # حفظ مؤقت
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success("✅ الملف جاهز")

    if st.button("🚀 استخراج النص"):
        with st.spinner("جاري المعالجة السريعة..."):
            try:
                # معالجة سريعة وخفيفة
                result = model.transcribe(uploaded_file.name, language='ar')
                st.session_state['result_text'] = result['text'].strip()
                os.remove(uploaded_file.name)
            except Exception as e:
                st.error(f"حدث ضغط على السيرفر، يرجى المحاولة لاحقاً: {e}")

if 'result_text' in st.session_state:
    st.markdown("---")
    st.subheader("📄 النص المستخرج:")
    st.write(st.session_state['result_text'])

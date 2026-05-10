import streamlit as st
import whisper
from deep_translator import GoogleTranslator
import os

st.set_page_config(page_title="نظام USUR الاحترافي", page_icon="💠")
st.title("💠 نظام USUR: استخراج نص ذكي")

@st.cache_resource
def load_model():
    # انتقلنا لموديل small لزيادة الدقة مع الحفاظ على سرعة السيرفر
    return whisper.load_model("small")

model = load_model()

uploaded_file = st.file_uploader("ارفع مقطع الواتساب أو الفيديو", type=["mp3", "wav", "m4a", "mp4", "amr", "opus"])

if uploaded_file is not None:
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success("✅ تم استقبال الملف بنجاح")

    if st.button("🚀 بدء الاستخراج بدقة عالية"):
        with st.spinner("جاري تحليل الكلام بدقة... يرجى الانتظار"):
            try:
                # إجبار الموديل على العربية وإعطاؤه "سياق" لتحسين النتائج
                result = model.transcribe(
                    uploaded_file.name, 
                    language='ar', 
                    initial_prompt="هذا تسجيل صوتي باللغة العربية يتحدث عن مواضيع هامة"
                )
                text_out = result['text'].strip()
                
                # ترجمة النص (اختياري)
                translated_out = GoogleTranslator(source='auto', target='ar').translate(text_out)
                
                st.session_state['original'] = text_out
                os.remove(uploaded_file.name)
            except Exception as e:
                st.error(f"خطأ تقني: {e}")

if 'original' in st.session_state:
    st.markdown("---")
    st.subheader("📄 النص المستخرج (بعد التحسين):")
    st.write(st.session_state['original'])

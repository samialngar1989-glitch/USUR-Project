import streamlit as st
import whisper
from deep_translator import GoogleTranslator
import os

# 1. إعدادات الصفحة
st.set_page_config(page_title="نظام USUR للترجمة", page_icon="💠")
st.title("💠 نظام USUR: تحويل وترجمة الوسائط")

# 2. تحميل الموديل (تخزين مؤقت للسرعة)
@st.cache_resource
def load_model():
    return whisper.load_model("base")

model = load_model()

# 3. واجهة رفع الملفات (دعم شامل لكل الصيغ)
uploaded_file = st.file_uploader("ارفع ملف الصوت أو الفيديو (يدعم واتساب AMR)", type=["mp3", "wav", "m4a", "mp4", "amr", "opus"])

if uploaded_file is not None:
    # حفظ الملف مؤقتاً باسمه الأصلي لتجنب خطأ "الملف غير موجود"
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success(f"✅ تم استقبال الملف: {uploaded_file.name}")

    if st.button("🎙️ استخراج النص والترجمة"):
        with st.spinner("جاري تحليل الصوت... يرجى الانتظار"):
            try:
                # التأكد من وجود الملف قبل البدء
                if os.path.exists(uploaded_file.name):
                    # معالجة الملف باستخدام الموديل
                    result = model.transcribe(uploaded_file.name)
                    text_out = result['text'].strip()
                    
                    # الترجمة الفورية للعربية
                    translated_out = GoogleTranslator(source='auto', target='ar').translate(text_out)
                    
                    # حفظ النتائج في الجلسة للعرض
                    st.session_state['original'] = text_out
                    st.session_state['translated'] = translated_out
                    
                    # حذف الملف المؤقت فوراً لتنظيف السيرفر
                    os.remove(uploaded_file.name)
                else:
                    st.error("فشل النظام في العثور على الملف المرفوع.")
            except Exception as e:
                st.error(f"حدث خطأ تقني: {e}")

# 4. عرض النتائج
if 'original' in st.session_state:
    st.markdown("---")
    st.subheader("📄 النص المستخرج:")
    st.info(st.session_state['original'])
    
    st.subheader("🌍 الترجمة العربية:")
    st.success(st.session_state['translated'])

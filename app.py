import streamlit as st
import whisper
import os

st.set_page_config(page_title="نظام USUR الاحترافي", page_icon="💠")
st.title("💠 نظام USUR: الدقة المحسنة")

@st.cache_resource
def load_model():
    # سنحاول تشغيل موديل medium، إذا كان السيرفر ضعيفاً سيعود لـ small تلقائياً
    try:
        return whisper.load_model("medium")
    except:
        return whisper.load_model("small")

model = load_model()

uploaded_file = st.file_uploader("ارفع مقطع الواتساب (AMR/OPUS) أو الفيديو", type=["mp3", "wav", "m4a", "mp4", "amr", "opus"])

if uploaded_file is not None:
    # حفظ الملف مؤقتاً
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success("✅ تم استقبال الملف")

    if st.button("🚀 بدء استخراج النص بدقة"):
        with st.spinner("جاري التحليل... قد يستغرق المقطع الطويل بضع دقائق"):
            try:
                # تحسين الاستخراج عبر تحديد اللغة وإعطاء سياق عربي
                result = model.transcribe(
                    uploaded_file.name, 
                    language='ar',
                    beam_size=5, # زيادة الدقة في التخمين
                    best_of=5
                )
                
                text_out = result['text'].strip()
                st.session_state['final_text'] = text_out
                
                # تنظيف
                os.remove(uploaded_file.name)
            except Exception as e:
                st.error(f"عذراً، السيرفر المجاني لم يتحمل المعالجة: {e}")

if 'final_text' in st.session_state:
    st.markdown("---")
    st.subheader("📄 النتيجة النهائية:")
    st.write(st.session_state['final_text'])
    st.download_button("تحميل النص كملف", st.session_state['final_text'], file_name="usur_text.txt")

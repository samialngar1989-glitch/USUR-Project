
import whisper
import gradio as gr
from deep_translator import GoogleTranslator
import torch

# التحقق من تفعيل GPU
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"النظام يعمل الآن باستخدام: {device}")

# تحميل موديل medium (التوازن المثالي)
# يتم تحميله على الـ GPU مباشرة لسرعة المعالجة
model = whisper.load_model("medium").to(device)

def usur_optimized_process(audio_file, target_lang):
    if audio_file is None:
        return "⚠️ يرجى رفع ملف أولاً", ""
    
    # معالجة الصوت باستخدام GPU
    # FP16=True تسرع العملية جداً على كروت الشاشة
    result = model.transcribe(audio_file, language='ar', fp16=True)
    original_text = result['text'].strip()
    
    # الترجمة
    lang_map = {"العربية": "ar", "English": "en", "Urdu": "ur", "French": "fr"}
    try:
        translated_text = GoogleTranslator(source='auto', target=lang_map[target_lang]).translate(original_text)
    except:
        translated_text = "خطأ في الاتصال بمحرك الترجمة."
        
    return original_text, translated_text

# الواجهة
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 💠 نظام USUR فائق السرعة (Turbo GPU)")
    gr.Markdown(f"المحرك الحالي: **Medium Model** | المعالج: **{device.upper()}**")
    
    with gr.Row():
        audio_input = gr.Audio(type="filepath", label="ارفع ملفك (صوت أو فيديو)")
        target_lang = gr.Dropdown(choices=["العربية", "English", "Urdu", "French"], value="English", label="لغة الترجمة")
    
    btn = gr.Button("🚀 بدء المعالجة الفورية", variant="primary")
    
    with gr.Row():
        out_original = gr.Textbox(label="النص المستخرج بدقة", lines=12, show_copy_button=True)
        out_translated = gr.Textbox(label="الترجمة المعتمدة", lines=12, show_copy_button=True)
    
    btn.click(usur_optimized_process, inputs=[audio_input, target_lang], outputs=[out_original, out_translated])

demo.launch(share=True)

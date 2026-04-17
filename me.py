import streamlit as st
from textblob import TextBlob
from PIL import Image, ImageStat
import PyPDF2
from docx import Document
import io

# إعدادات الصفحة
st.set_page_config(page_title="Analyse Pro", layout="centered")

st.title("📊 Emotion Analysis Pro")

tab1, tab2, tab3 = st.tabs(["📷 Image", "✍️ Text", "📂 Files"])

# --- قسم الصور ---
with tab1:
    up_img = st.file_uploader("Upload Image", type=['jpg', 'png'], key="img_p")
    if up_img:
        img = Image.open(up_img)
        st.image(img)
        stat = ImageStat.Stat(img.convert('L'))
        res = "Positive/Bright" if stat.stddev[0] > 45 else "Neutral/Muted"
        st.info(f"Visual Tone: {res}")

# --- قسم النصوص ---
with tab2:
    txt = st.text_area("Enter Text", key="txt_p")
    if st.button("Analyze Text"):
        if txt:
            score = TextBlob(txt).sentiment.polarity
            if score > 0: st.success("Positive 😊")
            elif score < 0: st.error("Negative 😡")
            else: st.warning("Neutral 😐")

# --- قسم الملفات (تم إصلاحه ليعمل في الويب والتطبيق) ---
with tab3:
    st.subheader("File Analysis")
    up_file = st.file_uploader("Choose PDF, DOCX, or TXT", type=['pdf', 'docx', 'txt'], key="file_p")
    
    if up_file is not None:
        try:
            filename = up_file.name.lower()
            text_data = ""

            # قراءة PDF
            if filename.endswith('.pdf'):
                pdf_reader = PyPDF2.PdfReader(up_file)
                for page in pdf_reader.pages:
                    text_data += page.extract_text() + " "
            
            # قراءة Word
            elif filename.endswith('.docx'):
                doc = Document(up_file)
                text_data = " ".join([p.text for p in doc.paragraphs])
            
            # قراءة Text
            elif filename.endswith('.txt'):
                text_data = up_file.read().decode("utf-8")

            # التحليل إذا وجد نص
            if text_data.strip():
                analysis = TextBlob(text_data).sentiment.polarity
                # تحويل لنسب مئوية
                p = max(0, analysis * 100) if analysis > 0 else 0
                n = abs(min(0, analysis * 100)) if analysis < 0 else 0
                neu = 100 - (p + n)

                st.markdown(f"**Results for:** {up_file.name}")
                col1, col2, col3 = st.columns(3)
                col1.metric("Positive", f"{p:.1f}%")
                col2.metric("Negative", f"{n:.1f}%")
                col3.metric("Neutral", f"{neu:.1f}%")
                st.progress(int(max(p, n, neu)))
            else:
                st.warning("No readable text found in this file.")
                
        except Exception as e:
            st.error(f"Error: {e}")
            

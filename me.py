import streamlit as st
from textblob import TextBlob
from PIL import Image, ImageStat
import PyPDF2
from docx import Document
import io

# 1. إعداد واجهة التطبيق
st.set_page_config(page_title="Analyse Pro", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; border-radius: 20px; background: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Emotion Analysis Pro")

tab1, tab2, tab3 = st.tabs(["📷 Image", "✍️ Text", "📂 Files"])

# --- قسم الصور (تحليل السطوع) ---
with tab1:
    st.subheader("Visual Analysis")
    up_img = st.file_uploader("Upload Image", type=['jpg', 'jpeg', 'png'], key="img_u")
    if up_img:
        img = Image.open(up_img)
        st.image(img, use_container_width=True)
        if st.button("Analyze Image Tone"):
            # تحويل الصورة للأبيض والأسود لحساب السطوع بدقة
            stat = ImageStat.Stat(img.convert('L'))
            brightness = stat.mean[0]
            if brightness > 120:
                st.success(f"Result: Positive & Bright Tone (Brightness: {brightness:.1f})")
            else:
                st.warning(f"Result: Muted or Dark Tone (Brightness: {brightness:.1f})")

# --- قسم النصوص ---
with tab2:
    st.subheader("Sentiment Analysis")
    txt = st.text_area("Enter English Text", height=150)
    if st.button("Check Emotion"):
        if txt:
            score = TextBlob(txt).sentiment.polarity
            if score > 0.1: st.success("Outcome: Positive 😊")
            elif score < -0.1: st.error("Outcome: Negative 😡")
            else: st.warning("Outcome: Neutral 😐")

# --- قسم الملفات (التحليل بالنسب المئوية) ---
with tab3:
    st.subheader("File Analysis (Percentage)")
    up_file = st.file_uploader("Choose PDF, DOCX, or TXT", type=['pdf', 'docx', 'txt'], key="file_u")
    
    if up_file:
        try:
            ext = up_file.name.split('.')[-1].lower()
            text_data = ""

            if ext == 'pdf':
                reader = PyPDF2.PdfReader(up_file)
                text_data = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
            elif ext == 'docx':
                doc = Document(up_file)
                text_data = " ".join([p.text for p in doc.paragraphs])
            elif ext == 'txt':
                text_data = up_file.read().decode("utf-8")

            if text_data.strip():
                analysis = TextBlob(text_data).sentiment.polarity
                
                # حساب النسب المئوية
                if analysis > 0:
                    pos = analysis * 100
                    neg = 0
                elif analysis < 0:
                    neg = abs(analysis) * 100
                    pos = 0
                else:
                    pos = 0
                    neg = 0
                
                neu = 100 - (pos + neg)

                st.info(f"Analysis for: {up_file.name}")
                col1, col2, col3 = st.columns(3)
                col1.metric("Positive", f"{pos:.1f}%")
                col2.metric("Negative", f"{neg:.1f}%")
                col3.metric("Neutral", f"{neu:.1f}%")
                st.progress(int(max(pos, neg, neu)))
            else:
                st.error("No text could be extracted from this file.")
        except Exception as e:
            st.error(f"Error: {e}")
            

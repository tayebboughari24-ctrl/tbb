import streamlit as st
import pandas as pd
import PyPDF2
from docx import Document
from PIL import Image, ImageStat
from textblob import TextBlob

# إعدادات تجعل الموقع يبدو كتطبيق هاتف
st.set_page_config(page_title="Emotion Analysis App", layout="centered")

# تصميم CSS لتحسين مظهر التطبيق
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3.5em;
        background: linear-gradient(45deg, #007bff, #00d4ff);
        color: white;
        font-weight: bold;
    }
    div[data-testid="stMetric"] {
        background-color: #1e2130;
        border-radius: 15px;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center;'>📊 Emotion Analysis</h2>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📷 Photo", "✍️ Text", "📂 Files"])

with tab1:
    up_img = st.file_uploader("Upload Image", type=['jpg', 'png'])
    if up_img:
        img = Image.open(up_img)
        st.image(img, use_container_width=True)
        if st.button("Analyze Photo"):
            stat = ImageStat.Stat(img.convert('L'))
            res = "Positive/Bright" if stat.stddev[0] > 45 else "Neutral/Muted"
            st.info(f"Result: {res}")

with tab2:
    text = st.text_area("Write text here...", height=100)
    if st.button("Check Emotion"):
        if text:
            pol = TextBlob(text).sentiment.polarity
            if pol > 0: st.success("Positive 😊")
            elif pol < 0: st.error("Negative 😡")
            else: st.warning("Neutral 😐")

with tab3:
    up_file = st.file_uploader("Upload Document", key="file")
    if up_file:
        ext = up_file.name.split('.')[-1].lower()
        content = ""
        try:
            if ext == 'pdf':
                pdf = PyPDF2.PdfReader(up_file)
                content = " ".join([p.extract_text() for p in pdf.pages])
            elif ext == 'docx':
                doc = Document(up_file)
                content = " ".join([p.text for p in doc.paragraphs])
            elif ext in ['xlsx', 'csv']:
                df = pd.read_excel(up_file) if 'xls' in ext else pd.read_csv(up_file)
                content = " ".join(df.astype(str).values.flatten())
            
            if content.strip():
                analysis = TextBlob(content).sentiment.polarity
                p = max(0, analysis * 100) if analysis > 0 else 0
                n = abs(min(0, analysis * 100)) if analysis < 0 else 0
                neu = 100 - (p + n)
                
                c1, c2, c3 = st.columns(3)
                c1.metric("Positive", f"{p:.1f}%")
                c2.metric("Negative", f"{n:.1f}%")
                c3.metric("Neutral", f"{neu:.1f}%")
                st.progress(int(max(p, n, neu)))
        except:
            st.error("Analysis Error")
      

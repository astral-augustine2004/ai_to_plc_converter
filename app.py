import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import re

# Load Gemini API Key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ---- PAGE CONFIG ----
st.set_page_config(page_title="AI to PLC Converter", page_icon="🤖", layout="wide")

# ---- CUSTOM CSS ----
st.markdown("""
    <style>
        body { background-color: #0e1117; color: white; }
        .stTextArea textarea { background-color: #1e222b !important; color: #f0f0f0 !important; border-radius: 10px !important; }
        .stSelectbox div[data-baseweb="select"] > div { background-color: #1e222b !important; color: #f0f0f0 !important; border-radius: 8px !important; }
        .stButton button {
            background: linear-gradient(90deg, #00C6FF 0%, #0072FF 100%);
            color: white; font-weight: 600; border-radius: 10px; height: 3em; width: 100%;
        }
        .stButton button:hover {
            background: linear-gradient(90deg, #0072FF 0%, #00C6FF 100%);
            transform: scale(1.02);
            transition: 0.2s ease;
        }
        h1 {
            background: linear-gradient(90deg, #00C6FF 0%, #0072FF 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            font-weight: 800; text-align: center;
        }
        .footer { text-align: center; color: #aaa; margin-top: 40px; font-size: 0.9em; }
        .ladder-box { background-color: #1e222b; padding: 10px; border-radius: 10px; }
        .rung { border-bottom: 2px solid #00C6FF; margin: 10px 0; padding: 5px; }
        .contact { display: inline-block; border: 2px solid #00C6FF; padding: 5px 15px; margin: 5px; border-radius: 6px; }
        .coil { display: inline-block; border: 2px solid #FF0080; padding: 5px 15px; margin: 5px; border-radius: 6px; }
    </style>
""", unsafe_allow_html=True)

# ---- SIDEBAR ----
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/4712/4712100.png", width=100)
st.sidebar.title("⚙️ AI to PLC Converter")
menu = st.sidebar.radio("Navigation", ["🏠 Home", "ℹ️ About", "👨‍💻 Developer Info"])

# ---- LADDER DIAGRAM GENERATOR ----
def generate_ladder_diagram(plc_code):
    """Simple visual representation of ladder logic"""
    lines = plc_code.split("\n")
    diagram_html = "<div class='ladder-box'>"
    rung_count = 1
    for line in lines:
        if re.search(r"(XIC|XIO|LD|AND|OR)", line, re.IGNORECASE):
            diagram_html += f"<div class='rung'><b>Rung {rung_count}</b><br>"
            contacts = re.findall(r"[A-Z]+\s*[\w_]+", line)
            for c in contacts:
                diagram_html += f"<span class='contact'>{c}</span>"
            diagram_html += "</div>"
            rung_count += 1
        elif re.search(r"(OUT|OTE|SET|RESET|COIL)", line, re.IGNORECASE):
            diagram_html += f"<div class='rung'><span class='coil'>{line.strip()}</span></div>"
    diagram_html += "</div>"
    return diagram_html

# ---- HOME PAGE ----
if menu == "🏠 Home":
    st.markdown("<h1>🤖 AI to PLC Converter</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#aaa;'>Convert Python, C, or Java code into Ladder Logic or Structured Text using Google Gemini 2.5 🚀</p>", unsafe_allow_html=True)

    language = st.selectbox("🧠 Select PLC Output Format", ["Ladder Logic", "Structured Text (ST)"])
    user_code = st.text_area("💻 Paste your program code here:", height=200)

    if st.button("⚙️ Convert with AI"):
        if not user_code.strip():
            st.warning("⚠️ Please paste a program first!")
        else:
            with st.spinner("✨ Converting your code... please wait..."):
                try:
                    prompt = f"Convert the following program into PLC {language} format:\n\n{user_code}"
                    model = genai.GenerativeModel(model_name="models/gemini-2.5-flash")
                    response = model.generate_content(prompt)
                    result = response.text

                    st.success("✅ Conversion Complete!")
                    st.code(result, language="pascal")

                    if language == "Ladder Logic":
                        st.markdown("### 🔍 Ladder Diagram Preview")
                        ladder_html = generate_ladder_diagram(result)
                        st.markdown(ladder_html, unsafe_allow_html=True)

                    st.download_button(
                        label="⬇️ Download Converted PLC Code",
                        data=result,
                        file_name="converted_plc_code.txt",
                        mime="text/plain"
                    )

                except Exception as e:
                    st.error(f"❌ Error: {e}")

    st.markdown("<div class='footer'>Created by <b>Augustine .P</b> | Powered by Google Gemini 2.5 ⚡</div>", unsafe_allow_html=True)

# ---- ABOUT PAGE ----
elif menu == "ℹ️ About":
    st.markdown("<h1>ℹ️ About This Project</h1>", unsafe_allow_html=True)
    st.write("""
    The **AI to PLC Converter** automatically transforms your programming code 
    (Python, C, or Java) into **PLC Ladder Logic** or **Structured Text (ST)**.

    ### 🔧 Features:
    - Converts modern code → PLC logic instantly  
    - Supports Ladder Logic visualization 🪜  
    - Downloadable PLC file output  
    - Built with **Google Gemini 2.5** + **Streamlit**

    Ideal for **students**, **engineers**, and **automation developers** 💡
    """)

# ---- DEVELOPER INFO PAGE ----
elif menu == "👨‍💻 Developer Info":
    st.markdown("<h1>👨‍💻 Developer Information</h1>", unsafe_allow_html=True)
    st.write("""
    **Developer:** Augustine .P  
    **Department:** ECE  
    **Project:** Smart AI-PLC Integration Tool  
    **Location:** India 🇮🇳  

    🔗 **Contact Me:**  
    - 📧 Email: *your_email@example.com*  
    """)


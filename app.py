import streamlit as st
import base64
from pathlib import Path

#Import your encryption functions from the toolkit
try:
    from ciphers import (
        caesar_encrypt, caesar_decrypt,
        vigenere_encrypt, vigenere_decrypt,
        reverse_text,
        ascii_shift, ascii_unshift,
        base64_encode, base64_decode,
        generate_sha256 # Added SHA-256
    )
    from multilayer import multi_encrypt, multi_decrypt
except ImportError:
    st.error("Logic files (ciphers.py or multilayer.py) not found! Please ensure they are in the same directory.")

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="NovaCrypt",
    page_icon="🔐",
    layout="centered"
)


#LOAD AND ENCODE STATIC FILES
def load_css_with_assets():
    #Load CSS and embed static assets as base64
    #Read the font file and encode to base64
    try:
        with open("static/pixel-font.ttf", "rb") as font_file:
            font_data = base64.b64encode(font_file.read()).decode()
    except FileNotFoundError:
        font_data = ""
        st.warning("⚠️pixel-font.ttf not found in static/ folder")

    #Read the background image and encode to base64
    try:
        with open("static/bg.png", "rb") as bg_file:
            bg_data = base64.b64encode(bg_file.read()).decode()
    except FileNotFoundError:
        bg_data = ""
        st.warning("⚠️bg.png not found in static/ folder")

    #Inject CSS with embedded assets
    css = f"""
    <style>
    @font-face {{
        font-family: 'PixelFont';
        src: url(data:font/truetype;charset=utf-8;base64,{font_data}) format('truetype');
    }}

    /* REMOVE STREAMLIT TOP BAR */
    header {{
        visibility: hidden;
        height: 0px;
    }}

    /* BACKGROUND IMAGE */
    [data-testid="stApp"] {{
        background: url(data:image/png;base64,{bg_data}) no-repeat center center fixed;
        background-size: cover;
    }}

    /* TRANSLUCENT MAIN CARD */
    .block-container {{
        background: rgba(230, 215, 255, 0.25) !important;
        backdrop-filter: blur(15px) saturate(180%);
        -webkit-backdrop-filter: blur(15px) saturate(180%);
        border-radius: 28px;
        max-width: 720px;
        margin: 6vh auto;
        padding: 3rem 3.2rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }}

    /* TITLE */
    .novacrypt-title {{
        font-family: 'PixelFont', monospace !important;
        font-size: 56px !important;
        text-align: center;
        color: #6a1bb1;
        margin-bottom: 0.3rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }}

    /* SUBTITLE */
    .subtitle {{
        text-align: center;
        font-size: 20px !important;
        font-weight: 600 !important;
        color: #4a0e78 !important;
        margin-bottom: 2.5rem;
        letter-spacing: 0.5px;
    }}

    /* LARGER FIELD LABELS */
    .stTextArea label, .stSelectbox label, .stNumberInput label, .stTextInput label, label p {{
        font-size: 20px !important;
        font-weight: 700 !important;
        color: #4a0e78 !important;
        margin-bottom: 10px !important;
    }}

    /* PURPLE RESULT HEADER */
    h3 {{
        color: #6a1bb1 !important;
        font-size: 30px !important;
        font-weight: 800 !important;
        margin-top: 2rem !important;
    }}

    /* BUTTONS */
    .stButton > button {{
        background: linear-gradient(135deg, #7a2cbf, #9b4dff);
        color: white;
        border-radius: 12px;
        padding: 0.6rem 1.6rem;
        font-size: 15px;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
    }}

    .stButton > button:hover {{
        transform: scale(1.05);
        box-shadow: 0 8px 20px rgba(122, 44, 191, 0.4);
        color: white;
        border: none;
    }}

    /* RESULT BOX STYLING - TRANSLUCENT */
    .result-box {{
        background: rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(5px);
        border: 2px solid #9b4dff;
        border-radius: 12px;
        padding: 1.2rem;
        min-height: 150px;
        font-family: monospace;
        font-size: 16px;
        color: #1a1a1a;
        word-wrap: break-word;
        white-space: pre-wrap;
        margin-top: 0.5rem;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


#Load the custom translucent UI
load_css_with_assets()

#Initialize session state for result
if 'result' not in st.session_state:
    st.session_state['result'] = ""

#TITLE
st.markdown('<div class="novacrypt-title">NovaCrypt</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Multi-Layer Text Encryption Lab</div>', unsafe_allow_html=True)

#UI INPUTS
text = st.text_area("📝Enter the Text", height=150, key="input_text")

method = st.selectbox(
    "🔐Select Encryption Method",
    [
        "Caesar Cipher",
        "Reverse Cipher",
        "ASCII Shift",
        "Vigenère Cipher",
        "Base64 Encoding",
        "Multi-Layer Encryption",
        "SHA-256 Hashing"
    ]
)

#Parameter logic for different methods
shift = ascii_val = None
key = ""

if method == "Caesar Cipher":
    shift = st.number_input("🔑Shift Key", 1, 50, 3)

elif method == "ASCII Shift":
    ascii_val = st.number_input("🔢ASCII Shift Value", 1, 50, 5)

elif method == "Vigenère Cipher":
    key = st.text_input("🔤Keyword")

elif method == "Multi-Layer Encryption":
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        shift = st.number_input("🔑Caesar Shift", 1, 50, 3)
        ascii_val = st.number_input("🔢ASCII Shift", 1, 50, 5)
    with col_m2:
        key = st.text_input("🔤Vigenère Keyword", value="KEY")

st.write("---")  #Visual separator

#ACTION BUTTONS
col1, col2 = st.columns(2)

with col1:
    if st.button("🔒Encrypt / Hash", use_container_width=True):
        if not text:
            st.warning("⚠ Enter some text first.")
        else:
            try:
                if method == "Caesar Cipher":
                    st.session_state['result'] = caesar_encrypt(text, shift)
                elif method == "Reverse Cipher":
                    st.session_state['result'] = reverse_text(text)
                elif method == "ASCII Shift":
                    st.session_state['result'] = ascii_shift(text, ascii_val)
                elif method == "Vigenère Cipher":
                    if not key:
                        st.error("Please enter a keyword!")
                    else:
                        st.session_state['result'] = vigenere_encrypt(text, key)
                elif method == "Base64 Encoding":
                    st.session_state['result'] = base64_encode(text)
                elif method == "Multi-Layer Encryption":
                    if not key:
                        st.error("Please enter a keyword!")
                    else:
                        st.session_state['result'] = multi_encrypt(text, shift, key, ascii_val, verbose=False)
                elif method == "SHA-256 Hashing":
                    st.session_state['result'] = generate_sha256(text)

                if st.session_state['result']:
                    st.success("✅Encryption successful!")
            except Exception as e:
                st.error(f"Error: {str(e)}")

with col2:
    if st.button("🔓Decrypt", use_container_width=True):
        if not text:
            st.warning("⚠ Enter text to decrypt.")
        else:
            try:
                if method == "Caesar Cipher":
                    st.session_state['result'] = caesar_decrypt(text, shift)
                elif method == "Reverse Cipher":
                    st.session_state['result'] = reverse_text(text)
                elif method == "ASCII Shift":
                    st.session_state['result'] = ascii_unshift(text, ascii_val)
                elif method == "Vigenère Cipher":
                    if not key:
                        st.error("Please enter a keyword!")
                    else:
                        st.session_state['result'] = vigenere_decrypt(text, key)
                elif method == "Base64 Encoding":
                    st.session_state['result'] = base64_decode(text)
                elif method == "Multi-Layer Encryption":
                    if not key:
                        st.error("Please enter a keyword!")
                    else:
                        st.session_state['result'] = multi_decrypt(text, shift, key, ascii_val, verbose=False)
                elif method == "SHA-256 Hashing":
                    st.error("SHA-256 is a one-way hash and cannot be decrypted!")
                    st.session_state['result'] = ""

                if st.session_state['result'] and method != "SHA-256 Hashing":
                    st.success("✅Decryption successful!")
            except Exception as e:
                st.error(f"Decryption error: {str(e)}")

#RESULT DISPLAY
st.markdown("### ✨Result")

if st.session_state['result']:
    st.markdown(
        f'<div class="result-box">{st.session_state["result"]}</div>',
        unsafe_allow_html=True
    )
    st.info("💡Highlight the text above to copy it.")
else:
    st.markdown(
        '<div class="result-box" style="color: #666;">Waiting for input...</div>',
        unsafe_allow_html=True
    )
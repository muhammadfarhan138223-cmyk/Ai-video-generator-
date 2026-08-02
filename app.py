import base64
import os
import groq
import replicate
import streamlit as st

# -------------------------------------------------------------
# 1. PAGE CONFIG & CLEAN UI STYLING (High Contrast Dark Mode)
# -------------------------------------------------------------
st.set_page_config(
    page_title="Nova AI - Video & Image Ad Generator",
    page_icon="🎬",
    layout="centered",
)

st.markdown(
    """
    <style>
    /* Clean Dark Theme Fixes */
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    .stChatMessage {
        background-color: #1E222D !important;
        border: 1px solid #2E3440;
        border-radius: 12px;
        color: #FFFFFF !important;
    }
    p, span, div {
        color: #FFFFFF !important;
    }
    .stTextInput input {
        color: #FFFFFF !important;
        background-color: #1E222D !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# -------------------------------------------------------------
# 2. API KEYS CONFIGURATION
# -------------------------------------------------------------
# Hardcoded Replicate Token for Video Generation
REPLICATE_KEY = "r8_P3UFtKeJNRaMlijK4hgAn2uLo2hwfoZ00Exiw"
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_KEY

# Sidebar for Groq API Key & Settings
with st.sidebar:
    st.header("⚙️ Settings & API Keys")
    groq_api_key = st.text_input("Groq API Key (Optional for Vision):", type="password", help="Enter your Groq API key here")
    st.markdown("---")
    st.markdown("<b>Mode:</b> Direct Image to Video Ad Conversion", unsafe_allow_html=True)

# -------------------------------------------------------------
# 3. HEADER
# -------------------------------------------------------------
st.title("🎬 Nova AI - E-Commerce Ad Generator")
st.caption("Upload product photo or type prompt to generate HD 4K Video Ads!")

# -------------------------------------------------------------
# 4. CHAT HISTORY INITIALIZATION
# -------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi! Main Nova AI hoon. Product ki pic upload karein ya text description dein, main ad video generate kar doonga!",
        }
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if "image" in msg:
            st.image(msg["image"], width=300)
        if "video_url" in msg:
            st.video(msg["video_url"])

# -------------------------------------------------------------
# 5. INPUT SECTION (IMAGE + TEXT)
# -------------------------------------------------------------
uploaded_file = st.file_uploader("📷 Upload Product Image (Optional):", type=["jpg", "png", "jpeg"])
user_prompt = st.chat_input("Write prompt or describe ad angle...")

if user_prompt or uploaded_file:
    prompt_text = user_prompt if user_prompt else "Create cinematic studio commercial ad video for this product."
    
    # Process User Message
    user_msg = {"role": "user", "content": prompt_text}
    if uploaded_file:
        user_msg["image"] = uploaded_file
    st.session_state.messages.append(user_msg)
    
    with st.chat_message("user"):
        st.write(prompt_text)
        if uploaded_file:
            st.image(uploaded_file, width=300)

    # Process AI Video Generation
    with st.chat_message("assistant"):
        with st.spinner("⏳ Cloud AI Engine video render kar raha hai (30-40 sec)..."):
            try:
                # Video Generation via Replicate API
                output = replicate.run(
                    "minimax/video-01",
                    input={
                        "prompt": f"Commercial studio product video of {prompt_text}, 4k resolution, cinematic lighting, ultra realistic motion",
                        "prompt_optimizer": True
                    }
                )
                video_url = str(output)
                
                success_text = f"✅ Aapki AI Video Ad Ready Hai!"
                st.write(success_text)
                st.video(video_url)
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": success_text,
                    "video_url": video_url
                })
            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

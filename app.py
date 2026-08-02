import os
import replicate
import streamlit as st

# -------------------------------------------------------------
# 1. GOOGLE SEO & RESPONSIVE PAGE CONFIGURATION
# -------------------------------------------------------------
st.set_page_config(
    page_title="Nova AI - Free E-Commerce Product Video Generator",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# -------------------------------------------------------------
# 2. SLEEK MODERN UI & CONTRAST FIX (CSS)
# -------------------------------------------------------------
st.markdown(
    """
    <style>
    /* Global Background & Font Styling */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #f8fafc !important;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    
    /* Header Typography */
    h1 {
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem !important;
    }
    
    .sub-caption {
        font-size: 0.88rem;
        color: #94a3b8 !important;
        margin-bottom: 1.2rem;
    }

    /* Chat Message Bubbles */
    .stChatMessage {
        background-color: rgba(30, 41, 59, 0.75) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 14px !important;
        padding: 12px 16px !important;
        margin-bottom: 10px !important;
        backdrop-filter: blur(10px);
    }
    
    /* Text Color Fixes */
    p, span, label, div {
        color: #f1f5f9 !important;
    }

    /* Input Fields Fix */
    .stTextInput input, .stChatInput input {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border: 1px solid #475569 !important;
        border-radius: 10px !important;
        font-size: 0.9rem !important;
    }

    /* File Uploader Container */
    [data-testid="stFileUploader"] {
        background-color: rgba(30, 41, 59, 0.5);
        border: 1px dashed #475569;
        border-radius: 12px;
        padding: 8px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# -------------------------------------------------------------
# 3. EMBEDDED API AUTHENTICATION (No User Action Required)
# -------------------------------------------------------------
REPLICATE_TOKEN = "r8_P3UFtKeJNRaMlijK4hgAn2uLo2hwfoZ00Exiw"
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_TOKEN

# -------------------------------------------------------------
# 4. APP HEADER & DESCRIPTION
# -------------------------------------------------------------
st.markdown("<h1>🎬 Nova AI Video Generator</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='sub-caption'>Transform product descriptions & photos into 4K HD Video Ads in 30 seconds.</p>",
    unsafe_allow_html=True,
)

# -------------------------------------------------------------
# 5. CHAT SESSION INITIALIZATION
# -------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "👋 Assalam-o-Alaikum! Main **Nova AI** hoon. Apne product ki photo upload karein ya text description dein (e.g., *'Luxury gold watch with neon glowing display'*), main HD Video Ad generate kar dunga!",
        }
    ]

# Render previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "image" in msg:
            st.image(msg["image"], use_column_width=True)
        if "video_url" in msg:
            st.video(msg["video_url"])

# -------------------------------------------------------------
# 6. DYNAMIC USER INPUT SECTION
# -------------------------------------------------------------
uploaded_file = st.file_uploader(
    "📷 Upload Product Image (Optional):", type=["jpg", "png", "jpeg"]
)
user_prompt = st.chat_input(
    "Describe your product ad angle (e.g., Red sneaker running on water track)..."
)

if user_prompt or uploaded_file:
    prompt_text = (
        user_prompt
        if user_prompt
        else "Create high-converting cinematic studio commercial video ad for this product."
    )

    # 1. Show User Input
    user_msg = {"role": "user", "content": prompt_text}
    if uploaded_file:
        user_msg["image"] = uploaded_file

    st.session_state.messages.append(user_msg)
    with st.chat_message("user"):
        st.markdown(prompt_text)
        if uploaded_file:
            st.image(uploaded_file, use_column_width=True)

    # 2. Generate Video via AI Engine
    with st.chat_message("assistant"):
        with st.spinner(
            "⚡ Cloud AI Engine 4K Video render kar raha hai (30-40 sec)..."
        ):
            try:
                output = replicate.run(
                    "minimax/video-01",
                    input={
                        "prompt": f"Commercial studio product video of {prompt_text}, 4k resolution, cinematic lighting, ultra realistic motion",
                        "prompt_optimizer": True,
                    },
                )
                video_url = str(output)

                reply_text = f"✨ **Aapki AI Commercial Video Ready Hai!**"
                st.markdown(reply_text)
                st.video(video_url)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": reply_text,
                        "video_url": video_url,
                    }
                )

            except Exception as e:
                error_msg = f"⚠️ **Error:** {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append(
                    {"role": "assistant", "content": error_msg}
                )

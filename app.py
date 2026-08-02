import os
import replicate
import streamlit as st

# -------------------------------------------------------------
# 1. SEO & PAGE CONFIGURATION (For Google Ranking)
# -------------------------------------------------------------
st.set_page_config(
    page_title="Nova AI - Free E-Commerce AI Video Generator",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Dark Theme & Custom CSS Styling for Modern Chat Look
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    .stChatMessage {
        border-radius: 12px;
        padding: 10px;
        margin-bottom: 10px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# -------------------------------------------------------------
# 2. REPLICATE API KEY SETUP
# -------------------------------------------------------------
# GitHub Secrets ya direct token setup
REPLICATE_TOKEN = os.environ.get(
    "REPLICATE_API_TOKEN", "r8_P3UFtKeJNRaMlijK4hgAn2uLo2hwfoZ00Exiw"
)
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_TOKEN

# -------------------------------------------------------------
# 3. HEADER & HERO SECTION
# -------------------------------------------------------------
st.title("🎬 Nova AI Video Generator")
st.caption(
    "Turn product names or descriptions into high-converting 4K AI Video Ads instantly."
)

# -------------------------------------------------------------
# 4. CHAT HISTORY INITIALIZATION
# -------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi! Main Nova AI hoon. Apne product ka naam ya ad concept batao (e.g., 'Luxury black smartwatch with glowing neon display'), main 4K Video Ad generate karke dunga!",
        }
    ]

# Render past chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if "video_url" in msg:
            st.write(msg["content"])
            st.video(msg["video_url"])
        else:
            st.write(msg["content"])

# -------------------------------------------------------------
# 5. USER CHAT INPUT & VIDEO GENERATION
# -------------------------------------------------------------
user_prompt = st.chat_input(
    "Describe your product or video ad (e.g., Wireless Earbuds on water splash)..."
)

if user_prompt:
    # Append User Message
    st.session_state.messages.append(
        {"role": "user", "content": user_prompt}
    )
    with st.chat_message("user"):
        st.write(user_prompt)

    # Process AI Video Response
    with st.chat_message("assistant"):
        with st.spinner(
            "⏳ Cloud AI Engine video render kar raha hai... (takes 30-40 seconds)"
        ):
            try:
                # Call MiniMax / Luma AI Video API
                output = replicate.run(
                    "minimax/video-01",
                    input={
                        "prompt": f"Commercial studio product video of {user_prompt}, 4k resolution, cinematic lighting, ultra realistic motion",
                        "prompt_optimizer": True,
                    },
                )
                video_url = str(output)

                success_text = f"✅ Aapki AI Video Ad tayar hai for: **{user_prompt}**"
                st.write(success_text)
                st.video(video_url)

                # Save to session history
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": success_text,
                        "video_url": video_url,
                    }
                )

            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append(
                    {"role": "assistant", "content": error_msg}
                )

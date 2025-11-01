import streamlit as st
import time
import base64

# Page configuration
st.set_page_config(
    page_title="WhatsApp Message Sender",
    page_icon="📱",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #25D366;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-message {
        padding: 1rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.5rem;
        color: #155724;
    }
    .warning-message {
        padding: 1rem;
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 0.5rem;
        color: #856404;
    }
    .info-message {
        padding: 1rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 0.5rem;
        color: #0c5460;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<h1 class="main-header">📱 WhatsApp Message Sender</h1>', unsafe_allow_html=True)

# Sidebar for instructions
with st.sidebar:
    st.header("ℹ️ Instructions")
    st.markdown("""
    1. **Fill in all fields** in the main form
    2. **Click 'Generate Instructions'**
    3. **Follow the step-by-step guide**
    4. **Run the provided Python script on your computer**
    
    **⚠️ Important:**
    - Use responsibly
    - Respect privacy
    - Avoid spam
    - Requires Python on your local machine
    """)

# Main form
with st.form("whatsapp_form"):
    st.markdown('<h3>Message Details</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        your_number = st.text_input(
            "**Your WhatsApp Number** 📞",
            placeholder="+919059170516",
            help="Your WhatsApp number with country code"
        )
        
        num_times = st.number_input(
            "**Number of Messages** 🔢",
            min_value=1,
            max_value=100,
            value=10,
            help="How many messages to send (max 100 for safety)"
        )
    
    with col2:
        recipient_number = st.text_input(
            "**Recipient's Number** 👥",
            placeholder="+919059170516", 
            help="Recipient's WhatsApp number with country code"
        )
        
        delay = st.slider(
            "**Delay between messages (seconds)** ⏱️",
            min_value=0.5,
            max_value=5.0,
            value=1.0,
            help="Delay between each message"
        )
    
    message = st.text_area(
        "**Message Content** 💬",
        value="Hello! This is an automated message.",
        height=100,
        help="The message that will be sent repeatedly"
    )
    
    submit_button = st.form_submit_button("🚀 Generate Instructions & Code")

if submit_button:
    if not all([your_number, recipient_number, message]):
        st.error("🚫 Please fill in all required fields!")
    else:
        # Validation
        if not your_number.startswith('+'):
            st.error("🚫 Please include country code in your number (e.g., +91)")
        elif not recipient_number.startswith('+'):
            st.error("🚫 Please include country code in recipient's number (e.g., +91)")
        else:
            # Generate Python script
            python_script = f'''import pyautogui
import webbrowser
import time

# WhatsApp configuration
phone_number = "{recipient_number}"
message = "{message}"
num_messages = {num_times}
delay_between_messages = {delay}

print("🚀 Starting WhatsApp Message Sender...")
print(f"📱 Sending {{num_messages}} messages to {{phone_number}}")
print(f"💬 Message: {{message}}")
print(f"⏱️ Delay: {{delay_between_messages}} seconds")

# Open WhatsApp Web
print("🌐 Opening WhatsApp Web...")
webbrowser.open(f"https://web.whatsapp.com/send?phone={{phone_number}}")

print("⏳ Waiting 15 seconds for WhatsApp to load...")
print("⚠️ Please ensure WhatsApp Web is logged in and don't touch your keyboard/mouse!")
time.sleep(15)

print("📤 Starting to send messages...")
# Send messages
for i in range(num_messages):
    pyautogui.typewrite(message)
    pyautogui.press("enter")
    time.sleep(delay_between_messages)
    print(f"✅ Sent message {{i+1}}/{{num_messages}}")

print("🎉 All messages sent successfully!")
'''

            # Display instructions
            st.markdown('<div class="info-message">📋 Follow these steps to send messages:</div>', unsafe_allow_html=True)
            
            st.markdown("""
            ### Step-by-Step Guide:

            1. **Copy the Python code below**
            2. **Save it as a `.py` file on your computer** (e.g., `whatsapp_sender.py`)
            3. **Install required packages** (if not already installed):
               ```bash
               pip install pyautogui
               ```
            4. **Run the script**:
               ```bash
               python whatsapp_sender.py
               ```
            5. **Follow the on-screen instructions**
            """)

            # Display the code
            st.subheader("📜 Python Script:")
            st.code(python_script, language='python')
            
            # Download button
            st.download_button(
                label="📥 Download Python Script",
                data=python_script,
                file_name="whatsapp_sender.py",
                mime="text/python"
            )
            
            # Important warnings
            st.markdown('<div class="warning-message">⚠️ IMPORTANT WARNINGS:</div>', unsafe_allow_html=True)
            st.markdown("""
            - **Keep the browser window visible** during execution
            - **Don't touch keyboard/mouse** while script is running
            - **Ensure WhatsApp Web is already logged in**
            - **Use responsibly and respect privacy**
            - **Test with 1-2 messages first** to verify it works
            """)


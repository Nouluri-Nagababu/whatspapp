import streamlit as st
import pyautogui
import webbrowser
import time
import threading
import os

# Page configuration
st.set_page_config(
    page_title="WhatsApp Message Sender",
    page_icon="📱",
    layout="centered"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #25D366;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        color: #128C7E;
        margin-top: 2rem;
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
    .stButton button {
        width: 100%;
        background-color: #25D366;
        color: white;
        font-weight: bold;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
    }
    .stButton button:hover {
        background-color: #128C7E;
        color: white;
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
    2. **Ensure WhatsApp Web is logged in** in your browser
    3. **Click 'Start Sending Messages'**
    4. **Don't touch keyboard/mouse** during sending
    5. **Keep browser window visible**
    
    **⚠️ Important:**
    - Use responsibly
    - Respect privacy
    - Avoid spam
    - Stable internet required
    """)

# Main form
with st.form("whatsapp_form"):
    st.markdown('<h3 class="sub-header">Message Details</h3>', unsafe_allow_html=True)
    
    # Create two columns for better layout
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
            max_value=500,
            value=10,
            help="How many messages to send (max 500 for safety)"
        )
    
    with col2:
        recipient_number = st.text_input(
            "**Recipient's Number** 👥",
            placeholder="+919059170516", 
            help="Recipient's WhatsApp number with country code"
        )
        
        delay = st.slider(
            "**Delay between messages (seconds)** ⏱️",
            min_value=0.1,
            max_value=2.0,
            value=0.5,
            help="Delay between each message"
        )
    
    message = st.text_area(
        "**Message Content** 💬",
        value="Hello! This is an automated message.",
        height=100,
        help="The message that will be sent repeatedly"
    )
    
    # Advanced options
    with st.expander("Advanced Options"):
        load_time = st.slider(
            "WhatsApp Web loading time (seconds)",
            min_value=5,
            max_value=30,
            value=15,
            help="Time to wait for WhatsApp Web to load"
        )
        
        browser_choice = st.selectbox(
            "Browser preference",
            ["Default Browser", "Chrome", "Firefox", "Safari"],
            help="Choose your preferred browser"
        )
    
    # Submit button
    submit_button = st.form_submit_button("🚀 Start Sending Messages")

# Message sending function
def send_whatsapp_messages(recipient, msg, count, delay_time, load_time):
    """Function to send WhatsApp messages"""
    try:
        # Show status
        st.session_state['sending'] = True
        st.session_state['progress'] = 0
        
        # Open WhatsApp Web
        webbrowser.open(f"https://web.whatsapp.com/send?phone={recipient}")
        
        # Wait for WhatsApp to load
        time.sleep(load_time)
        
        # Send messages with progress tracking
        for i in range(count):
            if not st.session_state.get('sending', True):
                break
                
            pyautogui.typewrite(msg)
            pyautogui.press("enter")
            time.sleep(delay_time)
            
            # Update progress
            progress = (i + 1) / count
            st.session_state['progress'] = progress
            
        st.session_state['sending'] = False
        return True, f"✅ Successfully sent {count} messages!"
        
    except Exception as e:
        st.session_state['sending'] = False
        return False, f"❌ Error: {str(e)}"

# Initialize session state
if 'sending' not in st.session_state:
    st.session_state.sending = False
if 'progress' not in st.session_state:
    st.session_state.progress = 0

# Handle form submission
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
            # Show warnings
            st.markdown('<div class="warning-message">⚠️ Please don\'t touch your keyboard or mouse while messages are being sent!</div>', unsafe_allow_html=True)
            st.markdown('<div class="info-message">📱 Make sure WhatsApp Web is open and logged in on your default browser.</div>', unsafe_allow_html=True)
            
            # Create columns for progress and stop button
            col1, col2 = st.columns([3, 1])
            
            with col1:
                progress_bar = st.progress(st.session_state.progress)
                status_text = st.empty()
            
            with col2:
                stop_button = st.button("🛑 Stop", key="stop")
                if stop_button:
                    st.session_state.sending = False
                    st.warning("Stopping message sending...")
            
            # Run in a separate thread
            def run_messages():
                success, result = send_whatsapp_messages(
                    recipient_number, 
                    message, 
                    num_times, 
                    delay,
                    load_time
                )
                
                if success:
                    st.balloons()
                    st.markdown(f'<div class="success-message">{result}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="warning-message">{result}</div>', unsafe_allow_html=True)
            
            # Start the process
            thread = threading.Thread(target=run_messages)
            thread.daemon = True
            thread.start()
            
            # Progress updater
            while st.session_state.sending and st.session_state.progress < 1.0:
                progress_bar.progress(st.session_state.progress)
                status_text.text(f"Progress: {int(st.session_state.progress * 100)}%")
                time.sleep(0.1)

# Footer
st.markdown("---")
st.markdown("""
### 📋 Usage Tips:
- **Test with 1-2 messages** first to ensure it works
- **Use appropriate delays** to avoid being flagged as spam
- **Keep the browser window active** and don't minimize it
- **Ensure good internet connection** throughout the process

### 🔒 Privacy & Safety:
- Only send messages to people who have consented
- Don't use for spam or harassment
- Respect WhatsApp's terms of service
- Use responsibly and ethically
""")

# Add some space at the bottom
st.markdown("<br><br>", unsafe_allow_html=True)
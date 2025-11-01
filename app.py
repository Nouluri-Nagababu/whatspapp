import streamlit as st
import urllib.parse

st.set_page_config(
    page_title="WhatsApp Message Sender",
    page_icon="📱",
    layout="centered"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #25D366;
        text-align: center;
        margin-bottom: 2rem;
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
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">📱 Direct WhatsApp Message Sender</h1>', unsafe_allow_html=True)

with st.form("message_form"):
    st.subheader("Send Message Directly")
    
    phone_number = st.text_input(
        "**Recipient's WhatsApp Number**",
        placeholder="919059170516",
        help="Enter phone number with country code (without +)"
    )
    
    message = st.text_area(
        "**Message**",
        value="Hello!",
        height=100
    )
    
    submit = st.form_submit_button("📤 Send WhatsApp Message")

if submit:
    if phone_number and message:
        # URL encode the message
        encoded_message = urllib.parse.quote(message)
        
        # Create WhatsApp direct link
        whatsapp_url = f"https://web.whatsapp.com/send?phone={phone_number}&text={encoded_message}"
        
        st.success("✅ Click the button below to open WhatsApp and send your message!")
        
        # Display direct link
        st.markdown(f"""
        ### Ready to Send!
        
        **Number:** {phone_number}  
        **Message:** {message}
        
        Click the button below to open WhatsApp Web:
        """)
        
        st.markdown(f'<a href="{whatsapp_url}" target="_blank"><button style="background-color:#25D366; color:white; padding:10px 20px; border:none; border-radius:5px; font-size:16px;">📱 Open WhatsApp to Send</button></a>', unsafe_allow_html=True)
        
        # Alternative: API-based approach (theoretical)
        st.info("💡 **Tip:** Make sure you're logged into WhatsApp Web in your browser!")
        
    else:
        st.error("Please enter both phone number and message")

# Multiple Messages Section
st.markdown("---")
st.subheader("Send Multiple Messages")

with st.form("multiple_messages"):
    phone_number2 = st.text_input(
        "Recipient's Number for Multiple Messages",
        placeholder="919059170516"
    )
    
    message2 = st.text_area(
        "Message to Repeat",
        value="Hello!"
    )
    
    repeat_count = st.slider("Number of times to send", 1, 50, 5)
    
    submit_multiple = st.form_submit_button("🔄 Generate Multiple Message Links")

if submit_multiple:
    if phone_number2 and message2:
        encoded_message = urllib.parse.quote(message2)
        
        st.success(f"Generated {repeat_count} message links!")
        
        for i in range(repeat_count):
            whatsapp_url = f"https://web.whatsapp.com/send?phone={phone_number2}&text={encoded_message}"
            st.markdown(f'**Message {i+1}:** <a href="{whatsapp_url}" target="_blank">Click to Send</a>', unsafe_allow_html=True)

# Instructions
st.markdown("---")
st.subheader("📋 How to Use:")
st.markdown("""
1. **Enter the recipient's phone number** (with country code, without +)
2. **Type your message**
3. **Click "Send WhatsApp Message"**
4. **Click the generated link** to open WhatsApp Web
5. **Press Enter** in WhatsApp to send the message

**For multiple messages:**
- Click each generated link one by one
- Or use the automated method below
""")

# Browser Automation Alternative
st.markdown("---")
st.subheader("🔄 Automated Sending (Local Computer)")

st.info("""
For fully automated sending without manual clicking, you'll need to run this on your local computer. 
The web version can't control your browser automatically due to security restrictions.
""")

local_code = '''
import pyautogui
import webbrowser
import time
import urllib.parse

def send_whatsapp_message(phone, message, count=1, delay=1):
    encoded_msg = urllib.parse.quote(message)
    
    for i in range(count):
        webbrowser.open(f"https://web.whatsapp.com/send?phone={phone}&text={encoded_msg}")
        time.sleep(10)  # Wait for WhatsApp to load
        pyautogui.press('enter')  # Send message
        time.sleep(delay)
        print(f"Sent message {i+1}/{count}")

# Usage
send_whatsapp_message("919059170516", "Hello!", count=5, delay=2)
'''

st.code(local_code, language='python')
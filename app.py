import streamlit as st
import urllib.parse
import base64

st.set_page_config(page_title="WhatsApp Auto-Sender", page_icon="📱")

st.markdown("""
<style>
    .auto-button {
        background-color: #25D366 !important;
        color: white !important;
        font-size: 18px !important;
        padding: 15px !important;
        border-radius: 10px !important;
        margin: 10px 0px !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("🤖 WhatsApp Auto-Sender")
st.warning("⚠️ Due to security restrictions, full automation requires user interaction")

# Main form
col1, col2 = st.columns(2)

with col1:
    phone = st.text_input("📞 Phone Number", "919059170516", help="With country code, no +")
    count = st.slider("🔄 Number of Messages", 1, 20, 5)

with col2:
    message = st.text_area("💬 Message", "Hello! This message was sent automatically.")
    delay = st.slider("⏱️ Delay between sends (seconds)", 1, 10, 2)

if st.button("🚀 Generate Auto-Links", type="primary"):
    if phone and message:
        encoded_msg = urllib.parse.quote(message)
        
        st.success("✅ Auto-links generated! Follow these steps:")
        
        # Generate multiple links
        for i in range(count):
            whatsapp_url = f"https://api.whatsapp.com/send?phone={phone}&text={encoded_msg}"
            
            st.markdown(f"""
            **Message {i+1}:**
            """)
            
            # Create clickable button that opens WhatsApp
            button_html = f'''
            <a href="{whatsapp_url}" target="_blank" style="text-decoration: none;">
                <button class="auto-button">
                    📱 Tap to Send Message {i+1}
                </button>
            </a>
            '''
            st.components.v1.html(button_html, height=80)
            
            if i < count - 1:
                st.info(f"⏳ Wait {delay} seconds before next message")
        
        # Alternative: Bookmarklet method
        st.markdown("---")
        st.subheader("🔧 Advanced: One-Click Method")
        
        bookmarklet_code = f'''
        javascript:(function(){{
            var phone = "{phone}";
            var message = "{message}";
            var count = {count};
            var delay = {delay} * 1000;
            
            function sendMessage(i) {{
                if (i >= count) return;
                
                var url = "https://api.whatsapp.com/send?phone=" + phone + "&text=" + encodeURIComponent(message);
                window.open(url, "_blank");
                
                setTimeout(function() {{
                    sendMessage(i + 1);
                }}, delay + 2000);
            }}
            
            sendMessage(0);
        }})()
        '''
        
        st.code(bookmarklet_code, language='javascript')
        st.info("💡 Save this as a bookmarklet and click it to auto-open all messages!")

# Mobile-specific instructions
st.markdown("---")
st.subheader("📱 Mobile Instructions")

st.markdown("""
**For best results on mobile:**

1. **Save the generated links** as bookmarks
2. **Tap each link one by one**
3. **WhatsApp will open** with your message pre-filled
4. **Tap the send button** ↗️
5. **Return to this app** for the next message

**Pro Tip:** Use two devices - one to view this app, another to send messages!
""")

# Disclaimer
st.markdown("---")
st.error("""
**Important Limitations:**
- Full automation is not possible due to security restrictions
- User must manually tap 'Send' in WhatsApp
- This tool is for legitimate use only
- Respect WhatsApp's terms of service
- Don't spam or harass users
""")
import streamlit as st
from openai import OpenAI
import time

client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY", ""))

st.set_page_config(page_title="AI Cold Email Generator", page_icon="📧")

st.title("📧 AI Cold Email Generator Pro")
st.markdown("*Generate personalized cold emails that actually get responses*")

# Sidebar для настроек
with st.sidebar:
    st.header("⚙️ Settings")
    
    your_name = st.text_input("Your Name:", placeholder="John Smith")
    your_company = st.text_input("Your Company:", placeholder="GrowthLabs")
    your_email = st.text_input("Your Email:", placeholder="john@growthlabs.com")
    
    st.divider()
    
    email_style = st.selectbox(
        "Email Style:",
        ["Professional & Friendly", "Formal & Corporate", "Casual & Direct", "Value-Focused"]
    )
    
    email_length = st.select_slider(
        "Length:",
        options=["Short (100 words)", "Medium (150 words)", "Long (200 words)"]
    )

# Main form
st.subheader("🎯 Target Information")

col1, col2 = st.columns(2)

with col1:
    company_name = st.text_input("Company Name:", placeholder="Tesla")
    
with col2:
    recipient_name = st.text_input("Recipient Name:", placeholder="Elon")

your_service = st.text_area(
    "What you offer (be specific):", 
    placeholder="AI automation for customer support that reduces response time by 80%",
    height=100
)

# Generate button
if st.button("✨ Generate Email", type="primary", use_container_width=True):
    
    if not all([company_name, recipient_name, your_service]):
        st.error("⚠️ Please fill in all target information fields")
    else:
        with st.spinner("🤖 AI is crafting your email..."):
            
            # Формируем промпт в зависимости от настроек
            style_instructions = {
                "Professional & Friendly": "friendly but professional tone, warm opening",
                "Formal & Corporate": "formal corporate language, very professional",
                "Casual & Direct": "casual conversational tone, get to the point quickly",
                "Value-Focused": "focus heavily on ROI and concrete benefits"
            }
            
            length_map = {
                "Short (100 words)": "100",
                "Medium (150 words)": "150", 
                "Long (200 words)": "200"
            }
            
            prompt = f"""
Create a highly personalized cold email for B2B sales.

TARGET:
- Recipient: {recipient_name}
- Company: {company_name}
- Our service: {your_service}

SENDER:
- Name: {your_name if your_name else "[Your Name]"}
- Company: {your_company if your_company else "[Your Company]"}
- Email: {your_email if your_email else "[your@email.com]"}

STYLE: {style_instructions[email_style]}
LENGTH: Maximum {length_map[email_length]} words

REQUIREMENTS:
1. Compelling subject line (separate line at top)
2. Research-based personalization about {company_name}
3. Clear value proposition
4. Strong call-to-action
5. Professional signature

Output format:
Subject: [subject line]

[email body]

Best regards,
{your_name if your_name else "[Your Name]"}
{your_company if your_company else "[Your Company]"}
{your_email if your_email else "[your@email.com]"}
"""
            
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.8
                )
                
                result = response.choices[0].message.content
                
                # Показываем результат
                st.success("✅ Email generated successfully!")
                
                st.subheader("📨 Your Email:")
                st.text_area("", result, height=400, label_visibility="collapsed")
                
                # Кнопка копирования
                st.code(result, language=None)
                
                # Дополнительные опции
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("🔄 Generate Another Version"):
                        st.rerun()
                        
                with col2:
                    st.download_button(
                        "💾 Download as .txt",
                        result,
                        file_name=f"email_{company_name.lower()}.txt",
                        mime="text/plain"
                    )
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Footer
st.divider()
st.markdown("*💡 Tip: The more specific your service description, the better the personalization*")
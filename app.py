import streamlit as st
import anthropic
import os

st.set_page_config(
    page_title="Security Vulnerability Scanner",
    page_icon="🔒",
    layout="wide"
)

st.title("🔒 Security Vulnerability Scanner")
st.subheader("Powered by Claude API | Detect code vulnerabilities in seconds")

api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    st.error("API key not configured.")
else:
    code_input = st.text_area(
        "Paste your code here",
        height=300,
        placeholder="Paste Python, JavaScript, Java, or any code...",
    )
    
    if st.button("🔍 Scan for Vulnerabilities", type="primary", use_container_width=True):
        if not code_input:
            st.error("Please paste code to scan.")
        else:
            with st.spinner("Claude is analyzing your code..."):
                try:
                    client = anthropic.Anthropic(api_key=api_key)
                    
                    prompt = f"""You are a cybersecurity expert. Analyze this code for security vulnerabilities.

CODE:
{code_input}

Provide analysis in this format:

## Vulnerabilities Found
[List each vulnerability as a separate item]

For each vulnerability:
- Type: [SQL Injection, XSS, Hardcoded Credentials, etc.]
- Severity: [CRITICAL/HIGH/MEDIUM/LOW]
- Line: [approximate line number]
- Issue: [Explanation of the vulnerability]
- Fix: [How to fix it]

## Overall Risk Score
[0-100]

## Recommendations
[Top 3 security improvements for this code]

Be specific and technical."""

                    message = client.messages.create(
                        model="claude-sonnet-4-5",
                        max_tokens=2000,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    
                    st.markdown("---")
                    st.markdown(message.content[0].text)
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
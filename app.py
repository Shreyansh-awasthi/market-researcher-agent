import sys
import subprocess
import streamlit as st
import base64

st.set_page_config(
    page_title="VeloQuant AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background: radial-gradient(circle at 50% -20%, #0f172a 0%, #020617 80%) !important;
        color: #f8fafc !important;
    }
    
    .stTextInput > div > div > input {
        background-color: rgba(15, 23, 42, 0.6) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        padding: 16px 20px !important;
        font-size: 16px !important;
        backdrop-filter: blur(12px) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.3) !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.2), inset 0 2px 4px rgba(0, 0, 0, 0.2) !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        padding: 16px 32px !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        width: 100% !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 24px rgba(37, 99, 235, 0.4) !important;
        border-color: rgba(255, 255, 255, 0.2) !important;
    }
    
    .header-panel {
        text-align: center;
        padding: 60px 0 40px 0;
        margin-bottom: 30px;
    }
    
    .brand-title {
        font-size: 56px !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #ffffff 30%, #94a3b8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 14px;
        letter-spacing: -0.06em;
    }
    
    .brand-subtitle {
        color: #64748b !important;
        font-size: 19px !important;
        font-weight: 500;
        letter-spacing: -0.02em;
        max-width: 600px;
        margin: 0 auto;
    }
    
    .report-card {
        background: rgba(15, 23, 42, 0.4) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 24px !important;
        padding: 40px !important;
        margin-top: 35px !important;
        backdrop-filter: blur(20px) !important;
        box-shadow: 0 30px 60px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
    }
    
    .query-badge {
        background: linear-gradient(90deg, rgba(37, 99, 235, 0.15), rgba(29, 78, 216, 0.05)) !important;
        color: #3b82f6 !important;
        padding: 8px 18px !important;
        border-radius: 100px !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        border: 1px solid rgba(37, 99, 235, 0.25) !important;
        display: inline-block !important;
        margin-bottom: 25px !important;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }
    
    .pdf-btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: rgba(30, 41, 59, 0.5) !important;
        color: #f8fafc !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        padding: 12px 24px;
        font-size: 14px;
        font-weight: 600;
        border-radius: 12px;
        text-decoration: none;
        transition: all 0.2s ease;
        margin-top: 25px;
        backdrop-filter: blur(8px);
    }
    
    .pdf-btn:hover {
        background: rgba(51, 65, 85, 0.8) !important;
        border-color: rgba(255, 255, 255, 0.15) !important;
        color: #ffffff !important;
        transform: translateY(-1px);
    }
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #ffffff !important;
        font-weight: 700 !important;
        letter-spacing: -0.04em !important;
        margin-top: 30px !important;
        background: linear-gradient(to right, #ffffff, #cbd5e1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .stMarkdown li {
        color: #cbd5e1 !important;
        font-size: 16px !important;
        line-height: 1.8 !important;
        margin-bottom: 12px !important;
    }
    
    .stMarkdown strong {
        color: #60a5fa !important;
        font-weight: 600;
    }
    
    div[data-testid="stExpander"] {
        background: rgba(15, 23, 42, 0.2) !important;
        border: 1px solid rgba(255, 255, 255, 0.04) !important;
        border-radius: 16px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
    }
    
    .clear-btn > button {
        background: transparent !important;
        color: #64748b !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 12px !important;
        padding: 8px 16px !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
        width: auto !important;
        float: right;
    }
    
    .clear-btn > button:hover {
        color: #ef4444 !important;
        border-color: rgba(239, 68, 68, 0.2) !important;
        background: rgba(239, 68, 68, 0.05) !important;
    }
    </style>
""", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []

st.markdown("""
    <div class="header-panel">
        <div class="brand-title">VeloQuant AI Engine</div>
        <div class="brand-subtitle">High-speed dual-brain network synthesis for deep competitor cross-examinations and market vectors</div>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([5, 1])

with col1:
    user_query = st.text_input(
        label="Search Query",
        label_visibility="collapsed",
        placeholder="Compare valuation of openai and anthropic in deep..."
    )

with col2:
    submit_button = st.button("Analyze Engine")

def build_pdf_data(text_content, query_title):
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
        import io

        pdf_buffer = io.BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=letter, rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54, title="AlphaRoute Intelligence Data")
        styles = getSampleStyleSheet()
        
        custom_title = ParagraphStyle(
            'PDFTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=22,
            leading=26,
            textColor=colors.HexColor('#0f172a'),
            spaceAfter=15
        )
        
        custom_body = ParagraphStyle(
            'PDFBody',
            parent=styles['BodyText'],
            fontName='Helvetica',
            fontSize=10.5,
            leading=16,
            textColor=colors.HexColor('#334155'),
            spaceAfter=8
        )
        
        story = []
        story.append(Paragraph(f"AlphaRoute Intelligence Target Analysis: {query_title}", custom_title))
        story.append(Spacer(1, 15))
        
        paragraphs = text_content.split('\n')
        for p in paragraphs:
            if p.strip():
                clean_p = p.replace('•', '').replace('*', '').strip()
                story.append(Paragraph(clean_p, custom_body))
                
        doc.build(story)
        pdf_data = pdf_buffer.getvalue()
        pdf_buffer.close()
        return pdf_data
    except Exception:
        return None

if submit_button and user_query:
    with st.spinner("Executing asymmetric micro-routing and pipeline compilation..."):
        try:
            process = subprocess.Popen(
                [sys.executable, "market_research.py"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8'
            )
            
            stdout, stderr = process.communicate(input=f"{user_query}\nexit\n", timeout=180)
            
            if "Assistant Output Begin" in stdout:
                raw_report = stdout.split("Assistant Output Begin")[-1].split("Assistant Output End")[0].strip()
            else:
                raw_report = stdout.strip()

            clean_lines = []
            for line in raw_report.split("\n"):
                line_stripped = line.strip()
                if not line_stripped:
                    continue
                if any(x in line_stripped for x in ["[Fast Router]", "Route Match:", "Executing native", "[System Notice]", "Response ("]):
                    continue
                if line_stripped.startswith("│"):
                    line_stripped = line_stripped.lstrip("│").rstrip("│").strip()
                if any(c in line_stripped for c in ["┌", "└", "─", "━", "┏", "┗", "┃"]):
                    continue
                clean_lines.append(line_stripped)
            
            final_report = "\n".join(clean_lines).strip()

            if final_report:
                st.session_state.history.append({
                    "query": user_query,
                    "report": final_report                })
            else:
                if stderr:
                    st.error(f"Pipeline Execution Error: {stderr}")
                else:
                    st.warning("The analysis returned an empty response. Verify your API keys.")

        except subprocess.TimeoutExpired:
            process.kill()
            st.error("The background data pipeline timed out while fetching live market assets.")
        except Exception as e:
            st.error(f"Failed to connect to backend script: {str(e)}")

if st.session_state.history:
    st.markdown("<br>", unsafe_allow_html=True)
    h_col1, h_col2 = st.columns([5, 1])
    
    with h_col1:
        st.markdown("<h3 style='margin: 0;'>Intelligence Reports</h3>", unsafe_allow_html=True)
    with h_col2:
        st.markdown('<div class="clear-btn">', unsafe_allow_html=True)
        if st.button("Clear Audits"):
            st.session_state.history = []
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    for idx, item in enumerate(reversed(st.session_state.history)):
        if idx == 0:
            st.markdown(f"""
                <div class="report-card">
                    <div class="query-badge">Target System Vector: {item['query']}</div>
            """, unsafe_allow_html=True)
            st.markdown(item['report'])
            
            pdf_bytes = build_pdf_data(item['report'], item['query'])
            if pdf_bytes:
                b64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
                pdf_href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="Report_{item["query"].replace(" ", "_")}.pdf" class="pdf-btn">📥 Export Audit Sheet (PDF)</a>'
                st.markdown(pdf_href, unsafe_allow_html=True)
            st.markdown("</div><br>", unsafe_allow_html=True)
        else:
            with st.expander(f"Historical Audit Block: {item['query']}", expanded=False):
                st.markdown(item['report'])

                              
import html
import json

import streamlit as st

from market_research import (
    high_speed_router,
    intelligence_unit,
    fallback_unit,
    yfinance_toolkit,
    duckduckgo_toolkit,
)

st.set_page_config(page_title="Market Desk", page_icon="📈", layout="centered")

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@400;500;700&display=swap');

html, body, [class*="st-"], .stApp {
    font-family: "Schibsted Grotesk", system-ui, -apple-system, "Segoe UI", sans-serif;
}
#MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden; height: 0; }
.block-container { max-width: 760px; padding-top: 1.5rem; padding-bottom: 6rem; }

.desk-header { padding-bottom: 14px; margin-bottom: 18px; border-bottom: 1px solid rgba(128,138,150,.3); }
.desk-header h1 { font-size: 1.35rem; font-weight: 700; letter-spacing: -.01em; margin: 0; padding: 0; }
.desk-header p { margin: 2px 0 0; opacity: .65; font-size: .92rem; }

.empty-state h2 { font-size: 1.55rem; font-weight: 700; letter-spacing: -.02em; margin: 24px 0 8px; }
.empty-state p { opacity: .7; line-height: 1.5; max-width: 480px; margin: 0 0 14px; }

.meta { display: flex; gap: 8px; margin-bottom: 6px; font-size: .78rem; }
.tag { border: 1px solid rgba(128,138,150,.45); border-radius: 6px; padding: 1px 8px; opacity: .85; }
.tag.warn { color: #c47a14; border-color: #c47a14; opacity: 1; }

[data-testid="stChatMessage"] {
    border: 1px solid rgba(128,138,150,.25);
    border-radius: 6px 16px 16px 16px;
    padding: 14px 16px;
    margin-bottom: 14px;
}
[data-testid="stChatMessage"] p { line-height: 1.55; }
[data-testid="stChatMessage"] a { word-break: break-all; }

div[data-testid="stButton"] > button {
    border-radius: 999px;
    border: 1px solid rgba(128,138,150,.4);
    padding: 6px 14px;
    font-size: .9rem;
    width: 100%;
}
div[data-testid="stButton"] > button:hover { border-color: #2a4fa8; color: #2a4fa8; }
</style>
""",
    unsafe_allow_html=True,
)

INTENT_LABELS = {
    "stock_analysis": "Stock analysis",
    "web_news": "Web news",
    "conversational": "Chat",
}

EXAMPLES = ["NVDA", "TCS stock", "Latest OpenAI news", "SpaceX investment outlook"]


def get_tool(toolkit, name):
    return next(t for t in toolkit.tools if t.__name__ == name)


def route(query):
    meta = {"intent": "conversational", "cleaned_query": query, "requires_web": False}
    try:
        raw = high_speed_router.run(query).content.strip()
        if raw.startswith("```"):
            raw = raw.split("```json")[-1].replace("```", "").strip()
        meta.update(json.loads(raw))
    except Exception:
        pass
    return meta


def run_pipeline(query):
    meta = route(query)
    intent = meta.get("intent", "conversational")
    cleaned = str(meta.get("cleaned_query", query)).strip()
    context = ""

    if intent == "stock_analysis":
        try:
            context = (
                f"Stock Ticker Data for {cleaned}:\n"
                f"Price: {get_tool(yfinance_toolkit, 'get_stock_price')(cleaned)}\n"
                f"Recommendations: {get_tool(yfinance_toolkit, 'get_analyst_recommendations')(cleaned)}\n"
                f"Info: {get_tool(yfinance_toolkit, 'get_company_info')(cleaned)}"
            )
        except Exception as e:
            context = f"Failed to acquire stock data: {e}"
            intent = "web_news"

    q = query.lower()
    if intent == "web_news" or meta.get("requires_web") or any(k in q for k in ("openai", "spacex", "tcs")):
        try:
            results = get_tool(duckduckgo_toolkit, "duckduckgo_search")(f"{cleaned} investment overview")
            context += f"\n\nLive Web News Context:\n{results}"
        except Exception as e:
            context += f"\nSearch execution dropped out: {e}"

    prompt = f"User Request: {query}\nFetched Background Context:\n{context}"
    try:
        return {"intent": intent, "ticker": cleaned, "engine": "primary",
                "answer": intelligence_unit.run(prompt).content}
    except Exception:
        try:
            return {"intent": intent, "ticker": cleaned, "engine": "backup",
                    "answer": fallback_unit.run(prompt).content}
        except Exception as e:
            return {"intent": intent, "ticker": cleaned, "engine": "none",
                    "answer": f"Both models failed: {e}"}


def meta_html(item):
    label = html.escape(INTENT_LABELS.get(item["intent"], item["intent"]))
    out = f'<div class="meta"><span class="tag">{label}</span>'
    if item["intent"] != "conversational" and item.get("ticker"):
        out += f'<span class="tag">{html.escape(item["ticker"])}</span>'
    if item["engine"] == "backup":
        out += '<span class="tag warn">Backup model</span>'
    return out + "</div>"


def queue_example(text):
    st.session_state.queued = text


if "history" not in st.session_state:
    st.session_state.history = []

st.markdown(
    """
<div class="desk-header">
  <h1>Market Desk</h1>
  <p>Ask about a stock or a company's latest news.</p>
</div>
""",
    unsafe_allow_html=True,
)

if not st.session_state.history:
    st.markdown(
        """
<div class="empty-state">
  <h2>What do you want to look into?</h2>
  <p>Enter a ticker for price, analyst ratings and company info, or name a company for recent news.</p>
</div>
""",
        unsafe_allow_html=True,
    )
    cols = st.columns(len(EXAMPLES))
    for col, text in zip(cols, EXAMPLES):
        col.button(text, key=f"ex_{text}", on_click=queue_example, args=(text,))

for item in st.session_state.history:
    if item["role"] == "user":
        with st.chat_message("user"):
            st.markdown(item["content"])
    else:
        with st.chat_message("assistant"):
            st.markdown(meta_html(item), unsafe_allow_html=True)
            st.markdown(item["content"])

typed = st.chat_input("Try \"NVDA\" or \"latest SpaceX news\"")
prompt = typed or st.session_state.pop("queued", None)

if prompt:
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Pulling data and writing the summary..."):
            result = run_pipeline(prompt)
        st.markdown(meta_html(result), unsafe_allow_html=True)
        st.markdown(result["answer"])

    st.session_state.history.append({
        "role": "assistant",
        "content": result["answer"],
        "intent": result["intent"],
        "ticker": result["ticker"],
        "engine": result["engine"],
    })
    st.rerun()

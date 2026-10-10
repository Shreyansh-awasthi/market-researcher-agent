import asyncio
import os
import sys
import json
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.google import Gemini
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools

load_dotenv()

if not os.getenv("GOOGLE_API_KEY") or not os.getenv("GROQ_API_KEY"):
    sys.exit(1)

high_speed_router = Agent(
    name="High Speed Pre-Processor",
    model=Groq(id="qwen/qwen3.8-27b"),
    instructions=[
        "You are an elite real-time traffic classifier. Analyze the user query instantly.",
        "Your only job is to categorize the intent and isolate the core asset or ticker name if applicable.",
        "Output raw JSON format only with these exact keys: 'intent', 'cleaned_query', 'requires_web'. Do not wrap in markdown code blocks.",
        "Intent must be one of: 'stock_analysis', 'web_news', 'conversational'.",
        "Example Output: {\"intent\": \"stock_analysis\", \"cleaned_query\": \"NVDA\", \"requires_web\": false}"
    ],
)

intelligence_unit = Agent(
    name="Deep Synthesis Engine",
    model=Gemini(id="gemini-3.8-flash"),
    instructions=[
        "You are a master analytical system.",
        "You will be given raw tool extraction context. Condense it into clear metrics and updates.",
        "Be punchy and direct. Format output strictly with bullet points and bold highlights.",
        "If web data is provided, always surface source URLs."
    ],
    markdown=True,
)

fallback_unit = Agent(
    name="Backup Synthesis Engine",
    model=Groq(id="qwen/qwen3.8-27b"),
    instructions=[
        "You are a master analytical system acting as a backup server.",
        "You will be given raw tool extraction context. Condense it into clear metrics and updates.",
        "Be punchy and direct. Format output strictly with bullet points and bold highlights."
    ],
    markdown=True,
)

yfinance_toolkit = YFinanceTools(
    enable_stock_price=True,
    enable_analyst_recommendations=True,
    enable_company_info=True
)
duckduckgo_toolkit = DuckDuckGoTools()

async def process_pipeline(user_query: str):
    meta = {"intent": "conversational", "cleaned_query": user_query, "requires_web": False}
    try:
        router_response = high_speed_router.run(user_query)
        raw_text = router_response.content.strip()
        if raw_text.startswith("```"):
            raw_text = raw_text.split("```json")[-1].split("```").strip()
        parsed_meta = json.loads(raw_text)
        meta.update(parsed_meta)
    except Exception:
        pass

    intent = meta.get("intent", "conversational")
    cleaned = meta.get("cleaned_query", user_query).strip()
    tool_context = ""

    if intent == "stock_analysis":
        try:
            tools_list = yfinance_toolkit.tools
            price_fn = next(t for t in tools_list if t.__name__ == "get_stock_price")
            recs_fn = next(t for t in tools_list if t.__name__ == "get_analyst_recommendations")
            info_fn = next(t for t in tools_list if t.__name__ == "get_company_info")
            
            price = price_fn(cleaned)
            recs = recs_fn(cleaned)
            info = info_fn(cleaned)
            tool_context = f"Stock Ticker Data for {cleaned}:\nPrice: {price}\nRecommendations: {recs}\nInfo: {info}"
        except Exception as e:
            tool_context = f"Failed to acquire stock data: {str(e)}"
            intent = "web_news"

    if intent == "web_news" or meta.get("requires_web", False) or "openai" in user_query.lower() or "spacex" in user_query.lower() or "tcs" in user_query.lower():
        try:
            tools_list = duckduckgo_toolkit.tools
            search_fn = next(t for t in tools_list if t.__name__ == "duckduckgo_search")
            search_results = search_fn(f"{cleaned} investment overview")
            tool_context += f"\n\nLive Web News Context:\n{search_results}"
        except Exception as e:
            tool_context += f"\nSearch execution dropped out: {str(e)}"

    print("Assistant Output Begin")
    final_prompt = f"User Request: {user_query}\nFetched Background Context:\n{tool_context}"
    
    try:
        response = intelligence_unit.run(final_prompt)
        print(response.content)
    except Exception:
        try:
            fallback_response = fallback_unit.run(final_prompt)
            print(fallback_response.content)
        except Exception as e:
            print(f"Synthesis completely unavailable: {str(e)}")
            
    print("Assistant Output End")

async def chat_loop():
    while True:
        try:
            user_query = input().strip()
            if not user_query:
                continue
            if user_query.lower() in ['exit', 'quit']:
                break
            await process_pipeline(user_query)
        except (KeyboardInterrupt, EOFError):
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')
    asyncio.run(chat_loop())

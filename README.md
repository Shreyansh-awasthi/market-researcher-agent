# VeloQuant AI Engine

VeloQuant AI is an enterprise-grade quantitative market intelligence platform powered by the Agno AI framework. Engineered to bypass standard multi-agent coordination delays, the system utilizes a high-speed parallel routing architecture that couples a sub-100ms Llama/Qwen pre-processor on Groq with a deep synthesis Gemini engine to deliver near-instant, tool-grounded financial analytics and competitor cross-examinations.

## System Architecture

- **High-Speed Classification Vector (Groq / Qwen 27B)**: Intercepts raw natural language prompts, strips conversational filler, and structure-maps query parameters into deterministic JSON records within milliseconds.
- **Direct Tool Execution Layer**: Bypasses the traditional LLM loop to execute background extraction toolkits (Yahoo Finance API and DuckDuckGo Indexes) as native Python functions, reducing latency by orders of magnitude.
- **Deep Synthesis Framework (Gemini 3.8 Flash)**: Consolidates multi-source background payloads into unified investment profiles. Operates with an integrated failure circuit that diverts tasks to a backup processing unit if high-demand server blocks occur.
- **Sovereign Dashboard Interface (Streamlit & Custom CSS)**: A low-latency web application featuring a responsive dark-themed grid, real-time historical logging, and an on-demand ReportLab PDF compilation module.

## Workspace Topography

```text
VeloQuant_AI/
│
├── app.py                  # Streamlit Web Core (HTML/CSS Interface & PDF Vector)
├── market_research.py      # Core Dual-Brain Data Pipeline (Agno Framework)
├── requirements.txt        # Production Dependencies Manifest
└── .env                    # Isolated Security Access Credentials
```

## Setup Specification

Ensure your local development machine runs Python 3.10 or higher. Configure your environmental layers exactly as specified below:

### 1. Environment Variable Configuration (`.env`)
Create a `.env` file in the root directory to store your API access records securely:

```env
GOOGLE_API_KEY=your_actual_gemini_api_key_here
GROQ_API_KEY=your_actual_groq_api_key_here
```

### 2. Dependency Manifest (`requirements.txt`)
Establish the foundational library state inside a `requirements.txt` file:

```text
agno
yfinance
duckduckgo-search
python-dotenv
streamlit
reportlab
pydantic
asyncio
```

## System Deployment

1. Initialize your terminal and navigate to the local workspace folder:
   ```bash
   cd C:\Users\ayush\OneDrive\Desktop\Market_Research_team
   ```

2. Establish an isolated Python virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the workspace sandbox environment:
   - **Windows PowerShell**: `.\venv\Scripts\Activate.ps1`
   - **Windows Command Prompt**: `.\venv\Scripts\activate.bat`
   - **macOS / Linux**: `source venv/bin/activate`

4. Upgrade the native package manager and install all system requirements concurrently:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

## Operating the Platform

Execute the system run command to launch the unified streaming dashboard:

```bash
streamlit run app.py
```

The system will verify the neural network routing tables and automatically launch a secure interface instance in your browser at `http://localhost:8505`.

## Operational Scope

- **Quantitative Stock Audits**: Parses unstructured text queries, standardizes international identifiers using dynamic ticker mapping algorithms (e.g., auto-resolving suffix protocols like `.NS`), and extracts current prices, moving averages, and consensus distributions.
- **Asymmetric Private Market Inquiries**: Detects non-public targets (e.g., OpenAI, SpaceX, Anthropic), reroutes execution trees away from traditional ticker endpoints, and scrapes web telemetry indexes for funding history and market valuation metrics.
- **Narrative Data Processing**: Normalizes tool stdout arrays, stripping legacy layout artifacts to deliver clean typography inside the dashboard view.
- **Document Compilation**: Packages structured system analytics into standard downloadable audit files using ReportLab's layout flow engine.
LIVE DEMO LINK - [https://market-researcher-agent-icy9jbd4rx7vkvdr36lnrx.streamlit.app/]

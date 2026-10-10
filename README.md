# NexusVect AI Engine

A high-speed, dual-brain AI market intelligence hub built with the Agno AI framework. This application bypasses standard multi-agent orchestration delays by combining a lightning-fast Groq pre-processor with a deep synthesis Gemini engine to deliver sub-second financial and competitor research.

## System Architecture

- **High-Speed Classifier (Groq / Qwen 27B)**: Instantly processes natural language inputs, strips conversational filler, and isolates targets into structural JSON parameters.
- **Native Execution Layer**: Bypasses the intermediate LLM reasoning loop to trigger background tools (Yahoo Finance and DuckDuckGo) directly as native Python functions.
- **Deep Synthesis Engine (Gemini 3.8 Flash)**: Consolidates the structural tool context into professional analytical reports. Includes an automated recovery circuit that activates a backup processor if primary API demand spikes.
- **Premium Frontend Dashboard (Streamlit & CSS)**: A dark-themed web platform equipped with dynamic data formatting, an audit sheet log, and automated ReportLab PDF document compilation.

## Folder Structure

```text
Market_Research_team/
│
├── app.py                  # Streamlit Web UI (HTML, CSS, PDF Engine)
├── market_research.py      # Core Dual-Brain Data Pipeline (Agno Framework)
├── requirements.txt        # Production System Dependencies
└── .env                    # Multi-Provider Security API Credentials
```

## System Requirements

Ensure you have Python 3.10 or higher installed, then configure the configuration files as follows:

### 1. Security Environment (`.env`)
Create a `.env` file in the root folder containing your target access keys:

```env
GOOGLE_API_KEY=your_actual_gemini_api_key_here
GROQ_API_KEY=your_actual_groq_api_key_here
```

### 2. Dependency List (`requirements.txt`)
Create a `requirements.txt` file containing the core libraries:

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

## Setup and Installation

1. Open your terminal window and navigate to your project workspace directory:
   ```bash
   cd C:\Users\ayush\OneDrive\Desktop\Market_Research_team
   ```

2. Initialize your project's clean virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the isolated workspace environment:
   - **Windows PowerShell**: `.\venv\Scripts\Activate.ps1`
   - **Windows Command Prompt**: `.\venv\Scripts\activate.bat`
   - **macOS / Linux**: `source venv/bin/activate`

4. Upgrade the package installer tool and implement the requirements manifest simultaneously:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

## Running the Application

Launch the frontend dashboard server using the application run script command line:

```bash
streamlit run app.py
```

The system will initialize the dual-brain network routes and launch a secure browser window automatically at `http://localhost:8505`.

## Strategic Execution Capabilities

- **Stock Metric Tracking**: Intercepts ticker configurations or company names, translates obscure targets via dynamic lookup, and extracts margins, averages, prices, and consensus profiles instantly.
- **Competitor Cross-Examinations**: Automatically detects private corporations (e.g., OpenAI, SpaceX, Anthropic), switches routing logic away from traditional financial tools, and queries live search indexes for funding rounds, macro updates, and valuation milestones.
- **Automated Data Processing**: Strips raw layout borders from target streams to present clean narrative prose in the dashboard web panels.
- **Export Utility**: Instantly compiles complex data models into professional PDF document formats using the integrated ReportLab flow canvas tool.

## WebDataCleaner: Structured Web Data Extraction for LLMs

### The Problem
Cleaning and preparing web data for consumption by Large Language Models (LLMs) is a significant bottleneck for developers building agentic AI applications that ingest web-scale information. Web pages are inherently noisy, containing a mix of content, navigation, advertisements, and other elements not relevant to an LLM's task. Extracting specific, structured information (e.g., product details, article content, news headlines) from this unstructured soup is a recurring pain point, leading to poor LLM performance, increased token usage, and complex pre-processing pipelines.

### Why this Project Shape/Stack
This prototype is a lightweight Python CLI tool leveraging `BeautifulSoup` for HTML parsing and `lxml` for XPath capabilities. Python is the de-facto standard for data processing and scripting in the AI/ML community, making it an accessible choice. A CLI tool allows for easy integration into existing data pipelines, whether for one-off cleaning tasks or as part of a larger ingestion framework. The focus is on robust, rule-based extraction combined with a simple, declarative configuration, avoiding the overhead of an LLM for the *cleaning* itself.

We explicitly *avoid* using an LLM for the core cleaning logic because the problem is about providing *clean data to the LLM*, not having the LLM clean its own input. Using an LLM for this pre-processing would be circular, costly, and prone to the same noise issues we're trying to solve. The output of this tool is designed to be directly consumable by an LLM.

### Setup and Usage (Zero API Keys Required)

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-org/webdatacleaner.git
    cd webdatacleaner
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3.  **Run with fixture data:**
    The project includes `fixtures/sample_page.html` and `fixtures/config.json` to demonstrate its functionality without needing an internet connection or an LLM API key.

    ```bash
    python web_cleaner.py -u fixtures/sample_page.html -c fixtures/config.json
    ```

    This will output structured JSON data to your console, representing the cleaned content extracted from the sample HTML based on the provided configuration.

### Optional LLM Adapter
This tool does *not* include an optional real-LLM adapter. The core problem it solves is *preparing data for* an LLM, not interacting with one. Integrating an LLM here would introduce unnecessary complexity and cost for a task that is best handled by deterministic parsing and extraction rules. The output JSON is ready for direct ingestion by any LLM.

---

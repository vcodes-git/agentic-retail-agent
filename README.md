# Merchandise Analytics: RAG API Microservice

A Proof of Concept (POC) demonstrating how Large Language Models (LLMs) and Vector Databases can be leveraged to extract dynamic, 1:1 insights from large-scale retail inventory data.

## 📌 Project Overview
This microservice ingests a 10,000-row synthetic grocery dataset (modeled after Loblaw brands and PC Optimum promotional structures) and exposes a FastAPI endpoint for natural language querying. It translates complex inventory metrics (margin percentages, stock levels, promotional velocity) into actionable business intelligence.

## 🏗️ Architecture & Tech Stack
* **Web Framework:** FastAPI (Uvicorn ASGI)
* **AI Orchestration:** LangChain
* **Vector Database:** ChromaDB (Local/Persistent)
* **Embeddings:** HuggingFace (`all-MiniLM-L6-v2`)
* **LLM:** Google Gemini 2.5 Flash
* **Deployment:** Docker & GitHub Actions (CI/CD)

### Architectural Decisions & Trade-offs
1. **Local Embeddings over Cloud APIs:** Initially prototyped using cloud-based embedding models, but quickly hit `429 RESOURCE_EXHAUSTED` rate limits during the 10k-row ingestion phase. Pivoted to a local HuggingFace embedding model to ensure zero-cost, rate-limit-proof horizontal scaling.
2. **Separation of Concerns:** Transitioned from a monolithic script to a modular architecture (`app/api`, `app/services`) to mimic production environments and allow parallel development of the web server and the LangChain engine.
3. **Pydantic Validation:** Implemented strict request/response models to ensure API type safety and prevent injection/hallucination edge cases.

---

## 🚀 Quick Start (Docker)

The easiest way to run this POC is via the pre-configured Docker container.

### 1. Prerequisites
* Docker installed on your machine.
* A Google Gemini API Key.

### 2. Environment Setup
Create a `.env` file in the root directory and add your API key:
```text
GOOGLE_API_KEY="your_api_key_here"          # my key is "youseriouslythoughtiwouldgiveyoumykey"
```

### 3. Build and Run
```bash
# Build the Docker image
docker build -t loblaw-rag-api .

# Run the container (maps port 8000)
docker run -p 8000:8000 --env-file .env loblaw-rag-api
```

### 4. Test the API
Once the container is running and the AI engine has booted, navigate to the auto-generated interactive Swagger UI:
👉 **[http://localhost:8000/docs](http://localhost:8000/docs)**

---

## 💻 Local Development Setup

If you wish to run the service locally without Docker:

```bash
# 1. Clone the repository
# then...

# 2. Set up a virtual environment
cd loblaw-rag-analytics
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Generate the 10k synthetic dataset
python data/generate_data.py

# 5. Boot the FastAPI server
uvicorn main:app --reload
```

## 📊 Sample Queries
Try submitting these natural language queries to the `/chat` endpoint:
* *"Which President's Choice products are currently on clearance and have a stock level above 100?"*
* *"What is our highest margin produce item currently running a PC Optimum Bonus?"*
* *"Summarize the inventory health of the Frozen food category."*

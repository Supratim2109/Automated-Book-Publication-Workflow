Automated Book Publication Workflow

An end-to-end Python-based system that automates the process of scraping online content, processing it through intelligent pipelines, incorporating Human-in-the-Loop (HITL) reviews, and preparing high-quality book chapters for publication.

This project is designed for scalable, modular, and controlled book or document generation using agent-based architecture.

Project Overview

The Automated Book Publication Workflow enables:

- Scraping chapter-level content from URLs
- Processing content using modular AI/logic-based agents
- Supporting multiple rounds of Human-in-the-Loop (HITL) review
- Storing processed versions and embeddings
- Orchestrating the entire workflow programmatically

The system balances automation with human oversight to ensure quality, accuracy, and editorial control.

Architecture Overview

Automated-Book-Publication-Workflow/
│
├── agents/ # Individual agents (processing, review, logic)
├── scraper/ # Web scraping using Playwright
├── orchestrator/ # Workflow and pipeline orchestration
├── embeddings/ # Embedding generation & vector storage logic
├── db/ # Storage, versioning, and metadata
├── main.py # Main entry point
├── requirements.txt # Python dependencies
└── README.md


---

## 🛠️ Key Features

- Automated Web Scraping
  - Extracts structured chapter content from URLs
  - Designed for dynamic and static web pages

- Agent-Based Processing
  - Each task (cleaning, enhancement, validation) handled by a dedicated agent
  - Easy to extend with new agents

- Human-in-the-Loop (HITL)
  - Supports iterative review cycles
  - Manual approval or edits before finalization

- Versioning & Storage
  - Maintains multiple content versions
  - Enables traceability across iterations

- Embeddings & Semantic Retrieval
  - Stores embeddings for intelligent search and retrieval
  - Useful for chapter similarity and future RAG pipelines

- Fully Modular Workflow
  - Pipelines can be rearranged or reused
  - Backend-first design (no UI dependency)

---

Installation & Setup

Prerequisites
- Python 3.10+
- pip
- Playwright dependencies (for scraping)

Installation

```bash
git clone https://github.com/Supratim2109/Automated-Book-Publication-Workflow.git
cd Automated-Book-Publication-Workflow
pip install -r requirements.txt



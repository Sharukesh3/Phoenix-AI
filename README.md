# Phoenix AI 🦅🔥
> **Rise from Rejection. Rebuild Your Career.**

![Phoenix AI Banner](https://img.shields.io/badge/Status-MVP_Ready-orange?style=for-the-badge) 
![Docker](https://img.shields.io/badge/Docker-Enabled-blue?logo=docker&style=for-the-badge)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi&style=for-the-badge)
![React](https://img.shields.io/badge/Frontend-React_Vite-61DAFB?logo=react&style=for-the-badge)
![LangGraph](https://img.shields.io/badge/Agents-LangGraph-FF4B4B?style=for-the-badge)

## 🚀 Overview
**Phoenix AI** is an intelligent, agentic career recovery system designed to help job seekers bounce back from rejection. Unlike generic career coaches, Phoenix AI uses a **Multi-Agent System** to analyze your specific situation, diagnose the "silent killers" in your resume, and generate a personalized, step-by-step recovery roadmap.

It's not just advice; it's a **strategic campaign** to get you hired.

## ✨ Key Features
*   **🧠 Agentic Memory (RAG)**: Remembers your entire interaction history using **Qdrant** (Vector Hub) and **PostgreSQL**. It knows your skills, your past rejections, and your goals.
*   **🕵️‍♂️ Profile Intelligence Agent**: detailed analysis of your Resume (PDF) and GitHub profile to uncover hidden strengths and gaps.
*   **🎯 Opportunity Discovery Agent**: Matches your true capabilities with live market opportunities (via Tavily Search).
*   **🛡️ Recovery Strategist Agent**: The core of Phoenix. It takes a rejection email or context and generates a **custom diagnosis** and a **tactical recovery plan**.
*   **💬 Persistent Chat**: A context-aware chat interface that acts as your 24/7 career mentor.
*   **🐳 Fully Dockerized**: Deploy the entire stack (Frontend, Backend, DBs, LLM) with a single command.

## 🏗️ Architecture
The system is built on a robust, scalable architecture:

```mermaid
graph TD
    %% Styling
    classDef container fill:#f9f9f9,stroke:#333,stroke-width:2px;
    classDef db fill:#e1f5fe,stroke:#0277bd,stroke-width:2px,rx:10,ry:10;
    classDef external fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px,stroke-dasharray: 5 5;
    classDef agent fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;

    %% Nodes
    User(["User / Job Seeker"])
    UI["Frontend UI<br/>(React + Vite + shadcn/ui)"]
    API["Backend API<br/>(FastAPI)"]
    
    %% Agent Layer
    Orchestrator{"Workflow Orchestrator"}
    AgentProfile["Profile Intelligence Agent<br/>(GitHub & Resume Analysis)"]:::agent
    AgentOpp["Opportunity Discovery Agent<br/>(Job Matching)"]:::agent
    AgentRec["Recovery Strategist Agent<br/>(Custom Plans)"]:::agent
    
    %% Databases
    DB[("PostgreSQL<br/>Users/History")]:::db
    VectorDB[("Qdrant<br/>Memory Embeddings")]:::db
    
    %% External Services
    Firebase["Firebase Auth"]:::external
    Groq["Groq Cloud<br/>(Llama 3 Inference)"]:::external
    GitHubAPI["GitHub API"]:::external
    Tavily["Tavily Search API"]:::external

    %% Relations
    User -->|HTTPS| UI
    
    subgraph "Docker Compose Network"
        UI -->|Axios / REST API| API
        
        subgraph "AI Agent Layer"
            API --> Orchestrator
            Orchestrator --> AgentProfile
            Orchestrator --> AgentOpp
            Orchestrator --> AgentRec
        end
        
        API -->|SQL Queries| DB
        API -->|Vector Search| VectorDB
    end

    %% External Connections
    UI -.->|Auth Token| Firebase
    API -.->|Verify Token| Firebase

    AgentProfile -->|Fetch Data| GitHubAPI
    AgentProfile -->|Extract Skills| Groq
    
    AgentOpp -->|Search Jobs| Tavily
    AgentOpp -->|Match| Groq
    
    AgentRec -->|Generate Strategy| Groq
```

## 🛠️ Tech Stack
*   **Frontend**: React, Vite, TailwindCSS, shadcn/ui (Phoenix Theme 🟠)
*   **Backend**: Python, FastAPI
*   **AI/ML**: LangChain, LangGraph, Ollama/Groq (Llama 3)
*   **Database**: PostgreSQL (Relational), Qdrant (Vector)
*   **DevOps**: Docker, Nginx

## 🚀 Getting Started

### Prerequisites
*   Docker & Docker Desktop
*   Git

### Installation
1.  **Clone the repository**:
    ```bash
    git clone https://github.com/Sharukesh3/Phoenix-AI.git
    cd Phoenix-AI
    ```

2.  **Set up Environment**:
    Create a `.env` file in the root directory:
    ```env
    GROQ_API_KEY=your_key_here
    TAVILY_API_KEY=your_key_here
    GITHUB_TOKEN=your_key_here
    ```

3.  **Run with Docker**:
    ```bash
    docker-compose up --build
    ```
    *   **Frontend**: [http://localhost](http://localhost)
    *   **API Docs**: [http://localhost/docs](http://localhost/docs)

## 🤝 Contributing
Built with ❤️ for **Anokha 2026**.
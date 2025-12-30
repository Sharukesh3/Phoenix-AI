# CareerForge AI - Agentic Career Recovery System

> **Phase 2**: Multi-Agent Career Intelligence System with MIRAS Memory

An intelligent career recovery system powered by **5 specialized AI agents**, **LangGraph orchestration**, and **MIRAS-inspired memory** to analyze profiles, match jobs, and generate personalized recovery strategies.

---

## 🚀 Features

### **Core Capabilities**
- ✅ **Intelligent Resume Parsing** - Extracts skills, experience, and GitHub username from PDFs
- ✅ **GitHub Profile Analysis** - Analyzes repos, languages, commits, and activity
- ✅ **LLM-Powered Job Matching** - Uses Groq LLaMA 3.3 70B for intelligent skill extraction
- ✅ **Detailed Skill Gap Analysis** - Compares your level vs industry expectations
- ✅ **YouTube Tutorial Recommendations** - Finds learning resources for missing skills
- ✅ **MIRAS Memory System** - Surprise-based retention (no deep learning training)
- ✅ **Tree-of-Thoughts Reasoning** - Multi-hypothesis rejection diagnosis

### **5 Specialized Agents**
1. **Profile Intelligence Agent** - Resume + GitHub analysis
2. **Opportunity Discovery Agent** - Job search + matching (Tavily API)
3. **Recovery Strategist Agent** - Rejection diagnosis + action plans
4. **Detailed Analysis Agent** - Skill gap assessment + competitive positioning
5. **YouTube Tutorial Agent** - Curated learning resources

---

## 📦 Installation

```bash
cd c:\Users\rdeva\Downloads\sem6\hack
pip install -r requirements.txt
```

**Required API Keys** (already configured in `.env`):
- Groq API
- Tavily API
- GitHub Personal Access Token

---

## 🎯 Usage

### **Basic Command**
```bash
python main.py <resume.pdf> <job_description.txt>
```

### **Example**
```bash
python main.py Deva-new.pdf jd.txt
```

### **What It Does**
1. Parses your resume (extracts skills, auto-detects GitHub username)
2. Analyzes your GitHub profile (languages, repos, commits)
3. Uses **LLM to extract skills** from job description (works for ANY job)
4. Searches for matching jobs using Tavily
5. Compares your skills vs job requirements
6. Generates detailed gap analysis
7. Provides YouTube tutorials for missing skills
8. Creates week-by-week learning roadmap
9. Saves insights to MIRAS memory

---

## 📊 Output Sections

### **1. Profile Analysis**
- AI-generated professional summary
- GitHub statistics (repos, commits, languages)
- Skills extracted from resume (with proficiency scores)

### **2. Skill Matching Analysis**
- Overall match percentage
- ✅ Your matching skills
- ❌ Skills you need to learn

### **3. Job Opportunities**
- Top 5-10 job matches with scores
- Direct application links
- Required skills for each job

### **4. Detailed Skill Analysis**
- Your current level (Junior/Mid/Senior/Expert)
- Industry expectations
- Critical skill gaps
- GitHub improvement areas
- Competitive positioning (market percentile)

### **5. YouTube Learning Resources**
- Skill-specific tutorial playlists
- Direct video links
- Curated learning paths

### **6. Career Development Roadmap**
- Week-by-week learning plan
- Priority actions with descriptions
- Detailed timeline with deliverables
- Learning resources for each skill

### **7. MIRAS Memory Stats**
- Total insights retained
- Novelty scores
- Access patterns

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Manager Agent                        │
│              (LangGraph Orchestration)                  │
└─────────────────────────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   Profile    │  │ Opportunity  │  │   Recovery   │
│ Intelligence │  │  Discovery   │  │  Strategist  │
└──────────────┘  └──────────────┘  └──────────────┘
        │                 │                 │
        └─────────────────┼─────────────────┘
                          ▼
                ┌──────────────────┐
                │  MIRAS Memory    │
                │ (Shared Instance)│
                └──────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   Detailed   │  │   YouTube    │  │  Groq LLM    │
│   Analysis   │  │   Tutorial   │  │ (LLaMA 3.3)  │
└──────────────┘  └──────────────┘  └──────────────┘
```

---

## 🧠 MIRAS Memory System

**Surprise-Based Retention** (inspired by Google's Titans MIRAS):
- **Novelty Threshold**: 0.7 (configurable)
- **Max Size**: 1000 memories
- **Retention Logic**: Embeddings + surprise scoring
- **Consolidation**: Time decay + access frequency + novelty

**How It Works**:
1. Generates embedding for each insight
2. Computes novelty score vs existing memories
3. Retains only if novelty > threshold
4. Consolidates when limit reached

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **LLM** | Groq (LLaMA 3.3 70B) |
| **Orchestration** | LangGraph + LangChain |
| **Job Search** | Tavily API |
| **GitHub Analysis** | PyGithub |
| **Resume Parsing** | PyPDF2 + Hyperlink Extraction |
| **Embeddings** | Sentence Transformers |
| **Memory** | MIRAS (Surprise-based) |
| **Skill Extraction** | LLM-based (works for ANY job) |

---

## 📁 Project Structure

```
hack/
├── agents/
│   ├── profile_intelligence.py      # Resume + GitHub analysis
│   ├── opportunity_discovery.py     # Job search + matching
│   ├── recovery_strategist.py       # Diagnosis + recovery
│   ├── detailed_analysis.py         # Skill gap analysis
│   ├── youtube_tutorial.py          # Tutorial finder
│   └── utils/
│       ├── resume_parser.py         # PDF parsing
│       ├── github_analyzer.py       # GitHub API
│       ├── skill_extractor.py       # NER extraction
│       ├── job_scraper.py           # LLM-based skill extraction
│       └── tot_reasoning.py         # Tree-of-Thoughts
├── manager/
│   ├── agent_manager.py             # Workflow coordinator
│   ├── workflow_graph.py            # LangGraph definition
│   └── state.py                     # State schema
├── memory/
│   ├── miras_memory.py              # MIRAS implementation
│   └── embedding_utils.py           # Embeddings + similarity
├── llm/
│   └── groq_client.py               # Groq API wrapper
├── examples/                        # Usage examples
├── tests/                           # Unit tests
├── main.py                          # Entry point
├── config.py                        # Configuration
└── requirements.txt                 # Dependencies
```

---

## 🎓 Key Innovations

### **1. LLM-Based Skill Extraction**
- **No predefined skill lists**
- Works for **ANY job description** (AI Engineer, Data Entry, etc.)
- Uses Groq LLaMA to intelligently extract skills

### **2. Hyperlink-Aware Resume Parsing**
- Extracts clickable URLs from PDF annotations
- Auto-detects GitHub username from resume links
- Captures portfolio links, LinkedIn, email

### **3. Shared MIRAS Memory**
- All agents use **one unified memory instance**
- Surprise-based retention (novelty > 0.7)
- No redundant storage

### **4. Detailed Analysis Agent**
- Assesses your level (Junior/Mid/Senior/Expert)
- Compares vs industry expectations
- Provides competitive positioning

### **5. YouTube Tutorial Agent**
- Finds skill-specific tutorials
- Curated playlists for missing skills
- Direct video links

---

## 🧪 Testing

```bash
# Test MIRAS memory
pytest tests/test_miras_memory.py -v

# Run full workflow
python main.py Deva-new.pdf jd.txt
```

---

## 📝 Example Output

```
📊 Overall Match: 76.47%
✅ Matching Skills: 13/17
❌ Missing Skills: 4

🎯 YOUR CURRENT LEVEL: Expert (10/10)
   • Total Skills: 48
   • GitHub Commits: 682

🏢 INDUSTRY EXPECTATIONS:
   • Expected Level: Senior
   • Experience: 3-5 years

🚨 CRITICAL SKILL GAPS:
   • Fine-tuning
   • Vector Database
   • Knowledge Graph

📅 DETAILED LEARNING TIMELINE:
   Week 1: Fine-tuning, Vector Database
   Week 2: Knowledge Graph, Machine Learning

🎥 YOUTUBE LEARNING RESOURCES:
   Fine-tuning:
      • Hugging Face Fine-tuning Guide
      🔗 https://youtube.com/...
```

---

## 🤝 Contributing

This is a hackathon project. Feel free to:
- Add more agents
- Enhance MIRAS memory
- Improve skill extraction
- Add more job boards

---

## 📄 License

MIT License - Built for CareerForge AI Hackathon

---

## 🙏 Acknowledgments

- **Google Research** - MIRAS memory inspiration
- **Groq** - Fast LLM inference
- **Tavily** - Job search API
- **LangChain/LangGraph** - Agent orchestration

---

**Built with ❤️ for the CareerForge AI Hackathon**

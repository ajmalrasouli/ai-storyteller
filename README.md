# 🌟 Free GenAI Bootcamp 2025 🌟
## 6 Weeks Of Free Online GenAI Training And Hands-on Programming

<div align="center">

  ***Learn, Code, Create: Transforming Language Learning with AI***

  ![Visitor Badge](https://visitor-badge.laobi.icu/badge?page_id=ajmalrasouli.free-genai-bootcamp-2025)
  ![Weeks](https://img.shields.io/badge/Duration-6%20Weeks-brightgreen)
  ![Projects](https://img.shields.io/badge/Projects-8-orange)
  ![Focus](https://img.shields.io/badge/Focus-Persian%2FDari-blue)
  [![CodeRabbit Pull Request Reviews](https://img.shields.io/coderabbit/prs/github/ajmalrasouli/free-genai-bootcamp-2025?utm_source=oss&utm_medium=github&utm_campaign=ajmalrasouli%2Ffree-genai-bootcamp-2025&labelColor=171717&color=FF570A&link=https%3A%2F%2Fcoderabbit.ai&label=CodeRabbit+Reviews)](https://coderabbit.ai/github/ajmalrasouli/free-genai-bootcamp-2025)

</div>

---

This repository contains projects developed during the 2025 GenAI Bootcamp [Free GenAI Bootcamp](https://genai.cloudprojectbootcamp.com/), focusing on practical applications of generative AI and language technologies, particularly for Persian/Dari language learning. All projects are designed to be run via Docker Compose from the central `Launcher` directory.

## 🏗️ GenAI System Architecture

![GenAI Architecture](genai-architecting/genai-architecture.png)

*This architecture diagram illustrates our approach to building a cost-effective, privacy-focused AI system for language learning. We've designed this solution around open-source models (like IBM Granite) that can run on dedicated AI hardware, avoiding ongoing API costs while maintaining control over student data. The system supports 300 simultaneous users and integrates our own proprietary learning materials to address copyright concerns. This self-hosted approach offers the perfect balance of performance, privacy, and long-term sustainability for language education.*


## 🎬 Launcher Demo Video
[![Watch the Launcher Demo Video on YouTube](Thumbnail.png)](https://youtu.be/X8bxv_mLoHE&ab)

## 📅 Weekly Development Progress

### 🔍 Week 0: Project Architecture and Initial Setup
- 📊 Created comprehensive architectural diagrams
- 💬 Developed prompting strategies for multiple LLM platforms
- 🧠 Implemented Sentence Constructor activity
- 🧩 Designed modular architecture for study activities

### 🚀 Week 1: DariMaster Language Learning App
- 💻 Set up full-stack application with Vite, TypeScript, and Express.js
- 🎮 Implemented core features including flashcards and matching games
- 🎨 Created responsive UI with Tailwind CSS and Shadcn/ui
- 🔄 Added RTL support for Dari text

### 🤖 Week 2: Persian Learning Assistant
- 💬 Implemented Chat with Nova system with Persian language support
- 📝 Created transcript processing and vocabulary extraction
- 🔒 Added security enhancements and proper environment configuration
- 🌐 Developed bilingual chat interface

### 🔊 Week 3: Text-to-Speech Microservice
- 🐳 Implemented Docker containerization for TTS services
- 🚀 Created FastAPI endpoints for text-to-speech conversion
- 🎵 Integrated Coqui TTS with custom configuration
- 🔄 Developed audio format conversion utilities

### 🎮 Week 4: Farsi Text Adventure MUD
- 📊 Solved critical issues with Farsi text display
- 🔄 Implemented centralized text processing with normalize_farsi function
- ⚙️ Created custom ArabicReshaper configuration for Farsi
- 🔄 Improved bidirectional text support

### 📱 Week 5: Visual Applications and Tools
- 🎵 Developed Farsi Song Vocabulary Generator with lyric analysis
- 🎬 Created interactive Farsi Learning Visual Novel with bilingual support
- ✍️ Implemented Farsi Writing Practice App with OCR technology
- 🔄 Added comprehensive RTL support across all applications

---

<div align="center">
  
  ## 🚀 Projects Overview
  
</div>

### 0️⃣ GenAI Platform Launcher (launcher)
A simple web dashboard (running on port 3000) that provides direct links to launch the various learning applications and shows their current running status (via `docker compose ps`). Note: Starting/stopping services must be done manually via `docker compose` commands on the host machine.

**Technical Stack:**
- 🐍 Python 3.10+
- 🚀 FastAPI & Uvicorn
- ✨ Jinja2 Templates
- 🐳 Docker & Docker Compose

### 1️⃣ Farsi Text Adventure MUD Game (fa-mud)
A text-based adventure game that helps users learn Farsi vocabulary through an immersive MUD (Multi-User Dungeon) experience.

**Key Features:**
- 🎮 Command flow: User Input → Parser → Game Engine → Response Gen → UI
- 🈯 Exactly one Farsi word per English sentence
- 🔣 13 predefined commands (Look, Move, Take, Drop, Talk, Use, Give, Open, Close, Eat, Inventory, Drink, Help)
- 🔁 RTL support for mixed LTR/RTL text rendering
- 📦 JSON-based vocabulary system

**Technical Stack:**
- 🐍 Python 3.10+
- 📟 Textual for terminal UI
- 🔤 Hazm for Farsi NLP
- 🔣 Arabic-reshaper and python-bidi for text processing
- ⚛️ React frontend with RTL support

### 2️⃣ ASL Finger Spelling Application (finger-spelling)
An interactive application that helps users learn and practice American Sign Language (ASL) finger spelling using computer vision and machine learning.

**Key Features:**
- 👋 Real-time hand tracking and gesture recognition using MediaPipe
- 🤟 ASL finger spelling detection and prediction
- 🖼️ Displays reference images for predicted letters (placeholders used for D-Z currently)
- 🏫 Interactive learning and test modes for practicing the ASL alphabet
- 📊 Performance feedback and accuracy metrics in test mode
- 🖥️ User-friendly web interface with webcam integration

**Technical Stack:**
- 🖐️ Hand tracking and landmark extraction using MediaPipe
- 🧠 Custom scikit-learn model for gesture recognition (trained on collected landmarks)
- 📷 Real-time image processing with OpenCV
- 🌐 Gradio-based web interface

*Note: For optimal performance, users should train the gesture recognition model using their own hand data by following the instructions in the `finger-spelling/README.md`.*

### 3️⃣ Language Learning Portal (lang-portal)
A comprehensive language learning platform with various activities and tools to help users learn new languages. Accessed via port 8009 when run with the launcher.

**Key Features:**
- 🏫 Interactive language learning modules (Flashcards, Matching Game)
- 📈 Progress tracking (Dashboard, Session History)
- 🐳 Separate Frontend (React/Vite/Nginx) and Backend (Node/Express/SQLite) services
- 🎨 Responsive UI with Tailwind CSS and Shadcn/ui

**Technical Stack:**
- Frontend: React, Vite, TypeScript, Tailwind CSS, Shadcn/ui, Nginx (serving)
- Backend: Node.js, Express, TypeScript, Sequelize, SQLite

### 4️⃣ Persian Learning Assistant (listening-comp)
An interactive chat system for learning Persian with transcript analysis capabilities.

**Key Features:**
- 💬 Chat with Nova Implementation
- 📊 Structured Data Processing
- 📝 Transcript analysis
- 📚 Vocabulary extraction with Persian character handling
- 📏 Grammar pattern recognition

**Technical Stack:**
- 🔤 sentence-transformers
- 🔍 faiss-cpu
- ⛓️ langchain
- 🎤 Azure Speech Services

### 5️⃣ Text-to-Speech (TTS) Microservice (opea-comps)
A microservice that combines Coqui TTS with FastAPI to provide text-to-speech conversion through a REST API.

**Key Features:**
- 🔊 Text-to-speech conversion API
- 🐳 Docker containerization
- 🚀 FastAPI integration
- 🔄 Audio format conversion

**Technical Stack:**
- 🐳 Docker and Docker Compose
- 🎵 Coqui TTS service
- 🚀 FastAPI framework
- 🌐 RESTful API design

### 6️⃣ Farsi Song Vocabulary Generator (song-vocab)
An application that analyzes Farsi songs to extract vocabulary for language learning purposes.

**Key Features:**
- 🌐 API for song lyric analysis
- 📚 Vocabulary extraction
- 🔍 SERP integration for song search
- 🧪 Interactive testing tools

**Technical Stack:**
- 🚀 Uvicorn server
- 🤖 Ollama SDK
- 🌐 API endpoints
- 🧪 Testing frameworks

### 7️⃣ Farsi Learning Visual Novel (visual-novel)
A web-based visual novel for learning Farsi, featuring interactive dialogue, language switching, and audio management.

**Key Features:**
- 🌐 Bilingual Support: Switch between English and Farsi text with RTL support
- 🔊 Audio System: Voice acting, background music, and sound effects
- 💬 Interactive Dialogue: Choice-based dialogue system with branching paths
- 👥 Character System: Rich cast of characters with dynamic expressions
- 💾 Save/Load System: Multiple save slots for game progress

**Technical Stack:**
- 📜 Pure JavaScript for game logic
- 🎨 HTML5 and CSS3 for interface
- 🔊 Web Audio API for sound management
- 🚀 Express.js for serving static files
- 🔤 Google Fonts (Noto Naskh Arabic) for Farsi text

### 8️⃣ Farsi Writing Practice App (writing-practice)
An interactive application (running on port 8008) to help users practice writing in Farsi (Persian). Provides English sentence prompts, verifies handwritten uploads using Tesseract OCR, and gives feedback using the Google Gemini API.

**Key Features:**
- 🔄 Random English sentences for translation practice
- 📤 Upload and verify handwritten Farsi text
- 👁️ Real-time OCR processing with Tesseract
- ✨ AI-powered translation and grading feedback (via Google Gemini)
- 🎨 Gradio web interface
- 🔣 Proper RTL text display

**Technical Stack:**
- 🐍 Python 3.10+
- ✨ Gradio for web UI
- 🧠 Google Generative AI (Gemini API)
- 👁️ Tesseract-OCR with Persian language support
- 🔣 Arabic-reshaper and python-bidi for text processing
- 🐳 Docker & Docker Compose

---

<div align="center">
  
  ## 📸 Reference Images
  
</div>

### 1. Farsi Text Adventure MUD Game (fa-mud)
![Farsi MUD Game](fa-mud/reference_images/image1.png)![Farsi MUD Game](fa-mud/reference_images/image2.png)
*The Farsi MUD game features a text-based interface with mixed English and Farsi text, allowing users to explore virtual environments while learning vocabulary.*

### 2. ASL Finger Spelling Application (finger-spelling)
![ASL Finger Spelling](finger-spelling/reference_images/dashboard.png)![ASL Finger Spelling](finger-spelling/reference_images/image1.png)
![ASL Finger Spelling](finger-spelling/reference_images/image2.png)![ASL Finger Spelling](finger-spelling/reference_images/image3.png)
![ASL Finger Spelling](finger-spelling/reference_images/image4.png)
![ASL Finger Spelling](finger-spelling/reference_images/FingerSpelling.mp4)

*The ASL application uses computer vision to recognize hand gestures and translate them into letters, with a practice mode for learning.*

### 3. Language Learning Portal (lang-portal)
![Language Portal](lang-portal/reference_images/dashboard.png)
![Language Portal](lang-portal/reference_images/image1.png)
![Language Portal](lang-portal/reference_images/image2.png)
![Language Portal](lang-portal/reference_images/image3.png)
![Language Portal](lang-portal/reference_images/image4.png)
![Language Portal](lang-portal/reference_images/image5.png)
![Language Portal](lang-portal/reference_images/image6.png)
![Language Portal](lang-portal/reference_images/image7.png)
*The language portal provides a comprehensive dashboard for tracking progress and accessing various learning activities.*

### 4. Persian Learning Assistant (listening-comp)
![Persian Learning Assistant](listening-comp/reference_images/Chat_with_Nova.png)
![Persian Learning Assistant](listening-comp/reference_images/Interactive_Learning.png)
![Persian Learning Assistant](listening-comp/reference_images/RAG_Implementation.png)
![Persian Learning Assistant](listening-comp/reference_images/Raw_Transcript.png)
![Persian Learning Assistant](listening-comp/reference_images/Structured_Data.png)
[Visual Novel Demo Video](listening-comp/reference_images/Listening_Comp_Video.mp4) (download to view)
### 🎬 listening-comp Demo Video
[![Watch the listening-comp Demo Video on YouTube](Thumbnail.png)](https://youtu.be/uMh1SHP28wY)

*The listening comprehension tool analyzes Persian audio and provides vocabulary extraction and grammar pattern recognition.*

### 5. Text-to-Speech (TTS) Microservice (opea-comps)
![TTS Microservice](opea-comps/reference_images/image0.png)
![TTS Microservice](opea-comps/reference_images/image1.png)
![TTS Microservice](opea-comps/reference_images/image2.png)
<audio controls src="opea-comps/reference_images/thanks.wav">
  Listen to TTS Microservice audio: <a href="opea-comps/reference_images/thanks.wav">thanks.wav</a>
</audio>

*The TTS microservice architecture demonstrates the containerized services working together to provide text-to-speech conversion.*

### 6. Farsi Song Vocabulary Generator (song-vocab)
![Song Vocabulary Generator](song-vocab/reference_images/image1.png)
![Song Vocabulary Generator](song-vocab/reference_images/lyrics.png)
*The song vocabulary tool searches for and analyzes Farsi lyrics to extract useful vocabulary for language learners.*

### 7. Farsi Learning Visual Novel (visual-novel)
![Visual Novel](visual-novel/reference_images/apartment.png)
![Visual Novel](visual-novel/reference_images/cafe.png)
![Visual Novel](visual-novel/reference_images/postoffice.png)
![Visual Novel](visual-novel/reference_images/school_exterior.png)
[Visual Novel Demo Video](visual-novel/reference_images/video.mp4) (download to view)

*The visual novel presents interactive scenarios with characters and dialogue choices to teach Farsi in context.*

### 8. Farsi Writing Practice App (writing-practice)
![Writing Practice](writing-practice/reference_images/image0.png)
![Writing Practice](writing-practice/reference_images/image1.png)
![Writing Practice](writing-practice/reference_images/image2.png)
![Writing Practice](writing-practice/reference_images/image3.png)
![Writing Practice](writing-practice/reference_images/image4.png)
![Writing Practice](writing-practice/reference_images/image5.png)
![Writing Practice](writing-practice/reference_images/image6.png)
![Writing Practice](writing-practice/reference_images/image7.png)

*The writing practice app allows users to practice handwritten Farsi and checks accuracy using OCR technology.*

---

## Special Thanks

Big thanks to Andrew Brown for providing the Free GenAI Bootcamp – an amazing resource that helped guide this project. [Free GenAI Bootcamp](https://genai.cloudprojectbootcamp.com/)

---

## Repository Structure

```
free-genai-bootcamp-2025/
├── fa-mud/                   # Farsi text adventure MUD game
│   ├── backend/              # Python backend for game logic
│   ├── frontend/             # React frontend with RTL support
│   └── README.md             # Project documentation
│
├── finger-spelling/          # ASL finger spelling recognition
│   ├── models/               # ML models for gesture recognition
│   ├── app.py                # Main application
│   └── README.md             # Project documentation
│
├── lang-portal/              # Language learning portal
│   ├── darimasterlan/        # Dari master language app
│   └── README.md             # Project documentation
│
├── listening-comp/           # Persian learning assistant
│   ├── backend/              # Backend services
│   ├── structured_data.py    # Data processing utilities
│   └── README.md             # Project documentation
│
├── opea-comps/               # Text-to-Speech microservice
│   ├── mega-service/         # FastAPI service
│   ├── models/               # TTS models
│   └── README.md             # Project documentation
│
├── song-vocab/               # Farsi song vocabulary generator
│   ├── tools/                # Utility tools
│   ├── tests/                # Testing modules
│   └── README.md             # Project documentation
│
├── visual-novel/             # Farsi learning visual novel
│   ├── assets/               # Audio, backgrounds, characters
│   ├── js/                   # Game engine and logic
│   ├── styles/               # CSS styling
│   └── README.md             # Project documentation
│
├── writing-practice/         # Farsi writing practice app
│   ├── gradio_app.py         # Main application
│   └── README.md             # Project documentation
│
└── README.md                 # Main repository documentation
```

## Getting Started

This project uses Docker Compose to manage and run all the different services. The **Launcher service** (`http://localhost:3000`) acts as the central dashboard to view the status of and access all the other learning applications.

**It is recommended to run all projects via the Launcher's Docker Compose setup.**

1.  **Prerequisites:**
    *   Install [Docker](https://docs.docker.com/get-docker/).
    *   Install [Docker Compose](https://docs.docker.com/compose/install/) (often included with Docker Desktop).
    *   Ensure you have any necessary API keys (e.g., `GOOGLE_API_KEY` for Writing Practice) and potentially accounts for services like Azure Speech (for Listening Comp).
    *   Ability to run Python scripts locally for project-specific setup (e.g., training the ASL model in `finger-spelling` by following its README).

2.  **Configuration:**
    *   **Navigate to the `Launcher` directory.** This is the main directory for controlling all services.
    *   Create a `.env` file by copying `.env.template` (`cp .env.template .env`).
    *   Edit the `Launcher/.env` file and add your required API keys (e.g., `GOOGLE_API_KEY=YOUR_KEY_HERE`). This file provides environment variables to all services started by the compose file.

3.  **Build and Run All Services:**
    *   **From the `Launcher` directory,** run:
        ```bash
        docker-compose up -d
        ```
    *   This command will build the images for all services (which might take some time on the first run) and start them in the background.

4.  **Access the Launcher Dashboard:**
    *   Open your web browser to `http://localhost:3000`.
    *   This dashboard shows the status of each service and provides links to launch them.

5.  **Launch Projects:**
    *   From the Launcher Dashboard, click the link for a project.
    *   This will open the project's specific URL (e.g., `http://localhost:8009` for Language Learning Portal, `http://localhost:8008` for Writing Practice) in a new tab.

6.  **Managing Services:**
    *   **Use your terminal in the `Launcher` directory** to manage the services:
    *   To stop all services: `docker-compose down`.
    *   To start/stop individual services: `docker-compose start <service_name>` or `docker-compose stop <service_name>`.
    *   To view logs: `docker-compose logs <service_name>`.

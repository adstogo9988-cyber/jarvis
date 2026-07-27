# 🤖 Jarvis — 100% Free & Unlimited AI Assistant

A complete local, offline-first personal AI assistant built entirely on your PC with no cloud dependencies or usage limits.

## ✨ Features

- **Local Brain**: Ollama + Llama 3.1 (runs entirely on your computer)
- **Voice Control**: Speech-to-text with Whisper + Text-to-speech with Coqui TTS
- **File Automation**: Create, delete, organize files and folders
- **Browser Control**: Automate web searches, YouTube playback
- **Vision**: Camera and screenshot analysis
- **Memory**: SQLite database remembers your preferences and tasks
- **100% Offline**: No cloud APIs, no daily limits, no internet required*
- **Single .exe**: One-click installer for Windows

*Except browser automation and email (which require internet)

## 🚀 Quick Start

### Automatic Setup (Recommended):
```bash
python main.py
# Wait for automatic setup on first run
# Say "Hello Jarvis, test" to begin
```

### Manual Setup:

**Prerequisites:**
- Windows 10/11
- Python 3.10+
- 16GB+ RAM

**Step 1: Install Ollama**
```bash
Download from https://ollama.com/download
```

**Step 2: Install Dependencies**
```bash
git clone https://github.com/adstogo9988-cyber/jarvis.git
cd jarvis
pip install -r requirements.txt
```

**Step 3: Run Jarvis**
```bash
python main.py
```

## 📁 Project Structure

```
jarvis/
├── main.py                 # Entry point
├── first_run_setup.py      # Auto installer
├── requirements.txt        # Dependencies
├── config.yaml            # Settings
├── brain/                 # AI Brain
├── voice/                 # Voice I/O
├── automation/            # PC Automation
├── vision/                # Vision Module
├── memory/                # Database
├── agents/                # Background Tasks
└── ui/                    # Dashboard UI
```

## 🗣️ Example Commands

```
"Hello Jarvis, create a folder called MyProject"
"Hello Jarvis, what time is it?"
"Hello Jarvis, search YouTube for Python"
"Hello Jarvis, remember I like coffee at 9 AM"
```

## 100% Local & Free

- ✅ No cloud APIs
- ✅ No daily limits
- ✅ No subscription fees
- ✅ Fully offline (except browser automation)
- ✅ Open source

---

**Made with ❤️ — Building Jarvis Phase by Phase**

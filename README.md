# ReportEase: AI-Powered Report Generation Tool

**ReportEase** streamlines secure report generation for teams using an AI agent built with LangGraph, local AI solutions (Llama 3.2 3B, Whisper models) and a Flask-based web interface, ensuring efficiency and ease of use without cloud dependencies.

## Motivation

The primary motivation behind ReportEase is to significantly optimize employee workflows with a straightforward, user-friendly design. By exclusively utilizing open-source, locally-hosted models, ReportEase maintains strict compliance with corporate data policies.

## Features

### Flexible PDF Generation
- Integrates customizable company PDF templates via FPDF.
- Supports precise signature placement (PNG uploads).

### Voice-to-Text Transcription
- **Accurate Mode:** Whisper 3.5 Turbo (high precision).
- **Fast Mode:** Whisper Base (optimized speed).
- PyWhisperCPP optimizes performance, even on low-end hardware.

### Advanced Agentic System (LangGraph)
- Automates content structuring with consistent, high-quality outputs.
- Supports built-in function-calling for complex workflows.

### Web-Based Interface
- User-friendly Flask interface for easy access and customization.

## Technical Stack
- **Local LLM:** Llama 3.2 3B for efficient and quality outputs.
- **Whisper Models:** Whisper 3.5 Turbo (accurate), Whisper Base (fast).
- **PyWhisperCPP:** Transcription optimization.
- **FPDF:** PDF template generation.
- **LangGraph:** Intelligent content structuring.
- **Flask:** Web interface.

## Todo

- Implement file processing using Unstructured library with LangGraph integration.
- Add OCR fallback via Doctr models (`db_resnet50` / `crnn_vgg16_bn`) for problematic files.

## Getting Started

1. **Clone the repository**:
   ```bash
   git clone https://github.com/M0ckenv1r0n/ReportEase.git
   cd ReportEase
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install all required Python packages from the requirements.txt file**:
   ```bash
   pip install -r requirements.txt
   ```

## Install External Tools

4. **Install Ollama**  
   You can install Ollama using one of the following methods:

   - **Using Homebrew (macOS/Linux)**:  
     If you don’t have Homebrew, install it from [https://brew.sh/](https://brew.sh/).

     ```bash
     brew install ollama
     ```

   - **Alternatively**:  
     Visit the [Ollama website](https://ollama.com/) and follow the provided installation instructions.

5. **Download the Llama 3.2 3B Model**  
   After installing Ollama, download the required model by running:

   ```bash
   ollama pull llama3.2
   ```

6. **Install pywhispercpp**  
   Follow the installation guidance from the official repository: [https://github.com/absadiki/pywhispercpp](https://github.com/absadiki/pywhispercpp)

7. **Download Whisper Models**  
   Download the necessary Whisper models and test which one is more suitable for your system (e.g., `whisper3.5-turbo-model`, `whisper-base-model`) by running the following command inside the project folder:

   ```bash
   test-download-whisper.py
   ```

## Feedback and Contributions

Feedback and contributions are welcome!


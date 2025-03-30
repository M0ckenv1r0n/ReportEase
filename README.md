# ReportEase: AI-Powered Report Generation Tool

**ReportEase** is an advanced productivity tool designed to streamline the report-writing process for teams, focusing on efficiency, security, and ease of use. Leveraging locally-run Large Language Models (LLMs) and voice-to-text models, ReportEase ensures your data remains secure within your own infrastructure—no cloud dependencies.

## Motivation

The primary motivation behind ReportEase is to significantly optimize the workflow of employees by providing a straightforward and user-friendly design. By exclusively utilizing completely open-source, locally hosted models, ReportEase ensures compliance with corporate data policies, eliminating reliance on cloud-based solutions and protecting company confidentiality.

## Features

### Flexible PDF Generation
- Seamlessly integrates your company's specific PDF formats using FPDF.
- Supports custom-defined templates, including precise placement of signatures via PNG uploads.

### Voice-to-Text Transcription
- **Accurate Mode:** Utilizes Whisper 3.5 Turbo, offering highly precise transcription results.
- **Fast Mode:** Employs Whisper Base for quicker transcription, suitable for devices with lower hardware specifications.
- Both modes are optimized with PyWhisperCPP, significantly enhancing transcription speed and efficiency even on resource-limited hardware like the MacBook Air M1 (2020).

### Advanced Agentic System (LangGraph)
- Delivers structured, consistent, and high-quality content generation.
- Features automated paragraph structuring and built-in function-calling capabilities, simplifying complex report creation workflows.

### Web-Based Interface
- Developed using Flask, providing a simple, intuitive interface accessible through web browsers.
- Offers seamless interaction with all features, including transcription, PDF generation, and template customization.

## Technical Stack
- **Local LLM:** Ensures secure, on-premises content generation.
- **Whisper Models:** Voice transcription using Whisper 3.5 Turbo (accurate) and Whisper Base (fast).
- **PyWhisperCPP:** Optimizes transcription models for high performance.
- **FPDF:** Manages customizable PDF generation based on user-defined templates.
- **LangGraph:** Core agentic framework handling intelligent content structuring and automation.
- **Flask:** Web-based interface framework for user-friendly interactions.

## Todo

- Implement file processing using the Unstructured library integrated with the LangGraph agentic system.
- Add fallback OCR capabilities using Doctr models (`db_resnet50` / `crnn_vgg16_bn`) for processing unrecognizable or problematic file formats.

## Getting Started

(Provide detailed instructions here on how users can install dependencies, set up the environment, and run the application.)

## Feedback and Contributions

Your feedback is greatly appreciated. Contributions to further enhance ReportEase are welcome!

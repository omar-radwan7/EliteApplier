EliteApplier

EliteApplier is an advanced, automated job application system specifically designed for LinkedIn. It streamlines the job search process by autonomously discovering, filtering, and applying to positions based on highly customizable user criteria. The system integrates intelligent resume selection and artificial intelligence to maximize application quality and volume without constant manual oversight.

Project Overview

The core objective of EliteApplier is to handle the repetitive aspects of job hunting. It navigates LinkedIn's job search, evaluates postings against strict filters (such as experience required, specific technical keywords, and blacklist criteria), and submits tailored applications. It utilizes AI to dynamically generate cover letters and connection request notes for hiring managers, ensuring each application remains personalized and professional.

Technology Stack

The project relies on a modern automation and data processing stack:
- Core Language: Python
- Browser Automation: Selenium WebDriver and Undetected ChromeDriver
- Artificial Intelligence: Integrations with OpenAI, Gemini, and DeepSeek for dynamic content generation
- Data Handling: Python CSV module and Pandas for logging applications and failed attempts
- Styling & Interface: CSS for the companion Command Center interface

System Architecture

EliteApplier is designed with a modular architecture to separate configuration, automation logic, and AI services.

Core Engine
The primary execution loop is managed in the main bot script. It is responsible for initiating browser sessions, iterating through specified job search queries, handling pagination, and executing the application workflow (including filling dynamic form fields, dropdowns, and checkboxes).

Automation Modules
The system features dedicated modules for handling distinct tasks:
- Browser Management: Initializes undetected browser sessions to bypass basic bot detection and handles profile management.
- Smart Resume Selector: Parses job descriptions to automatically select the most appropriate CV (e.g., German, Data-focused, Cloud-focused, or General Engineering).
- AI Integration: Connects to external LLM providers to answer custom text questions, generate tailored cover letters, and write connection requests to hiring managers.
- Helper Utilities: Manages directory structures, file logging, and delay buffers.

Configuration Layer
All user-specific parameters are stored in the configuration directory. This includes default answers to common application questions, geographic preferences, salary expectations, and security clearance statuses.

Logging and Observability
The system maintains strict observability by tracking all processed applications. Successfully submitted jobs, along with metadata (HR name, date applied, resume used), are recorded in an applied jobs registry. Any failures or rejections (due to experience mismatches or blacklisted keywords) are logged separately with stack traces and screenshots for debugging.

Getting Started

Ensure you have Python installed and the required dependencies. A virtual environment is highly recommended.

1. Install dependencies:
   pip install -r requirements.txt

2. Update the configuration files with your personal details and preferences.

3. Run the application:
   python runAiBot.py

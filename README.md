# Text Summarization Tool

Text Summarization Tool is a web application built with Django that extracts text from PDF files and generates concise summaries using Natural Language Processing (NLP).

## About The Project

This tool streamlines the process of condensing lengthy PDF documents like research papers, reports, or articles into short, informative summaries. By leveraging NLP algorithms, it identifies key information to capture the essence of the original text.

**Disclaimer:** This tool uses core NLP libraries (NLTK, spaCy) for summarization and does not use any Large Language Models (LLMs) or AI. It may also not extract text from tables within PDF documents accurately.

## Screenshots

![Screenshot 1](screenshots/screenshot1.png)
![Screenshot 2](screenshots/screenshot2.png)


## Features

-   **PDF Text Extraction**: Extracts all textual content from uploaded PDF files.
-   **Text Summarization**: Generates a summary of the extracted text, limited to 500 words.
-   **NLP-Powered**: Employs advanced NLP techniques to identify key sentences and phrases for summarization.

## Getting Started

Follow these steps to get a local copy up and running.

### Using Docker (Recommended)

1.  **Build and run the container:**
    ```sh
    docker-compose up --build
    ```

2.  **Access the application:**
    Open your web browser and navigate to `http://localhost:8000`.

### Manual Installation

### Prerequisites

-   Python 3.10
-   Git

### Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/naitridoshi/Text-Summarization-Tool.git
    cd Text-Summarization-Tool
    ```

2.  **Create and activate a virtual environment:**
    ```sh
    # For macOS and Linux
    python3 -m venv .venv
    source .venv/bin/activate

    # For Windows
    python -m venv .venv
    .\.venv\Scripts\activate
    ```

3.  **Install the dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Download NLTK data:**
    Run the following command in your terminal to download the 'punkt' tokenizer.
    ```sh
    python -c "import nltk; nltk.download('punkt')"
    ```

5.  **Run the Django development server:**
    ```sh
    python TextSummary/manage.py runserver
    ```

6.  **Access the application:**
    Open your web browser and navigate to `http://127.0.0.1:8000/`.

## Usage

1.  Navigate to the homepage.
2.  Upload a PDF file containing the text you wish to summarize.
3.  The tool will display the extracted text and the generated summary.
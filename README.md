# Tagging and Extraction Application
POC leveraging OpenAI API for tagging and extraction from natural language text

## Features
- FastAPI web interface
- Entity extraction using OpenAI's GPT-3
- Environment variable management with `python-dotenv`

## Setup and Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/weslleyrsr/tagging_and_exctraction.git
    cd tagging_and_exctraction
    ```

2. Create a virtual environment and activate it:
    ```bash
    python3 -m venv env
    source env/bin/activate  # On Windows use: .\env\Scripts\activate
    ```

3. Install the dependencies:
    ```bash
    py -m pip install -r requirements.txt
    ```

4. Add your OpenAI API key to the `.env` file: 
    ```
    OPENAI_API_KEY=your-openai-api-key-here
    ```

## Running the Application
1. To run the application locally, use the following command:
    ```bash
    uvicorn app.main:app --reload
    ```

2. Visit http://127.0.0.1:8000/ in your browser to use the web interface.
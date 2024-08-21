import openai
import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
from typing import List
from pydantic import BaseModel, Field
from langchain.utils.openai_functions import convert_pydantic_to_openai_function
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser

# Load environment variables from the .env file
load_dotenv()

# Set the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initiate chat model
model = ChatOpenAI(temperature=0)

# FastAPI app instance
app = FastAPI()

# Define tagging model
class Tagging(BaseModel):
    """Tag the piece of text with particular info."""
    sentiment: str = Field(description="sentiment of text, should be `pos`, `neg`, or `neutral`")
    language: str = Field(description="language of text (should be ISO 639-1 code)")

# Convert pydantic model to OpenAI function
tagging_functions = [convert_pydantic_to_openai_function(Tagging)]

# Define prompt to tag text
prompt = ChatPromptTemplate.from_messages([
    ("system", "Think carefully, and then tag the text as instructed"),
    ("user", "{input}")
])

# Bind functions to model
model_with_functions = model.bind(
    functions=tagging_functions,
    function_call={"name": "Tagging"}
)

# Set taggin chain
tagging_chain = prompt | model_with_functions | JsonOutputFunctionsParser()

# Function to extract meaningful data from text using OpenAI API
def extract_meaningful_data(text):
    return tagging_chain.invoke({"input": text})

# HTML form for user input
@app.get("/", response_class=HTMLResponse)
async def get_form():
    return '''
        <html>
            <head><title>Text Extractor</title></head>
            <body>
                <h1>Extract Entities from Text</h1>
                <form action="/extract" method="post">
                    <textarea name="text" rows="10" cols="30">Enter text here...</textarea>
                    <br><input type="submit" value="Extract">
                </form>
            </body>
        </html>
    '''

# Endpoint to extract data from submitted text
@app.post("/extract")
async def extract_data(text: str = Form(...)):
    extracted_data = extract_meaningful_data(text)
    return {"Extracted Data": extracted_data}

# Run the application (For development/testing purposes)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

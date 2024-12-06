import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")

genai.configure(api_key=api_key) 

def get_gemini_response(input_text, model_name="gemini-1.5-flash"):
    model = genai.GenerativeModel(model_name=model_name)
    response = model.generate_content(input_text)
    return response.text

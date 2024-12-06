from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")

app = FastAPI()

genai.configure(api_key=api_key)

DEFAULT_SYSTEM_PROMPT = """당신은 한국에 거주하는 외국인 노동자를 위한 정확한 법률을 알려주는 전문가입니다.
질문자의 입장에서 법률 정보를 이해하기 쉽게 전달해야 하며, 간결하고 실용적인 답변을 제공합니다."""

class InputText(BaseModel):
    prompt: str
    temperature: float = 0.7
    max_length: int = 150
    top_p: float = 1.0

def get_gemini_response(prompt, temperature, max_length, top_p):
    try:
        full_prompt = f"{DEFAULT_SYSTEM_PROMPT}\n\n질문: {prompt}\n답변:"
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        response = model.generate_content(
            full_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_length,
                top_p=top_p
            )
        )

        return response.text

    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail={"error": str(e), "message": "Gemini API 호출 중 오류가 발생했습니다."}
        )

@app.post("/generate/")
def generate_text(input_text: InputText):
    try:
        response = get_gemini_response(
            prompt=input_text.prompt,
            temperature=input_text.temperature,
            max_length=input_text.max_length,
            top_p=input_text.top_p
        )
        
        if response:
            return {"output": response}
        else:
            raise HTTPException(status_code=500, detail="No response from the model.")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
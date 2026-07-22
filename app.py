from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64
import os
import google.generativeai as genai

genai.configure(api_key="AQ.Ab8RN6LODR1M6OXNnC1l6vpRoCSLpzcR0XVS9Rv6mahJ4Bz9qg")

model = genai.GenerativeModel("gemini-3.5-flash")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RequestData(BaseModel):
    image_base64: str
    question: str

class AnswerResponse(BaseModel):
    answer: str

@app.get("/")
def home():
    return {"message": "running"}

@app.post("/answer-image", response_model=AnswerResponse)
async def answer_image(data: RequestData):
    try:
        image_bytes = base64.b64decode(data.image_base64)

        response = model.generate_content(
            [
                {
                    "mime_type": "image/png",
                    "data": image_bytes,
                },
                f"""
Answer the question using the image.

Rules:
- Return only the answer.
- No explanation.
- If numeric, return only the number.
- No units or currency symbols.

Question:
{data.question}
"""
            ]
        )

        answer = response.text.strip()

        return {"answer": answer}

    except Exception:
        return {"answer": ""}
